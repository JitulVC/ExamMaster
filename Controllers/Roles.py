from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required

from Models.Roles import Role, RoleSchema
from Extension import db,ma

class RoleListResource(Resource):
    @jwt_required()
    def get(self):
        try:
            roles = Role.query.all()
            roleSchema = RoleSchema(many=True)
            data = roleSchema.dump(roles)
            return jsonify(data)
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            roleSchema = RoleSchema()
            error = roleSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            roledesc = data.get('role')
            if len(roledesc.strip()) == 0: 
                return jsonify({'Message': 'Missing Role data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            role = Role()
            role.role = roledesc

            db.session.add(role)
            db.session.commit()
            return jsonify({'Message': f'Record# {role.id} Inserted', 'HTTPStatus': HTTPStatus.CREATED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

class RoleResource(Resource):
    @jwt_required()
    def get(self,id):
        try:
            role = Role.query.filter_by(id=id).first()
            if not role:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
        
            roleSchema = RoleSchema(many=False)
            data = roleSchema.dump(role)
            return jsonify(data)
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
    
    @jwt_required()
    def put(self,id):
        try:
            data = request.get_json()
            roleSchema = RoleSchema()
            error = roleSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            role = Role.query.get(id)
            if not role:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            roledesc = data.get('role')
            if len(roledesc.strip()) == 0: 
                return jsonify({'Message': 'Missing Role data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            role.role = roledesc
            db.session.commit()
            return jsonify({'Message': f'Record# {id} updated', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def delete(self,id):
        try:
            role = Role.query.get(id)
            if not role:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
                
            db.session.delete(role)
            db.session.commit()
            return jsonify({'Message': f'Record# {id} deleted', 'HTTPStatus': HTTPStatus.ACCEPTED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
