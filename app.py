from flask import Flask, render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import re 
import settings,views
from database import Database
from flask_cors import CORS



def create_app():
    app = Flask(__name__)
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type,Authorization')
        return response
    app.config['CORS_HEADERS'] = 'Content-Type'
    cors = CORS(app, resources={r"/": {"origins": ""}})
    app.config.from_object("settings")
    app.add_url_rule("/", view_func=views.login,methods=["GET", "POST"])
    app.add_url_rule("/homepage",view_func = views.homepage, methods=["GET","POST"])
    app.add_url_rule("/login", view_func=views.login,methods=["GET", "POST"])
    app.add_url_rule("/registerForStudent", view_func=views.registerForStudent,methods=["GET", "POST"])
    app.add_url_rule("/registerForCompany", view_func=views.registerForCompany,methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=views.logout,methods=["GET", "POST"])
    app.add_url_rule("/create_announcement", view_func = views.create_announcement,methods = ["GET", "POST"])
    app.add_url_rule("/get_announcements", view_func=views.get_announcements,methods = ['GET'])
    app.add_url_rule("/announcements/<int:ann_key>",view_func = views.announcement,methods = ['GET','POST'])
    app.add_url_rule("/applicationsStudents",view_func = views.get_applications_student,methods = ['GET'])
    app.add_url_rule("/applicationsCompanies",view_func = views.get_applications_company,methods = ['GET','POST'])
    app.add_url_rule("/applicationsCompanies/<int:app_id>/<int:s_id>",view_func = views.application_action,methods = ['GET','POST'])
    app.add_url_rule("/accepted/<int:app_id>", view_func=views.accept_app,methods=["GET", "POST"])
    app.add_url_rule("/rejected/<int:app_id>", view_func=views.reject_app,methods=["GET", "POST"])
    app.add_url_rule("/profile", view_func=views.profile,methods=["GET","POST"])
    app.add_url_rule("/profile/edit", view_func=views.edit_text,methods=["GET","POST"])
    app.add_url_rule("/profile/editphoto", view_func = views.edit_photo, methods = ["GET", "POST"])
    app.add_url_rule("/companies", view_func=views.companies, methods = ["GET"])
    app.add_url_rule("/companies/<int:c_id>", view_func=views.company_page, methods = ["GET"])
    app.add_url_rule("/profile/editinformations",view_func=views.edit_profile,methods = ["GET","POST"])
    app.add_url_rule("/deleted",view_func=views.delete_profile,methods = ["GET"])
    app.add_url_rule("/deleteapp/<int:app_id>",view_func=views.delete_app,methods = ["GET","POST"])
    app.add_url_rule("/deleteann/<int:ann_id>",view_func=views.delete_announcement,methods = ["GET","POST"])
    app.add_url_rule("/edit_announcement/<int:ann_id>",view_func=views.edit_announcement,methods = ["GET","POST"])
    mysql = Database(app)
    app.config["db"] = mysql
    return app

if __name__ == '__main__':
    app= create_app()
    app.run(host="0.0.0.0",port=8080,debug=True)