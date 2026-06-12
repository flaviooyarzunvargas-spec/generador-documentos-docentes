from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from docx import Document
from pathlib import Path
import unicodedata
import uuid


app = FastAPI(
    title="Generador de Documentos Docentes",
    version="0.1.0"
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Generador de Documentos Docentes",
        version="0.1.0",
        description="API para generar documentos docentes en formato DOCX.",
        routes=app.routes,
    )

    openapi_schema["servers"] = [
        {
            "url": "https://generador-documentos-docentes.onrender.com",
            "description": "Servidor en Render"
        }
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


class DocumentoRequest(BaseModel):
    tipo: str
    titulo: str
    curso: str
    asignatura: str
    contenido: str


def normalizar_texto(texto: str) -> str:
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )
    return texto


@app.get("/")
def inicio():
    return {
        "mensaje": "API generadora de documentos activa"
    }


def seleccionar_plantilla(tipo: str):
    base_dir = Path(__file__).parent
    plantillas_dir = base_dir / "plantillas"

    tipo_normalizado = normalizar_texto(tipo)

    plantillas = {
        "guia": "GuíaICA.docx",
        "prueba": "PruebaICA.docx",
        "planificacion": "PlanificacionICA.docx",
        "planificacion clase": "PlanificacionICA.docx",
        "rubrica": "RubricaICA.docx",
        "solucionario": "GuíaICA.docx"
    }

    nombre_plantilla = plantillas.get(tipo_normalizado)

    if not nombre_plantilla:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de documento no válido: {tipo}. Use guia, prueba, planificacion, rubrica o solucionario."
        )

    ruta_plantilla = plantillas_dir / nombre_plantilla

    if not ruta_plantilla.exists():
        raise HTTPException(
            status_code=404,
            detail=f"No existe la plantilla: {nombre_plantilla}"
        )

    return ruta_plantilla


@app.post("/generar-documento")
def generar_documento(data: DocumentoRequest):
    try:
        plantilla = seleccionar_plantilla(data.tipo)

        doc = Document(str(plantilla))

        doc.add_heading(data.titulo, level=1)
        doc.add_paragraph(f"Curso: {data.curso}")
        doc.add_paragraph(f"Asignatura: {data.asignatura}")
        doc.add_paragraph(f"Tipo de documento: {data.tipo}")

        doc.add_heading("Contenido", level=2)

        for linea in data.contenido.split("\n"):
            doc.add_paragraph(linea)

        nombre_archivo = f"{uuid.uuid4()}.docx"
        ruta_salida = Path("/tmp") / nombre_archivo

        doc.save(str(ruta_salida))

        return FileResponse(
            path=str(ruta_salida),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=f"{data.titulo}.docx"
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
