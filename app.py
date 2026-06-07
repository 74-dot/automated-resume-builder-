import io
from textwrap import wrap
from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():

    name = request.form.get("name", "")
    email = request.form.get("email", "")
    phone = request.form.get("phone", "")
    dob = request.form.get("dob", "")
    gender = request.form.get("gender", "")
    nationality = request.form.get("nationality", "")
    languages = request.form.get("languages", "")
    education = request.form.get("education", "")
    skills = request.form.get("skills", "")
    projects = request.form.get("projects", "")
    certifications = request.form.get("certifications", "")
    hobbies = request.form.get("hobbies", "")

    photo = request.files.get("photo")

    objective = (
        f"A motivated {education} student seeking opportunities "
        f"to apply technical and problem-solving skills while "
        f"contributing to innovative projects and continuous learning."
    )


    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setTitle("Resume")
    pdf.setLineWidth(1)

    if photo and photo.filename:
        image = ImageReader(photo)
        pdf.drawImage(image,
            450,     #x-position
            740,      #y-position
            width=90,
            height=90,
            preserveAspectRatio=True,
            mask='auto'


            
        )
         
        pdf.rect(448 ,738, 94, 94)

    # HEADER
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawCentredString(300, 800, name)

    pdf.setFont("Helvetica", 11)
    pdf.drawCentredString(300, 780, f"{email} | {phone}")
    pdf.line(40, 730, 560, 730)

    y = 700

    # PERSONAL DETAILS
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "PERSONAL DETAILS")
    pdf.line(50, y - 5, 550, y - 5)
    y -= 25

    pdf.setFont("Helvetica", 11)
    pdf.drawString(60, y, f"Date of Birth : {dob}")
    y -= 18
    pdf.drawString(60, y, f"Gender : {gender}")
    y -= 18
    pdf.drawString(60, y, f"Nationality : {nationality}")
    y -= 18
    pdf.drawString(60, y, f"Languages Known : {languages}")

    # CAREER OBJECTIVE
    y -= 40
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "CAREER OBJECTIVE")
    pdf.line(50, y - 5, 550, y - 5)
    y -= 25

    pdf.setFont("Helvetica", 11)
    # The wrap function imported from textwrap now executes perfectly
    for line in wrap(objective, width=75):
        pdf.drawString(60, y, line)
        y -= 15

    # EDUCATION
    y -= 15
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "EDUCATION")
    pdf.line(50, y - 5, 550, y - 5)
    y -= 25

    pdf.setFont("Helvetica", 11)
    pdf.drawString(60, y, education)

    # SKILLS
    y -= 40
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "SKILLS")
    pdf.line(50, y - 5, 550, y - 5)
    y -= 25

    for skill in skills.split(","):
        if skill.strip():
            pdf.drawString(60, y, f"• {skill.strip()}")
            y -= 18

    # PROJECTS
    y -= 10
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "PROJECTS")
    pdf.line(50, y - 5, 550, y - 5)
    y -= 25

    for project in projects.split(","):
        if project.strip():
            pdf.drawString(60, y, f"• {project.strip()}")
            y -= 18

    # CERTIFICATIONS
    y -= 10
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "CERTIFICATIONS")
    pdf.line(50, y - 5, 550, y - 5)
    y -= 25

    for cert in certifications.split(","):
        if cert.strip():
            pdf.drawString(60, y, f"• {cert.strip()}")
            y -= 18

    # HOBBIES
    y -= 10
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "HOBBIES / INTERESTS")
    pdf.line(50, y - 5, 550, y - 5)
    y -= 25

    for hobby in hobbies.split(","):
        if hobby.strip():
            pdf.drawString(60, y, f"• {hobby.strip()}")
            y -= 18

    # 3. Finalise and stream the document from RAM
    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="resume.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)