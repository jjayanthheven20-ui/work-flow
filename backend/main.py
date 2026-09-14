import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .agent import application_pack, interview_pack, score_job
from .discovery import discover
from .resume_parser import parse_resume
from .tracker import Tracker
load_dotenv()
app=FastAPI(title='JAY Job AI',version='1.0')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_methods=['*'],allow_headers=['*'])
tracker=Tracker(os.getenv('DATABASE_PATH','data/jobs.db'));resume_text='';resume_filename=''
class Job(BaseModel):
 id:str='';title:str;company:str;location:str='';url:str='';source:str='';description:str=''
@app.get('/health')
def health(): return {'ok':True,'agent':'JAY Job AI','resume_loaded':bool(resume_text),'jobs_tracked':len(tracker.all())}
@app.post('/resume/upload')
async def upload_resume(file:UploadFile=File(...)):
 global resume_text,resume_filename
 data=await file.read()
 try: resume_text=parse_resume(file.filename or 'resume',data)
 except Exception as e: raise HTTPException(400,str(e)) from e
 Path('data').mkdir(exist_ok=True);Path('data/resume.original').write_bytes(data);Path('data/resume.txt').write_text(resume_text,encoding='utf-8');resume_filename=file.filename or 'resume'
 return {'ok':True,'filename':resume_filename,'characters':len(resume_text),'preview':resume_text[:1000]}
@app.get('/resume')
def get_resume(): return {'loaded':bool(resume_text),'filename':resume_filename,'characters':len(resume_text)}
@app.post('/discover')
def discover_jobs():
 jobs=discover()
 for job in jobs: tracker.upsert(job)
 return {'count':len(jobs),'jobs':jobs}
@app.get('/jobs')
def get_jobs(): return tracker.all()
@app.post('/jobs/score')
def score(job:Job):
 if not resume_text: raise HTTPException(400,'Upload a resume first.')
 result=score_job(resume_text,job.model_dump())
 if job.id: tracker.score(job.id,result)
 return result
@app.post('/applications/draft')
def draft(job:Job):
 if not resume_text: raise HTTPException(400,'Upload a resume first.')
 return application_pack(resume_text,job.model_dump())
@app.post('/interview')
def interview(job:Job):
 if not resume_text: raise HTTPException(400,'Upload a resume first.')
 return interview_pack(resume_text,job.model_dump())
