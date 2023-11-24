from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required
import re

from Models.StudentExams import StudentExam, StudentExamSchema
from Extension import db,ma

date_pattern_str = r'^\d{4}-\d{2}-\d{2} \d{2}\:\d{2}\:\d{2}$'

class StudentExamListResource(Resource):
    @jwt_required()
    def get(self):
        try:
            studentexams = StudentExam.query.all()
            studentexamSchema = StudentExamSchema(many=True)
            data = studentexamSchema.dump(studentexams)
            return jsonify(data)
        except Exception as ex:    
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            studentexamSchema = StudentExamSchema()
            error = studentexamSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            studentid = data.get('studentid')
            if studentid == 0: 
                return jsonify({'Message': 'Missing Student ID data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            examid = data.get('examid')
            if examid == 0: 
                return jsonify({'Message': 'Missing Exam ID data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            attemptno = data.get('attemptno')
            if attemptno == 0: 
                return jsonify({'Message': 'Missing Attempt No. data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            examscore = data.get('examscore')
            if examscore < 0: 
                return jsonify({'Message': 'Missing Exam Score data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            starttime = data.get('starttime')
            if not re.match(date_pattern_str, starttime): 
                return jsonify({'Message': 'Missing Start Time data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            endtime = data.get('endtime')
            if not re.match(date_pattern_str, endtime): 
                return jsonify({'Message': 'Missing End Time data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            studentexam = StudentExam()
            studentexam.studentid = studentid
            studentexam.examid = examid
            studentexam.attemptno = attemptno
            studentexam.examscore = examscore
            studentexam.starttime = starttime
            studentexam.endtime = endtime

            db.session.add(studentexam)
            db.session.commit()
            return jsonify({'Message': f'Record# {studentexam.id} Inserted.', 'HTTPStatus': HTTPStatus.CREATED})
        except Exception as ex:
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

class StudentExamResource(Resource):
    @jwt_required()
    def get(self,id,studentid):
        try:
            if id == 0 and studentid:
                studentexam = StudentExam.query.filter_by(studentid=studentid).all()
                studentexamSchema = StudentExamSchema(many=True)
            else:
                studentexam = StudentExam.query.filter_by(id=id).first()
                studentexamSchema = StudentExamSchema(many=False)

            if not studentexam:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
        
            data = studentexamSchema.dump(studentexam)
            return jsonify(data)

        except Exception as ex:
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def put(self,id):
        try:
            data = request.get_json()
            studentexamSchema = StudentExamSchema()
            error = studentexamSchema.validate(data)
            if error:
                return jsonify({'Message': 'Missing data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            studentexam = StudentExam.query.get(id)
            if not studentexam:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            studentid = data.get('studentid')
            if studentid == 0: 
                return jsonify({'Message': 'Missing Student ID data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            examid = data.get('examid')
            if examid == 0: 
                return jsonify({'Message': 'Missing Exam ID data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            attemptno = data.get('attemptno')
            if attemptno == 0: 
                return jsonify({'Message': 'Missing Attempt No. data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            examscore = data.get('examscore')
            if examscore < 0: 
                return jsonify({'Message': 'Missing Exam Score data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            starttime = data.get('starttime')
            if not re.match(date_pattern_str, starttime): 
                return jsonify({'Message': 'Missing Start Time data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            endtime = data.get('endtime')
            if not re.match(date_pattern_str, endtime): 
                return jsonify({'Message': 'Missing End Time data', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

            studentexam.studentid = studentid
            studentexam.examid = examid
            studentexam.attemptno = attemptno
            studentexam.examscore = examscore
            studentexam.starttime = starttime
            studentexam.endtime = endtime
            db.session.commit()
            return jsonify({'Message': f'Record# {id} Updated', 'HTTPStatus': HTTPStatus.ACCEPTED})

        except Exception as ex:
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})

    @jwt_required()
    def delete(self,id,studentid):
        try:
            if id == 0 and studentid:
                studentexam = StudentExam.query.filter_by(studentid=studentid).all()
                studentexamSchema = StudentExamSchema(many=True)
            else:
                studentexam = StudentExam.query.get(id)
                studentexamSchema = StudentExamSchema(many=False)

            if not studentexam:
                return jsonify({'Message': 'Item not found', 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
                
            if id == 0 and studentid:
                studentexam = StudentExam.query.filter_by(studentid=studentid).delete()
            else:
                db.session.delete(studentexam)
            db.session.commit()
            return jsonify({'Message': f'Record# {id} Deleted', 'HTTPStatus': HTTPStatus.ACCEPTED})
        except Exception as ex:
            return jsonify({'Message': str(ex), 'HTTPStatus': HTTPStatus.INTERNAL_SERVER_ERROR})
