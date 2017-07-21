# Validates the finalized features through crowdsourcing
#
# Posts a survey to Mechanical Turk using the Mechanical Turk API. For each feature, the survey
# asks whether it is related to the topic it originated from. The API is polled every 10 seconds
# until enough workers have answered the survey. If enough workers validate a feature, it will
# be written to the results file.
#
# This script requires the user to have an account with Mechanical Turk and an access ID and a
# secret key for authentication. The user can choose whether to post the survey to the testing
# site or the production site.
#
# 	Sample question:
# 	Select all app features related to the topic "help, donate, text"

import csv
import getpass
import sys
import time

from boto.mturk.connection import MTurkConnection, HIT
from boto.mturk.question import QuestionContent, Question, QuestionForm, Overview, \
	AnswerSpecification, SelectionAnswer, FormattedContent


DEBUG_HOST = 'mechanicalturk.sandbox.amazonaws.com'
PROD_HOST = 'mechanicalturk.amazonaws.com'

TITLE = 'Select app features related to a set of words'
DESCRIPTION = ('Select all app features that are related to a certain set of words.')
KEYWORDS = 'apps, app features, words, word association'

INPUT_FILENAME = 'finalizedFeatures.csv'
INPUT_PATH = 'output'
OUTPUT_PATH = 'output'


def createQuestion(topic, features):
	qc = QuestionContent()
	qc.append_field('Title','Select all app features related to the topic "{}"'.format(', '.join(topic)))

	fta = SelectionAnswer(min=0, max=len(features), style='checkbox',
	                      selections=features,
	                      type='text',
	                      other=False)

	q = Question(identifier=1,
	              content=qc,
	              answer_spec=AnswerSpecification(fta),
	              is_required=False)
	return q


def readFeatures():
	questions = []
	with open('{}/{}'.format(INPUT_PATH, INPUT_FILENAME), 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			count = 1
			features = []
			topic = row[0].split('+')
			featureList = row[1].split(', ')

			for feature in featureList:
				if feature:
					features.append([feature, count, 0])
					count += 1

			if features:
				questions.append([topic, features])
	return questions


def createForm(overview, questions):
	q_form = QuestionForm()
	q_form.append(overview)
	for q in questions:
		q_form.append(q)
	return q_form


def createHit(q_form, mtc, pay, numWorkers):
	hit = mtc.create_hit(questions=q_form,
	               max_assignments=numWorkers,
	               title=TITLE,
	               description=DESCRIPTION,
	               keywords=KEYWORDS,
	               duration=60*5,
	               reward=pay)
	return hit


def fetchResults(mtc, questions, numWorkers, votes, hitId):
	# Wait until enough workers have completed the survey
	assignments = mtc.get_assignments(hitId)
	while len(assignments) < int(numWorkers):
		time.sleep(10)
		assignments = mtc.get_assignments(hitId)

	data = []

	# Process each survey result
	for assignment in assignments:
		i = 0
		for answer in assignment.answers[0]:
			question = questions[i]
			i += 1
			if answer:
				for key in answer.fields:
					# Increment the number of votes received
					count = question[1][int(key) - 1][2]
					question[1][int(key) - 1][2] = count + 1

			data.append(question)

		# Approve the survey result
		if assignment.AssignmentStatus != 'Approved':
			mtc.approve_assignment(assignment.AssignmentId)
	mtc.disable_hit(hitId)
	return data


def getUserInput():
	numWorkers = raw_input('\nEnter the number of workers you want to answer each survey: ')
	votes = raw_input('Enter the number of votes each feature needs for it to be validated: ')	
	reward = raw_input('Enter the amount each worker will be paid to complete this survey: ')

	print 'Warning: This will cost up to $%.2f.' % (float(numWorkers) * float(reward))

	prod = raw_input('Would you like to post this survey to production? [y/n]: ')
	HOST = ''
	if prod == 'y':
		print '\nPosting questions to Mechanical Turk...\n'
		HOST = PROD_HOST
	elif prod == 'n':
		print '\nPosting questions to https://workersandbox.mturk.com...\n'
		HOST = DEBUG_HOST
	else:
		sys.exit()
	return reward, HOST, numWorkers, votes


def outputResults(data, numWorkers):
	with open('{}/validatedFeatures.csv'.format(OUTPUT_PATH), 'wb') as w:
		writer = csv.writer(w)
		for i, question, in enumerate(data):
			topic = question[0]
			validated = []
			features = question[1]
			for feature in features:
				# If a feature has been voted on by enough workers, we consider it to be 'validated'
				if feature[2] >= int(numWorkers):
					validated.append(feature[0])
			if validated:
				writer.writerow([('+').join(topic), (', ').join(validated)])
		w.close()


def validate():
	print '\nValidating results on Mechanical Turk...\n'

	ACCESS_ID = getpass.getpass("Enter your access ID: ")
	SECRET_KEY = getpass.getpass("Enter your secret key: ")

	reward, HOST, numWorkers, votes = getUserInput()

	mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)

	overview = Overview()
	overview.append_field('Title', 'Select app features related to a set of words')

	# Get features from file
	questions = readFeatures()

	# Create questions
	mtc_questions = []
	for q in questions:
		mtc_questions.append(createQuestion(q[0], q[1]))

	# Create survey with the questions inside
	q_form = createForm(overview, mtc_questions)

	# Post the survey
	result = createHit(q_form, mtc, reward, numWorkers)
	hitId = result[0].HITId

	# Process the results when they come in
	print '\nFetching results...\n'
	data = fetchResults(mtc, questions, numWorkers, votes, hitId)

	# Write the validated features to file
	outputResults(data, numWorkers)


if __name__ == "__main__":
	validate()
