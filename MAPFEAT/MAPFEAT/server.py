''' Server-end code for MAPFEAT web tool
Python files written by Rachel Quapp '''

''' Import MAPFEAT Python files ''' 
import classifyTweets
import extractFeatures
import finalizeFeatures
import processTweets
import searchAppStore
import topicModeling
import querysearch

''' Import Flask Backend '''
from flask import *
from werkzeug.utils import secure_filename # blocks malicious files disguised as csv
import os, csv, sys
import random
import shutil
import requests
import tablib

import globa
import sqlite3
import StringIO

from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask import session, abort
from wtforms import Field, TextField, widgets, SelectMultipleField, Form
from wtforms.widgets import TextInput, html_params
from flask_recaptcha import ReCaptcha
from flask_wtf import RecaptchaField, FlaskForm

from globa import *
from functools import wraps
from sqlalchemy.orm import sessionmaker
from tabledef import *

import dummy


from os.path import basename
import glob
import pandas as pd
import re

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

#from flask_sqlalchemy import SQLAlchemy

#from flask_mail import Mail, Message

#app.config[] -- set up mail server

engine = create_engine('sqlite:///userpass.db', echo=True)

reload(sys)  
sys.setdefaultencoding('utf8')

RECAPTCHA_PUBLIC_KEY = '6Ld6aWYUAAAAAM00of-ydMGGFtzRoLMmwU8avCj4'
RECAPTCHA_PRIVATE_KEY = '6Ld6aWYUAAAAAAAQ4cT6H45PTzrKcs27vlJrCr1q'

''' Instantiation of Flask class and environment variables '''
app = Flask(__name__)
app.config.from_object(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/manjeet.dev1/Desktop/mapfeat_web_summer-2018/mapfeat/mapfeat/login.db'
app.config['SECRET_KEY'] = 'thisissecret'

db = SQLAlchemy(app)

recaptcha = ReCaptcha(app=app)
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Ld6aWYUAAAAAM00of-ydMGGFtzRoLMmwU8avCj4'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Ld6aWYUAAAAAAAQ4cT6H45PTzrKcs27vlJrCr1q'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/manjeet.dev1/Desjtio/login.db'

app.secret_key = '\xf9o\n\xfbP\xd4\xb7\xa6$\x1e\xb9\x8c\xb6\x06$\xce\xca\xeb\x14\x1cwo\xce\xec'

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/data/'
OUTPUT_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/output/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
ALLOWED_EXTENSIONS = set(['csv'])

login_manager = LoginManager()
login_manager.init_app(app)

class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    
@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)

#RECAPTCHA_ENABLED = True
#RECAPTCHA_SITE_KEY = "6Ld6aWYUAAAAAM00of-ydMGGFtzRoLMmwU8avCj4"
#RECAPTCHA_SECRET_KEY = "6Ld6aWYUAAAAAAAQ4cT6H45PTzrKcs27vlJrCr1q"
#RECAPTCHA_THEME = "dark"
#RECAPTCHA_TYPE = "image"
#RECAPTCHA_SIZE = "normal"
#RECAPTCHA_RTABINDEX = 10
#reCaptcha.init(app, site_key, secret_key, is_enabled=True)

'''def checkRecaptcha(response, secretkey):
        url = 'https://www.google.com/recaptcha/api/siteverify?'
        url = url + 'secret=' + str(secretkey)
        url = url + '&response=' +str(response)

        jsonobj = json.loads(urllib2.urlopen(url).read())
        print jsonobj['success']
        if jsonobj['success']:
            print jsonobj['success']
            return True
        else:
            return False'''

''' Instantiation of class check boxes '''

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class SimpleForm(Form):
    string_of_files = ['one\r\ntwo\r\nthree\r\n']
    list_of_files = string_of_files[0].split()
    # create a list of value/description tuples
    files = [(x, x) for x in list_of_files]
    example = MultiCheckboxField('Label', choices=files)


class parameters_2:
    def __init__(self, var1, var2, var3, var4):
        self.keyword1 = var1
        self.keyowrd2 = var2
        self.keyword3 = var3
        self.keyword4 = var4

parameters_2 = parameters_2(-1, -1, -1, -1)


class LoginForm(FlaskForm):
    recaptcha = RecaptchaField()





''' Instantiation of class for environment vars '''
class parameters:
    def __init__(self, var1, var2, var3, var4):
        self.wordsPerTopics = var1
        self.numTopics = var2
        self.appLimit = var3
        self.sharedBetween = var4

parameters = parameters(-1, -1, -1, -1)

''' Attaching timestamp onto css files to clear cache '''
@app.context_processor
def override_url_for():
    return dict(url_for = dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            # insert random timestamp onto csv such that it updates without caching.
            values['q'] = int(random.random()*os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)








''' login decorators'''
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('you need to log in first to access this page')
            return redirect(url_for('login'))
    return wrap










''' Start Page '''

@app.route('/', methods = ['GET', 'POST'])
def home_():
    return render_template('home_.html')

'''login page'''

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if request.method == 'POST':
        
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
        
        response = request.form.get('g-recaptcha-response')
        
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
        result = query.first()
        print(query)
        print('query^')
        print(result)
        
        #if recaptcha.verify():
            #print('yes verify')
        if request.form.get('remember'):
            print('dog,cat')
            remember = True
        print(recaptcha.verify())
        #print(g-recaptcha-response)
        if result and recaptcha.verify(): #and recaptcha.verify():
            session['logged_in'] = True
            flash('successful login')
            
            #login_user(request.form['username'],remember=True,duration=200,force=False,fresh=True)
            
            login_user(User,True)
            #login_user(user, remember=form.remember_me.data)
            #return redirect(url_for('post_home'))
            return render_template('index.html', form=form)
        else:
            error = 'Invalid Credentials. Please try again.\n\n Contact Suport -> ruhe@ucalgary.ca'
    return render_template('login.html', error=error)
        

'''logout'''

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('successful logout')
    return render_template('home_.html')

'''home after login'''
@app.route('/post_home')
@login_required
def post_home():
    '''if recaptcha.verify():
        # SUCCESS
        flash('good job ')
        return render_template('post_login_home.html')
    else:
        # FAILED
        return render_template('login.html', error=error)'''
    return render_template('post_login_home.html')
    


@app.route('/first', methods = ['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and permit(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            try:
                os.rename(os.path.join(app.config['UPLOAD_FOLDER'], filename), \
                          os.path.join(app.config['UPLOAD_FOLDER'], 'dataSet.csv'))
            except:
                # catch overwrite cases
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'dataSet.csv'))
                os.rename(os.path.join(app.config['UPLOAD_FOLDER'], filename), \
                          os.path.join(app.config['UPLOAD_FOLDER'], 'dataSet.csv'))
            return redirect(url_for('inputs'))
        return redirect(url_for('error'))
    return render_template('index.html')

def permit(filename):
    return'.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

''' Input Page '''
@app.route('/inputs', methods = ['GET', 'POST'])
@login_required
def inputs():
    if request.method == 'POST':
        text1 = request.form['text1']
        text2 = request.form['text2']
        text3 = request.form['text3']
        text4 = request.form['text4']
        try:
            text1, text2, text3, text4 = str(text1), str(text2), str(text3), str(text4)
            text1, text2, text3, text4 = int(text1), int(text2), int(text3), int(text4)
        
            parameters.wordsPerTopic = text1
            parameters.numTopics = text2
            parameters.appLimit = text3
            parameters.sharedBetween = text4
            
            return redirect(url_for('results'))
        except:
            return render_template('redirect.html')
    return render_template('inputs.html')


''' new page search '''
@app.route('/screen1', methods = ['GET', 'POST'])
@login_required
def screen1():
    formData = request.values if request.method == "GET" else request.values
    if request.method == 'POST':
        
  
        text1 = request.form['t_1']
        text2 = request.form['t_2']
        text3 = request.form['t_3']
        text4 = request.form['t_4']
        try:
            
            text1, text2, text3, text4 = str(text1), str(text2), str(text3), str(text4)
          
            parameters_2.keyword1 = text1
            parameters_2.keyword2 = text2
            parameters_2.keyword3 = text3
            parameters_2.keyword4 = text4
        
            response = "Form Contents <pre>%s</pre>" % "<br/>\n".join(["%s:%s" % item for item in formData.items(multi=True)] )
            
            checks = ''
            if 'apple' in response:
                #print('APPLE')
                checks += '1'
                
            if 'google' in response:
                
                checks += '2'
                #print('#5')
            data = [checks, text1, text2, text3, text4]
            #print('#6')
            
            with open("querys.csv", "wb") as fin:
                #print('#1')
                writer = csv.writer(fin)
                #print(writer)
                #print('#2')
                for row in data:
                    #print('#3')
                    writer.writerow([row])
                    #print('#4')
                    #print(row)
                   
            
            
            return redirect(url_for('results_screen1')) 
        except Exception as e:
            print(e)
            return render_template('about.html')
    return render_template('screen1.html')



''' Results for screen 1 Page '''
@app.route('/results_screen1', methods = ['GET', 'POST'])
@login_required
def results_screen1():
    if request.method == 'GET':
        try:
            querysearch.search()
            data = []
            app =[]
            dev =[]
            htmllist=[]
            file_reader = csv.reader(open('appdata.csv', 'rb'), delimiter=',')

            for row in file_reader:
                if len(row)>=2:
                    biglist.append([i.encode('utf8') for i in row])
                    htmllist.append([i.encode('utf8') for i in row])
                    app.append(row[0])
                    dev.append(row[1])
            print(biglist)
            data.append([app, dev])
            big_dict = {}
            small_dict = {}
            for i in range(len(app)):
                big_dict[app[i]]= dev[i]
            for i in range(len(app)):
                small_dict[dev[i]]= app[i]
            length_dict=len(big_dict)
        except:
            return('Sorry, Please Try Again')
 
     
        return render_template('results_screen1.html', big_dict=big_dict,
                               htmllist=htmllist, data=data, app=app,
                               dev = dev, length_dict = length_dict,
                               small_dict = small_dict)
    return render_template('about.html')
        


'''-------------------------------------------------------------'''

''' Results Page '''
@app.route('/results', methods = ['GET', 'POST'])
@login_required
def results():
    if request.method == 'GET':
        wordsPerTopic = parameters.wordsPerTopic
        numTopics = parameters.numTopics
        appLimit = parameters.appLimit
        sharedBetween = parameters.sharedBetween
        
        print(wordsPerTopic, numTopics, appLimit, sharedBetween)
        os.chdir('C:/Users/manjeet.dev1/Desktop/mapfeat_web_summer-2018/MAPFEAT/MAPFEAT')
        OUTPUT_PATH = 'output'
        
        # Create Output path
        if os.path.exists(OUTPUT_PATH):
            shutil.rmtree(OUTPUT_PATH)
        os.makedirs(OUTPUT_PATH)
        
        # Process Tweets
        processTweets.process()
        
        
        
        render_template('inputs.html')
        # Attain classification results - k fold validation results
        results = classifyTweets.classify()
        
        
        
        accuracy = results[0]
        precision = results[1]
        recall = results[2]
        F1 = results[3]
        stdev = results[4]
   
        render_template('inputs.html')
        topicModeling.extractTopics(wordsPerTopic, numTopics)
        
        
        
        searchAppStore.search(appLimit)
        
        
    
        extractFeatures.extract()
        
        
        
        finalizeFeatures.finalize(sharedBetween)
        
        
        
        return render_template('results.html', accuracy = accuracy, \
                               precision = precision, recall = recall, \
                               F1 = F1, stdev = stdev)
    return render_template('results.html')

def permit(filename):
    return'.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 
    

''' Error Page '''
@app.route('/error', methods = ['GET', 'POST'])
@login_required
def error():
    if request.method == 'POST':
        file = request.files['file']
        if file and permit(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('inputs'))
        return redirect(url_for('error'))
    return render_template('error.html')

def permit(filename):
    return'.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

''' Default Home '''
@app.route('/home')
def home():
    return redirect(url_for('index'))






''' About Page '''
@app.route('/about')
def about():
    return render_template('about.html')








''' Contact Page '''
@app.route('/contact')
def contact():
    return render_template('contact.html')



''' Features CSV '''
@app.route('/features')
@login_required
def features():
    
    os.chdir('C:/Users/manjeet.dev1/Desktop/mapfeat_web_summer-2018/MAPFEAT/MAPFEAT/output')
    file_reader = csv.reader(open('finalizedFeatures.csv', 'rb'), delimiter=',')
    for row in file_reader:
        if row[1] == '':
            continue
        finallist2.append([i.encode('utf8') for i in row])
        if 'Application' in row:
                continue
        finallist.append([i.encode('utf8') for i in row])
        
    print(finallist)
    print(finallist2)


    return render_template('finalizedfeatures.html', finallist = finallist, finallist2 = finallist2)
    

@app.route('/getPlotCSV4')
@login_required
def post4():
   
    si = StringIO.StringIO()
    cw = csv.writer(si)
    cw.writerows(finallist2)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=finalfeatures.csv"
    output.headers["Content-type"] = "text/csv"
    return output




''' features per app '''
@app.route('/ffroma')
@login_required
def ffroma():
    
    print(os.getcwd())
    print(os.listdir(os.curdir))
    dic = {}
    
    ''' dic['app']=['features'] '''
    print(dic)
    
    
    for dirpath, dirnames, filenames in os.walk('C:/Users/manjeet.dev1/Desktop/mapfeat_web_summer-2018/MAPFEAT/MAPFEAT/output/features'):
        print('')
        print('')
        print('current path:', dirpath)
        print('directories:', dirnames)
        print('files:', filenames)
        print('#2')
        for filename in filenames:
            print('')
            print('')
            print(dirpath)
            print('-0----0----0-0-')
            print(dirnames)
            print(filenames)
            print(filename)
            
            '''with open(dirpath + '/' + filename, mode='r') as csv_file:
                csv_reader = csv.reader(csv_file)
                read = []
                print('working?')
                for row in csv_reader:
                    if len(row) !=0 :
                        read = read + [row]
                        
                    'dict key = column 1 and dict value pair = list of column d' 
                    'dic[column a] = [column d]'
            csv_file.close()
            
            df = pd.DataFrame(read)
            print(df)'''
            
            data = pd.read_csv(dirpath + '/' + filename)
            with open(dirpath + '/' + filename, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    column3, column1 = row[2], row[0]
                    str_col1 = ''.join(column1)
                    str_col3 = ''.join(column3)
                    if str_col3 != '[]':
                        str_col3 = str_col3.replace(", []","")
                        str_col3 = str_col3.replace("[[","[")
                        str_col3 = str_col3.replace("]]","]")
                        str_col3 = str_col3.replace("'","")
                        str_col3 = str_col3.replace("[],","")


                        dic[str_col1]=str_col3
            '''i=0
            print('DATA',data)
            Count_Row=data.shape[0]
            while (i < Count_Row):
                print('ROW numbers', Count_Row)
                column3 = data.iloc[i,2]
                print(column3)
                column1 = data.iloc[i,0]
                'print(column1 , column3)'
                print('this is number', i)
                str_col1 = ''.join(column1)
                dic[str_col1]=column3
                i+=1'''
    

    with open(os.path.join(app.config['OUTPUT_FOLDER'], 'Features_from_Apps.csv'), 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Application','Features Extracted'])
        for key, value in dic.items():
            #writer.writerow(['',''])
            writer.writerow([key, value])
    
    '''dataset = tablib.Dataset()
    with open(os.path.join(app.config['OUTPUT_FOLDER'], 'Features_from_Apps.csv')) as f:
        dataset.csv = f.read()
        
    return dataset.html'''
    
    for dirpath, dirnames, filenames in os.walk('C:/Users/manjeet.dev1/Desktop/mapfeat_web_summer-2018/MAPFEAT/MAPFEAT/output'):
        print('')
        print('')
        print('current path:', dirpath)
        print('directories:', dirnames)
        print('files:', filenames)
        print('#3')

    os.chdir('C:/Users/manjeet.dev1/Desktop/mapfeat_web_summer-2018/MAPFEAT/MAPFEAT/output')    
    file_reader = csv.reader(open('Features_from_Apps.csv', 'rb'), delimiter=',')
    for row in file_reader:
        appslist2.append([i.encode('utf8') for i in row])
        if 'Application' in row:
                continue
        appslist.append([i.encode('utf8') for i in row])
        
    print(appslist)


    return render_template('ffroma.html', dic = dic, appslist = appslist, appslist2 = appslist2)



''' features from queeries '''
@app.route('/ffromq')
@login_required
def ffromq():
    dic2 ={}
    '''dic2['search queery']='features' '''
    
    for dirpath, dirnames, filenames in os.walk('C:/Users/manjeet.dev1/Desktop/mapfeat_web_summer-2018/MAPFEAT/MAPFEAT/output/features'):
        print('')
        print('')
        print('current path:', dirpath)
        print('directories:', dirnames)
        print('files:', filenames)
        print('#2')
        for filename in filenames:
            print('')
            print('')
            print(dirpath)
            print('-0----0----0-0-')
            print(dirnames)
            print(filenames)
            print(filename)
    
            data = pd.read_csv(dirpath + '/' + filename)
            with open(dirpath + '/' + filename, 'r') as f:
                reader = csv.reader(f)
                column1 = filename
                str_col1 = ''.join(column1)
                str_col1 = str_col1.replace(".csv","")
                str_col1 = str_col1.replace("+",",")
                bigstr=''
                for row in reader:
                    column3 = row[2]
                    str_col3 = ''.join(column3)
                    bigstr = bigstr + str_col3
                '''if str_col1 in dic2:
                    x=dic2.get(str_col1)
                    bigstr = bigstr + x'''
                    
                '''^ dont need this, same features from both'''
                #bigstr = bigstr.replace(", []","")
                #str_col3 = str_col3.replace("[[","[")
                #str_col3 = str_col3.replace("]]","]")
                #str_col3 = str_col3.replace("'","")
                if bigstr != '[]':
                        #bigstr = bigstr.replace(", []",",")
                    bigstr = bigstr.replace("][","")
                    bigstr = bigstr.replace("[], ","")
                    bigstr = bigstr.replace("[]","")
                    bigstr = bigstr.replace("[[","[")
                    bigstr = bigstr.replace("]]","]")
                    bigstr = bigstr.replace("'","")
                        #bigstr = bigstr.replace("[],","")
                    #bigstr = bigstr.replace("[]","")
                
                    dic2[str_col1]=bigstr
                
                
    
    
    with open(os.path.join(app.config['OUTPUT_FOLDER'], 'Features_from_Queeries.csv'), 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Search Queery','Features'])
        for key, value in dic2.items():
            #writer.writerow(['',''])
            writer.writerow([key, value])
    
    for dirpath, dirnames, filenames in os.walk('C:/Users/manjeet.dev1/Desktop/mapfeat_web_summer-2018/MAPFEAT/MAPFEAT/output'):
        print('')
        print('')
        print('current path:', dirpath)
        print('directories:', dirnames)
        print('files:', filenames)
        print('#3')

    os.chdir('C:/Users/manjeet.dev1/Desktop/mapfeat_web_summer-2018/MAPFEAT/MAPFEAT/output')    
    file_reader = csv.reader(open('Features_from_Queeries.csv', 'rb'), delimiter=',')
    for row in file_reader:
        queerieslist2.append([i.encode('utf8') for i in row])
        if 'Search Queery' in row:
                continue
        queerieslist.append([i.encode('utf8') for i in row])
        
    print(queerieslist)
    
    '''dataset = tablib.Dataset()
    with open(os.path.join(app.config['OUTPUT_FOLDER'], 'Features_from_Queeries.csv')) as f:
        dataset.csv = f.read()
    return dataset.html'''
    
    return render_template('ffromq.html', dic2 = dic2, queerieslist = queerieslist, queerieslist2 = queerieslist2)
    
    

''' forgot password '''
@app.route('/forgotpass', methods = ['GET', 'POST'])
def forgotpass():
    if request.method == 'POST': 
        try:   
            text1 = request.form['usernames']
            text1 = str(text1)      
            parameters_2.keyword1 = text1
            flash('Please Check Your email (this may take a few minutes :)')
            return render_template('forgotpass.html')
        except:
            return render_template('forgotpass.html')
    return render_template('forgotpass.html')



''' create new account '''
@app.route('/newacc')
def newacc():
    return render_template('New_Account.html')


''' About_postlogin Page '''
@app.route('/about_postlogin')
@login_required
def about_postlogin():
    return render_template('about-postlogin.html')

''' Contactp post login Page '''
@app.route('/contact_postlogin')
@login_required
def contact_postlogin():
    
    return render_template('contact_postlogin.html')


@app.route('/getPlotCSV')
@login_required
def post():
   
    si = StringIO.StringIO()
    cw = csv.writer(si)
    cw.writerows(biglist)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=Apps_and_Devs.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@app.route('/getPlotCSV2')
@login_required
def post2():
   
    si = StringIO.StringIO()
    cw = csv.writer(si)
    cw.writerows(queerieslist2)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=features_and_queeries.csv"
    output.headers["Content-type"] = "text/csv"
    return output  
    
@app.route('/getPlotCSV3')
@login_required
def post3():
   
    si = StringIO.StringIO()
    cw = csv.writer(si)
    cw.writerows(appslist2)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=features_and_apps.csv"
    output.headers["Content-type"] = "text/csv"
    return output
    
if __name__ == '__main__':
    app.run(port = 4000)