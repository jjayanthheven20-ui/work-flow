import json,os
from openai import OpenAI
def _json(prompt):
 c=OpenAI(api_key=os.environ['OPENAI_API_KEY']);r=c.responses.create(model=os.getenv('OPENAI_MODEL','gpt-5'),input=prompt);return json.loads(r.output_text.strip())
def score_job(resume,job):
 return _json(f'''You are a strict job-fit scoring engine. Return JSON only with score, decision, matched_skills, missing_skills, evidence, risks, reason. decision must be APPLY, REVIEW or SKIP. Use only facts present in the resume and job. Never invent qualifications. Score skills 30%, experience 20%, title 15%, location/work-mode 15%, education 10%, preferences 10%.\nRESUME:\n{resume}\nJOB:\n{json.dumps(job,ensure_ascii=False)}''')
def application_pack(resume,job):
 return _json(f'''Create a truthful application preparation pack. JSON only: headline, cover_letter, summary, known_answers, unknown_questions. Never fabricate qualifications or answer unknown sensitive questions.\nRESUME:\n{resume}\nJOB:\n{json.dumps(job,ensure_ascii=False)}''')
def interview_pack(resume,job):
 return _json(f'''Create interview preparation JSON only: tell_me_about_yourself, why_this_role, likely_questions, star_stories, company_research_points, questions_to_ask. Candidate-specific claims must be grounded in the resume.\nRESUME:\n{resume}\nJOB:\n{json.dumps(job,ensure_ascii=False)}''')
