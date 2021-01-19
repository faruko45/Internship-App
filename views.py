from flask import Flask, render_template, request, redirect, url_for, session ,current_app
from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import re 
import settings,views
from database import Database
from werkzeug.datastructures import  FileStorage
from base64 import b64encode
import hashlib, binascii, os

def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def homepage():
    values = {}
    if request.method == 'GET' and 'id' in session and session["status"] == 'student':
        mysql = current_app.config["db"]
        values = mysql.get_all_announcements_students()
        deps = mysql.get_departments()
        comps = mysql.get_companies()
    elif request.method == 'POST' and 'id' in session and session["status"] == 'student':
        mysql = current_app.config["db"]
        if request.form['company'] != 'all' and request.form['department'] != 'all':
            values = mysql.get_all_announcements_with_company_and_department(request.form['company'],request.form['department'])
        elif request.form['company'] != 'all':
            values = mysql.get_all_announcements(request.form['company'])
        elif request.form['department'] != 'all':
            values = mysql.get_all_announcements_with_department(request.form['department'])
        else:
            values = mysql.get_all_announcements_students()
        print(request.form)
        deps = mysql.get_departments()
        comps = mysql.get_companies()
    for value in values:
        if isinstance((value['photo']),bytes):
            value['photo'] = b64encode(value['photo']).decode("utf-8")
    return render_template("homePage.html",values = values, deps = deps, comps = comps)

def login(): 
    msg = '' 
    if (request.method == 'POST') and (('email' in request.form and 'password' in request.form) or ('c_email' in request.form and 'c_password' in request.form)): 
        if ('email' in request.form and 'password' in request.form):
            email = request.form['email'] 
            password = request.form['password'] 
            mysql=current_app.config["db"] 
            account = mysql.get_student_with_email(email)
            if account:
                if verify_password(account['s_password'],password):
                    session['loggedin'] = True
                    current_app.config["log"] = True
                    session['id'] = account['id'] 
                    session['name'] = account['student_name'] 
                    session['status'] = 'student'
                    msg = 'Logged in successfully !'
                    return render_template('index.html', msg = msg)
                else:
                    msg = 'Incorrect'
            else: 
                msg = 'Incorrect username / password !' 
        if ('c_email' in request.form and 'c_password' in request.form):
            email = request.form['c_email']
            password = request.form['c_password']
            mysql = current_app.config["db"] 
            account = mysql.get_company_with_email(email)
            if account:
                if verify_password(account['c_password'],password):
                    session['loggedin'] = True
                    current_app.config["log"] = True
                    session['id'] = account['id'] 
                    session['name'] = account['companyName']
                    session['status'] = 'company' 
                    msg = 'Logged in successfully !'
                    return render_template('index.html', msg = msg)
                else:
                    msg = 'Incorrect'
            else: 
                msg = 'Incorrect'
    return render_template('login.html', msg = msg) 


def registerForStudent(): 
    msg = ''
    mysql=current_app.config["db"]
    deps = mysql.get_departments() 
    facs = mysql.get_faculties()
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form and 'surname' in request.form and 'department' in request.form and 'faculty' in request.form  and 'birthDate' in request.form: 
        name = request.form['name']
        surname = request.form['surname'] 
        password = request.form['password'] 
        email = request.form['email']
        faculty = request.form['faculty']
        department = request.form['department']
        birthDate = request.form['birthDate']
        mysql=current_app.config["db"] 
        account= mysql.get_student_with_email(email)  
        if account: 
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', name): 
            msg = 'Username must contain only characters and numbers !'
        elif not name or not password or not email: 
            msg = 'Please fill out the form !'
        else: 
            h = hash_password(password)
            mysql.set_student_info(email,h,name,surname,birthDate,faculty,department) 
            msg = 'You have successfully registered !'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('registerForStudent.html', msg = msg, deps = deps, facs = facs)

def registerForCompany(): 
    msg = '' 
    if request.method == 'POST' and 'cname' in request.form and 'password' in request.form and 'email' in request.form : 
        cname = request.form['cname'] 
        password = request.form['password'] 
        email = request.form['email'] 
        mysql=current_app.config["db"] 
        account= mysql.get_company_with_email(email)
        if account: 
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', cname): 
            msg = 'Name must contain only characters and numbers !'
        elif not cname or not password or not email: 
            msg = 'Please fill out the form !'
        else:
            h = hash_password(password) 
            mysql.set_company_info(cname, email,h)
            msg = 'You have successfully registered !'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('registerForCompany.html', msg = msg)

def profile():
    if request.method == 'GET':
        if session['status'] == 'student':
            mysql = current_app.config['db']
            informations = mysql.get_student_info_with_id(session['id'])
            texts = mysql.get_text_with_student_id(session['id'])
            if informations['photo'] != None and isinstance((informations['photo']),bytes):
                informations['photo'] = b64encode(informations['photo']).decode("utf-8")
            return render_template('studentProfile.html',informations = informations, texts = texts, announcements = None)
        elif session['status'] == 'company':
            mysql = current_app.config['db']
            informations = mysql.get_company_info_with_id(session['id'])
            texts = mysql.get_text_with_company_id(session['id'])
            announcements = mysql.get_all_announcements(session['id'])
            company_photos = mysql.get_company_photos(session['id'])
            for photo in company_photos:
                if isinstance((photo['photo']),bytes):
                    photo['photo'] = b64encode(photo['photo']).decode("utf-8")
            return render_template('companyProfile.html',informations = informations,texts = texts, announcements = announcements, company_photos = company_photos)
    elif request.method == 'POST':
        if session['status'] == 'student':
            mysql = current_app.config['db']
            informations = mysql.get_student_info_with_id(session['id'])
            texts = mysql.get_text_with_student_id(session['id'])
            if request.files['s_photo']:
                photo = request.files['s_photo']
                photo_read = photo.read()
                photo_id = mysql.add_photo(photo_read)
                if informations['photo_id'] is not None:
                    mysql.delete_photo(informations['photo_id'])
                mysql.update_student_photo(photo_id,session['id'])
            informations = mysql.get_student_info_with_id(session['id'])
            if informations['photo'] != None and isinstance((informations['photo']),bytes):
                informations['photo'] = b64encode(informations['photo']).decode("utf-8")
            return render_template('studentProfile.html',informations = informations, texts = texts, announcements = None)
        if session['status'] == 'company':
            mysql = current_app.config['db']
            if request.files['c_photo']:
                photo = request.files['c_photo']
                photo_read = photo.read()
                mysql.add_photo_company(photo_read,session['id'])
            company_photos = mysql.get_company_photos(session['id'])
            for photo in company_photos:
                if isinstance((photo['photo']),bytes):
                    photo['photo'] = b64encode(photo['photo']).decode("utf-8")
            informations = mysql.get_company_info_with_id(session['id'])
            texts = mysql.get_text_with_company_id(session['id'])
            announcements = mysql.get_all_announcements(session['id'])
            return render_template('companyProfile.html',informations = informations,texts = texts, announcements = announcements, company_photos = company_photos)
def edit_profile():
    if request.method == 'GET':
        if session['status'] == 'student':
            mysql = current_app.config['db']
            deps = mysql.get_departments()
            facs = mysql.get_faculties()
            return render_template('edit_profile.html',deps = deps, facs = facs)
        if session['status'] == 'company':
            return render_template('edit_profile.html')
    if request.method == 'POST':
        if session['status'] == 'student':
            if 'name' in request.form and 'password' in request.form and 'email' in request.form and 'surname' in request.form and 'department' in request.form and 'faculty' in request.form  and 'birthDate' in request.form:
                name = request.form['name']
                surname = request.form['surname'] 
                password = request.form['password'] 
                email = request.form['email']
                faculty = request.form['faculty']
                department = request.form['department']
                birthDate = request.form['birthDate']
                mysql=current_app.config["db"]
                informations = mysql.get_student_info_with_id(session['id'])
                account = mysql.get_student_with_email(email)
                if account and account['e_mail'] != informations['e_mail']:
                    return render_template('information.html',msg = "An acoount exists with this e-mail.")
                h = hash_password(password)
                mysql.update_student(session['id'],name,surname,email,h,birthDate,faculty,department)
                return redirect(url_for('profile'))  
            else:
                return render_template('information.html',msg = "missing parts")
        if session['status'] == 'company':
            if 'cname' in request.form and 'password' in request.form and 'email' in request.form:
                cname = request.form['cname'] 
                password = request.form['password'] 
                email = request.form['email'] 
                mysql=current_app.config["db"] 
                account= mysql.get_company_with_email(email)
                informations = mysql.get_company_info_with_id(session['id'])
                if account and account['e_mail'] != informations['e_mail']:
                    return render_template('information.html',msg = "An acoount exists with this e-mail.")
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
                    msg = 'Invalid email address !'
                    return render_template('information.html',msg = msg)
                elif not re.match(r'[A-Za-z0-9]+', cname): 
                    msg = 'Name must contain only characters and numbers !'
                    return render_template('information.html',msg = msg)
                elif not cname or not password or not email: 
                    msg = 'Please fill out the form !'
                    return render_template('information.html',msg = msg)
                h = hash_password(password)
                mysql.update_company(session['id'],cname,email,h)
                return redirect(url_for('profile'))
            else:
                return render_template('information.html',msg = "missing parts")

def delete_profile():
    if request.method == 'GET':
        mysql = current_app.config['db']
        if session['status'] == 'student':
            informations = mysql.get_student_info_with_id(session['id'])
            mysql.delete_photo(informations['photo_id'])
            mysql.delete_student(session['id'])
            return redirect(url_for('logout'))
        if session['status'] == 'company':
            announcements = mysql.get_all_announcements(session['id'])
            for x in announcements:
                mysql.delete_photo(x['photo_id'])
                mysql.delete_text(x['text_id'])
            mysql.delete_company(session['id'])
            return redirect(url_for('logout'))

def create_announcement():
    msg = ''
    if request.method == 'POST' and 'a_topic' in request.form and 'a_date' in request.form and request.form['a_date'] != "" and 'a_department' in request.form and 'a_text' in request.form  and request.files['a_photo'] :
        topic = request.form['a_topic']
        date = request.form['a_date']
        dep = request.form['a_department']
        text = request.form['a_text']
        photo = request.files['a_photo']
        photo_read = photo.read()
        mysql = current_app.config['db']
        currentText = mysql.add_text(text)
        currentPhoto = mysql.add_photo(photo_read)
        mysql.create_announcement(topic,date,session['id'],dep,currentText,currentPhoto)
        msg = 'Announcement successfully created !'
    elif request.method == 'GET':
        mysql = current_app.config['db']
        deps = mysql.get_departments()
        return render_template('create_ann.html',msg = msg,deps = deps)
    else:
        msg = 'missing parts'
    return render_template('information.html',msg = msg)

def get_announcements():
    if request.method == 'GET':
        mysql = current_app.config['db']
        values = mysql.get_all_announcements(session['id'])
        for value in values:
            if isinstance((value['photo']),bytes):
                value['photo'] = b64encode(value['photo']).decode("utf-8")
        return render_template('announcements.html',values = values)

def announcement(ann_key):
    if request.method == 'GET':
        mysql = current_app.config['db']
        ann = mysql.get_announcement(ann_key)
        if isinstance((ann['photo']),bytes):
            ann['photo'] = b64encode(ann['photo']).decode("utf-8")
        return render_template('announcement.html',ann = ann)
    elif request.method == 'POST':
        if session['status'] == 'student':
            mysql = current_app.config['db']
            mysql.apply_announcement(ann_key,session['id'])
            return render_template('information.html',msg = "You have succesfully applied.")
        elif session['status'] == 'company':
            mysql = current_app.config['db']
            mysql.close_announcement(ann_key)
            return render_template('information.html',msg = "Announcement has been closed.")

def edit_announcement(ann_id):
    mysql = current_app.config['db']
    if request.method == 'GET':
        ann = mysql.get_announcement(ann_id)
        deps = mysql.get_departments()
        return render_template('ann_edit.html',ann = ann,deps = deps)
    if request.method == 'POST':
        ann = mysql.get_announcement(ann_id)
        if request.files['a_photo']:
            photo = request.files['a_photo']
            photo_read = photo.read()
            mysql.update_photo(ann['photo_id'],photo_read)
        if 'a_topic' in request.form and 'a_date' in request.form and request.form['a_date'] != "" and 'a_department' in request.form and 'a_text' in request.form:
            topic = request.form['a_topic']
            date = request.form['a_date']
            dep = request.form['a_department']
            text = request.form['a_text']

            mysql.update_text(ann['text_id'],text)
            mysql.update_announcement(ann_id,topic,date,dep)
            return redirect(url_for('announcement',ann_key = ann_id))
            

def delete_announcement(ann_id):
    if request.method == 'POST':
        mysql = current_app.config['db']
        ann = mysql.get_announcement(ann_id)
        mysql.delete_photo(ann['photo_id'])
        mysql.delete_text(ann['text_id'])
        mysql.delete_announcement(ann_id)
        return redirect(url_for('get_announcements'))

def get_applications_student():
    if request.method == 'GET':
        mysql = current_app.config['db']
        applications = mysql.get_all_applications_students(session['id'])
        count = mysql.get_count_applications_students(session['id'])
        print(count)
        return render_template('applicationsStudent.html',applications=applications,count = count)

def get_applications_company():
    if request.method == 'GET':
        mysql = current_app.config['db']
        applications = mysql.get_all_applications_companies(session['id'])
        count = mysql.get_count_applications_companies(session['id'])
        return render_template('applicationsCompanies.html',applications=applications,count=count)

def application_action(app_id,s_id):
    if request.method == 'GET':
        mysql = current_app.config['db']
        announcement = mysql.get_announcement_with_app_id(app_id)
        if isinstance((announcement['photo']),bytes):
            announcement['photo'] = b64encode(announcement['photo']).decode("utf-8")
        student = mysql.get_student_info_with_id(s_id)
        s_texts = mysql.get_text_with_student_id(s_id)
        if isinstance((student['photo']),bytes):
            student['photo'] = b64encode(student['photo']).decode("utf-8")
        return render_template('action_application.html',announcement = announcement, student = student, application_id = app_id,s_texts = s_texts)

def accept_app(app_id):
    msg = ''
    if request.method == 'POST':
        mysql = current_app.config['db']
        mysql.set_app_status(app_id,'Accepted')
        msg = 'ACCEPTED'
        return render_template('information.html',msg = msg)

def reject_app(app_id):
    msg = ''
    if request.method == 'POST':
        mysql = current_app.config['db']
        mysql.set_app_status(app_id,'Rejected')
        msg = 'REJECTED'
        return render_template('information.html',msg = msg)

def delete_app(app_id):
    if request.method == 'POST' or request.method == 'GET':
        mysql = current_app.config['db']
        mysql.delete_application(app_id)
        return redirect(url_for('get_applications_student'))

def edit_text():
    if request.method == 'GET':
        if session['status'] == 'student':
            mysql = current_app.config['db']
            texts = mysql.get_text_with_student_id(session['id'])
        elif session['status'] == 'company':
            mysql = current_app.config['db']
            texts = mysql.get_text_with_company_id(session['id'])
        return render_template('text_manipulation.html',texts = texts)
    elif request.method == 'POST':
        if 'addText' in request.form:
            if session['status'] == 'student':
                mysql = current_app.config['db']
                text = request.form['addText']
                mysql.add_text_with_student(text,session['id'])
            elif session['status'] == 'company':
                mysql = current_app.config['db']
                text = request.form['addText']
                mysql.add_text_with_company(text,session['id'])
        else:
            mysql = current_app.config['db']
            values = request.form
            for x in values.keys():
                mysql.update_text(x,values[x])
        return redirect(url_for('profile'))

def edit_photo():
    if request.method == 'GET':
        mysql = current_app.config['db']
        company_photos = mysql.get_company_photos(session['id'])
        for photo in company_photos:
            if isinstance((photo['photo']),bytes):
                photo['photo'] = b64encode(photo['photo']).decode("utf-8")
        return render_template('edit_photo.html',photos = company_photos)
    if request.method == 'POST':
        mysql = current_app.config['db']
        for x in request.form.getlist('photo'):
            mysql.delete_photo(x)
        return redirect(url_for('profile'))

def companies():
    if request.method == 'GET':
        mysql = current_app.config['db']
        comps = mysql.get_companies()
        return render_template('companies.html',companies = comps)
    
def company_page(c_id):
    if request.method == 'GET':
        mysql = current_app.config['db']
        informations = mysql.get_company_info_with_id(c_id)
        texts = mysql.get_text_with_company_id(c_id)
        announcements = mysql.get_all_announcements(c_id)
        company_photos = mysql.get_company_photos(c_id)
        for photo in company_photos:
            if isinstance((photo['photo']),bytes):
                photo['photo'] = b64encode(photo['photo']).decode("utf-8")
        return render_template('companyProfile.html',informations = informations,texts = texts, announcements = announcements, company_photos = company_photos)


def logout(): 
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('name', None) 
    session.pop('status', None)
    return redirect(url_for('login')) 