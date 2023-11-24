from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required

from Models.StudentAnswers import StudentAnswer, StudentAnswerSchema
from Extension import db,ma

class StudentAnswerListResource(Resource):
    @jwt_required()
    def get(self):
        try:
            studentanswers = StudentAnswer.query.all()
            studentanswerSchema = StudentAnswerSchema(many=True)
            data = studentanswerSchema.dump(studentanswers)
            return jsonify(data)
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            studentanswerSchema = StudentAnswerSchema()
            error = studentanswerSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            studentexamid = data.get('studentexamid')
            if studentexamid == 0: 
                return jsonify({'Message': 'Missing Exam ID data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            examquestionid = data.get('examquestionid')
            if examquestionid == 0: 
                return jsonify({'Message': 'Missing Question ID data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            question_response = data.get('question_response')
            if len(question_response.strip()) == 0: 
                return jsonify({'Message': 'Missing Question Response data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            response_result = data.get('response_result')
            if len(response_result.strip()) == 0: 
                return jsonify({'Message': 'Missing Response Result data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            studentanswer = StudentAnswer()
            studentanswer.studentexamid = studentexamid
            studentanswer.examquestionid = examquestionid
            studentanswer.question_response = question_response
            studentanswer.response_result = response_result

            db.session.add(studentanswer)
            db.session.commit()
            return jsonify({'Message': f'Record# {studentanswer.id} Inserted', 'HTTPStatus': HTTPStatus.CREATED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

class StudentAnswerResource(Resource):
    @jwt_required()
    def get(self,id):
        try:
            studentanswer = StuentAnswer.query.filter_by(id=id).first()
            if not studentanswer:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
        
            studentanswerSchema = StudentAnswerSchema(many=False)
            data = studentanswerSchema.dump(studentanswer)
            return jsonify(data)
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
    
    @jwt_required()
    def put(self,id):
        try:
            data = request.get_json()
            studentanswerSchema = StudentAnswerSchema()
            error = studentanswerSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            studentanswer = StudentAnswer.query.get(id)
            if not studentanswer:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            studentexamid = data.get('studentexamid')
            if studentexamid == 0: 
                return jsonify({'Message': 'Missing Exam ID data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            examquestionid = data.get('examquestionid')
            if examquestionid == 0: 
                return jsonify({'Message': 'Missing Question ID data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            question_response = data.get('question_response')
            if len(question_response.strip()) == 0: 
                return jsonify({'Message': 'Missing Question Response data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            response_result = data.get('response_result')
            if len(response_result.strip()) == 0: 
                return jsonify({'Message': 'Missing Response Result data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            studentanswer.studentexamid = studentexamid
            studentanswer.examquestionid = examquestionid
            studentanswer.question_response = question_response
            studentanswer.response_result = response_result
            db.session.commit()

            return jsonify({'Message': f'Record# {id} Updated', 'HTTPStatus': HTTPStatus.ACCEPTED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def delete(self,id):
        try:
            studentanswer = StudentAnswer.query.get(id)
            if not studentanswer:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
                
            db.session.delete(studentanswer)
            db.session.commit()
            return jsonify({'Message': f'Record# {id} Deleted', 'HTTPStatus': HTTPStatus.ACCEPTED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
