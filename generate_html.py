import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Load CSV file
data = pd.read_csv('data/questions.csv', delimiter=';')

# Set up Jinja2 environment and load template
env = Environment(loader=FileSystemLoader('templates'))

# Loop through each question, render HTML, and save to file
for index, row in data.iterrows():
	question_type = row['Type']
	context = row['Context']
	question_text = row['Question']
	response_data = row['Response'].split(',')
    
	# Select template based on question type
	if question_type == 'Multiple Choice':
	    template = env.get_template('multiple_choice_template.html')
	    options = response_data
	elif question_type == 'Short Answer':
		template = env.get_template('short_answer_template.html')
		char_limit_range = (int(response_data[0]), int(response_data[1]))
	elif question_type == 'Rating Scale':
	    template = env.get_template('rating_scale_template.html')
	    scale_range = (int(response_data[0]), int(response_data[1]))
	# Render HTML
	html_content = template.render(
		context=context,
		question_text=question_text,
		options=options if question_type == 'Multiple Choice' else None,
		char_limit_range=char_limit_range if question_type == 'Short Answer' else None,
		scale_range=scale_range if question_type == 'Rating Scale' else None,
		question_number=index + 1,
		total_questions=len(data),
	)
    
	# Save to file
	with open(f'output/question_{index + 1}.html', 'w') as file:
		file.write(html_content)
		
		
@app.route('/question_<int:question_number>.html')
def question(question_number):
    return render_template(f'question_{question_number}.html', question_number=question_number)
	