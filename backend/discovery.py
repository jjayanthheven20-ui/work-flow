import hashlib,re
from urllib.parse import urljoin
import httpx,yaml
from bs4 import BeautifulSoup

def clean_html(v): return BeautifulSoup(v or '','html.parser').get_text(' ',strip=True)
def make_id(url): return hashlib.sha256(url.encode()).hexdigest()[:20]
def wanted(j,keywords,locations,excludes):
 text=f"{j.get('title','')} {j.get('description','')} {j.get('location','')}".lower()
 if any(x.lower() in text for x in excludes): return False
 return (not keywords or any(k.lower() in text for k in keywords)) and (not locations or any(k.lower() in text for k in locations))
def greenhouse(token):
 r=httpx.get(f'https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true',timeout=25);r.raise_for_status();out=[]
 for j in r.json().get('jobs',[]):
  u=j.get('absolute_url') or '';out.append({'id':make_id(u or str(j.get('id'))),'title':j.get('title',''),'company':token,'location':(j.get('location') or {}).get('name',''),'url':u,'source':'Greenhouse','description':clean_html(j.get('content',''))})
 return out
def lever(company):
 r=httpx.get(f'https://api.lever.co/v0/postings/{company}?mode=json',timeout=25);r.raise_for_status();out=[]
 for j in r.json():
  u=j.get('hostedUrl') or j.get('applyUrl') or '';c=j.get('categories') or {};out.append({'id':make_id(u or str(j.get('id'))),'title':j.get('text',''),'company':company,'location':c.get('location') or '','url':u,'source':'Lever','description':clean_html(j.get('descriptionPlain') or j.get('description') or '')})
 return out
def career_page(url):
 r=httpx.get(url,timeout=25,follow_redirects=True,headers={'User-Agent':'JAY-Job-AI/1.0'});r.raise_for_status();s=BeautifulSoup(r.text,'html.parser');out=[]
 for a in s.select('a[href]'):
  t=a.get_text(' ',strip=True);u=urljoin(url,a.get('href'))
  if t and len(t)>=4 and re.search(r'\b(hr|human resources|recruit|talent|people)\b',t,re.I): out.append({'id':make_id(u),'title':t,'company':url.split('/')[2],'location':'','url':u,'source':'Career page','description':t})
 return out
def discover(config_path='config/sources.yaml'):
 cfg=yaml.safe_load(open(config_path,encoding='utf-8')) or {};s=cfg.get('search',{});jobs=[]
 for t in cfg.get('greenhouse_board_tokens',[]):
  try: jobs.extend(greenhouse(t))
  except Exception: pass
 for c in cfg.get('lever_companies',[]):
  try: jobs.extend(lever(c))
  except Exception: pass
 for u in cfg.get('career_urls',[]):
  try: jobs.extend(career_page(u))
  except Exception: pass
 return list({j['id']:j for j in jobs if wanted(j,s.get('keywords',[]),s.get('locations',[]),s.get('exclude_keywords',[]))}.values())
