from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus
from utils import Utils
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

from Models.Users import User, UserSchema
from Extension import db,ma

class AuthenticateResource(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()

            useraccount = data.get('useraccount')
            passcode = data.get('passcode')
            if useraccount is None or passcode is None or len(useraccount.strip()) == 0 or len(passcode.strip()) == 0: 
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            user = User.query.filter_by(useraccount=useraccount).first()
            if not user:
                return jsonify({'Message': 'User Account not found!', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
        
            decpasscode = Utils.decryptText(user.passcode)
            if decpasscode != passcode:
                return jsonify({'Message': 'Password is incorrect!', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            userSchema = UserSchema(many=False)
            data = userSchema.dump(user)
            return jsonify(data)
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
    
    @jwt_required()
    def put(self):
        try:
            data = request.get_json()
            useraccount = data.get('useraccount')
            passcode = data.get('passcode')
            if useraccount is None or passcode is None or len(useraccount.strip()) == 0 or len(passcode.strip()) == 0: 
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            user = User.query.filter_by(useraccount=useraccount).first()
            if not user:
                return jsonify({'Message': 'User Account not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            useraccount = user.useraccount
            username = user.username
            passcode = Utils.encryptText(passcode)
            roleid = user.roleid

            user.useraccount = useraccount
            user.username = username
            user.passcode = passcode
            user.roleid = roleid
            db.session.commit()
            return jsonify({'Message': f'Record# {user.id} Password updated', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

class TokenResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            useraccount = data.get('useraccount')
            passcode = data.get('passcode')
            apikey = data.get('apikey')
            if useraccount is None or passcode is None or apikey is None or len(useraccount.strip()) == 0 or len(passcode.strip()) ==  0 or len(apikey.strip()) == 0: 
                return jsonify({'Message': 'Missing data','HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            user = User.query.filter_by(useraccount=useraccount).first()
            if not user:
                return jsonify({'Message': 'User Account not found!', 'HTTPStatus': HTTPStatus.UNAUTHORIZED}) 
        
            decpasscode = Utils.decryptText(user.passcode)
            if decpasscode != passcode:
                return jsonify({'Message': 'Password is incorrect!', 'HTTPStatus': HTTPStatus.UNAUTHORIZED})

            if apikey != user.apikey:
                return jsonify({'Message': 'API Key is incorrect!', 'HTTPStatus': HTTPStatus.UNAUTHORIZED})
            
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

class TokenResourceRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        try:
            user_id = get_jwt_identity()        
            access_token = create_access_token(identity=user_id, fresh=False)

            return {'access_token': access_token}, HTTPStatus.OK
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
