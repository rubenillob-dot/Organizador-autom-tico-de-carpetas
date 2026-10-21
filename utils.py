"""Modulo con funciones para la organización de archivos"""

import os


def una_dentro_de_otra(ruta_a, ruta_b):
    """Compruebo si dos rutas son la misma carpeta o si una está dentro de la otra

    Convierto las rutas a absolutas y añade el separador del sistema
    """
    abs_a = os.path.abspath(ruta_a)
    if not abs_a.endswith(os.sep):
        abs_a += os.sep

    abs_b = os.path.abspath(ruta_b)
    if not abs_b.endswith(os.sep):
        abs_b += os.sep

    return abs_a.startswith(abs_b) or abs_b.startswith(abs_a)


def obtener_extension(archivo):
    """Devuelvo la extensión de un archivo en minúsculas y sin el .
    Si el archivo no tiene extensión, devuelve 'sin_extension'
    """
    _, extension = os.path.splitext(archivo)

    # Si no tiene extensión devuelvo 'sin_extension'
    if not extension or extension == ".":
        return "sin_extension"

    return extension.lstrip(".").lower()


def tamano_legible(tamano_bytes):
    """Convierto un tamaño en bytes a una unidad legible (bytes, KB, MB o GB)
    dividiendo entre 1024 mediante un bucle while
    """
    unidades = ["bytes", "KB", "MB", "GB"]
    tamano = float(tamano_bytes)
    indice = 0

    while tamano >= 1024 and indice < len(unidades) - 1:
        tamano /= 1024
        indice += 1

    if indice == 0:
        return f"{int(tamano)} {unidades[0]}"
    return f"{round(tamano, 2)} {unidades[indice]}"


def nombre_disponible(destino, nombre_archivo):
    """Devuelvo un nombre de archivo que no exista en la carpeta del de destino

    Si el archivo ya existe añade un sufijo con el barrabaja antes de la extensión
    hasta encontrar un nombre libre
    """
    nombre_base, extension = os.path.splitext(nombre_archivo)
    nombre_candidato = nombre_archivo
    contador = 1

    while os.path.exists(os.path.join(destino, nombre_candidato)):
        nombre_candidato = f"{nombre_base}_{contador}{extension}"
        contador += 1

    return nombre_candidato

