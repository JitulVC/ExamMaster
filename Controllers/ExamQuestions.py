from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required

from Models.ExamQuestions import ExamQuestion, ExamQuestionSchema
from Extension import db,ma

class ExamQuestionListResource(Resource):
    @jwt_required()
    def get(self):
        try:
            examquestions = ExamQuestion.query.all()
            examquestionSchema = ExamQuestionSchema(many=True)
            data = examquestionSchema.dump(examquestions)
            return jsonify(data)
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            examquestionSchema = ExamQuestionSchema()
            error = examquestionSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            examid = data.get('examid')
            if examid == 0: 
                return jsonify({'Message': 'Missing Exam ID data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            question = data.get('question')
            if len(question.strip()) == 0: 
                return jsonify({'Message': 'Missing Question data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            answer_type = data.get('answer_type')
            if len(answer_type.strip()) == 0: 
                return jsonify({'Message': 'Missing Answer Type data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            answer1 = data.get('answer1')
            if len(answer1.strip()) == 0: 
                return jsonify({'Message': 'Missing Answer 1 data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            answer2 = data.get('answer2')
            if len(answer2.strip()) == 0: 
                return jsonify({'Message': 'Missing Answer 2 data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
                
            answer3 = data.get('answer3')
            if len(answer3.strip()) == 0: 
                return jsonify({'Message': 'Missing Answer 3 data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            answer4 = data.get('answer4')
            if len(answer4.strip()) == 0: 
                return jsonify({'Message': 'Missing Answer 4 data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            marks = data.get('marks')
            if marks == 0: 
                return jsonify({'Message': 'Missing Marks data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            correct_answer = data.get('correct_answer')
            if len(correct_answer.strip()) == 0: 
                return jsonify({'Message': 'Missing Correct Answer data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            examquestion = ExamQuestion()
            examquestion.examid = examid
            examquestion.question = question
            examquestion.answer_type = answer_type
            examquestion.answer1 = answer1
            examquestion.answer2 = answer2
            examquestion.answer3 = answer3
            examquestion.answer4 = answer4
            examquestion.marks = marks
            examquestion.correct_answer = correct_answer

            db.session.add(examquestion)
            db.session.commit()
            return jsonify({'Message': f'Record# {examquestion.id} Inserted', 'HTTPStatus': HTTPStatus.CREATED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

class ExamQuestionResource(Resource):
    @jwt_required()
    def get(self,id):
        try:
            examquestion = ExamQuestion.query.filter_by(id=id).first()
            if not examquestion:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
        
            examquestionSchema = ExamQuestionSchema(many=False)
            data = examquestionSchema.dump(examquestion)
            return jsonify(data)
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
    
    @jwt_required()
    def put(self,id):
        try:
            data = request.get_json()
            examquestionSchema = ExamQuestionSchema()
            error = examquestionSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            examquestion = ExamQuestion.query.get(id)
            if not examquestion:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            examid = data.get('examid')
            if examid == 0: 
                return jsonify({'Message': 'Missing Exam ID data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            question = data.get('question')
            if len(question.strip()) == 0: 
                return jsonify({'Message': 'Missing Question data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            answer_type = data.get('answer_type')
            if len(answer_type.strip()) == 0: 
                return jsonify({'Message': 'Missing Answer Type data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            answer1 = data.get('answer1')
            if len(answer1.strip()) == 0: 
                return jsonify({'Message': 'Missing Answer 1 data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            answer2 = data.get('answer2')
            if len(answer2.strip()) == 0: 
                return jsonify({'Message': 'Missing Answer 2 data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
                
            answer3 = data.get('answer3')
            if len(answer3.strip()) == 0: 
                return jsonify({'Message': 'Missing Answer 3 data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            answer4 = data.get('answer4')
            if len(answer4.strip()) == 0: 
                return jsonify({'Message': 'Missing Answer 4 data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            marks = data.get('marks')
            if marks == 0: 
                return jsonify({'Message': 'Missing Marks data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            correct_answer = data.get('correct_answer')
            if len(correct_answer.strip()) == 0: 
                return jsonify({'Message': 'Missing Correct Answer data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            examquestion.examid = examid
            examquestion.question = question
            examquestion.answer_type = answer_type
            examquestion.answer1 = answer1
            examquestion.answer2 = answer2
            examquestion.answer3 = answer3
            examquestion.answer4 = answer4
            examquestion.marks = marks
            examquestion.correct_answer = correct_answer
            db.session.commit()

            return jsonify({'Message': f'Record# {id} Updated', 'HTTPStatus': HTTPStatus.ACCEPTED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def delete(self,id):
        try:
            examquestion = ExamQuestion.query.get(id)
            if not examquestion:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
                
            db.session.delete(examquestion)
            db.session.commit()
            return jsonify({'Message': f'Record# {id} deleted', 'HTTPStatus': HTTPStatus.ACCEPTED})
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
