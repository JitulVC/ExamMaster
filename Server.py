from flask import Flask, render_template
from flask_restful import Api 
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from datetime import datetime, timedelta

from dbConfig import DbConfig
from Extension import db, ma

from Models.Privileges import Privilege
from Controllers.Privileges import PrivilegeListResource, PrivilegeResource

from Models.Roles import Role
from Controllers.Roles import RoleListResource, RoleResource

from Models.RolePrivileges import RolePrivilege
from Controllers.RolePrivileges import RolePrivilegeListResource, RolePrivilegeResource

from Models.Users import User
from Controllers.Users import UserListResource, UserResource
from Controllers.Authenticate import AuthenticateResource, TokenResource, TokenResourceRefresh

from Models.Students import Student
from Controllers.Students import StudentListResource, StudentResource

from Models.Exams import Exam
from Controllers.Exams import ExamListResource, ExamResource

from Models.ExamQuestions import ExamQuestion
from Controllers.ExamQuestions import ExamQuestionListResource, ExamQuestionResource

from Models.StudentExams import StudentExam
from Controllers.StudentExams import StudentExamListResource, StudentExamResource

from Models.StudentAnswers import StudentAnswer
from Controllers.StudentAnswers import StudentAnswerListResource, StudentAnswerResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(DbConfig)
    app.config["JWT_SECRET_KEY"] = '8292329iowiewow030pwop0302'
    app.config['JWT_ALGORITHM'] = 'HS256'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=180)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(seconds=240)

    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)

def register_resources(app):
    api = Api(app)
    api.add_resource(PrivilegeListResource, '/privilege')
    api.add_resource(PrivilegeResource, '/privilege/<int:id>')
    api.add_resource(RoleListResource, '/role')
    api.add_resource(RoleResource, '/role/<int:id>')
    api.add_resource(RolePrivilegeListResource, '/roleprivilege')
    api.add_resource(RolePrivilegeResource, '/roleprivilege/<int:id>')
    api.add_resource(UserListResource, '/user')
    api.add_resource(UserResource, '/user/<int:id>')
    api.add_resource(AuthenticateResource, '/authenticate')
    api.add_resource(StudentListResource, '/student')
    api.add_resource(StudentResource, '/student/<int:id>')
    api.add_resource(ExamListResource, '/exam')
    api.add_resource(ExamResource, '/exam/<int:id>')
    api.add_resource(ExamQuestionListResource, '/examquestion')
    api.add_resource(ExamQuestionResource, '/examquestion/<int:id>')
    api.add_resource(StudentExamListResource, '/studentexam')
    api.add_resource(StudentExamResource, '/studentexam/<int:id>/<int:studentid>')
    api.add_resource(StudentAnswerListResource, '/studentanswer')
    api.add_resource(StudentAnswerResource, '/studentanswer/<int:id>')

    api.add_resource(TokenResource, '/token')
    api.add_resource(TokenResourceRefresh, '/token/refresh')

if __name__ == '__main__':
    app = create_app()
    jwt = JWTManager(app)
    
    @app.route('/', methods=['GET'])
    def home():
        return render_template('exammaster_apidoc.html')

    app.run(host='0.0.0.0', port=8080)
