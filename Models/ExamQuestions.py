from flask import Flask

from Extension import db,ma

class ExamQuestion(db.Model):
    __tablename__ = 'examquestions'

    id = db.Column(db.Integer, primary_key=True)
    examid = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String(2000), nullable=False)
    answer_type = db.Column(db.String(1), nullable=False)
    answer1 = db.Column(db.String(2000), nullable=False)
    answer2 = db.Column(db.String(2000), nullable=False)
    answer3 = db.Column(db.String(2000), nullable=False)
    answer4 = db.Column(db.String(2000), nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    correct_answer = db.Column(db.String(7), nullable=False)
    rec_insertedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    rec_lastupdatedon = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

class ExamQuestionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ExamQuestion
        load_instance = True
        ordered = True
