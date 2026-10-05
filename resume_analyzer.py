from pathlib import Path
import os
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("wrong api key")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-20b"

#Resume/Descirption  
class JobD(BaseModel):
    role: str
    Required_Skills: list[str]
    Programming_langauges : list[str]
    Preferred_Skills : list[str]
    Education : list[str]
    Experience : str
    Responsibilites : list[str]
    
schema = JobD.model_json_schema()

job_description = f"""
    Software Development Engineer

Job Description

We are looking for a Software Development Engineer to join our engineering team and help build reliable, scalable, and high-quality software applications. The ideal candidate is someone who enjoys solving technical problems, learning new technologies, and working collaboratively with other engineers and product teams.

As a Software Development Engineer, you will be involved in the complete software development lifecycle, from understanding requirements and designing solutions to implementation, testing, deployment, and maintenance. You will work on new features as well as improvements to existing applications and services.

Responsibilities

- Design, develop, test, and maintain software applications and services.
- Translate business and technical requirements into well-designed software solutions.
- Write clean, efficient, readable, and maintainable code.
- Participate in the design and architecture of new features and services.
- Develop and maintain RESTful APIs and backend services.
- Work with relational and non-relational databases to store and retrieve application data.
- Write unit tests, integration tests, and automated tests to ensure software quality.
- Debug application issues and troubleshoot problems across development and production environments.
- Participate in code reviews and provide constructive feedback to other developers.
- Collaborate with product managers, designers, QA engineers, and other software engineers.
- Monitor application performance and identify opportunities for optimization.
- Improve the scalability, reliability, security, and performance of existing applications.
- Participate in the complete software development lifecycle, including planning, development, testing, deployment, and maintenance.
- Use version control systems and follow established software development and coding standards.
- Document technical designs, software components, and development processes.
- Stay up to date with current software development practices and technologies.

Required Qualifications

- Bachelor's degree in Computer Science, Computer Engineering, Information Technology, or a related technical field.
- Strong understanding of computer science fundamentals.
- Strong knowledge of data structures and algorithms.
- Good understanding of object-oriented programming and software design principles.
- Proficiency in at least one programming language such as Java, Python, C++, or JavaScript.
- Understanding of relational databases and SQL.
- Familiarity with software development and debugging practices.
- Understanding of basic operating system concepts.
- Knowledge of fundamental computer networking concepts.
- Ability to write readable, maintainable, and well-tested code.
- Strong analytical and problem-solving skills.
- Ability to work effectively in a collaborative team environment.
- Good written and verbal communication skills.

Preferred Qualifications

- Experience developing web applications or backend services.
- Experience building and consuming REST APIs.
- Familiarity with Spring Boot, Django, Flask, Node.js, or similar backend frameworks.
- Experience with React, Angular, or other modern frontend frameworks.
- Familiarity with Git and GitHub or other version control systems.
- Experience with MySQL, PostgreSQL, MongoDB, or other database technologies.
- Familiarity with Linux or Unix-based operating systems.
- Understanding of cloud computing concepts and platforms such as AWS, Microsoft Azure, or Google Cloud.
- Familiarity with Docker and containerization.
- Understanding of CI/CD and automated software deployment.
- Experience with distributed systems or microservices architecture.
- Experience working on academic, personal, open-source, or professional software projects.

Experience

This position is open to candidates with 0–2 years of professional software development experience. Fresh graduates with strong programming fundamentals and relevant academic or personal projects are encouraged to apply.

Education

A bachelor's degree in Computer Science, Computer Engineering, Information Technology, or a related technical discipline is required.

What We Look For

We are looking for engineers who are curious, willing to learn, and comfortable working on unfamiliar technical problems. Candidates should be able to break complex problems into smaller components, understand existing code, identify potential issues, and develop practical solutions.

The successful candidate will demonstrate strong programming fundamentals, attention to detail, good communication skills, and the ability to work effectively with engineers and cross-functional teams.

The role provides opportunities to work on production software, learn modern development technologies, and contribute to projects that have a direct impact on customers and the business.
"""


SYSTEM_PROMPT = f"""
You are a senior-level job description analyzer.

Your task is to analyze the job description provided by the user and
extract the important information into the exact structure defined by
the following JSON schema:

{schema}

Rules:
1. Extract information only from the given job description.
2. Do not invent or assume information that is not present.
3. Put programming languages such as Python, Java, C++, JavaScript, etc.
   in Programming_langauges.
4. Put technical and general skills required for the job in Required_Skills.
5. Put skills that are mentioned as optional, bonus, or preferred in
   Preferred_Skills.
6. Put required educational qualifications in Education.
7. Extract the required years of experience as a number.
   If the job says "0-2 years", use 0 as the minimum required experience.
   If it says "2+ years", use 2.
   If no experience requirement is mentioned, use 0.
8. Extract the actual tasks and duties the employee is expected to perform
   in Responsibilites.
9. If a field has no information, return an empty list [] for list fields.
10. Return ONLY valid JSON matching the provided schema.
11. Do not add explanations, comments, or additional fields.
"""

User_prompt = f"""This is the Job Description : {job_description}"""

sysmsg = {
    "role" : "system",
    "content" : SYSTEM_PROMPT
}
msg = {
    "role" : "user",
    "content" : User_prompt
} 

msgs = [sysmsg,msg]
resp_form = {
    "type" : "json_object"
}
responce = client.chat.completions.create(model=model, messages=msgs, temperature=0,response_format=resp_form)

raw_json = responce.choices[0].message.content

import json
job_data = json.loads(raw_json)
job = JobD(**job_data)

class MatchResult(BaseModel):
    score : float
    details : dict 

class Exp(BaseModel):
    company : str | None = None
    role : str | None = None
    duration : str | None = None
    description : str | None = None
    skills_used : list[str] = []
    
class Resume(BaseModel):
    name : str | None = None
    email : str | None = None
    phone : str | None = None 
    
    Total_exp : str | None = None 
    
    skills : list[str] = []
    experience : list[Exp] = []
    education : list[str] = []
    projects : list[str] = []
    certifications : list[str] = []
    
resume_schema = Resume.model_json_schema()

def parse_text(text):
    system_prompt = f"""
    You are an expert resume parser.

    Extract information from the resume based on its meaning,
    not only based on exact section headings.

    Different resumes may use different headings.

    For example:
    - Experience
    - Professional Experience
    - Work History
    - Employment
    - Internships

    These may all contain relevant experience.

    Skills may also appear in the skills section, work experience,
    internships or projects.

    Return ONLY valid JSON matching this schema:

    {resume_schema}

    Important rules:

    1. Do not invent information.
    2. If a value is not available, return null.
    3. If a list has no information, return an empty list.
    4. Include internships inside experiences.
    5. Extract skills mentioned across the entire resume.
    """
    user_prompt = f"""
    Parse the following resume:

    {text}
    """
    message_system={
        "role" : "system",
        "content" : system_prompt
    }
    message_user={
        "role" : "user",
        "content" : user_prompt
    }
    messages=[message_system, message_user]
    response_format={
        "type": "json_object"
    }
    response=client.chat.completions.create(model=model, messages=messages, response_format=response_format)
    raw_output = response.choices[0].message.content
    data = json.loads(raw_output)
    resume = Resume(**data)
    return resume

def finalScore(job,resume):
    match_schema = MatchResult.model_json_schema()
    prompt = f"""
    You are an HR recruiter.

    Compare the candidate's resume with the job description.

    JOB DESCRIPTION:
    {job.model_dump_json(indent=2)}

    CANDIDATE RESUME:
    {resume.model_dump_json(indent=2)}
    Return JSON matching this schema:

    {match_schema}

    Give me:

    1. Candidate name
    2. Matching skills
    3. Missing important skills
    4. Whether experience requirement is met
    5. Overall match percentage from 0 to 100
    6. A short final verdict

    Keep the response concise and easy to read.
    """
    message={
        "role": "user",
        "content" : prompt
    }
    messages=[message]
    response_format={
        "type": "json_object"
    }
    response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)
    data = json.loads(response.choices[0].message.content)
    return MatchResult(**data)


import pymupdf

doc = pymupdf.open("resume.pdf")
text = ""
for page in doc:
    text += page.get_text()
    
parsed_text = parse_text(text)

result = finalScore(job,parsed_text)
print("Candidate Name : ",parsed_text.name)
print("Final Score : ",result.score)
print("Details : ",result.details)

