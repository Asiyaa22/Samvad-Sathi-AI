from dotenv import load_dotenv
import json
import os
from openai import OpenAI
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import HTTPException
import boto3
import PyPDF2
import io
from fastapi.responses import JSONResponse
from botocore.exceptions import BotoCoreError
from typing import Optional
from core.prompts.interview import extract_resume_template, gen_question_template


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))




def call_llm(prompt: str, system:str = None,model: str = "gpt-4o-mini", temperature: float = 0.7) -> str:
    try:
        messages = []
        if system:
            messages = [{"role":"system","content":system}]
        messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error in call_llm func: {e}"
    
class TextRequest(BaseModel):
    text: str
    
class dictRequest(BaseModel):
    profile : dict
    
class intRequest(BaseModel):
    num : int

    
    
def extract_json_dict(text: str):
    try:
        start = min(
            (text.index('{') if '{' in text else float('inf')),
            (text.index('[') if '[' in text else float('inf'))
        )
        end = max(
            (text.rindex('}') + 1 if '}' in text else -1),
            (text.rindex(']') + 1 if ']' in text else -1)
        )
        json_str = text[start:end]
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(text)
        print(json_str)
        raise ValueError(f"Invalid JSON found: {e}")
    
async def process_resume_from_s3_and_generate_questions(
    s3_url: str,
    target_job: str,
    number_of_ques: int,
    job_description: Optional[str] = None
):
    """
    Downloads resume PDF from S3, extracts text, runs LLM to extract data + generate questions.
    """

    try:
        # Step 1: Download PDF file from S3
        s3 = boto3.client('s3')
        
        # Parse bucket name and key from S3 URL
        # Example s3_url: https://your-bucket.s3.amazonaws.com/path/to/resume.pdf
        parsed = s3_url.replace("https://", "").split(".s3.amazonaws.com/")
        bucket = parsed[0]
        key = parsed[1]

        resume_file = io.BytesIO()
        s3.download_fileobj(bucket, key, resume_file)
        resume_file.seek(0)

        # Step 2: Extract text from PDF
        pdf_reader = PyPDF2.PdfReader(resume_file)
        text = "".join(page.extract_text() or "" for page in pdf_reader.pages).strip()

        # Step 3: Extract structured resume data using LLM
        json_str = call_llm(system=extract_resume_template, prompt=text)
        resume_data = extract_json_dict(json_str)

        # Step 4: Generate questions
        job_description_formatted = f"- Job Requirements: {job_description}" if job_description else ''
        prompt = gen_question_template.format(
            n=str(number_of_ques),
            relevent_info=str(resume_data),
            job_highlights=job_description_formatted,
            target_role=target_job
        )
        system = "You generate structured interview questions based on a candidate's profile and job role. Output must follow the given JSON format."
        result = call_llm(system=system, prompt=prompt)
        questions_data = extract_json_dict(result)

        return {
            "resume_data": resume_data,
            "questions": questions_data,
            "metadata": {
                "target_job": target_job,
                "number_of_questions": number_of_ques,
                "has_job_description": job_description is not None
            }
        }

    except BotoCoreError as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file from S3: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

# async def extract_resume_and_gen_questions(
#     file: UploadFile = File(...),
#     target_job: str = Body(...),
#     number_of_ques: int = Body(...),
#     job_description: Optional[str] = Body(default=None)
# ):
#     """
#     Combined endpoint that extracts resume data from PDF and generates interview questions
    
#     Args:
#         file: PDF file containing the resume
#         target_job: Target job role for the candidate
#         number_of_ques: Number of questions to generate
#         job_description: Optional job description/requirements
    
#     Returns:
#         JSON containing both extracted resume data and generated questions
#     """
    
#     # Validate file type
#     if not file.filename.endswith(".pdf"):
#         raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
#     try:
#         # Step 1: Extract resume data from PDF
#         contents = await file.read()
#         pdf_reader = PyPDF2.PdfReader(io.BytesIO(contents))
#         text = ""
        
#         for page in pdf_reader.pages:
#             text += page.extract_text() or ""
        
#         text = text.strip()
        
#         # Extract structured resume data using the agent
#         json_str = call_llm(system=extract_resume_template,prompt=text)
#         resume_data = extract_json_dict(json_str)
        
#         # Step 2: Generate questions based on extracted resume data
#         n = str(number_of_ques)
        
#         if job_description:
#             job_description_formatted = "- Job Requirements: " + job_description
#         else:
#             job_description_formatted = ''
        
#         prompt = gen_question_template.format(
#             n=n,
#             relevent_info=str(resume_data),
#             job_highlights=job_description_formatted,
#             target_role=target_job
#         )
        
#         # Generate questions using the agent
#         system="You generate structured interview questions based on a candidate's profile and job role. Output must follow the given JSON format."
#         result = call_llm(system=system,prompt=prompt)
#         questions_data = extract_json_dict(result)
        
#         # Step 3: Return combined response
#         response = {
#             "resume_data": resume_data,
#             "questions": questions_data,
#             "metadata": {
#                 "target_job": target_job,
#                 "number_of_questions": number_of_ques,
#                 "has_job_description": job_description is not None
#             }
#         }
        
#         return JSONResponse(content=response)
        
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, 
#             detail=f"Failed to process resume and generate questions: {str(e)}"
#         )


