"""Módulo principal del organizador automático de carpetas."""

import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from utils import una_dentro_de_otra

consola = Console()


def mostrar_cabecera(consola):
    """Muestra el título del programa dentro de un panel azul."""
    consola.print(Panel("Organizador de Carpetas", border_style="blue"))


def main():
    """Punto de entrada principal del programa."""
    mostrar_cabecera(consola)
    ruta_origen = Prompt.ask("Ruta de origen", console=consola)
    ruta_destino = Prompt.ask("Ruta de destino", console=consola)

    # Compruebo que la carpeta origen de verdad existe y si es un directorio
    if not os.path.isdir(ruta_origen):
        consola.print(
            Panel("La carpeta de origen no existe o no es un directorio.", border_style="red")
        )
        return

    # Si la ruta de destino existe compruebo que sea una carpeta
    if os.path.exists(ruta_destino) and not os.path.isdir(ruta_destino):
        consola.print(
            Panel("La ruta de destino existe pero no es una carpeta", border_style="red")
        )
        return

    # Compruebo que las carpetas no sean la misma ni una contenga a la otra
    if una_dentro_de_otra(ruta_origen, ruta_destino):
        consola.print(
            Panel(
                "La carpeta de origen y la de destino no pueden ser la misma ni estar una dentro de la otra.",
                border_style="red",
            )
        )
        return


if __name__ == "__main__":
    main()
