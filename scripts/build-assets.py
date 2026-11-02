from pathlib import Path
from io import BytesIO
import json,argparse
import fitz
from PIL import Image,ImageDraw,ImageFont,ImageOps
BASE=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('portfolio',type=Path);args=parser.parse_args()
doc=fitz.open(args.portfolio);data=json.loads((BASE/'content.json').read_text());dest=BASE/'public/assets/projects';dest.mkdir(exist_ok=True)
records=[]
for p in data['projects']:
 for i,(xref,page,caption) in enumerate(p['photos'],1):
  if xref is None:continue
  im=Image.open(BytesIO(doc.extract_image(xref)['image'])).convert('RGB');im.thumbnail((2400,2400),Image.Resampling.LANCZOS)
  for label,maxwidth in [('large',2400),('small',640)]:
   variant=im.copy()
   if variant.width>maxwidth:variant.resize((maxwidth,round(variant.height*maxwidth/variant.width)),Image.Resampling.LANCZOS).save(dest/f'{p["slug"]}-{i}-{label}.webp','WEBP',quality=82,method=6)
   else:variant.save(dest/f'{p["slug"]}-{i}-{label}.webp','WEBP',quality=82,method=6)
   path=dest/f'{p["slug"]}-{i}-{label}.webp';q=78
   while path.stat().st_size>300000 and q>35:
    variant.thumbnail((maxwidth,2400),Image.Resampling.LANCZOS);variant.save(path,'WEBP',quality=q,method=6);q-=5
  records.append(dict(slug=p['slug'],index=i,width=im.width,height=im.height,file=f'/assets/projects/{p["slug"]}-{i}-large.webp',source_url='https://drive.google.com/file/d/1PMNVKv-gKaBzzzbplonBovruHO9isucU/view',source_page=page,pdf_image_xref=xref,caption=caption,credit=p['firm'],photographer='Not identified in supplied portfolio',permission='User-supplied portfolio; third-party photographer credit/permission to be confirmed before publication'))
# Unique social previews for non-photo pages and the two approval-pending Seattle projects.
font=str(BASE/'resources/fonts/DejaVuSans.ttf')
serif=str(BASE/'resources/fonts/DejaVuSerif.ttf')
shares={'home':('Jyoti Bhadrashetti','Construction Manager · Seattle'),'projects':('Projects','Seattle · Dubai · Mumbai'),'resume':('Résumé','Experience and qualifications'),'contact':('Contact','jbhadrashetti@gmail.com'),'gridline':('Gridline Apartments','178 homes · Capitol Hill, Seattle'),'altaire-jackson':('Altaire at Jackson Park','207 affordable homes · North Seattle')}
for slug,(title,sub) in shares.items():
 im=Image.new('RGB',(1200,630),'#f8f7f3');draw=ImageDraw.Draw(im);draw.line((72,72,1128,72),fill='#053369',width=3)
 f=ImageFont.truetype(serif,60);words=title.split();lines=['']
 for word in words:
  attempt=(lines[-1]+' '+word).strip()
  if draw.textlength(attempt,font=f)>1056:lines.append(word)
  else:lines[-1]=attempt
 for n,line in enumerate(lines):draw.text((72,180+n*80),line,fill='#202320',font=f)
 draw.text((72,410),sub,fill='#053369',font=ImageFont.truetype(font,27))
 if slug in ['gridline','altaire-jackson']:draw.text((72,466),'Approved exterior photograph pending',fill='#62685f',font=ImageFont.truetype(font,21))
 draw.text((72,550),'jyotib.com',fill='#62685f',font=ImageFont.truetype(font,22));im.save(BASE/f'public/assets/share-{slug}.jpg',quality=88)
# Favicon with a simple typographic mark, plus touch icon.
im=Image.new('RGB',(180,180),'#f8f7f3');draw=ImageDraw.Draw(im);f=ImageFont.truetype(serif,81);draw.text((34,35),'JB',font=f,fill='#053369');im.save(BASE/'public/assets/apple-touch-icon.png');im.save(BASE/'public/favicon.ico',sizes=[(16,16),(32,32),(48,48)])
(BASE/'public/assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#f8f7f3"/><text x="9" y="45" font-family="Georgia,serif" font-size="36" fill="#053369">JB</text></svg>')
(BASE/'asset-records.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
print(f'Exported {len(records)} portfolio images in two responsive sizes; social cards and favicons.')
