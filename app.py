from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///responses.db'
db = SQLAlchemy(app)

# Load CSV file
data = pd.read_csv('data/questions.csv', delimiter=';')



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
		return redirect(url_for('question', question_number=1))
	return render_template('survey_id_entry.html')
	
@app.route('/question_<int:question_number>', methods=['GET', 'POST'])
def question(question_number):	
	if request.method == 'POST':
		action = request.form.get('action')
		answer = request.form.get('answer') or request.form.get('rating')
		survey_id = session.get('survey_id')
		if not survey_id:
			# Handle the case where there is no survey_id in the session
			return redirect(url_for('enter_survey_id'))

		# Check if a response already exists
		existing_response = Response.query.filter_by(id=survey_id, question_number=question_number).first()
		if existing_response:
			existing_response.answer = answer  # Update existing answer
		else:
			response = Response(id=survey_id, question_number=question_number, answer=answer)  # New answer
			db.session.add(response)

		db.session.commit()

		if action == 'Next':
			next_question_number = question_number + 1
			return redirect(url_for('question', question_number=next_question_number))
		elif action == 'Submit':
			return redirect(url_for('thank_you'))

	else:  # GET request
		existing_response = Response.query.filter_by(id=session.get('survey_id'), question_number=question_number).first()
		saved_answer = existing_response.answer if existing_response else ''

	return render_template(f'question_{question_number}.html', question_number=question_number, saved_answer=saved_answer)

	
		
@app.route('/generate')
def generate_html():
    # Loop through each question, render HTML, and save to file
    for index, row in data.iterrows():
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

        # Render HTML
        html_content = render_template(
            template_name,
            context=context,
            question_text=question_text,
            options=options if question_type == 'Multiple Choice' else None,
            char_limit_range=char_limit_range if question_type == 'Short Answer' else None,
            scale_range=scale_range if question_type == 'Rating Scale' else None,
            question_number=index + 1,
            total_questions=len(data),
        )

        # Save to file
        with open(f'templates/question_{index + 1}.html', 'w') as file:
            file.write(html_content)

    return "HTML files generated successfully."

# Response

# Create a model for responses
class Response(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	question_number = db.Column(db.Integer, nullable=False)
	answer = db.Column(db.String, nullable=False)
	
		
@app.route('/thank_you')
def thank_you():
    return "Thank you for submitting your responses!"
	
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables on startup
    app.run(debug=True)
