from flask import Flask

from Extension import db,ma

class StudentAnswer(db.Model):
    __tablename__ = 'studentanswers'

    id = db.Column(db.Integer, primary_key=True)
    studentexamid = db.Column(db.Integer, nullable=False)
    examquestionid = db.Column(db.Integer, nullable=False)
    question_response = db.Column(db.String(7), nullable=False)
    response_result = db.Column(db.String(1), nullable=False)
    rec_insertedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    rec_lastupdatedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

class StudentAnswerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudentAnswer
        load_instance = True
        ordered = True
