from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required

from Models.RolePrivileges import RolePrivilege, RolePrivilegeSchema
from Extension import db,ma

class RolePrivilegeListResource(Resource):
    @jwt_required()
    def get(self):
        try:
            roleprivileges = RolePrivilege.query.all()
            roleprivilegeSchema = RolePrivilegeSchema(many=True)
            data = roleprivilegeSchema.dump(roleprivileges)
            return jsonify(data)
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            roleprivilegeSchema = RolePrivilegeSchema()
            error = roleprivilegeSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            roleid = data.get('roleid')
            privilegeid = data.get('privilegeid')
            if roleid == 0 or privilegeid == 0: 
                return jsonify({'Message': 'Missing Role or Privilege data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            roleprivilege = RolePrivilege()
            roleprivilege.roleid = roleid
            roleprivilege.privilegeid = privilegeid
            db.session.add(roleprivilege)
            db.session.commit()
            return jsonify({'Message': f'Record# {roleprivilege.id} Inserted', 'HTTPStatus': HTTPStatus.CREATED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

class RolePrivilegeResource(Resource):
    @jwt_required()
    def get(self,id):
        try:
            roleprivilege = RolePrivilege.query.filter_by(roleid=id).all()
            if not roleprivilege:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
        
            roleprivilegeSchema = RolePrivilegeSchema(many=True)
            data = roleprivilegeSchema.dump(roleprivilege)
            return jsonify(data)
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
    
    @jwt_required()
    def put(self,id):
        try:
            data = request.get_json()
            roleprivilegeSchema = RolePrivilegeSchema()
            error = roleprivilegeSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            roleprivilege = RolePrivilege.query.get(id)
            if not roleprivilege:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            roleid = data.get('roleid')
            privilegeid = data.get('privilegeid')
            if roleid == 0 or privilegeid == 0: 
                return jsonify({'Message': 'Missing Role or Privilege data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            roleprivilege.roleid = roleid
            roleprivilege.privilegeid = privilegeid
            db.session.commit()
            return jsonify({'Message': f'Record# {roleid} +  {privilegeid} updated', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def delete(self,id):
        try:
            roleprivilege = RolePrivilege.query.filter_by(roleid=id).all()
            if not roleprivilege:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
                
            roleprivilege = RolePrivilege.query.filter_by(roleid=id).delete()
            #db.session.delete().where(roleid=id)
            db.session.commit()
            return jsonify({'Message': f'Record# related to Role {id} Deleted', 'HTTPStatus': HTTPStatus.ACCEPTED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
