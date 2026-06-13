from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from docx import Document
from docx.shared import Inches
from pathlib import Path
import unicodedata
import uuid
import re
import numpy as np
import matplotlib.pyplot as plt


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
    return {"mensaje": "API generadora de documentos activa"}


@app.get("/test")
def test():
    return {"estado": "ok"}


@app.get("/ping")
def ping():
    return {"ping": "pong"}


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


def generar_grafico_funcion(
    expresion: str,
    titulo: str,
    x_min: float,
    x_max: float
) -> Path:
    """
    Genera gráfico de una función y devuelve la ruta PNG.
    La expresión debe escribirse en formato Python:
    2*x + 1
    -x + 3
    x**2 - 4
    """

    nombre_imagen = f"grafico_{uuid.uuid4()}.png"
    ruta_imagen = OUTPUT_DIR / nombre_imagen

    x = np.linspace(x_min, x_max, 400)

    entorno_seguro = {
        "x": x,
        "np": np,
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "sqrt": np.sqrt,
        "log": np.log,
        "exp": np.exp,
        "pi": np.pi,
        "abs": np.abs
    }

    try:
        y = eval(expresion, {"__builtins__": {}}, entorno_seguro)
    except Exception as e:
        raise ValueError(f"No se pudo graficar la función '{expresion}': {e}")

    plt.figure(figsize=(6, 4))
    plt.plot(x, y)
    plt.axhline(0, linewidth=1)
    plt.axvline(0, linewidth=1)
    plt.grid(True)
    plt.title(titulo)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()
    plt.savefig(str(ruta_imagen), dpi=150)
    plt.close()

    return ruta_imagen


def procesar_linea_con_grafico(doc: Document, linea: str) -> bool:
    """
    Detecta líneas con este formato:

    [GRAFICO_FUNCION: expr=2*x+1; titulo=f(x)=2x+1; x_min=-4; x_max=4]

    Si la línea contiene ese marcador, genera e inserta el gráfico.
    Retorna True si insertó gráfico; False si no.
    """

    patron = r"\[GRAFICO_FUNCION:(.*?)\]"
    coincidencia = re.search(patron, linea)

    if not coincidencia:
        return False

    contenido = coincidencia.group(1)

    parametros = {}
    partes = contenido.split(";")

    for parte in partes:
        if "=" in parte:
            clave, valor = parte.split("=", 1)
            parametros[clave.strip()] = valor.strip()

    expresion = parametros.get("expr")
    titulo = parametros.get("titulo", f"Gráfico de {expresion}")
    x_min = float(parametros.get("x_min", -5))
    x_max = float(parametros.get("x_max", 5))

    if not expresion:
        doc.add_paragraph("Error: marcador de gráfico sin expresión.")
        return True

    ruta_grafico = generar_grafico_funcion(
        expresion=expresion,
        titulo=titulo,
        x_min=x_min,
        x_max=x_max
    )

    doc.add_picture(str(ruta_grafico), width=Inches(5.5))
    return True


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

        for linea in data.contenido.split("\n"):
            linea_limpia = linea.strip()

            if procesar_linea_con_grafico(doc, linea_limpia):
                continue

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
