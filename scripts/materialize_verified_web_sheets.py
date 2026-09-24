#!/usr/bin/env python3
import argparse, json, os, re, subprocess, urllib.request

def norm(s): return re.sub(r'[^A-Z0-9]+',' ',s.upper()).strip()
def safe(s): return re.sub(r'[^A-Za-z0-9_.-]+','_',s)

def download(url,path):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=90) as r, open(path,'wb') as f: f.write(r.read())

def page_text(pdf,p,tmp):
    out=os.path.join(tmp,f'p{p}.txt')
    subprocess.run(['pdftotext','-f',str(p),'-l',str(p),'-layout',pdf,out],check=False)
    try: return open(out,errors='ignore').read()
    except: return ''

def choose(pages,label,title):
    nl,nt=norm(label),norm(title)
    best=None
    for i,t in enumerate(pages,1):
        n=norm(t)
        if nl not in n: continue
        score=8*n.count(nl)+5*n.count(nt)
        if 'SHEET INDEX' in n or 'INDEX OF DRAWINGS' in n or 'DRAWING INDEX' in n: score-=18
        if nt and nt in n: score+=12
        # actual title blocks commonly repeat sheet number/title
        if n.count(nl)>=2: score+=8
        if n.count(nt)>=2: score+=6
        cand=(score,i)
        if best is None or cand>best: best=cand
    return best[1] if best else None

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('manifest'); ap.add_argument('root'); a=ap.parse_args()
    import tempfile
    data=json.load(open(a.manifest))
    os.makedirs(a.root,exist_ok=True)
    for pr in data:
        d=os.path.join(a.root,pr['id'])
        for x in ['plans','plans/images','elevations-sections','elevations-sections/images','originals']: os.makedirs(os.path.join(d,x),exist_ok=True)
        rec={'project_id':pr['id'],'source_url':pr['url'],'status':'source_download_failed_image_capture_required','selected_sheets':[]}
        with tempfile.TemporaryDirectory() as tmp:
            pdf=os.path.join(tmp,'source.pdf')
            try:
                download(pr['url'],pdf)
                info=subprocess.check_output(['pdfinfo',pdf],text=True,errors='ignore')
                m=re.search(r'^Pages:\s+(\d+)',info,re.M); count=int(m.group(1))
                pages=[page_text(pdf,p,tmp) for p in range(1,count+1)]
                import shutil; shutil.copy2(pdf,os.path.join(d,'originals','source.pdf'))
                for sh in pr['sheets']:
                    p=choose(pages,sh['sheet'],sh['title'])
                    if not p: continue
                    role=sh['role']; base=safe(sh['sheet']+'_'+sh['title'])
                    outpdf=os.path.join(d,role,base+'.pdf')
                    subprocess.run(['pdfseparate','-f',str(p),'-l',str(p),pdf,outpdf],check=True)
                    prefix=os.path.join(d,role,'images',base)
                    subprocess.run(['pdftoppm','-f','1','-singlefile','-png','-r','200',outpdf,prefix],check=True)
                    rec['selected_sheets'].append({'sheet':sh['sheet'],'title':sh['title'],'role':role,'source_page':p,'pdf':os.path.relpath(outpdf,d),'image':os.path.relpath(prefix+'.png',d)})
                rec['status']='materialized_exact_sheet_match' if rec['selected_sheets'] else 'downloaded_no_exact_sheet_match_review_required'
            except Exception as e:
                rec['error']=str(e)[:500]
        json.dump(rec,open(os.path.join(d,'provenance.json'),'w'),indent=2)
        with open(os.path.join(d,'README.txt'),'w') as f:
            f.write(f"Project: {pr['id']}\nSource: {pr['url']}\nStatus: {rec['status']}\n")
            for s in rec['selected_sheets']: f.write(f"{s['role']}: {s['sheet']} {s['title']} source page {s['source_page']}\n")
if __name__=='__main__': main()
