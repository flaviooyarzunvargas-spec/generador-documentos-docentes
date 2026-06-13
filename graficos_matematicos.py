from pathlib import Path
import matplotlib.pyplot as plt


def crear_fraccion_simple(numerador, denominador, archivo_salida):
    """
    Genera una imagen simple de una fracción.
    """

    plt.figure(figsize=(3, 2))
    plt.axis("off")

    plt.text(
        0.5,
        0.5,
        rf"$\frac{{{numerador}}}{{{denominador}}}$",
        fontsize=30,
        ha="center"
    )

    plt.savefig(
        archivo_salida,
        bbox_inches="tight",
        transparent=True
    )

    plt.close()


def crear_decimal_a_fraccion(decimal, fraccion, archivo_salida):
    """
    Genera una imagen explicativa de conversión.
    """

    plt.figure(figsize=(6, 2))
    plt.axis("off")

    texto = f"{decimal} = {fraccion}"

    plt.text(
        0.5,
        0.5,
        texto,
        fontsize=22,
        ha="center"
    )

    plt.savefig(
        archivo_salida,
        bbox_inches="tight"
    )

    plt.close()


if __name__ == "__main__":

    carpeta = Path("imagenes")
    carpeta.mkdir(exist_ok=True)

    crear_fraccion_simple(
        3,
        4,
        carpeta / "fraccion_3_4.png"
    )

    crear_decimal_a_fraccion(
        "0,25",
        "1/4",
        carpeta / "decimal_025.png"
    )

    print("Imágenes generadas correctamente.")

