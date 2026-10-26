"""Modulo con funciones para la organización de archivos"""

import os
import shutil


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


def clasificar_archivo(ruta_origen, nombre_archivo, ruta_destino, historial):
    """Clasifico y muevo un archivo a la subcarpeta según su extensión

    Creo la subcarpeta con os.makedirs si no existe, busco un nombre libre
    para no sobreescribir, muevo el archivo y añado el movimiento al historial
    """
    ruta_archivo_origen = os.path.join(ruta_origen, nombre_archivo)
    tamano = os.path.getsize(ruta_archivo_origen)

    # Obtengo la extensión y la ruta de la subcarpeta destino
    extension = obtener_extension(nombre_archivo)
    carpeta_extension = os.path.join(ruta_destino, extension)
    if not os.path.exists(carpeta_extension):
        os.makedirs(carpeta_extension)

    
    nombre_libre = nombre_disponible(carpeta_extension, nombre_archivo)
    ruta_archivo_destino = os.path.join(carpeta_extension, nombre_libre)

    shutil.move(ruta_archivo_origen, ruta_archivo_destino)

    destino_nuevo = os.path.join(extension, nombre_libre)
    historial.append(f"{nombre_archivo} a {destino_nuevo}")

    return tamano


def clasificar_carpeta_recursivo(origen, destino, historial):
    """Recorro de forma recursiva una carpeta y clasifico todos sus archivos
    Si es una subcarpeta me llamo a mí misma y si es un
    archivo lo clasifico y sumo su tamaño en bytes
    """
    bytes_movidos = 0

    for elemento in os.listdir(origen):
        ruta_elemento = os.path.join(origen, elemento)

        if os.path.isdir(ruta_elemento):
            bytes_movidos += clasificar_carpeta_recursivo(ruta_elemento, destino, historial)
        elif os.path.isfile(ruta_elemento):
            bytes_movidos += clasificar_archivo(origen, elemento, destino, historial)

    return bytes_movidos
