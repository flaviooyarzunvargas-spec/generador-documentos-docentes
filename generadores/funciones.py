from pathlib import Path
import uuid
import numpy as np
import matplotlib.pyplot as plt


def obtener_entorno_seguro(x):
    return {
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


def generar_grafico_funcion(
    expresion: str,
    titulo: str,
    x_min: float,
    x_max: float,
    output_dir: Path
) -> Path:
    nombre_imagen = f"grafico_{uuid.uuid4()}.png"
    ruta_imagen = output_dir / nombre_imagen

    x = np.linspace(x_min, x_max, 400)
    entorno_seguro = obtener_entorno_seguro(x)

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


def generar_grafico_sistema(
    expresion_f: str,
    expresion_g: str,
    titulo: str,
    x_min: float,
    x_max: float,
    output_dir: Path
) -> Path:
    nombre_imagen = f"sistema_{uuid.uuid4()}.png"
    ruta_imagen = output_dir / nombre_imagen

    x = np.linspace(x_min, x_max, 400)
    entorno_seguro = obtener_entorno_seguro(x)

    try:
        y_f = eval(expresion_f, {"__builtins__": {}}, entorno_seguro)
        y_g = eval(expresion_g, {"__builtins__": {}}, entorno_seguro)
    except Exception as e:
        raise ValueError(f"No se pudo graficar el sistema: {e}")

    plt.figure(figsize=(6, 4))
    plt.plot(x, y_f, label=f"f(x) = {expresion_f}")
    plt.plot(x, y_g, label=f"g(x) = {expresion_g}")
    plt.axhline(0, linewidth=1)
    plt.axvline(0, linewidth=1)
    plt.grid(True)
    plt.title(titulo)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.tight_layout()
    plt.savefig(str(ruta_imagen), dpi=150)
    plt.close()

    return ruta_imagen
