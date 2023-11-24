from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required

from Models.Privileges import Privilege, PrivilegeSchema
from Extension import db,ma

class PrivilegeListResource(Resource):
    @jwt_required()
    def get(self):
        try:
            privileges = Privilege.query.all()
            privilegeSchema = PrivilegeSchema(many=True)
            data = privilegeSchema.dump(privileges)
            return jsonify(data)
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            privilegeSchema = PrivilegeSchema()
            error = privilegeSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            privileges = data.get('privileges')
            if len(privileges.strip()) == 0: 
                return jsonify({'Message': 'Missing Privilege data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            privilege = Privilege()
            privilege.privileges = privileges

            db.session.add(privilege)
            db.session.commit()
            return jsonify({'Message': f'Record# {privilege.id} Inserted', 'HTTPStatus': HTTPStatus.CREATED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

class PrivilegeResource(Resource):
    @jwt_required()
    def get(self,id):
        try:
            privilege = Privilege.query.filter_by(id=id).first()
            if not privilege:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
        
            privilegeSchema = PrivilegeSchema(many=False)
            data = privilegeSchema.dump(privilege)
            return jsonify(data)
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
    
    @jwt_required()
    def put(self,id):
        try:
            data = request.get_json()
            privilegeSchema = PrivilegeSchema()
            error = privilegeSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            privilege = Privilege.query.get(id)
            if not privilege:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            privileges = data.get('privileges')
            if len(privileges.strip()) == 0: 
                return jsonify({'Message': 'Missing Privilege data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            privilege.privileges = privileges
            db.session.commit()
            return jsonify({'Message': f'Record# {id} Updated', 'HTTPStatus': HTTPStatus.ACCEPTED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def delete(self,id):
        try:
            privilege = Privilege.query.get(id)
            if not privilege:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
                
            db.session.delete(privilege)
            db.session.commit()
            return jsonify({'Message': f'Record# {id} Deleted', 'HTTPStatus': HTTPStatus.ACCEPTED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
