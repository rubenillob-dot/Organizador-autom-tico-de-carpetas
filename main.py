"""Módulo principal del organizador automático de carpetas."""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

consola = Console()


def mostrar_cabecera(consola):
    """Muestra el título del programa dentro de un panel azul"""
    consola.print(Panel("Organizador de Carpetas", border_style="blue"))


def main():
    """Punto de entrada principal del programa"""
    mostrar_cabecera(consola)
    ruta_origen = Prompt.ask("Ruta de origen", console=consola)
    ruta_destino = Prompt.ask("Ruta de destino", console=consola)


if __name__ == "__main__":
    main()
