# AI Resume Analyzer

An AI-powered resume analyzer that compares a candidate's resume with a job description and evaluates how well the candidate matches the role.

## Features

- Upload a resume in PDF format
- Paste a job description
- Extract structured job requirements using an LLM
- Extract candidate information from the resume
- Identify matching skills
- Identify missing important skills
- Evaluate experience requirements
- Generate an overall match score
- Provide an AI-generated hiring-style verdict
- Interactive web interface built with Streamlit

## Tech Stack

- Python
- Streamlit
- Groq API
- OpenAI GPT-OSS 20B
- Pydantic
- PyMuPDF
- uv

## How It Works

```text
Job Description
       │
       ▼
Jdescription()
       │
       ▼
Structured Job Data
       │
       │
Resume PDF ──► PyMuPDF
                  │
                  ▼
             Resume Text
                  │
                  ▼
             parse_text()
                  │
                  ▼
          Structured Resume
                  │
                  └──────────────┐
                                 ▼
                            finalScore()
                                 │
                                 ▼
                          Match Result
                                 │
                                 ▼
                         Streamlit UI