#!/usr/bin/env python3
"""Build the user-facing cooking guide from reviewed editorial cards."""
import argparse,json,hashlib
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,KeepTogether
from reportlab.lib.units import inch
ROOT=Path(__file__).resolve().parents[1]
PAPER=(612,792)
INK=colors.HexColor('#203832'); GREEN=colors.HexColor('#315d4d'); PALE=colors.HexColor('#edf3ed')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='GuideTitle',fontName='Helvetica-Bold',fontSize=27,leading=31,textColor=INK,spaceAfter=10))
styles.add(ParagraphStyle(name='GuideSub',fontName='Helvetica',fontSize=12,leading=17,textColor=GREEN,spaceAfter=12))
styles.add(ParagraphStyle(name='GuideBody',fontName='Helvetica',fontSize=12.5,leading=18,spaceAfter=8,textColor=INK))
styles.add(ParagraphStyle(name='GuideSmall',fontName='Helvetica',fontSize=10,leading=14,textColor=INK,spaceAfter=7))
styles.add(ParagraphStyle(name='GuideHead',fontName='Helvetica-Bold',fontSize=13,leading=17,textColor=GREEN,spaceBefore=10,spaceAfter=7))
def para(text,style='GuideBody'):return Paragraph(text,styles[style])
def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#c5d3c9'));c.line(44,39,568,39);c.setFont('Helvetica',8);c.setFillColor(INK)
 c.drawString(44,26,'MINIMO COOKING GUIDE  |  Starter edition');c.drawRightString(568,26,str(doc.page))
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'output/pdf/MiniMo_Cooking_Guide.pdf');p.add_argument('--source-root',type=Path,default=ROOT);a=p.parse_args()
 data=json.loads((ROOT/'07_Output_Templates/quick-start-breakfasts.json').read_text())
 for recipe in data['recipes']:
  blob=(a.source_root/recipe['source_snapshot']).read_bytes()
  if hashlib.sha256(blob).hexdigest()!=recipe['source_snapshot_sha256']:
   raise ValueError('Source record changed: review the cooking card before rebuilding '+recipe['title'])
 story=[Spacer(1,18),para(data['title'],'GuideTitle'),para(data['subtitle'],'GuideSub'),para('Open this guide. Choose a breakfast. Gather its ingredients. Follow the numbered steps.'),Spacer(1,8),para('Choose your breakfast','GuideHead')]
 for i,r in enumerate(data['recipes'],2):story.extend([para(f'<b>Page {i} - {escape(r["title"])}</b>'),para(escape(r['choice']),'GuideSmall')])
 story.extend([para('Before you turn on the stove','GuideHead')])
 for t in ['Cook outdoors on a flat, stable surface. Never use the stove inside a tent, vehicle or building.', 'Light the burner without a pot or skillet on it. Then place the cookware as directed in the MiniMo manual. Use the Pot Support for the skillet.', 'Never fill the MiniMo pot more than half full. Stay with the stove, stir food frequently, and turn it off when finished.', 'Keep eggs and other perishable food at 40 F or colder. Discard it after more than 2 hours without cold storage, or 1 hour when the temperature is above 90 F.']:
  story.append(para('- '+escape(t)))
 story.extend([Spacer(1,5),para('Kitchen shorthand: tablespoon is the large measuring spoon; teaspoon is the small one. A simmer means gentle bubbling.','GuideSmall'),para('These are simplified MiniMo cooking directions, adapted from the preserved Jetboil recipes. Changes are noted on each card. This is a starter guide, not the full cookbook. Sources and review limits are on page 6.','GuideSmall')])
 for r in data['recipes']:
  story.extend([PageBreak(),para(escape(r['title']),'GuideTitle'),para(escape(r['quantity']),'GuideSub'),para('<b>Equipment:</b> '+escape(r['equipment'])),para('Gather these ingredients','GuideHead')])
  # Two-column ingredient list keeps each recipe on a single readable page.
  ing=r['ingredients'];cut=(len(ing)+1)//2
  rows=[]
  for i in range(cut):rows.append([para('- '+escape(ing[i])),para('- '+escape(ing[i+cut])) if i+cut<len(ing) else ''])
  table=Table(rows,colWidths=[258,258]);table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]));story.append(table)
  story.append(para('Cook it','GuideHead'))
  for i,t in enumerate(r['steps'],1):story.append(para(f'<b>{i}.</b> '+escape(t)))
  story.extend([Spacer(1,4),para('<b>MiniMo note:</b> '+escape(r['note']),'GuideSmall'),para('<b>What was adapted:</b> '+escape(r['adaptation']),'GuideSmall')])
 story.extend([PageBreak(),para('About this guide','GuideTitle'),para('The cooking pages are intentionally simple.','GuideSub'),para('The original Jetboil ingredient lists and instructions are preserved separately in your cookbook. This guide provides practical directions, with equipment and cooking notes added outside those originals.'),para('Sources','GuideHead')])
 for r in data['recipes']:
  url='https://jetboil.johnsonoutdoors.com/us/recipes/'+r['source_slug']
  story.append(para(f'<link href="{url}" color="#315d4d">{escape(r["title"])} - official Jetboil source</link>'))
 refs=[('MiniMo operating manual','https://jetboil.johnsonoutdoors.com/sites/default/files/2023-02/JB_product_manual_MicroMo_MiniMo_SUMO_0.pdf'),('MiniMo / Grande Coffee Press compatibility','https://jetboil.johnsonoutdoors.com/us/shop/stoves-systems/minimo-cooking-system/mnmad'),('USDA egg cooking guidance','https://ask.fsis.usda.gov/article/What-is-a-safe-internal-temperature-for-food-made-with-eggs'),('USDA cold-storage and leftover guidance','https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/leftovers-and-food-safety')]
 for title,url in refs:story.append(para(f'<link href="{url}" color="#315d4d">{escape(title)}</link>'))
 story.extend([para('Review limits','GuideHead'),para('Recipe text was checked against indexed copies of the official Jetboil pages on September 10, 2026. Jetboil blocked direct website access during that check. A fresh live-page comparison is still pending.'),para('These editorial adaptations have not been field-tested. No exact serving count, fuel use or total preparation time is promised. Quinoa quantities are exactly half the published amounts; the original simmer time is a starting point, not a tested time for the smaller batch.'),para('Your first meal','GuideHead'),para('If you have the Summit Skillet and Pot Support, start with French Toast on page 2. If you are using only the MiniMo pot, choose Quinoa Breakfast Bowl on page 4. You do not need to open any of the technical files to cook from this guide.'),Spacer(1,15),para(escape(data['edition']),'GuideSmall')])
 a.output.parent.mkdir(parents=True,exist_ok=True)
 SimpleDocTemplate(str(a.output),pagesize=PAPER,rightMargin=44,leftMargin=44,topMargin=40,bottomMargin=52,title=data['title'],author='MiniMo Cooking').build(story,onFirstPage=footer,onLaterPages=footer)
 print(a.output)
if __name__=='__main__':main()
