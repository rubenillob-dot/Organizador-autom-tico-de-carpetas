"""Módulo principal del organizador automático de carpetas."""

import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from utils import (
    una_dentro_de_otra,
    tamano_legible,
    clasificar_carpeta_recursivo,
    contar_archivos_recursivo,
)

consola = Console()


def mostrar_cabecera(consola):
    """Muestra el título del programa dentro de un panel azul."""
    consola.print(Panel("Organizador de Carpetas", border_style="blue"))


def validar_rutas(origen, destino, consola):
    """ Comprueba que:
    La carpeta de origen exista y sea un directorio ,si el destino existe, sea un directorio y ninguna de las dos carpetas esté dentro de la otra ni sean la misma

    """
    # Compruebo que la carpeta de origen existe y es un directorio
    if not os.path.isdir(origen):
        consola.print(
            Panel("La carpeta de origen no existe o no es un directorio.", border_style="red")
        )
        return False

    # Si la ruta de destino existe compruebo que sea una carpeta
    if os.path.exists(destino) and not os.path.isdir(destino):
        consola.print(
            Panel("La ruta de destino existe pero no es una carpeta.", border_style="red")
        )
        return False

    # Compruebo que las carpetas no sean la misma ni una contenga a la otra
    if una_dentro_de_otra(origen, destino):
        consola.print(
            Panel(
                "La carpeta de origen y la de destino no pueden ser la misma ni estar una dentro de la otra.",
                border_style="red",
            )
        )
        return False

    return True


def mostrar_informe(historial, bytes_movidos, archivos_origen, archivos_destino, consola):
    """Muestro el informe final con los resultados de la organización"""
    tabla = Table(title="Resumen del proceso")
    tabla.add_column("Concepto")
    tabla.add_column("Valor")


def main():
    """Punto de entrada principal del programa."""
    mostrar_cabecera(consola)
    ruta_origen = Prompt.ask("Ruta de origen", console=consola)
    ruta_destino = Prompt.ask("Ruta de destino", console=consola)

    if not validar_rutas(ruta_origen, ruta_destino, consola):
        return

    historial_movimientos = []
    bytes_movidos = clasificar_carpeta_recursivo(ruta_origen, ruta_destino, historial_movimientos)
    archivos_origen = contar_archivos_recursivo(ruta_origen)
    archivos_destino = contar_archivos_recursivo(ruta_destino)



if __name__ == "__main__":
    main()
