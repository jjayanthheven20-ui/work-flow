import json,sqlite3
from pathlib import Path
class Tracker:
 def __init__(self,path='data/jobs.db'):
  Path(path).parent.mkdir(parents=True,exist_ok=True);self.db=sqlite3.connect(path,check_same_thread=False);self.db.execute('''CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY,title TEXT,company TEXT,location TEXT,url TEXT,source TEXT,description TEXT,score INTEGER,decision TEXT,status TEXT DEFAULT 'new',reason TEXT,matched_skills TEXT,created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''');self.db.commit()
 def upsert(self,j): self.db.execute('''INSERT INTO jobs(id,title,company,location,url,source,description) VALUES(?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET title=excluded.title,company=excluded.company,location=excluded.location,url=excluded.url,source=excluded.source,description=excluded.description''',(j['id'],j.get('title',''),j.get('company',''),j.get('location',''),j.get('url',''),j.get('source',''),j.get('description','')));self.db.commit()
 def score(self,i,r): self.db.execute('UPDATE jobs SET score=?,decision=?,status=?,reason=?,matched_skills=? WHERE id=?',(r.get('score'),r.get('decision'),'ready' if (r.get('score') or 0)>=75 else 'review',r.get('reason',''),json.dumps(r.get('matched_skills',[])),i));self.db.commit()
 def all(self):
  c=self.db.execute('SELECT id,title,company,location,url,source,description,score,decision,status,reason,matched_skills FROM jobs ORDER BY COALESCE(score,0) DESC,created_at DESC');n=[x[0] for x in c.description];return [dict(zip(n,r)) for r in c.fetchall()]
