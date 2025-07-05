from docx import Document 

def generate_cv_from_template(data, template_path="C:\Users\Kayeon Dominique\Desktop\scripts\modele_cv.docx", output_path="cv_final.docx"):
    doc = Document(template_path)

    # Parcourir tous les paragraphes pour remplacer les balises
    for para in doc.paragraphs:
        for key, value in data.items():
            if isinstance(value, list):
                value = ", ".join(value)
            para.text = para.text.replace(f"{{{{{key}}}}}", value or "")

    doc.save(output_path)
    return output_path
