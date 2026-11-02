"""Generate a clean, phone-free PDF from the same role bullets as the website."""
from pathlib import Path
from html import escape
import json
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,KeepTogether,PageBreak
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("ResumeSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("ResumeBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("ResumeSerif", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))
BASE=Path(__file__).resolve().parents[1]
d=json.loads((BASE/'content.json').read_text())
OUT=BASE/'public/assets/jyoti-bhadrashetti-resume.pdf'
navy=colors.HexColor('#053369');ink=colors.HexColor('#202320');muted=colors.HexColor('#62685f')
styles={
 'name':ParagraphStyle('name',fontName='ResumeSerif',fontSize=30,leading=34,textColor=ink,spaceAfter=8),
 'title':ParagraphStyle('title',fontName='ResumeSans',fontSize=12,leading=17,textColor=navy,spaceAfter=12),
 'contact':ParagraphStyle('contact',fontName='ResumeSans',fontSize=9,leading=14,textColor=ink,spaceAfter=22),
 'section':ParagraphStyle('section',fontName='ResumeSerif',fontSize=18,leading=23,textColor=navy,spaceBefore=10,spaceAfter=10),
 'role':ParagraphStyle('role',fontName='ResumeBold',fontSize=11,leading=16,textColor=ink,spaceAfter=4),
 'meta':ParagraphStyle('meta',fontName='ResumeSans',fontSize=9,leading=14,textColor=muted,spaceAfter=9),
 'body':ParagraphStyle('body',fontName='ResumeSans',fontSize=9.5,leading=14,textColor=ink,spaceAfter=9),
 'bullet':ParagraphStyle('bullet',fontName='ResumeSans',fontSize=9.5,leading=14,leftIndent=12,firstLineIndent=-10,textColor=ink,spaceAfter=6),
}
def clean(s):return escape(s.replace('–','-').replace('—','-').replace('’',"'")).replace('&amp;','&amp;')
def para(t,s='body'):return Paragraph(clean(t),styles[s])
class ResumeCanvas(canvas.Canvas):
 def __init__(self,*a,**kw):super().__init__(*a,**kw);self.setTitle('Jyoti Bhadrashetti | Construction Manager');self.setAuthor('Jyoti Bhadrashetti');self.setSubject('Professional resume: construction management, preconstruction and architectural design');self.setKeywords('Jyoti Bhadrashetti, Construction Manager, Seattle, LEED AP BD+C')
def footer(c,doc):
 c.saveState();c.setStrokeColor(colors.HexColor('#d9dcd4'));c.line(48,44,564,44);c.setFont('ResumeSans',8);c.setFillColor(muted);c.drawString(48,30,'jyotib.com');c.drawRightString(564,30,str(doc.page));c.restoreState()
story=[para(d['name'],'name'),para('Construction Manager | Seattle, Washington','title')]
contact=f'<link href="mailto:{d["email"]}" color="#053369">{d["email"]}</link>  |  <link href="{d["linkedin"]}" color="#053369">linkedin.com/in/jbhadrashetti</link>  |  <link href="https://www.jyotib.com" color="#053369">jyotib.com</link>'
story.append(Paragraph(contact,styles['contact']))
story.append(para('Construction management, preconstruction and architectural design across Seattle, Dubai and Mumbai. Experience with GMP budgets, subcontractor buyout, contracts, cost forecasts and owner reporting.'))
story.append(para('Experience','section'))
for i,(date,title,company,location,bullets) in enumerate(d['roles']):
 if i==3:story += [PageBreak(),para('Earlier experience','section')]
 block=[para(title,'role'),para(f'{company} | {location} | {date}','meta')]
 block += [Paragraph('- '+clean(b),styles['bullet']) for b in bullets]
 block.append(Spacer(1,7));story.append(KeepTogether(block))
story.append(para('Education','section'))
for degree,school,date in d['education']:
 story += [para(degree,'role'),para(f'{school} | {date}','meta')]
story.append(para('Qualifications','section'))
for q in d['qualifications']:story.append(para(q,'body'))
SimpleDocTemplate(str(OUT),pagesize=(612,792),leftMargin=48,rightMargin=48,topMargin=44,bottomMargin=60,subject='Professional resume: construction management, preconstruction and architectural design',title='Jyoti Bhadrashetti | Construction Manager',author='Jyoti Bhadrashetti').build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=ResumeCanvas)
print(OUT)
