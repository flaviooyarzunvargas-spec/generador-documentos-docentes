from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from docx import Document
from docx.shared import Inches
from pathlib import Path
import unicodedata
import uuid


app = FastAPI(
    title="Generador de Documentos Docentes",
    version="0.1.0"
)


OUTPUT_DIR = Path("/tmp/documentos")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app.mount(
    "/documentos",
    StaticFiles(directory=str(OUTPUT_DIR)),
    name="documentos"
)


class DocumentoRequest(BaseModel):
    tipo: str
    titulo: str
    curso: str
    asignatura: str
    contenido: str


class DocumentoResponse(BaseModel):
    mensaje: str
    titulo: str
    curso: str
    asignatura: str
    tipo: str
    archivo: str
    url: str


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


@app.get("/test")
def test():
    return {
        "estado": "ok"
    }


@app.get("/ping")
def ping():
    return {
        "ping": "pong"
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
            detail=(
                f"Tipo de documento no válido: {tipo}. "
                "Use guia, prueba, planificacion, rubrica o solucionario."
            )
        )

    ruta_plantilla = plantillas_dir / nombre_plantilla

    if not ruta_plantilla.exists():
        raise HTTPException(
            status_code=404,
            detail=f"No existe la plantilla: {nombre_plantilla}"
        )

    return ruta_plantilla


def insertar_imagenes_matematicas(doc: Document):
    """
    Inserta imágenes matemáticas generadas previamente si existen.
    Busca imágenes dentro de la carpeta /imagenes.
    """

    base_dir = Path(__file__).parent
    imagenes_dir = base_dir / "imagenes"

    imagenes = [
        imagenes_dir / "fraccion_3_4.png",
        imagenes_dir / "decimal_025.png"
    ]

    imagenes_existentes = [
        imagen for imagen in imagenes
        if imagen.exists()
    ]

    if not imagenes_existentes:
        return

    doc.add_heading("Representaciones visuales", level=2)

    for imagen in imagenes_existentes:
        doc.add_picture(
            str(imagen),
            width=Inches(2.5)
        )


@app.post(
    "/generar-documento",
    response_model=DocumentoResponse
)
def generar_documento(data: DocumentoRequest):
    try:
        plantilla = seleccionar_plantilla(data.tipo)

        doc = Document(str(plantilla))

        doc.add_heading(data.titulo, level=1)
        doc.add_paragraph(f"Curso: {data.curso}")
        doc.add_paragraph(f"Asignatura: {data.asignatura}")
        doc.add_paragraph(f"Tipo de documento: {data.tipo}")

        doc.add_heading("Contenido", level=2)

        insertar_imagenes_matematicas(doc)

        for linea in data.contenido.split("\n"):
            doc.add_paragraph(linea)

        nombre_archivo = f"{uuid.uuid4()}.docx"
        ruta_salida = OUTPUT_DIR / nombre_archivo

        doc.save(str(ruta_salida))

        url_archivo = (
            "https://generador-documentos-docentes.onrender.com/"
            f"documentos/{nombre_archivo}"
        )

        return DocumentoResponse(
            mensaje="Documento generado correctamente",
            titulo=data.titulo,
            curso=data.curso,
            asignatura=data.asignatura,
            tipo=data.tipo,
            archivo=nombre_archivo,
            url=url_archivo
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
