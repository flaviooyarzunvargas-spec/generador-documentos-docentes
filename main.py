from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from docx import Document
from pathlib import Path
import uuid

app = FastAPI(title="Generador de Documentos Docentes")


class DocumentoRequest(BaseModel):
    tipo: str
    titulo: str
    curso: str
    asignatura: str
    contenido: str


@app.get("/")
def inicio():
    return {
        "mensaje": "API generadora de documentos activa"
    }


@app.post("/generar-documento")
def generar_documento(data: DocumentoRequest):

    try:

        # Ruta base del proyecto
        base_dir = Path(__file__).parent

        # Plantilla institucional
        plantilla = base_dir / "plantillas" / "GuíaICA.docx"

        # Abrir plantilla
        doc = Document(str(plantilla))

        # Nueva página para el contenido generado
#        doc.add_page_break()

        # Encabezado del documento
        doc.add_heading(data.titulo, level=1)

        doc.add_paragraph(f"Curso: {data.curso}")
        doc.add_paragraph(f"Asignatura: {data.asignatura}")
        doc.add_paragraph(f"Tipo: {data.tipo}")

        doc.add_heading("Contenido", level=2)

        # Insertar contenido línea por línea
        for linea in data.contenido.split("\n"):
            doc.add_paragraph(linea)

        # Nombre único
        nombre_archivo = f"{uuid.uuid4()}.docx"

        ruta_salida = Path("/tmp") / nombre_archivo

        # Guardar documento
        doc.save(str(ruta_salida))

        return FileResponse(
            path=str(ruta_salida),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=f"{data.titulo}.docx"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
