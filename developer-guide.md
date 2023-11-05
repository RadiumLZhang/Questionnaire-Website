[TOC]

# Developer Guide

## I. Structure of Project

The following directory structure provides an overview of the project components:

```
Questionnaire-Website/        # Root directory of project
│
├── LICENSE                    # License information for the project
├── README.md                  # Project description, setup, and usage instructions
├── app.py                     # Main server-side script to run the application
│
├── assets/                    # Static assets directory
│   ├── fonts/                 # Directory storing font assets
│   └── images/                # Directory storing image assets
│
├── data/                      # Directory containing data files
│   ├── questions.csv          # CSV file storing questionnaire questions
│   └── survey.csv             # CSV file related to survey details
│
├── generate_html.py           # Script to generate HTML templates for questions
│
├── instance/                  # Directory for instance-specific configurations
│   └── responses.db           # Database file storing responses to the questionnaire
│
├── output/                    # Temporary storage for generated data
│   ├── question_flow.txt      # File detailing the flow/order of questions
│   └── survey_numbers_map.txt # File mapping survey numbers to their details
│
├── server                     # (Not described, likely server configuration or main server script)
│
├── static/                    # Directory for static files like CSS and JavaScript
│   ├── css/                   # Stylesheets directory
│   │   └── styles.css         # Main stylesheet for the application
│   └── js/                    # JavaScript files directory
│       └── script.js          # Main client-side script
│
├── templates/                 # Directory containing HTML templates
│   ├── pre_generate_templates/ # Templates used before final generation
│   │   ├── multiple_choice_template.html    # Template for multiple-choice questions
│   │   ├── rating_scale_template.html       # Template for rating scale questions
│   │   └── short_answer_template.html       # Template for short answer questions
│   ├── question_1.html        # Specific HTML template for question 1
│   ├── ...                    # HTML templates for various questions
│   └── survey_id_entry.html   # Template for entering survey ID
│
└── tests/                     # Directory containing test scripts and data
```

---

## II. Back-End Setting

### A. Using a Custom Domain without Port Specification

When a URL is entered into a web browser without specifying a port, the browser defaults to:

- **Port 80** for HTTP requests.
- **Port 443** for HTTPS requests.

However, if the Flask app runs on a different port (e.g., port 5000), a reverse proxy can make it accessible through default ports.

#### Setting up Nginx for Reverse Proxy

1. **Edit the Nginx Configuration**

   ```bash
   sudo vim /etc/nginx/sites-available/socwebresearch
   ```

2. **Add the Following Configuration**

   ```plaintext
   server {
       listen 80;
       server_name www.socwebresearch.me;
   
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

3. **Enable the Configuration**

   ```bash
   sudo ln -s /etc/nginx/sites-available/socwebresearch /etc/nginx/sites-enabled/
   ```

4. **Reload Nginx**

   ```bash
   sudo systemctl reload nginx
   ```

### B. Run the Flask App on a VPS

For the Flask application to always remain operational on a Virtual Private Server (VPS), even after system reboots or crashes, additional configurations are required.

1. **Create a Systemd Service File**

   ```bash
   sudo vim /etc/systemd/system/myflaskapp.service
   ```

2. **Enter the Following Content**

   ```plaintext
   [Unit]
   Description=My Flask App
   After=network.target
   
   [Service]
   User=root
   Group=root
   WorkingDirectory=/root/Questionnaire-Website
   Environment="PATH=/root/Questionnaire-Website/venv/bin"
   ExecStart=/root/Questionnaire-Website/venv/bin/gunicorn app:app -b 127.0.0.1:5000
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

3. **Reload Systemd**

   ```bash
   sudo systemctl daemon-reload
   ```

4. **Start the Flask App Service**

   ```bash
   sudo systemctl start myflaskapp
   ```

5. **Enable Service at Boot**

   ```bash
   sudo systemctl enable myflaskapp
   ```

6. **Check Service Status**

   ```bash
   sudo systemctl status myflaskapp
   ```

---

## III. Database Documentation

### A. Overview

The database is designed to store and manage survey responses.

### B. Tables

1. **Survey**: Contains metadata about each survey instance.

   | Column Name          | Data Type | Description                                    |
   | -------------------- | --------- | ---------------------------------------------- |
   | id                   | Integer   | Auto-incremented primary key.                  |
   | survey_id            | String    | Unique identifier for each survey.             |
   | start_timestamp      | DateTime  | Time user first entered the survey.            |
   | completion_timestamp | DateTime  | Time user completed the survey (if completed). |

2. **RandomQuestionSet**: Represents the set of random questions generated for each survey.

   | Column Name  | Data Type | Description                                                  |
   | ------------ | --------- | ------------------------------------------------------------ |
   | id           | Integer   | Auto-incremented primary key.                                |
   | survey_id    | String    | Foreign key referencing `Survey`. Identifies the survey instance. |
   | question_ids | String    | Comma-separated list of question IDs.                        |

3. **Answer**: Contains answers given by users for each survey question.

   | Column Name      | Data Type | Description                                                  |
   | ---------------- | --------- | ------------------------------------------------------------ |
   | id               | Integer   | Auto-incremented primary key.                                |
   | survey_id        | String    | Foreign key referencing `Survey`. Identifies the survey instance. |
   | question_id      | Integer   | ID of the question being answered.                           |
   | answer_text      | String    | User's answer text.                                          |
   | answer_timestamp | DateTime  | Time the user answered the question.                         |

### C. Relationships

- Each `Survey` has one associated `RandomQuestionSet`.
- Each `Survey` has multiple associated `Answer` entries.
- Each `Answer` is linked to one `Survey` via the `survey_id`.

