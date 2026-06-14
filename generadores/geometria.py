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
