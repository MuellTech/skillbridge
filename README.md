# SkillBridge - Career Transition Analysis Platform  

SkillBridge is a web application designed to empower individuals navigating career transitions by analyzing their resumes and identifying transferable skills. Whether you're a college student considering a major change or a professional exploring new fields, SkillBridge provides personalized insights to help you make informed decisions.  

## Motivation  

Many college students and early-career professionals struggle with career transitions, especially after realizing that their chosen field may not align with their passions or goals. Often, they face uncertainty about how their current skills apply to new domains. SkillBridge was created to alleviate this frustration by offering a structured approach to identifying transferable skills and recommending actionable steps for skill development.  

By leveraging AI, SkillBridge enables users to uncover opportunities they might not have considered and helps them build a clear roadmap for success in their new field.  

## Features  

- **Resume Analysis**: Upload resumes in PDF, DOC, or DOCX formats for in-depth analysis.  
- **AI-Powered Recommendations**: Receive personalized insights about transferable skills and potential career paths using OpenAI's GPT API.  
- **Career Transition Guidance**: Get tailored suggestions for learning new skills and adapting to new roles.  
- **User Dashboard**: Manage and track your career transition journey, including insights from multiple analyses.  
- **Analysis History**: Access previous resume analyses to monitor progress and refine strategies.  
- **PDF Reports**: Generate detailed, downloadable reports with actionable recommendations.  
- **Analytics Dashboard**: Visualize skill patterns and career transition trends using interactive charts.  

## Tech Stack  

- **Backend**: Django 5.1.4 for robust and scalable web development.  
- **Frontend**: HTML, Tailwind CSS, and JavaScript for a responsive and user-friendly interface.  
- **Database**: SQLite3 for efficient data storage and management.  
- **Authentication**: JWT (JSON Web Tokens) for secure user login and session handling.  
- **AI Integration**: OpenAI GPT-3.5 API for advanced resume analysis and personalized recommendations.  
- **File Handling**: Built-in support for PDF and DOC processing with robust file validation.  

## Installation  

1. **Clone the Repository**:  
   ```bash  
   git clone https://github.com/your-username/skillbridge.git  
   cd skillbridge
   
## Set Up Virtual Environment  
python -m venv venv  
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate  

## Install dependencies
pip install -r requirements.txt  

## Set Up Environment Variables
SECRET_KEY=your_django_secret_key  
OPENAI_API_KEY=your_openai_api_key  

## Run Migrations
python manage.py migrate  

## Start Development Server
python manage.py runserver  

## How It Works  

1. **Upload Your Resume**  
   Upload your resume in a supported format (PDF, DOC, or DOCX) through the intuitive user interface.  

2. **AI-Powered Analysis**  
   SkillBridge uses OpenAI's GPT API to analyze your resume, extracting valuable insights into your transferable skills and aligning them with potential career paths.  

3. **Personalized Recommendations**  
   Access detailed career transition recommendations directly in your user dashboard. These insights include actionable steps for skill development tailored to your unique background.  

4. **Downloadable Reports**  
   Generate and download comprehensive PDF reports with a breakdown of your skills and suggested learning paths for future reference.  

5. **Analytics Dashboard**  
   Explore trends and skill frequency patterns through the analytics dashboard, helping you better understand the opportunities available in your target field.  

## Roadmap  

Planned future updates to enhance SkillBridge include:  

1. **LinkedIn Integration**  
   Enable seamless analysis of LinkedIn profiles to provide tailored career insights without requiring a resume upload.  

2. **Advanced Analytics**  
   Develop enhanced analytics features to track industry-specific trends, providing users with a more comprehensive understanding of evolving career opportunities.  

3. **Expanded File Format Support**  
   Add support for additional file formats and implement multilingual resume processing to accommodate a broader user base.  

## Contributions
I welcome contributions! Please feel free to fork the repository, create a feature branch, and submit a pull request.
