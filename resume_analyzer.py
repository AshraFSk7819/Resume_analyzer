from pathlib import Path
import os
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
import json
import time

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
def Jdescription(job_description):
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
    responce = client.chat.completions.create(model=model, messages=msgs, temperature=0,reasoning_effort="low",response_format=resp_form,max_completion_tokens=2048)

    raw_json = responce.choices[0].message.content


    job_data = json.loads(raw_json)
    job = JobD(**job_data)
    return job

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
    response=client.chat.completions.create(model=model, messages=messages,reasoning_effort="low", response_format=response_format,max_completion_tokens=2048)
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
def analyze_resume(resume_path, job_description):
    job = Jdescription(job_description)
    time.sleep(5)  # Add a delay of 5 second to avoid rate limiting
    doc = pymupdf.open(resume_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    parsed_text = parse_text(text)
    time.sleep(5)  # Add a delay of 5 second to avoid rate limiting
    result = finalScore(job,parsed_text)
    # print("Candidate Name : ",parsed_text.name)
    # print("Final Score : ",result.score)
    # print("Details : ",result.details)
    return parsed_text,result

