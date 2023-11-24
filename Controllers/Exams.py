from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required

from Models.Exams import Exam, ExamSchema
from Extension import db,ma

class ExamListResource(Resource):
    @jwt_required()
    def get(self):
        try:
            exams = Exam.query.all()
            examSchema = ExamSchema(many=True)
            data = examSchema.dump(exams)
            return jsonify(data)
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            examSchema = ExamSchema()
            error = examSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            examname = data.get('examname')
            if len(examname.strip()) == 0: 
                return jsonify({'Message': 'Missing Examname data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            no_of_questions = data.get('no_of_questions')
            if no_of_questions == 0: 
                return jsonify({'Message': 'Missing No. of Questions data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            duration = data.get('duration')
            if duration == 0: 
                return jsonify({'Message': 'Missing Duration data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            totalscore = data.get('totalscore')
            if totalscore == 0: 
                return jsonify({'Message': 'Missing Total Score data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            passingscore = data.get('passingscore')
            if passingscore == 0: 
                return jsonify({'Message': 'Missing Passing Score data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            exam = Exam()
            exam.examname = examname
            exam.no_of_questions = no_of_questions
            exam.duration = duration
            exam.totalscore = totalscore
            exam.passingscore = passingscore

            db.session.add(exam)
            db.session.commit()
            return jsonify({'Message': f'Record# {exam.id} Inserted', 'HTTPStatus': HTTPStatus.CREATED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

class ExamResource(Resource):
    @jwt_required()
    def get(self,id):
        try:
            exam = Exam.query.filter_by(id=id).first()
            if not exam:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
        
            examSchema = ExamSchema(many=False)
            data = examSchema.dump(exam)
            return jsonify(data)
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
    
    @jwt_required()
    def put(self,id):
        try:
            data = request.get_json()
            examSchema = ExamSchema()
            error = examSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            exam = Exam.query.get(id)
            if not exam:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            examname = data.get('examname')
            if len(examname.strip()) == 0: 
                return jsonify({'Message': 'Missing Exam Name data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            no_of_questions = data.get('no_of_questions')
            if no_of_questions == 0: 
                return jsonify({'Message': 'Missing No. of Questions data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            duration = data.get('duration')
            if duration == 0: 
                return jsonify({'Message': 'Missing Duration data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            totalscore = data.get('totalscore')
            if totalscore == 0: 
                return jsonify({'Message': 'Missing Total Score data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            passingscore = data.get('passingscore')
            if passingscore == 0: 
                return jsonify({'Message': 'Missing Passing Score data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            exam.examname = examname
            exam.no_of_questions = no_of_questions
            exam.duration = duration
            exam.totalscore = totalscore
            exam.passingscore = passingscore
            db.session.commit()
            return jsonify({'Message': f'Record# {id} Updated', 'HTTPStatus': HTTPStatus.ACCEPTED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def delete(self,id):
        try:
            exam = Exam.query.get(id)
            if not exam:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
                
            db.session.delete(exam)
            db.session.commit()
            return jsonify({'Message': f'Record# {id} Deleted', 'HTTPStatus': HTTPStatus.ACCEPTED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
