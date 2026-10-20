"""Modulo con funciones para la organización de archivos"""

import os


def una_dentro_de_otra(ruta_a, ruta_b):
    """Comprueba si dos rutas son la misma carpeta o si una está dentro de la otra

    Convierte las rutas a absolutas y añade el separador del sistema
    """
    abs_a = os.path.abspath(ruta_a)
    if not abs_a.endswith(os.sep):
        abs_a += os.sep

    abs_b = os.path.abspath(ruta_b)
    if not abs_b.endswith(os.sep):
        abs_b += os.sep

    return abs_a.startswith(abs_b) or abs_b.startswith(abs_a)
