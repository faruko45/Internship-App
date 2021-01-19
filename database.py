from flask_mysqldb import MySQL 
import settings
class Database:
    def __init__(self, app):
        app.config['MYSQL_HOST'] = settings.SQL_PORT
        app.config['MYSQL_USER'] = 'ubjbhdmtypwhsbbk'
        app.config['MYSQL_PASSWORD'] = settings.PASSWORD
        app.config['MYSQL_DB'] = 'bfyhtlyruvz3akf2nq3h'
        app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
        app.config["SECRET_KEY"] = '8_fCHi3kLIvjmTezEOL2jQ'
        mysql = MySQL(app)
        self.dbfile = mysql

    def get_student_info(self,email,password):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute('SELECT * FROM students WHERE e_mail = %s AND s_password = %s', (email, password, ))
        return  cursor.fetchone() 

    def get_student_with_email(self,email):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute('SELECT * FROM students  WHERE e_mail = %s', (email, )) 
        return  cursor.fetchone() 

    def set_student_info(self,email,password,name,surname,birthDate,faculty,department):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('INSERT INTO students VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, NULL)', (email,password,name,surname,birthDate,faculty,department, )) 
        self.dbfile.connection.commit()

    def get_student_info_with_id(self,s_id):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute("""select students.student_name,students.s_password, students.surname, students.photo_id,students.birthDate, students.e_mail,faculties.fname, departments.dname, photos.photo from students
        LEFT JOIN faculties on students.faculty_id = faculties.id
        LEFT JOIN departments on students.department_id = departments.id
        LEFT JOIN photos on students.photo_id = photos.id
        WHERE students.id = %s""", (s_id, ))
        return  cursor.fetchone()  

    def update_student(self,s_id,s_name,surname,email,password,birthDate,faculty,department):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('UPDATE students SET e_mail = %s,s_password = %s, student_name = %s, surname = %s, birthDate = %s,faculty_id = %s, department_id = %s Where id = %s', (email,password,s_name,surname,birthDate,faculty,department,s_id)) 
        self.dbfile.connection.commit()

    def delete_student(self,s_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('DELETE from students where id = %s',(s_id,)) 
        self.dbfile.connection.commit()

    def get_company_info(self,email,password):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute('SELECT * FROM companies WHERE e_mail = % s AND c_password = % s', (email, password, ))
        return  cursor.fetchone()  
    
    def get_company_info_with_id(self,c_id):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute('SELECT * FROM companies WHERE id = % s', (c_id, ))
        return  cursor.fetchone() 

    def set_company_info(self,name,email,password):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('INSERT INTO companies VALUES (NULL, % s, %s, %s)', (name,email,password, )) 
        self.dbfile.connection.commit()     

    def get_company_with_email(self,email):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute('SELECT * FROM companies  WHERE e_mail = % s', (email, )) 
        return  cursor.fetchone()

    def get_companies(self):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute('SELECT id,companyName FROM companies') 
        return  cursor.fetchall()
    
    def update_company(self,c_id,companyName,email,password):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('UPDATE companies SET e_mail = %s,c_password = %s,companyName = %s WHERE id = %s', (email,password,companyName,c_id,)) 
        self.dbfile.connection.commit()
    
    def delete_company(self,c_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('DELETE from companies where id = %s',(c_id,)) 
        self.dbfile.connection.commit()

    def create_announcement(self,topic,date,company,department,text,photo):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('INSERT INTO internship_announcements VALUES (NULL, %s, %s, %s, %s, %s, %s,False)',(topic, date, company, department, text, photo, ))
        self.dbfile.connection.commit()
    
    def get_all_announcements(self,c_id):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute("""select internship_announcements.id,internship_announcements.topic, companies.companyName, internship_announcements.announcement_date,internship_announcements.text_id,internship_announcements.photo_id, internship_announcements.expired,
        departments.dname, texts.content, photos.photo from internship_announcements 
        INNER JOIN departments ON internship_announcements.department_id = departments.id 
        INNER JOIN texts on internship_announcements.text_id = texts.id
        INNER JOIN companies on internship_announcements.company_id = companies.id
        INNER JOIN photos on internship_announcements.photo_id = photos.id
        WHERE internship_announcements.company_id = %s """,(c_id,)) 
        return  cursor.fetchall() 

    def get_all_announcements_with_company_and_department(self,c_id,d_id):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute("""select internship_announcements.id, internship_announcements.topic, companies.companyName, internship_announcements.announcement_date, internship_announcements.expired,
        departments.dname, texts.content, photos.photo from internship_announcements 
        INNER JOIN departments ON internship_announcements.department_id = departments.id 
        INNER JOIN texts on internship_announcements.text_id = texts.id
        INNER JOIN companies on internship_announcements.company_id = companies.id
        INNER JOIN photos on internship_announcements.photo_id = photos.id
        WHERE internship_announcements.company_id = %s AND internship_announcements.department_id = %s""",(c_id,d_id,)) 
        return  cursor.fetchall() 

    def get_all_announcements_with_department(self,d_id):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute("""select internship_announcements.id, internship_announcements.topic, companies.companyName, internship_announcements.announcement_date, internship_announcements.expired,
        departments.dname, texts.content, photos.photo from internship_announcements 
        INNER JOIN departments ON internship_announcements.department_id = departments.id 
        INNER JOIN texts on internship_announcements.text_id = texts.id
        INNER JOIN companies on internship_announcements.company_id = companies.id
        INNER JOIN photos on internship_announcements.photo_id = photos.id
        WHERE internship_announcements.department_id = %s""",(d_id,)) 
        return  cursor.fetchall()      

    def get_all_announcements_students(self):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute("""select internship_announcements.id, internship_announcements.topic, companies.companyName, internship_announcements.announcement_date, internship_announcements.expired, 
        departments.dname, texts.content, photos.photo from internship_announcements 
        INNER JOIN departments ON internship_announcements.department_id = departments.id 
        INNER JOIN texts on internship_announcements.text_id = texts.id
        INNER JOIN photos on internship_announcements.photo_id = photos.id
        INNER JOIN companies on internship_announcements.company_id = companies.id """) 
        return  cursor.fetchall()
    

    def get_announcement(self,a_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute("""select internship_announcements.id, topic, announcement_date, companies.companyName, departments.dname,internship_announcements.department_id, texts.content, internship_announcements.text_id,internship_announcements.photo_id,photos.photo, internship_announcements.expired from internship_announcements
        INNER JOIN companies on internship_announcements.company_id = companies.id
        INNER JOIN departments on internship_announcements.department_id = departments.id
        INNER JOIN texts on internship_announcements.text_id = texts.id
        INNER JOIN photos on internship_announcements.photo_id = photos.id
        where internship_announcements.id = %s""" ,(a_id,))
        return cursor.fetchone() 

    def get_announcement_with_app_id(self,app_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute("""select topic, dname, announcement_date, content, photos.photo, internship_announcements.expired from internship_announcements
        INNER JOIN internship_applications on internship_announcements.id = internship_applications.internshipAnnouncement_id
        INNER JOIN texts on internship_announcements.text_id = texts.id
        INNER JOIN departments on internship_announcements.department_id = departments.id
        INNER JOIN photos on internship_announcements.photo_id = photos.id
        WHERE internship_applications.id = %s""",(app_id,))
        return cursor.fetchone()

    def apply_announcement(self,a_id,s_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('INSERT INTO internship_applications VALUES (NULL,%s,%s,%s)',('Pending',s_id,a_id,))
        self.dbfile.connection.commit()

    def update_announcement(self,id,topic,announcement_date,department):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('UPDATE internship_announcements SET topic = %s, announcement_date = %s, department_id = %s WHERE id = %s',(topic,announcement_date,department,id,))
        self.dbfile.connection.commit()

    def delete_announcement(self,ann_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('DELETE from internship_announcements where id = %s',(ann_id,)) 
        self.dbfile.connection.commit()

    def delete_application(self,app_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('DELETE from internship_applications where id = %s',(app_id,)) 
        self.dbfile.connection.commit()

    def close_announcement(self,a_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('UPDATE internship_announcements SET expired = True where id = %s',(a_id,))
        self.dbfile.connection.commit()

    def add_text(self,text):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('INSERT INTO texts VALUES (NULL,%s,NULL,NULL)',(text,))
        self.dbfile.connection.commit()
        return cursor.lastrowid

    def add_text_with_company(self,text,c_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('INSERT INTO texts VALUES (NULL,%s,%s,NULL)',(text,c_id,))
        self.dbfile.connection.commit()

    def add_text_with_student(self,text,s_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('INSERT INTO texts VALUES (NULL,%s,NULL,%s)',(text,s_id,))
        self.dbfile.connection.commit()

    def get_text_with_id(self,t_id):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute('SELECT * FROM texts  WHERE id = % s', (t_id, )) 
        return  cursor.fetchone()

    def get_text_with_student_id(self,s_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('select * from texts where student_id = %s',(s_id,))
        return cursor.fetchall()

    def get_text_with_company_id(self,c_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('select * from texts where company_id = %s',(c_id,))
        return cursor.fetchall()

    def update_text(self,t_id,content):
        cursor = self.dbfile.connection.cursor()
        cursor.execute('UPDATE texts SET content = %s WHERE id = %s',(content,t_id,))
        self.dbfile.connection.commit()

    def delete_text(self,t_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute("DELETE FROM texts WHERE id = %s",(t_id, ))
        self.dbfile.connection.commit()

    def get_departments(self):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute('SELECT * FROM departments') 
        return  cursor.fetchall()

    def get_department_with_id(self,d_id):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute('SELECT * FROM departments  WHERE id = % s', (d_id, )) 
        return  cursor.fetchone()

    def get_faculties(self):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute('SELECT * FROM faculties') 
        return  cursor.fetchall()

    def get_all_applications_students(self,s_id):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute("""select internship_applications.id, internship_applications.student_id, topic, companyName, dname, announcement_date, content, app_status, photos.photo from internship_applications
        INNER JOIN internship_announcements ON internship_applications.internshipAnnouncement_id = internship_announcements.id
        LEFT JOIN companies ON internship_announcements.company_id = companies.id
        LEFT JOIN departments ON internship_announcements.department_id = departments.id
        LEFT JOIN texts ON internship_announcements.text_id = texts.id
        INNER JOIN photos ON internship_announcements.photo_id = photos.id
        WHERE internship_applications.student_id = %s """,(s_id,)) 
        return  cursor.fetchall()

    def get_all_applications_companies(self,c_id):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute("""select internship_applications.id, internship_applications.student_id, students.student_name, students.surname, topic, dname, announcement_date, content, app_status, photos.photo from internship_applications
        INNER JOIN internship_announcements ON internship_applications.internshipAnnouncement_id = internship_announcements.id
        LEFT JOIN departments ON internship_announcements.department_id = departments.id
        LEFT JOIN texts ON internship_announcements.text_id = texts.id
        LEFT JOIN students ON internship_applications.student_id = students.id
        INNER JOIN photos ON internship_announcements.photo_id = photos.id
        WHERE internship_announcements.company_id = %s """,(c_id,)) 
        return  cursor.fetchall()

    def count_apps_wrt_status(self,c_id):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute("""select app_status,Count(*) as count from internship_applications
        INNER JOIN internship_announcements ON internship_applications.internshipAnnouncement_id = internship_announcements.id
        WHERE internship_announcements.company_id = %s
        group by app_status""",(c_id,)) 
        return  cursor.fetchall()

    def get_count_applications_students(self,s_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute("select COUNT(*) from internship_applications Where student_id = %s",(s_id,))
        count = cursor.fetchone()['COUNT(*)']
        return count

    def get_count_applications_companies(self,c_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute(""" select COUNT(*) from internship_applications
        INNER JOIN internship_announcements ON internship_applications.internshipAnnouncement_id = internship_announcements.id
        LEFT JOIN departments ON internship_announcements.department_id = departments.id
        LEFT JOIN texts ON internship_announcements.text_id = texts.id
        LEFT JOIN students ON internship_applications.student_id = students.id
        INNER JOIN photos ON internship_announcements.photo_id = photos.id
        WHERE internship_announcements.company_id = %s """,(c_id, ))
        count = cursor.fetchone()['COUNT(*)']
        return count

    def set_app_status(self,app_id,status):
        cursor = self.dbfile.connection.cursor()
        cursor.execute("UPDATE internship_applications SET app_status = %s WHERE id = %s ",(status,app_id, ))
        self.dbfile.connection.commit()

    def add_photo(self,photo):
        cursor = self.dbfile.connection.cursor()
        cursor.execute("INSERT INTO photos VALUES (NULL,%s,NULL)",(photo, ))
        self.dbfile.connection.commit()
        return cursor.lastrowid
    
    def add_photo_company(self,photo,company_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute("INSERT INTO photos VALUES (NULL,%s,%s)",(photo,company_id, ))
        self.dbfile.connection.commit()
        return cursor.lastrowid

    def get_company_photos(self,c_id):
        cursor = self.dbfile.connection.cursor() 
        cursor.execute("""select * from photos WHERE company_id = %s """,(c_id,)) 
        return  cursor.fetchall()

    def update_student_photo(self,photo_id,student_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute("UPDATE students SET photo_id = %s WHERE id = %s",(photo_id,student_id ))
        self.dbfile.connection.commit()
    
    def delete_photo(self,p_id):
        cursor = self.dbfile.connection.cursor()
        cursor.execute("DELETE FROM photos WHERE id = %s",(p_id, ))
        self.dbfile.connection.commit()

    def update_photo(self,p_id,photo):
        cursor = self.dbfile.connection.cursor()
        cursor.execute("UPDATE photos SET photo = %s WHERE id = %s",(photo,p_id, ))
        self.dbfile.connection.commit()