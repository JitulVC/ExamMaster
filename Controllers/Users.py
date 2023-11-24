from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus
from utils import Utils
from flask_jwt_extended import get_jwt_identity, jwt_required

from Models.Users import User, UserSchema
from Extension import db,ma

class UserListResource(Resource):
    @jwt_required()
    def get(self):
        try:
            users = User.query.all()
            userSchema = UserSchema(many=True)
            data = userSchema.dump(users)
            return jsonify(data)
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            userSchema = UserSchema()
            error = userSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            useraccount = data.get('useraccount')
            username = data.get('username')
            passcode = data.get('passcode')
            roleid = data.get('roleid')
            apikey = data.get('apikey')
            if len(useraccount.strip()) == 0 or len(username.strip()) == 0 or len(passcode.strip()) == 0 or roleid == 0: 
                return jsonify({'Message': 'Missing User Account or User Name or Passcode data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            user = User()
            user.useraccount = useraccount
            user.username = username
            user.passcode = Utils.encryptText(passcode)
            user.roleid = roleid
            user.apikey = apikey

            db.session.add(user)
            db.session.commit()
            return jsonify({'Message': f'Record# {user.id} Inserted', 'HTTPStatus': HTTPStatus.CREATED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

class UserResource(Resource):
    @jwt_required()
    def get(self,id):
        try:
            user = User.query.filter_by(id=id).first()
            if not user:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
        
            userSchema = UserSchema(many=False)
            data = userSchema.dump(user)
            return jsonify(data)
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
    
    @jwt_required()
    def put(self,id):
        try:
            data = request.get_json()
            userSchema = UserSchema()
            error = userSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            user = User.query.get(id)
            if not user:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            useraccount = data.get('useraccount')
            username = data.get('username')
            passcode = user.passcode
            roleid = data.get('roleid')
            apikey = data.get('apikey')
            if len(useraccount.strip()) == 0 or len(username.strip()) == 0 or len(passcode.strip()) == 0 or roleid == 0: 
                return jsonify({'Message': 'Missing User Account or User Name or Passcode data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            user.useraccount = useraccount
            user.username = username
            user.passcode = passcode
            user.roleid = roleid
            user.apikey = apikey
                    
            db.session.commit()
            return jsonify({'Message': f'Record# {id} updated', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def delete(self,id):
        try:
            user = User.query.get(id)
            if not user:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
                
            db.session.delete(user)
            db.session.commit()
            return jsonify({'Message': f'Record# {id} Deleted', 'HTTPStatus': HTTPStatus.ACCEPTED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
