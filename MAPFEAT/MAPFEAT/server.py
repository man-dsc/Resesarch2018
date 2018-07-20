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

from globa import *
from functools import wraps
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///userpass.db', echo=True)

reload(sys)  
sys.setdefaultencoding('utf8')



''' Instantiation of Flask class and environment variables '''
app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = '\xf9o\n\xfbP\xd4\xb7\xa6$\x1e\xb9\x8c\xb6\x06$\xce\xca\xeb\x14\x1cwo\xce\xec'

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/data/'
OUTPUT_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/output/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
ALLOWED_EXTENSIONS = set(['csv'])








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
    error = None
    if request.method == 'POST':
        
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
 
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
        result = query.first()
        if result:
            session['logged_in'] = True
            flash('successful login')
            return redirect(url_for('post_home'))
        else:
            error = 'Invalid Credentials. Please try again.\n\n Contact Suport -> Suport@MAPFEAT.COM'
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
                checks += '1'
            if 'google' in response:
                checks += '2'
            
            data = [checks, text1, text2, text3, text4]
           
            
            with open("querys.csv", "wb") as fin:
                writer = csv.writer(fin)
                for row in data:
                    writer.writerow([row])
                    
            
            
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
        data.append([app, dev])
        big_dict = {}
        small_dict = {}
        for i in range(len(app)):
            big_dict[app[i]]= dev[i]
        for i in range(len(app)):
            small_dict[dev[i]]= app[i]
        length_dict=len(big_dict)
 
     
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
    dataset = tablib.Dataset()
    with open(os.path.join(app.config['OUTPUT_FOLDER'], 'finalizedFeatures.csv')) as f:
        dataset.csv = f.read()
    return dataset.html

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
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output
    
    
    
if __name__ == '__main__':
    app.run(port = 4000)