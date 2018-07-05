''' Server-end code for MAPFEAT web tool
Python files written by Rachel Quapp '''

''' Import MAPFEAT Python files ''' 
import classifyTweets
import extractFeatures
import finalizeFeatures
import processTweets
import searchAppStore
import topicModeling

''' Import Flask Backend '''
from flask import *
from werkzeug.utils import secure_filename # blocks malicious files disguised as csv
import os, csv
import random
import shutil
import requests
import tablib

from flask import Flask, render_template, request
from wtforms import Field, TextField, widgets, SelectMultipleField, Form
from wtforms.widgets import TextInput, html_params





''' Instantiation of Flask class and environment variables '''
app = Flask(__name__)
app.config.from_object(__name__)

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/data/'
OUTPUT_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/output/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
ALLOWED_EXTENSIONS = set(['csv'])

'''---------------------------------------------------------------'''






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







'''---------------------------------------------------------------'''
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

''' Start Page '''
@app.route('/', methods = ['GET', 'POST'])
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

'''-----------------------------------------------------------'''





''' new page search '''
@app.route('/screen1', methods = ['GET', 'POST'])
def screen1():
    formData = request.values if request.method == "GET" else request.values
    if request.method == 'POST':
        
  
        text1 = request.form['t_1']
        text2 = request.form['t_2']
        text3 = request.form['t_3']
        text4 = request.form['t_4']
        print([text1, text2, text3, text4])
        try:
            print('1')
            text1, text2, text3, text4 = str(text1), str(text2), str(text3), str(text4)
            print('2')
            parameters_2.keyword1 = text1
            parameters_2.keyword2 = text2
            parameters_2.keyword3 = text3
            parameters_2.keyword4 = text4
            print(text1, text2, text3, text4)
            print('')
            print('')
            print('')
            print('Form Data')
            print(formData)
            print('')
            print('')
            print('')
            print('')
            response = "Form Contents <pre>%s</pre>" % "<br/>\n".join(["%s:%s" % item for item in formData.items(multi=True)] )
            print(formData)
            print(response)
            checks = ''
            if 'apple' in response:
                checks += '1'
            if 'google' in response:
                checks += '2'
            print('')
            print(checks)
            data = [checks, text1, text2, text3, text4]
            
            '''with open('Inputcsv.csv', 'wb') as fin:
                writer = csv.writer(fin)
                for row in data:
                    writer.writerow(row)
            '''
           
            
            
            
            """form = SimpleForm()
            print('next s')
            print(form)
            if form.validate_on_submit():
                print('444444444444')
                print form.example.data
                print('55555555555')
            else:
                print('3333333333')
                print form.errors"""


            return redirect(url_for('loading')) 
        except Exception as e:
            print(e)
            return render_template('about.html')
    return render_template('screen1.html')


'''-----------------------------------------------------------'''

'''intermidiate page'''
@app.route('/loading', methods = ['GET', 'POST'])
def loading():
    if request.method == 'GET':
        '''Callfunction(data)
        apps = []
        devs = []
        with open('Outputcsv.csv', 'r') as fout:
            reader = csv.reader(fout)
            for row in csvreader:
                apps.append((row[0], row[1]))
                #devs.append(row[1])
            
            '''
        return render_template('results_screen1.html')
        '''return redirect(url_for('results_screen1'))'''
    return render_template('loading.html')

'''-------------------------------------------------------------'''

''' Results for screen 1 Page '''
@app.route('/results_screen1', methods = ['GET', 'POST'])
def results_screen1():
    if request.method == 'GET':
        for app, dev in apps:
            print (app, dev)
    
    return render_template('results_screen1.htm')










'''-------------------------------------------------------------'''

''' Results Page '''
@app.route('/results', methods = ['GET', 'POST'])
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
def features():
    dataset = tablib.Dataset()
    with open(os.path.join(app.config['OUTPUT_FOLDER'], 'finalizedFeatures.csv')) as f:
        dataset.csv = f.read()
    return dataset.html

if __name__ == '__main__':
    app.run(port = 4000)