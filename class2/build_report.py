from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

OUT = "/host/class2/Session02-NotesApp-Model.pdf"
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8, leading=10))
doc = SimpleDocTemplate(OUT, pagesize=A4, rightMargin=15*mm, leftMargin=15*mm, topMargin=15*mm, bottomMargin=15*mm)
story = [Paragraph("Class 2 - NotesApp Initial Threat Model", styles["Title"]),
         Paragraph("Yuchen Ye | Student ID 2023901708", styles["Normal"]), Spacer(1,8),
         Paragraph("Architecture and trust boundaries", styles["Heading2"]),
         Paragraph("Browser requests cross TB1 into Flask. Flask database operations cross TB2 into PostgreSQL. The admin ping feature and the mounted Docker socket cross TB3 into external or host-controlled resources.", styles["BodyText"]), Spacer(1,10)]
components = [["Component","Security role"],["Browser","Untrusted client input and rendered output"],["Flask web container","Authentication, authorization and business logic"],["PostgreSQL","Accounts, grades and comments"],["External target / Docker host","Ping destination and privileged host resources"]]
t=Table(components,colWidths=[45*mm,125*mm]); t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1F4E78")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),0.4,colors.grey),("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("VALIGN",(0,0),(-1,-1),"TOP"),("FONTSIZE",(0,0),(-1,-1),8),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#EAF2F8")])]))
story += [t, Spacer(1,12), Paragraph("Key findings", styles["Heading2"])]
for item in ["Spoofing: unsigned JWTs and weak credentials can impersonate users.","Tampering: SQL injection, CSRF and unsigned exports permit undetected changes.","Disclosure: HTTP, plaintext secrets and IDOR expose protected data.","Elevation: command injection combined with root/Docker socket access can compromise the host."]:
    story.append(Paragraph("- "+item, styles["BodyText"]))
story += [PageBreak(),Paragraph("Numbered logical flows",styles["Heading1"])]
flows = [
"Login credentials","Account lookup","Account record","Session and redirect","Dashboard request","Student grade query","Grade rows","Dashboard HTML","Note API request","Note-by-id query","Selected note","Note JSON","Teacher page request","Teaching-data queries","Teaching data","Teacher HTML","Grade form","Grade write","Write result","Post-write redirect","Export request","Export query","Export rows","CSV download","Admin input","User/class database action","ICMP request","Admin result"]
data=[["#","Flow"]]+[[str(i+1),v] for i,v in enumerate(flows)]
t=Table(data,colWidths=[12*mm,158*mm],repeatRows=1); t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2F75B5")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#94A3B8")),("FONTSIZE",(0,0),(-1,-1),8),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F1F5F9")])]))
story.append(t)
doc.build(story)
print(OUT)
