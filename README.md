# Questionnaire-Website

## 1. Structure of the Questionnaire File

The Questionnaire File is a structured document utilized to capture a variety of question types, responses, and accompanying contextual remarks. The document utilizes CSV (Comma-Separated Values) format with a unique delimiter system to effectively distinguish between individual data entries.

### File Format

- **File Extension**: .csv
- **Cell Delimiter**: Semicolon (;)
- **Sub-Cell Delimiter**: Comma (,)

### Table Structure

The questionnaire file comprises four columns:

1. **Type**: The type of question.
2. **Context**: Any contextual remarks or additional information regarding the question.
3. **Question**: The question prompt.
4. **Response**: The response format or options available.

| Column   | Description                                                  |
| -------- | ------------------------------------------------------------ |
| Type     | Specifies the question type e.g., Multiple Choice, Short Answer, Rating Scale. |
| Context  | Provides additional context or remarks about the question.   |
| Question | Contains the question to be answered.                        |
| Response | Defines the response format or lists the response options.   |

### Delimiter Usage

![image-20231024222143031](/Users/radium/Library/Application Support/typora-user-images/image-20231024222143031.png)

- **Primary Delimiter (Cell Delimiter)**: Semicolons (`;`) are utilized to separate each cell within a row. 
- **Secondary Delimiter (Sub-Cell Delimiter)**: Commas (`,`) are utilized to separate sub-elements within a cell, notably within the Response column.
- **Quotation Marks**: If a semicolon or comma is a part of the text within a cell (in Context or Question columns), enclose the entire text within double quotation marks (`" "`). The program will then recognize these characters as text rather than delimiters.

### Example

#### Sample Row

```plaintext
Multiple Choice;These chinese eats Koalas too?? wtf I wish all those eaters are dead!!!!;What is your favorite color?;Red,Green,Blue,Yellow
```

- **Type**: Multiple Choice
- **Context**: These chinese eats Koalas too?? wtf I wish all those eaters are dead!!!!
- **Question**: What is your favorite color?
- **Response**: Red,Green,Blue,Yellow

#### Sample File

![image-20231024222222012](/Users/radium/Library/Application Support/typora-user-images/image-20231024222222012.png)

```plaintext
Type;Context;Question;Response
Multiple Choice;These chinese eats Koalas too?? wtf I wish all those eaters are dead!!!!;What is your favorite color?;Red,Green,Blue,Yellow
Short Answer;If not take down the Chinese Communist Party ,various viruses will follow, because this virus is the CCP biological and chemical weapon, the CCP is poisoning the world, please don't be silent.;Please describe your ideal vacation.;50,max
Rating Scale;Thank you for saving me from those North Koreans man they had me locked up trying to force feed me corona virus.;Rate 1-10 blablah;1,10
```



## 2. Structure of Project

```toml
Questionnaire-Website/        # Root directory of project
|-- .git/                     # Git configuration and source directory
|-- .gitignore                # List of files and directories ignored by Git
|-- app.py                   	# Main server-side script
|-- assets/                   # All assets like images, fonts etc.
|   |-- images/
|   |-- fonts/
|-- css/                      # Stylesheets directory
|   |-- styles.css            # Main stylesheet
|-- js/                       # JavaScript files directory
|   |-- script.js             # Main JavaScript file
|-- data/                     # Data files (e.g., CSV file)
|   |-- questions.csv
|-- templates/                # HTML templates directory
|   |-- index.html            # Main HTML template
|   |-- questionnaire.html    # Questionnaire page template
|-- vendor/                   # Third-party libraries and frameworks
|-- tests/                    # Test scripts and data
|   |-- test_script.js
|-- README.md                 # Project description and instructions
|-- LICENSE                   # License information
```





## User Guide

1. Install Necessary Libraries:
   1. python
   2. pip install pandas jinja2 flask flask_sqlalchemy
2. fill out the questionnaire.cvs and run the code. generate html

```
python3 app.py
```

