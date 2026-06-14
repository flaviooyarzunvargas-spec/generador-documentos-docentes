from pathlib import Path
import uuid
import matplotlib.pyplot as plt


def generar_grafico_barras(
    categorias: list[str],
    valores: list[float],
    titulo: str,
    etiqueta_x: str,
    etiqueta_y: str,
    output_dir: Path
) -> Path:
    if len(categorias) != len(valores):
        raise ValueError(
            "La cantidad de categorías debe coincidir con la cantidad de valores."
        )

    nombre_imagen = f"barras_{uuid.uuid4()}.png"
    ruta_imagen = output_dir / nombre_imagen

    plt.figure(figsize=(6, 4))
    plt.bar(categorias, valores)
    plt.title(titulo)
    plt.xlabel(etiqueta_x)
    plt.ylabel(etiqueta_y)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig(str(ruta_imagen), dpi=150)
    plt.close()

    return ruta_imagen
