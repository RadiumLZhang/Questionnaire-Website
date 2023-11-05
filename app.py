from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///responses.db'
db = SQLAlchemy(app)

# Load CSV file
data = pd.read_csv('data/questions.csv', delimiter=';')
question_data_set = []
question_flow = []
MAX_QUESTIONS = 1000

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		session['survey_id'] = request.form['survey_id']  # Store survey_id in session
		return redirect(url_for('question', question_number=1))
	return render_template('survey_id_entry.html')

@app.route('/enter_survey_id', methods=['GET', 'POST'])
def enter_survey_id():
	if request.method == 'POST':
		survey_id = request.form['survey_id']
		session['survey_id'] = survey_id  # Store survey_id in session
		# Check if survey_id already exists
		existing_survey = Survey.query.filter_by(survey_id=survey_id).first()

		if existing_survey:
			# Check if the survey has already been completed
			if existing_survey.completion_timestamp:
				return "Error: This survey has already been completed." #TODO
			# Check if the survey has already been started
			if existing_survey.start_timestamp:
				# Check if the survey has a random question set
				random_question_set = RandomQuestionSet.query.filter_by(survey_id=survey_id).first()
				if random_question_set:
					# Load the random question set
					question_data_set = random_question_set.question_ids.split(',')
				else:
					# Generate the unique question set for this participant
					unique_question_set = []
					for question in question_flow:
						question_data_set.append(question)
				return redirect(url_for('question', question_number=1))
			else:
				# Update the start timestamp
				existing_survey.start_timestamp = datetime.utcnow()
				db.session.commit()


		else:
			# generate the unique question set for this participant
			unique_question_set = []
			for question in question_flow:
				question_data_set.append(question)

		return redirect(url_for('question', question_number=1))
	return render_template('survey_id_entry.html')
@app.route('/question/<question_number>', methods=['GET', 'POST'])
def question(question_number):	
	survey_id = session.get('survey_id')
	if request.method == 'POST':
		action = request.form.get('action')
		answer = request.form.get('answer') or request.form.get('rating')
		if not survey_id:
			# Handle the case where there is no survey_id in the session
			return redirect(url_for('enter_survey_id'))

		# Check if a response already exists
		existing_response = Response.query.filter_by(survey_id=survey_id, question_number=question_number).first()
		if existing_response:
			existing_response.answer = answer  # Update existing answer
		else:
			response = Response(survey_id=survey_id, question_number=question_number, answer=answer)  # New answer
			db.session.add(response)
			
		db.session.commit()

		if action == 'Next':
			next_question_number = question_number + 1
			return redirect(url_for('question', question_number=next_question_number))
		elif action == 'Submit':
			return redirect(url_for('thank_you'))

	else:  # GET request
		existing_responses = Response.query.filter_by(survey_id=survey_id, question_number=question_number)
		existing_response = existing_responses.first() if existing_responses else None
		saved_answer = existing_response.answer if existing_response else ''

	return render_template(f'question_{question_number}.html', question_number=question_number, saved_answer=saved_answer)

@app.route('/generate')
def generate_html():
	# Loop through each question, render HTML, and save to file
	# record the question working flow in question_flow
	for index, row in data.iterrows():
		#any of cell is nan then break
		if row.isnull().values.any():
			continue
		question_number = (index + 1)
		question_type = row['Type']
		context = row['Context']
		question_text = row['Question']
		response_data = row['Response'].split(',')

		# Select template based on question type
		if question_type == 'Multiple Choice':
			template_name = 'pre_generate_templates/multiple_choice_template.html'
			options = response_data
			question_flow.append(question_number)
		elif question_type == 'Short Answer':
			template_name = 'pre_generate_templates/short_answer_template.html'
			char_limit_range = (int(response_data[0]), int(response_data[1]))
			question_flow.append(question_number)
		elif question_type == 'Rating Scale':
			template_name = 'pre_generate_templates/rating_scale_template.html'
			scale_range = (int(response_data[0]), int(response_data[1]))
			question_flow.append(question_number)
		elif question_type == 'Random Question Set':
			generate_sub_html(response_data[0])
			for i in range(int(response_data[1])):
				question_flow.append(response_data[0])
			continue
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


	return "HTML files generated successfully."
def generate_sub_html(question_file):

	if question_file in question_data_set:
		return
	question_data_set.append(question_file)
	base_question_number = (question_data_set.index(question_file) + 1) * MAX_QUESTIONS

	# Load CSV file
	data = pd.read_csv(f'data/{question_file}.csv', delimiter=';')
	# Loop through each question, render HTML, and save to file

	for index, row in data.iterrows():
		if row.isnull().values.any():
			continue
		question_number=base_question_number + index + 1
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


# Create a model for responses
from datetime import datetime

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
	question_ids = db.Column(db.String, nullable=False)  # This can store a comma-separated list of question IDs or be structured differently based on requirements

class Answer(db.Model):
	__tablename__ = 'answer'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	survey_id = db.Column(db.String, db.ForeignKey('survey.survey_id'), nullable=False)
	question_id = db.Column(db.Integer, nullable=False)  # Assuming question IDs are integers. Adjust as needed.
	answer_text = db.Column(db.String, nullable=False)
	answer_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Timestamp when the question was answered

	__table_args__ = (db.UniqueConstraint('survey_id', 'question_id', name='uq_survey_question'),)


TEST_ENVIRONMENT = False

@app.route('/thank_you')
def thank_you():
    return "Thank you for submitting your responses!"
	
if __name__ == '__main__':

    with app.app_context():
        db.create_all()  # Create tables on startup

	if TEST_ENVIRONMENT:
		app.run(debug=True)
    else:
        app.run(host="0.0.0.0", port=5000, debug=True)


