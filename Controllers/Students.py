from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required

from Models.Students import Student, StudentSchema
from Extension import db,ma

class StudentListResource(Resource):
    @jwt_required()
    def get(self):
        try:
            students = Student.query.all()
            studentSchema = StudentSchema(many=True)
            data = studentSchema.dump(students)
            return jsonify(data)
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            studentSchema = StudentSchema()
            error = studentSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data','HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            studentname = data.get('studentname')
            if len(studentname.strip()) == 0: 
                return jsonify({'Message': 'Missing data','HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            userid = data.get('userid')
            if userid == 0: 
                return jsonify({'Message': 'Missing data','HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            student = Student()
            student.studentname = studentname
            student.userid = userid

            db.session.add(student)
            db.session.commit()
            return jsonify({'Message': f'Record# {student.id} Inserted', 'HTTPStatus': HTTPStatus.CREATED})
        except Exception as ex:
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

class StudentResource(Resource):
    @jwt_required()
    def get(self,id):
        try:
            student = Student.query.filter_by(id=id).first()
            if not student:
                return jsonify({'Message': 'Item not found','HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
        
            studentSchema = StudentSchema(many=False)
            data = studentSchema.dump(student)
            return jsonify(data)
        except Exception as ex:
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
    
    @jwt_required()
    def put(self,id):
        try:
            data = request.get_json()
            studentSchema = StudentSchema()
            error = studentSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data','HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            student = Student.query.get(id)
            if not student:
                return jsonify({'Message': 'Item not found','HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            studentname = data.get('studentname')
            if len(studentname.strip()) == 0: 
                return jsonify({'Message': 'Missing data','HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            userid = data.get('userid')
            if userid == 0: 
                return jsonify({'Message': 'Missing data','HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            student.studentname = studentname
            student.userid = userid
            db.session.commit()
            return jsonify({'Message': f'Record# {id} Updated', 'HTTPStatus': HTTPStatus.ACCEPTED})
        except Exception as ex:
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def delete(self,id):
        try:
            student = Student.query.get(id)
            if not student:
                return jsonify({'Message': 'Item not found','HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
                
            db.session.delete(student)
            db.session.commit()
            return jsonify({'Message': f'Record# {id} Deleted', 'HTTPStatus': HTTPStatus.ACCEPTED})
        except Exception as ex:
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
