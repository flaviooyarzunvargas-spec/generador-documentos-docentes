from pathlib import Path
import uuid
import numpy as np
import matplotlib.pyplot as plt


def generar_grafico_circunferencia(
    centro_x: float,
    centro_y: float,
    radio: float,
    titulo: str,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    output_dir: Path
) -> Path:
    if radio <= 0:
        raise ValueError("El radio debe ser mayor que 0.")

    nombre_imagen = f"circunferencia_{uuid.uuid4()}.png"
    ruta_imagen = output_dir / nombre_imagen

    theta = np.linspace(0, 2 * np.pi, 400)
    x = centro_x + radio * np.cos(theta)
    y = centro_y + radio * np.sin(theta)

    plt.figure(figsize=(6, 6))
    plt.plot(x, y, label=f"Centro ({centro_x}, {centro_y}), radio {radio}")
    plt.plot(centro_x, centro_y, marker="o")
    plt.axhline(0, linewidth=1)
    plt.axvline(0, linewidth=1)
    plt.grid(True)
    plt.title(titulo)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.legend()
    plt.tight_layout()
    plt.savefig(str(ruta_imagen), dpi=150)
    plt.close()

    return ruta_imagen


def generar_grafico_triangulo(
    puntos: list[tuple[float, float]],
    etiquetas: list[str],
    titulo: str,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    output_dir: Path
) -> Path:
    if len(puntos) != 3:
        raise ValueError("El gráfico de triángulo requiere exactamente 3 puntos.")

    if len(etiquetas) != 3:
        etiquetas = ["A", "B", "C"]

    nombre_imagen = f"triangulo_{uuid.uuid4()}.png"
    ruta_imagen = output_dir / nombre_imagen

    xs = [p[0] for p in puntos] + [puntos[0][0]]
    ys = [p[1] for p in puntos] + [puntos[0][1]]

    plt.figure(figsize=(6, 6))
    plt.plot(xs, ys, marker="o")
    plt.fill(xs, ys, alpha=0.15)

    for (x, y), etiqueta in zip(puntos, etiquetas):
        plt.text(x, y, f" {etiqueta}({x:g},{y:g})", fontsize=10)

    plt.axhline(0, linewidth=1)
    plt.axvline(0, linewidth=1)
    plt.grid(True)
    plt.title(titulo)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.tight_layout()
    plt.savefig(str(ruta_imagen), dpi=150)
    plt.close()

    return ruta_imagen


def generar_grafico_poligono(
    puntos: list[tuple[float, float]],
    etiquetas: list[str],
    titulo: str,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    output_dir: Path
) -> Path:
    if len(puntos) < 3:
        raise ValueError("Un polígono debe tener al menos 3 vértices.")

    nombre_imagen = f"poligono_{uuid.uuid4()}.png"
    ruta_imagen = output_dir / nombre_imagen

    xs = [p[0] for p in puntos] + [puntos[0][0]]
    ys = [p[1] for p in puntos] + [puntos[0][1]]

    plt.figure(figsize=(6, 6))
    plt.plot(xs, ys, marker="o")
    plt.fill(xs, ys, alpha=0.12)

    for i, (x, y) in enumerate(puntos):
        etiqueta = etiquetas[i] if i < len(etiquetas) else f"P{i + 1}"
        plt.text(x, y, f" {etiqueta}({x:g},{y:g})", fontsize=10)

    plt.axhline(0, linewidth=1)
    plt.axvline(0, linewidth=1)
    plt.grid(True)
    plt.title(titulo)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.tight_layout()
    plt.savefig(str(ruta_imagen), dpi=150)
    plt.close()

    return ruta_imagen


def generar_grafico_traslacion(
    puntos: list[tuple[float, float]],
    etiquetas: list[str],
    dx: float,
    dy: float,
    titulo: str,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    output_dir: Path
) -> Path:
    if len(puntos) < 3:
        raise ValueError("La figura a trasladar debe tener al menos 3 puntos.")

    if len(etiquetas) != len(puntos):
        etiquetas = [f"P{i + 1}" for i in range(len(puntos))]

    puntos_trasladados = [
        (x + dx, y + dy)
        for x, y in puntos
    ]

    nombre_imagen = f"traslacion_{uuid.uuid4()}.png"
    ruta_imagen = output_dir / nombre_imagen

    xs_original = [p[0] for p in puntos] + [puntos[0][0]]
    ys_original = [p[1] for p in puntos] + [puntos[0][1]]

    xs_trasladado = [p[0] for p in puntos_trasladados] + [puntos_trasladados[0][0]]
    ys_trasladado = [p[1] for p in puntos_trasladados] + [puntos_trasladados[0][1]]

    plt.figure(figsize=(6, 6))

    plt.plot(xs_original, ys_original, marker="o", label="Figura original")
    plt.fill(xs_original, ys_original, alpha=0.12)

    plt.plot(xs_trasladado, ys_trasladado, marker="o", linestyle="--", label="Figura trasladada")
    plt.fill(xs_trasladado, ys_trasladado, alpha=0.12)

    for (x, y), etiqueta in zip(puntos, etiquetas):
        plt.text(x, y, f" {etiqueta}({x:g},{y:g})", fontsize=9)

    for (x, y), etiqueta in zip(puntos_trasladados, etiquetas):
        plt.text(x, y, f" {etiqueta}'({x:g},{y:g})", fontsize=9)

    plt.axhline(0, linewidth=1)
    plt.axvline(0, linewidth=1)
    plt.grid(True)
    plt.title(titulo)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.legend()
    plt.tight_layout()
    plt.savefig(str(ruta_imagen), dpi=150)
    plt.close()

    return ruta_imagen


def generar_grafico_reflexion(
    puntos: list[tuple[float, float]],
    etiquetas: list[str],
    eje: str,
    titulo: str,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    output_dir: Path
) -> Path:
    if len(puntos) < 3:
        raise ValueError("La figura a reflejar debe tener al menos 3 puntos.")

    if len(etiquetas) != len(puntos):
        etiquetas = [f"P{i + 1}" for i in range(len(puntos))]

    eje = eje.lower().strip()

    if eje == "x":
        puntos_reflejados = [(x, -y) for x, y in puntos]
        etiqueta_eje = "Reflexión respecto del eje X"
    elif eje == "y":
        puntos_reflejados = [(-x, y) for x, y in puntos]
        etiqueta_eje = "Reflexión respecto del eje Y"
    else:
        raise ValueError("El eje de reflexión debe ser 'x' o 'y'.")

    nombre_imagen = f"reflexion_{uuid.uuid4()}.png"
    ruta_imagen = output_dir / nombre_imagen

    xs_original = [p[0] for p in puntos] + [puntos[0][0]]
    ys_original = [p[1] for p in puntos] + [puntos[0][1]]

    xs_reflejado = [p[0] for p in puntos_reflejados] + [puntos_reflejados[0][0]]
    ys_reflejado = [p[1] for p in puntos_reflejados] + [puntos_reflejados[0][1]]

    plt.figure(figsize=(6, 6))

    plt.plot(xs_original, ys_original, marker="o", label="Figura original")
    plt.fill(xs_original, ys_original, alpha=0.12)

    plt.plot(xs_reflejado, ys_reflejado, marker="o", linestyle="--", label="Figura reflejada")
    plt.fill(xs_reflejado, ys_reflejado, alpha=0.12)

    for (x, y), etiqueta in zip(puntos, etiquetas):
        plt.text(x, y, f" {etiqueta}({x:g},{y:g})", fontsize=9)

    for (x, y), etiqueta in zip(puntos_reflejados, etiquetas):
        plt.text(x, y, f" {etiqueta}'({x:g},{y:g})", fontsize=9)

    if eje == "x":
        plt.axhline(0, linewidth=2, label="Eje de reflexión")
        plt.axvline(0, linewidth=1)
    else:
        plt.axvline(0, linewidth=2, label="Eje de reflexión")
        plt.axhline(0, linewidth=1)

    plt.grid(True)
    plt.title(titulo if titulo else etiqueta_eje)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.legend()
    plt.tight_layout()
    plt.savefig(str(ruta_imagen), dpi=150)
    plt.close()

    return ruta_imagen
