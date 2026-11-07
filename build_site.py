"""Build the separate HTML pages from content.json. See REVIEW.md before publication."""
from html import escape as e
from pathlib import Path
import json,hashlib
BASE=Path(__file__).parent
ROOT=BASE/'public'
D=json.loads((BASE/'content.json').read_text())
NAME=D['name'];TITLE=D['title'];EMAIL=D['email'];LINKEDIN=D['linkedin'];ORIGIN=D['origin'];RESUME=D['resume'];PROJECTS=D['projects']
PAGES=[]
STYLE_VERSION=hashlib.sha256((ROOT/'styles.css').read_bytes()).hexdigest()[:12]
RECORDS=json.loads((BASE/'asset-records.json').read_text()) if (BASE/'asset-records.json').exists() else []

def link(href,label,cls='',external=False,download=False):
 arrow=' <span aria-hidden="true">↗</span>' if external else ''
 attrs=' target="_blank" rel="noopener noreferrer"' if external else ''
 if download:attrs+=' download'
 return f'<a href="{e(href)}" class="{cls}"{attrs}>{e(label)}{arrow}</a>'

def picture(p,index=0,sizes='(max-width: 700px) 100vw, 1120px'):
 if not p['photos'] or p['photos'][index][0] is None:
  label=p['photo_slots'][index] if not p['photos'] else 'Additional project photograph'
  return f'<div class="photo-placeholder" role="img" aria-label="{e(p["name"])}: {e(label.lower())}, approved photograph pending"><span>{e(label)}</span><small>Approved image pending</small></div>'
 stem=f'/assets/projects/{p["slug"]}-{index+1}'
 width=next((r['width'] for r in RECORDS if r.get('slug')==p['slug'] and r.get('index')==index+1),2400)
 cls = ' class="plan"' if 'plan' in p['photos'][index][2].lower() else ''
 return f'<img{cls} src="{stem}-large.webp" srcset="{stem}-small.webp 640w, {stem}-large.webp {width}w" sizes="{sizes}" width="1600" height="1000" alt="{e(p["photos"][index][2])}" loading="lazy" decoding="async">'

def layout(title,desc,active,body,path,ogimage):
 fulltitle=f'{NAME}, {TITLE}' if path=='/' else f'{title} | {NAME}, {TITLE}'
 nav=''.join(f'<a href="{url}" class="'+''+'"'+(' aria-current="page"' if name==active else '')+f'>{name}</a>' for name,url in [('Home','/'),('Projects','/portfolio/'),('Résumé','/resume/'),('Contact','/contact/')])
 return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(fulltitle)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{ORIGIN}{path}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(fulltitle)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{ORIGIN}{path}"><meta property="og:image" content="https://jyotib.com{ogimage}"><meta property="og:image:alt" content="{e(title)} — {NAME}"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#053369">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon.ico" sizes="32x32"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"><link rel="stylesheet" href="/styles.css?v={STYLE_VERSION}"></head>
<body><a class="skip" href="#main">Skip to content</a><header class="site-header wrap"><a class="brand" href="/" aria-label="Jyoti Bhadrashetti home">Jyoti Bhadrashetti</a><nav aria-label="Main navigation">{nav}</nav></header><main id="main">{body}</main>
<footer class="site-footer wrap"><div>{link('mailto:'+EMAIL,'Email')}{link(LINKEDIN,'LinkedIn',external=True)}{link(RESUME,'Résumé (PDF)',download=True) if active != 'Contact' else ''}</div><p>© 2026 Jyoti Bhadrashetti</p></footer></body></html>'''

def write(path,title,desc,active,body,ogimage):
 dest=ROOT/path.strip('/')/'index.html' if path!='/' else ROOT/'index.html'
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(layout(title,desc,active,body,path,ogimage));PAGES.append(path)

intro=''.join(f'<p>{e(p)}</p>' for p in D['intro'])
credentials=''.join(f'<li>{e(item)}</li>' for item in D['home_credentials'])
profile_intro=''.join(f'<p>{e(p)}</p>' for p in D['intro'][1:])
home=f'''<section class="wrap home-split home-sidebar"><div class="home-profile"><div class="profile-top"><div class="profile-details"><h1>{e(D['intro'][0])}</h1><ul class="profile-credentials">{credentials}</ul></div><figure class="portrait"><img src="/assets/jyoti-bhadrashetti.jpeg" width="1066" height="1280" alt="Jyoti Bhadrashetti" fetchpriority="high"></figure></div><div class="intro-copy">{profile_intro}</div><div class="home-resume">{link(RESUME,'Download résumé (PDF)','button',download=True)}</div></div><div class="home-highlights"><section class="home-numbers" aria-label="Selected project facts"><div><h2>178 homes</h2><p>Gridline Apartments<br>$101 million project value</p></div><div><h2>207 affordable homes</h2><p>Altaire at Jackson Park<br>Finished three months early</p></div><div><h2>14+ years</h2><p>Construction and architecture<br>Seattle, Dubai and Mumbai</p></div></section></div></section>'''
write('/','Home','Jyoti Bhadrashetti is a Seattle construction manager at SRM Construction, with multifamily housing work and earlier experience in Dubai and Mumbai.','Home',home,'/assets/share-home.jpg')

def card(p,featured=False):
 tag='h2' if featured else 'h3'
 return f'''<article class="project-card"><a href="/portfolio/{p['slug']}/"><{tag}>{e(p['name'])}</{tag}><p class="project-facts">{e(p['cardfacts'])}</p><div class="card-media">{picture(p,sizes='(max-width: 700px) 100vw, 560px')}</div><p class="card-summary">{e(p['summary'])}</p></a></article>'''

portfolio='<section class="wrap page-heading"><h1 class="location-heading">Seattle, WA</h1><p>Recent multifamily housing in Seattle, followed by selected architecture and interior work.</p></section><div class="wrap"><div class="featured-grid">'+''.join(card(p,True) for p in PROJECTS if p['region']=='Seattle')+'</div><section class="earlier-work"><h2>Dubai</h2><p>Restaurant, healthcare and club interiors in Dubai.</p><div class="earlier-grid">'+''.join(card(p) for p in PROJECTS if p['region']=='Dubai' and p['featured'])+'</div></section><section class="earlier-work"><h2>Mumbai</h2><p>Residential architecture in Mumbai.</p><div class="earlier-grid">'+''.join(card(p) for p in PROJECTS if p['region']=='Mumbai' and p['featured'])+'</div></section></div>'
write('/portfolio/','Projects','Selected projects by Jyoti Bhadrashetti: Gridline Apartments, Altaire at Jackson Park, and earlier interior fit-outs and architecture in Dubai and Mumbai.','Projects',portfolio,'/assets/share-projects.jpg')

for i,p in enumerate(PROJECTS):
 facts=''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k,v in p['facts'])
 gallery=''
 count=len(p['photos']) if p['photos'] else len(p['photo_slots'])
 for j in range(count):
  caption=p['photos'][j][2] if p['photos'] else p['photo_slots'][j]+'. Photograph or plan pending approval.'
  photo_credit=p.get('photo_credits',[])[j] if j<len(p.get('photo_credits',[])) else p.get('photo_credit','Project imagery: '+p['firm']+' · Jyoti Bhadrashetti’s portfolio.')
  credit=f'<span class="image-credit">{e(photo_credit)}</span>' if p['photos'] and p['photos'][j][0] is not None else ''
  gallery+=f'<figure>{picture(p,j)}<figcaption>{e(caption)}{credit}</figcaption></figure>'
 sequence=[item for item in PROJECTS if item['featured']] if p['featured'] else PROJECTS
 position=next(n for n,item in enumerate(sequence) if item['slug']==p['slug'])
 prev=sequence[(position-1)%len(sequence)];nxt=sequence[(position+1)%len(sequence)]
 nav=f'<nav class="project-pagination" aria-label="Project navigation"><a href="/portfolio/{prev["slug"]}/"><span>Previous project</span>{e(prev["name"])}</a><a href="/portfolio/{nxt["slug"]}/"><span>Next project</span>{e(nxt["name"])}</a></nav>'
 story=''.join(f'<section><h2>{heading}</h2><p>{e(p[key])}</p></section>' for heading,key in [('My role','role'),('Scope','scope'),('Result','result')])
 body=f'''<article class="wrap project-page"><a class="back-link" href="/portfolio/">All projects</a><header class="project-heading"><h1>{e(p['name'])}</h1><p>{e(p['summary'])}</p></header><dl class="project-details">{facts}</dl><div class="project-story">{story}</div><section class="project-gallery" aria-label="{e(p['name'])} images">{gallery}</section>{nav}</article>'''
 og=f'/assets/projects/{p["slug"]}-1-large.webp' if p['photos'] else f'/assets/share-{p["slug"]}.jpg'
 write('/portfolio/'+p['slug']+'/',p['name'],p['summary']+' '+p['cardfacts']+'.','Projects',body,og)

rows=''
for date,title,company,location,bullets in D['roles']:
 items=''.join(f'<li>{e(t)}</li>' for t in bullets)
 rows+=f'<article class="resume-role"><p class="role-date">{e(date)}</p><div><h3>{e(title)}</h3><p class="role-company">{e(company)} · {e(location)}</p><ul>{items}</ul></div></article>'
education=''.join(f'<div><h3>{e(degree)}</h3><p>{e(school)}<br>{e(date)}</p></div>' for degree,school,date in D['education'])
quals=''.join(f'<li>{e(t)}</li>' for t in D['qualifications'])
resume=f'''<section class="wrap page-heading resume-heading"><h1 class="visually-hidden">Résumé</h1>{link(RESUME,'Download résumé (PDF)','button',download=True)}<p>Construction management, preconstruction and architectural design across Seattle, Dubai and Mumbai.</p></section><div class="wrap resume"><section><h2>Experience</h2>{rows}</section><section class="resume-education"><h2>Education</h2><div>{education}</div></section><section class="resume-qualifications"><h2>Qualifications</h2><ul>{quals}</ul></section></div>'''
write('/resume/','Résumé','Jyoti Bhadrashetti’s construction management experience at SRM Construction, earlier Dubai and Mumbai roles, education and professional qualifications.','Résumé',resume,'/assets/share-resume.jpg')
contact=f'''<section class="wrap page-heading contact-heading"><h1 class="visually-hidden">Contact</h1></section><div class="wrap contact-page"><ul class="contact-list"><li><span>Email</span>{link('mailto:'+EMAIL,EMAIL)}</li><li><span>LinkedIn</span>{link(LINKEDIN,'linkedin.com/in/jbhadrashetti',external=True)}</li></ul><p class="contact-location">Based in Bothell, Washington. Working in the Seattle area.</p></div>'''
write('/contact/','Contact','Contact Jyoti Bhadrashetti about construction management opportunities and projects in Seattle. Email and LinkedIn.','Contact',contact,'/assets/share-contact.jpg')
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN}{path}</loc></url>' for path in PAGES)+'</urlset>\n')
(ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n')
print(f'Built {len(PAGES)} pages with unique metadata, sitemap and robots.txt.')
