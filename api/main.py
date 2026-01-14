from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from docxtpl import DocxTemplate
import uuid
import os

app = FastAPI()

class Experience(BaseModel):
    poste: str
    entreprise: str
    duree: str

class CVData(BaseModel):
    nom: str
    email: str
    telephone: str
    ville: str
    linkedin: str
    objectif: str
    diplomes: list[str]
    experiences: list[Experience]
    competences: list[str]
    langues: list[str]
    hobbies: list[str]

@app.post("/generate-cv")
def generate_cv(data: CVData):
    template_path = "modele_cv.docx"  # Ton modèle Word avec {{ }} et {% %}

    doc = DocxTemplate(template_path)

    # Contexte à injecter
    context = {
        "nom": data.nom,
        "email": data.email,
        "telephone": data.telephone,
        "ville": data.ville,
        "linkedin": data.linkedin,
        "objectif": data.objectif,
        "diplomes": data.diplomes,
        "experiences": [e.dict() for e in data.experiences],
        "competences": data.competences,
        "langues": data.langues,
        "hobbies": data.hobbies
    }

    os.makedirs("/tmp/output", exist_ok=True)
    filename = f"{uuid.uuid4()}_cv.docx"
    filepath = f"/tmp/output/{filename}"

    doc.render(context)
    doc.save(filepath)

    return FileResponse(filepath, 
                        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                        filename=filename)
