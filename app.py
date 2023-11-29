from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import shlex

from datetime import datetime
from collections import OrderedDict
import random
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///responses.db'
db = SQLAlchemy(app)

# Load CSV file

main_survey_numbers_map = OrderedDict()
main_question_flow = []
check_question_dict = {}
MAX_QUESTIONS = 1000


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template('main.html')
	elif session['survey_id']:
		return redirect(url_for('question', question_number=1))



@app.route('/survey_id_entry')
def survey_id_entry():
	return render_template('survey_id_entry.html')


@app.route('/enter_survey_id', methods=['GET', 'POST'])
def enter_survey_id():
	if request.method == 'POST':
		survey_id = request.form['survey_id']
		session['survey_id'] = survey_id  # Store survey_id in session

		survey = Survey.query.filter_by(survey_id=survey_id).first()
		# [1] if survey is completed, redirect to thank you page
		if survey and survey.completion_timestamp:
			return redirect(url_for('thank_you'))
		# [2] if survey is not completed, redirect to the next question
		elif survey and survey.start_timestamp and not survey.completion_timestamp:
			# find the current question number, by read the answers table and question
			random_question_set = RandomQuestionSet.query.filter_by(survey_id=survey_id).first()
			if random_question_set:
				question_ids = random_question_set.question_ids.split(',')
				session['question_ids'] = question_ids
				answers = Answer.query.filter_by(survey_id=survey_id).all()

				# find the first element in the question_ids which is not in answers
				for question_id in question_ids:
					if int(question_id) not in [answer.question_id for answer in answers]:
						return redirect(url_for('question', question_number=question_id))

				survey.completion_timestamp = datetime.utcnow()
				db.session.commit()
				return redirect(url_for('thank_you'))

		# [3] if survey is not started, record the start-timestamp
		start_timestamp = datetime.utcnow()
		survey = Survey(survey_id=survey_id, start_timestamp=start_timestamp)
		db.session.add(survey)
		db.session.commit()

		# Generate random question set and store in database
		question_ids = generate_question_ids(survey_id, main_survey_numbers_map, main_question_flow, check_question_dict)
		random_question_set = RandomQuestionSet(survey_id=survey_id, question_ids=','.join(map(str, question_ids)))
		db.session.add(random_question_set)
		db.session.commit()
		question_ids = random_question_set.question_ids.split(',')
		session['question_ids'] = question_ids

		# redirect to the first question
		return redirect(url_for('question', question_number=1))


def next_question(current_question_number):
	survey_id = session.get('survey_id')
	question_ids = session.get('question_ids')
	if question_ids:
		# find the in the question_ids, the next question number
		index_of_current_question = question_ids.index(current_question_number)
		if index_of_current_question < len(question_ids) - 1:
			next_question_number = question_ids[index_of_current_question + 1]
			return next_question_number
		else:
			return None
	else:
		# print error message
		print("Error: random_question_set is None")
		return None


def prev_question(current_question_number):
	survey_id = session.get('survey_id')
	question_ids = session.get('question_ids')

	if question_ids:
		# find the in the question_ids, the next question number
		index_of_current_question = question_ids.index(current_question_number)
		if index_of_current_question > 0:
			prev_question_number = question_ids[index_of_current_question - 1]
			return prev_question_number
		else:
			return None
	else:
		# print error message
		print("Error: random_question_set is None")
		return None


@app.route('/question/<question_number>', methods=['GET', 'POST'])
def question(question_number):
	session['current_question_number'] = question_number
	survey_id = session.get('survey_id')
	next_question_number = next_question(question_number)
	prev_question_number = prev_question(question_number)

	if request.method == 'POST':
		if 'answer' in request.form:  # Single answer submission
			answer_text = request.form['answer']
			process_answer(survey_id, question_number, answer_text)

		else:  # Multiple answer submission
			combined_answer = ""
			for key, answer_text in request.form.items():
				if key.startswith('answer_'):
					question_id = key.split('_')[1]  # Extract the question ID from the key
					combined_answer += f"{question_id}:{answer_text}||"  # Format: "question_id:answer||"

			combined_answer = combined_answer[:-2]  # Remove the last "||"
			# Process the combined answer
			process_answer(survey_id, question_number, combined_answer)


		db.session.commit()

		if next_question_number:
			return redirect(url_for('question', question_number=next_question_number))
		else:
			# update the survey completion_timestamp
			survey = Survey.query.filter_by(survey_id=survey_id).first()
			if survey:
				survey.completion_timestamp = datetime.utcnow()
				db.session.commit()
			return redirect(url_for('thank_you'))

	else:  # GET request
		# Retrieve saved answer from database
		answer_record = Answer.query.filter_by(survey_id=survey_id, question_id=question_number).first()
		saved_answer = []
		if answer_record:
			# Assuming 'answer_record.answer_text' contains the answer string
			saved_answer = parse_answer(answer_record.answer_text)

		return render_template(f'question_{question_number}.html', next_question_number=next_question_number,
		                       prev_question_number=prev_question_number, question_number=question_number,
		                       saved_answer=saved_answer)

def parse_answer(answer_text):
	# Check if the answer contains the "||" separator
	if "||" in answer_text:
		# Split the combined answer into segments
		segments = answer_text.split("||")
		parsed_answers = {}
		for segment in segments:
			if segment:  # Check if the segment is not empty
				parts = segment.split(":")
				if len(parts) == 2:
					question_id, answer = parts
					parsed_answers[int(question_id)] = answer
		return parsed_answers
	else:
		# Direct answer without question ID
		return [answer_text]


def process_answer(survey_id, question_id, answer_text):
	existing_answer = Answer.query.filter_by(survey_id=survey_id, question_id=question_id).first()

	if existing_answer:
		if not existing_answer.answer_text == answer_text:
			existing_answer.answer_text = answer_text
			existing_answer.answer_timestamp = datetime.utcnow()
	else:
		answer = Answer(survey_id=survey_id, question_id=question_id, answer_text=answer_text,
		                answer_timestamp=datetime.utcnow())
		db.session.add(answer)

@app.route('/generate')
def generate_html():

	data = pd.read_csv('data/questions.csv', delimiter=';')
	# Loop through each question, render HTML, and save to file
	# record the question working flow in question_flow
	for index, row in data.iterrows():
		# any of cell is nan then break
		if row.isnull().values.any():
			continue
		question_number = (index + 1)
		question_type = row['Type']
		context = row['Context']
		question_text = row['Question']
		response_data = row['Response'].split(',')

		options = None
		char_limit_range = None
		scale_range = None

		# Select template based on question type
		if question_type == 'Multiple Choice':
			template_name = 'pre_generate_templates/multiple_choice_template.html'
			options = response_data
			main_question_flow.append(question_number)
		elif question_type == 'Short Answer':
			template_name = 'pre_generate_templates/short_answer_template.html'
			char_limit_range = (int(response_data[0]), int(response_data[1]))
			main_question_flow.append(question_number)
		elif question_type == 'Rating Scale':
			template_name = 'pre_generate_templates/rating_scale_template.html'
			scale_range = (int(response_data[0]), int(response_data[1]))
			main_question_flow.append(question_number)
		elif question_type == 'Random Question Set':
			generate_random_question_sub_html(response_data[0])
			for i in range(int(response_data[1])):
				main_question_flow.append(response_data[0])
			continue
		elif question_type == 'Multiple Question Set':
			template_name = 'pre_generate_templates/multiple_question_set_template.html'
			questions = generate_multiple_question_set_questions(response_data[0])
			main_question_flow.append(question_number)
		elif question_type == 'Attention Check':
			# for attention check it works like normal question
			# variable response_data[0] is the correct answer
			# then response_data[..] follows with the question type, and the needed data
			sub_question_type = response_data[1]
			correct_answer = response_data[0]
			# trim the leading space and trailing space of response_data[1]
			response_data[1] = response_data[1].strip()
			if response_data[1] == 'Multiple Choice':
				template_name = 'pre_generate_templates/multiple_choice_template.html'
				options = response_data[2:]
			elif response_data[1] == 'Short Answer':
				template_name = 'pre_generate_templates/short_answer_template.html'
				char_limit_range = (int(response_data[2]), int(response_data[3]))
			elif response_data[1] == 'Rating Scale':
				template_name = 'pre_generate_templates/rating_scale_template.html'
				scale_range = (int(response_data[2]), int(response_data[3]))
			main_question_flow.append(question_number)
			check_question_dict[question_number] = correct_answer
		else:
			return "Error: Invalid question type." + str(question_number)

		# Render HTML
		html_content = render_template(
			template_name,
			context=context,
			question_text=question_text,
			options=options,
			char_limit_range=char_limit_range,
			scale_range=scale_range,
			questions=generate_multiple_question_set_questions(response_data[0]) if question_type == 'Multiple Question Set' else None,
			question_number=question_number,
		)

		# Save to file
		with open(f'templates/question_{question_number}.html', 'w') as file:
			file.write(html_content)

	# write the question flow to file
	with open(f'output/question_flow.txt', 'w') as file:
		file.write(str(main_question_flow))

	# write the survey_numbers_map to file
	with open(f'output/survey_numbers_map.txt', 'w') as file:
		file.write(str(main_survey_numbers_map))

	with open(f'output/check_question_dict.txt', 'w') as file:
		file.write(str(check_question_dict))
	return "HTML files generated successfully."


def generate_multiple_question_set_questions(question_file):
	data = pd.read_csv(f'data/{question_file}.csv', delimiter=';')
	questions = []
	for index, row in data.iterrows():
		if row.isnull().values.any():
			continue

		id = index + 1
		question_type = row['Type']
		context = row['Context']
		question_text = row['Question']
		response_data = row['Response'].split(',')
		questions.append({
			'id': id,
			'context': context,
			'question_text': question_text,
			'type': question_type,
			'options': response_data if question_type == 'Multiple Choice' else None,
			'char_limit_range': (int(response_data[0]), int(response_data[1])) if question_type == 'Short Answer' else None,
			'scale_range':  (int(response_data[0]), int(response_data[1])) if question_type == 'Rating Scale' else None,
		})
	return questions
def generate_random_question_sub_html(question_file):
	if question_file in main_survey_numbers_map:
		return
	question_pool = []

	if not question_file in main_survey_numbers_map:
		main_survey_numbers_map[question_file] = question_pool
	index_of_key: int = list(main_survey_numbers_map.keys()).index(question_file)
	base_question_number = (index_of_key + 1) * MAX_QUESTIONS

	# Load CSV file
	data = pd.read_csv(f'data/{question_file}.csv', delimiter=';')
	# Loop through each question, render HTML, and save to file

	for index, row in data.iterrows():
		if row.isnull().values.any():
			continue
		question_number = base_question_number + index + 1
		question_type = row['Type']
		context = row['Context']
		question_text = row['Question']
		response_data = row['Response'].split(',')

		# Select template based on question type
		if question_type == 'Multiple Choice':
			template_name = 'pre_generate_templates/multiple_choice_template.html'
			options = response_data
		elif question_type == 'Short Answer':
			template_name = 'pre_generate_templates/short_answer_template.html'
			char_limit_range = (int(response_data[0]), int(response_data[1]))
		elif question_type == 'Rating Scale':
			template_name = 'pre_generate_templates/rating_scale_template.html'
			scale_range = (int(response_data[0]), int(response_data[1]))
		else:
			return "Error: Invalid question type." + str(question_number)

		# Render HTML
		html_content = render_template(
			template_name,
			context=context,
			question_text=question_text,
			options=options if question_type == 'Multiple Choice' else None,
			char_limit_range=char_limit_range if question_type == 'Short Answer' else None,
			scale_range=scale_range if question_type == 'Rating Scale' else None,
			question_number=question_number,
		)

		# Save to file
		with open(f'templates/question_{question_number}.html', 'w') as file:
			file.write(html_content)

		question_pool.append(question_number)
	main_survey_numbers_map[question_file] = question_pool



def generate_question_ids(survey_id, main_survey_numbers_map, main_question_flow, check_question_dict):
	question_flow = main_question_flow
	survey_numbers_map = main_survey_numbers_map
	# if question_flow is empty list, read the question flow from file
	if not question_flow:
		# read the question flow from file and store in question_flow
		with open(f'output/question_flow.txt', 'r') as file:
			question_flow = eval(file.read())
			main_question_flow = question_flow

	if not survey_numbers_map:
		# read the survey_numbers_map from file and store in survey_numbers_map
		with open(f'output/survey_numbers_map.txt', 'r') as file:
			survey_numbers_map = eval(file.read())
			main_survey_numbers_map = survey_numbers_map

	if not check_question_dict:
		with open(f'output/check_question_dict.txt', 'r') as file:
			check_question_dict = eval(file.read())

	# iterate through question_flow and generate question_ids
	question_ids = []
	for element in question_flow:
		if isinstance(element, int):
			question_ids.append(element)
		elif isinstance(element, str):
			# search the survey_numbers_map
			if element in survey_numbers_map:
				questions_pool = survey_numbers_map.get(element)
				# random pick one number in questions_pool which is not in question_ids
				question_id = random.choice(questions_pool)
				while question_id in question_ids:
					question_id = random.choice(questions_pool)
				question_ids.append(question_id)

	return question_ids


class Survey(db.Model):
	__tablename__ = 'survey'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	survey_id = db.Column(db.String, unique=True, nullable=False)  # A unique identifier for the survey
	start_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # User's first entry time
	completion_timestamp = db.Column(db.DateTime)  # Timestamp when the user completed the survey


class RandomQuestionSet(db.Model):
	__tablename__ = 'random_question_set'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	survey_id = db.Column(db.String, db.ForeignKey('survey.survey_id'), nullable=False)
	question_ids = db.Column(db.String,
	                         nullable=False)  # This can store a comma-separated list of question IDs or be structured differently based on requirements


class Answer(db.Model):
	__tablename__ = 'answer'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	survey_id = db.Column(db.String, db.ForeignKey('survey.survey_id'), nullable=False)
	question_id = db.Column(db.Integer, nullable=False)  # Assuming question IDs are integers. Adjust as needed.
	answer_text = db.Column(db.String, nullable=False)
	answer_timestamp = db.Column(db.DateTime, nullable=False,
	                             default=datetime.utcnow)  # Timestamp when the question was answered

	__table_args__ = (db.UniqueConstraint('survey_id', 'question_id', name='uq_survey_question'),)


@app.route('/thank_you')
def thank_you():
	# check all the questions in the check_question_dict has the correct answer
	survey_id = session.get('survey_id')
	for question_id, correct_answer in check_question_dict.items():
		answer_record = Answer.query.filter_by(survey_id=survey_id, question_id=question_id).first()
		if not answer_record:
			render_template('thank_you.html', prolific_id="C2KTRG8D")
		if answer_record.answer_text.strip() != correct_answer.strip():
			return render_template('thank_you.html', prolific_id="C2KTRG8D")

	return render_template('thank_you.html', prolific_id="CIDZB9W8")

TEST_ENVIRONMENT = False

if __name__ == '__main__':
	with app.app_context():
		db.create_all()  # Create tables on startup
	if TEST_ENVIRONMENT:
		app.run(debug=True)
	else:
		app.run(host="0.0.0.0", port=5000, debug=False)
