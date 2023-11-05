# Questionnaire-Website

`Questionnaire-Website` is designed to allow users to define, manage, and deploy questionnaires seamlessly. The platform offers a unique approach by leveraging CSV files to define questionnaires.

## Documentation

### [User Guide](user-guide.md)

The User Guide provides step-by-step instructions and insights into using the platform effectively:

1. **Using the CSV File to Define the Questionnaire**
   - A. File Specifications
   - B. Delimiter Usage
   - C. Question Types
     - i. Multiple Choice
     - ii. Short Answer
     - iii. Rating Scale
     - iv. Random Question Set
   - D. Usage Tips
   - E. Example

2. **Starting a New Project**
   - A. Steps to Reset

3. **Environment Setup Guide**
   - A. Install Required Software and Libraries
     - i. Install Python
     - ii. Set Up Virtual Environment
     - iii. Install Required Python Libraries
   - B. Set Up the Application
     - i. Configure Application Data
     - ii. Run the Application
   - C. Set Up Web Server
     - i. Install Nginx
     - ii. Start and Enable Nginx
     - iii. Install Gunicorn
   - D. DigitalOcean DNS Configuration
     - i. Pointing to DigitalOcean Name Servers
     - ii. Managing DNS Records

### [Developer Guide](developer-guide.md)

For developers looking to contribute or understand the technical intricacies:

1. **Structure of Project**
2. **Back-End Setting**
   - A. Using a Custom Domain without Port Specification
     - Setting up Nginx for Reverse Proxy
   - B. Run the Flask App on a VPS
3. **Database Documentation**
   - A. Overview
   - B. Tables
   - C. Relationships

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/Questionnaire-Website.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Questionnaire-Website
   ```

3. Follow the instructions in the [User Guide](user-guide.md) for setup and usage.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
