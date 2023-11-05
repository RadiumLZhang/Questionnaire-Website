[TOC]

# User Guide


## I. Using the CSV File to Define the Questionnaire

### A. File Specifications

- **File Format**: Comma-Separated Values (CSV)
- **File Extension**: `.csv`
- **Cell Delimiter**: Semicolon (`;`)
- **Sub-Cell Delimiter**: Comma (`,`)

### B. Delimiter Usage

- **Primary Delimiter (Cell Delimiter)**: Semicolons separate each cell within a row.
- **Secondary Delimiter (Sub-Cell Delimiter)**: Commas separate sub-elements within a cell, especially in the Response column.
- **Quotation Marks**: Enclose text with semicolons or commas in double quotation marks to ensure the program recognizes these characters as text rather than delimiters.

### C. Question Types

#### i. Multiple Choice

- **Type**: Specify as `Multiple Choice`.
- **Context**: Additional remarks or context about the question.
- **Question**: The actual question to be answered.
- **Response**: List the available response options separated by commas.

#### ii. Short Answer

- **Type**: Specify as `Short Answer`.
- **Context**: Additional remarks or context about the question.
- **Question**: The actual question to be answered.
- **Response**: Define the response format, indicating the minimum and maximum length of the answer (both in terms of character count).

#### iii. Rating Scale

- **Type**: Specify as `Rating Scale`.
- **Context**: Additional remarks or context about the question.
- **Question**: The actual question to be answered.
- **Response**: Define the scale range, indicating the lowest and highest possible ratings.

#### iv. Random Question Set

Introduces variety by drawing questions randomly from pre-defined sets.

- **Type**: Specify as `Random Question Set`.
- **Context**: Instructions or remarks about the section.
- **Question**: Message about the number of questions the user will encounter.
- **Response**: Source file name and number of questions to randomly select, formatted as `[FILE_NAME], number_of_questions`.

**Important Notes for Random Question Set**:

1. **File Name Flexibility**: File names can vary. No duplicates will appear when extracting questions.
2. **Ensure Sufficient Questions**: The chosen file should contain enough questions for extraction. Insufficient questions trigger errors.
3. **File Searching**: The system searches for the specified file within the same directory or path. Ensure source files are in the correct location.

### D. Usage Tips

1. **Avoid Empty Rows**: Ensure there are no blank rows in the CSV. They can disrupt parsing.
2. **Avoid Empty Cells**: Populate every cell. Use "N/A" or a default value if data is missing.
3. **Consistent Columns**: Maintain the four-column structure without arbitrary modifications.
4. **Special Characters**: Enclose text with semicolons or commas in double quotation marks.

### E. Example

Here's a sample representation of the CSV file:

```plaintext
Type;Context;Question;Response
Multiple Choice;"Choosing favorite colors";"What is your favorite color?";Red,Green,Blue,Yellow
Short Answer;"Vacation preferences";"Describe your ideal vacation.";"50,250"
Rating Scale;"Feedback on our service";"Rate your experience from 1-10";1,10
Random Question Set;"Randomized question section";"In this section, you will encounter a random set of questions.";"[FILE_NAME], 5"
```

---

## II. Starting a New Project

To initiate a new project, it's crucial to remove the previous database and question files. This action ensures a fresh start and eliminates potential conflicts with older data.

### A. Steps to Reset

1. Run the cleanup script:

   ```bash
   bash cleanup.sh
   ```

   This script eradicates any lingering database and question files from your project.

2. Once the cleanup is successful, launch your application.

3. To create new HTML files for your survey, visit the `/generate` route of your app:

   ```
   [domain]/generate
   ```

   This step establishes a new survey environment for your endeavor.

**Note**: Substitute `[domain]` with the genuine domain or IP address where your application resides.

---



## III. Environment Setup Guide

### A. Install Required Software and Libraries

#### i. Install Python

For Debian/Ubuntu systems, you can install Python using the following commands:

```bash
sudo apt update
sudo apt install python3-full
```

#### ii. Set Up Virtual Environment

It's a good practice to use a virtual environment for your Python projects. Here's how to set it up:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### iii. Install Required Python Libraries

After activating your virtual environment, install the necessary Python libraries:

```bash
pip install Flask Flask-SQLAlchemy pandas jinja2
```

### B. Set Up the Application

#### i. Configure Application Data

Fill out the `questionnaire.csv` file with the required data.

#### ii. Run the Application

Execute the application using the command:

```bash
python3

 app.py
```

### C. Set Up Web Server

#### i. Install Nginx

Nginx will act as a reverse proxy for your application.

```bash
sudo apt update
sudo apt install nginx
```

#### ii. Start and Enable Nginx

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

#### iii. Install Gunicorn

Gunicorn will serve as the application server.

```bash
pip install gunicorn
```

### D. DigitalOcean DNS Configuration

#### i. Pointing to DigitalOcean Name Servers

For detailed steps on how to point to DigitalOcean name servers from various domain registrars, refer to:

[DigitalOcean Name Servers Configuration Guide](https://docs.digitalocean.com/products/networking/dns/getting-started/dns-registrars/)

#### ii. Managing DNS Records

For information on how to create, edit, and delete DNS records on DigitalOcean, check out:

[DigitalOcean DNS Records Management Guide](https://docs.digitalocean.com/products/networking/dns/how-to/manage-records/)

