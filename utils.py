"""Funciones auxiliares para la organización de archivos.

Aquí guardo las funciones para validar rutas, sacar extensiones,
convertir tamaños a unidades legibles, evitar que se sobrescriban
archivos repetidos y recorrer las carpetas de forma recursiva para
clasificar y contar los archivos.
"""

import os
import shutil


def una_dentro_de_otra(ruta_a, ruta_b):
    """Compruebo si dos rutas son la misma carpeta o si una está metida dentro de la otra.

    Convierto las rutas a absolutas y les añado la barra final para comparar si coinciden.

    Args:
        ruta_a (str): Primera ruta a comprobar.
        ruta_b (str): Segunda ruta a comprobar.

    Returns:
        bool: True si son la misma carpeta o una contiene a la otra, False si son independientes.
    """
    abs_a = os.path.abspath(ruta_a)
    if not abs_a.endswith(os.sep):
        abs_a += os.sep

    abs_b = os.path.abspath(ruta_b)
    if not abs_b.endswith(os.sep):
        abs_b += os.sep

    return abs_a.startswith(abs_b) or abs_b.startswith(abs_a)


def obtener_extension(archivo):
    """Saco la extensión de un archivo en minúsculas y sin el punto inicial.

    Si el archivo no tiene ninguna extensión, devuelvo 'sin_extension'.

    Args:
        archivo (str): Nombre o ruta del archivo.

    Returns:
        str: La extensión limpia en minúsculas (por ejemplo 'txt', 'png') o 'sin_extension'.
    """
    _, extension = os.path.splitext(archivo)

    # Si no tiene extensión devuelvo 'sin_extension'
    if not extension or extension == ".":
        return "sin_extension"

    return extension.lstrip(".").lower()


def tamano_legible(tamano_bytes):
    """Paso un tamaño en bytes a un formato fácil de leer (bytes, KB, MB o GB).

    Voy dividiendo entre 1024 en un bucle while hasta dar con la unidad adecuada.

    Args:
        tamano_bytes (int | float): Tamaño del archivo en bytes.

    Returns:
        str: Cadena formateada con el valor redondeado y su unidad (por ejemplo '2.5 MB').
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
    """Busco un nombre que no exista todavía en la carpeta de destino para no sobrescribir nada.

    Si el nombre ya está pillado, le voy añadiendo sufijos como '_1', '_2', etc., antes de la extensión.

    Args:
        destino (str): Carpeta donde se va a guardar el archivo.
        nombre_archivo (str): Nombre original del archivo que queremos mover.

    Returns:
        str: Nombre final disponible para usar sin machacar otro archivo.
    """
    nombre_base, extension = os.path.splitext(nombre_archivo)
    nombre_candidato = nombre_archivo
    contador = 1

    while os.path.exists(os.path.join(destino, nombre_candidato)):
        nombre_candidato = f"{nombre_base}_{contador}{extension}"
        contador += 1

    return nombre_candidato


def clasificar_archivo(ruta_origen, nombre_archivo, ruta_destino, historial):
    """Muevo un archivo a su subcarpeta correspondiente según su extensión.

    Crea la subcarpeta si hace falta, busca un nombre que no colisione,
    mueve el fichero con shutil, anota la acción en el historial y devuelve lo que ocupaba.

    Args:
        ruta_origen (str): Carpeta donde está el archivo actualmente.
        nombre_archivo (str): Nombre del archivo a mover.
        ruta_destino (str): Carpeta destino principal donde se organizará.
        historial (list): Lista donde voy guardando los movimientos realizados.

    Returns:
        int: Tamaño en bytes del archivo que se ha movido.
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
    """Recorro una carpeta entera de forma recursiva clasificando todos los archivos que encuentre.

    Si encuentro una subcarpeta me vuelvo a llamar a mí misma con esa ruta,
    y si es un archivo lo clasifico y voy sumando los bytes que ocupa.

    Args:
        origen (str): Ruta de la carpeta que quiero organizar.
        destino (str): Ruta de la carpeta donde se van a mover clasificados.
        historial (list): Lista donde se va registrando cada movimiento.

    Returns:
        int: Total de bytes movidos en todo el proceso.
    """
    bytes_movidos = 0

    for elemento in os.listdir(origen):
        ruta_elemento = os.path.join(origen, elemento)

        if os.path.isfile(ruta_elemento):
            bytes_movidos += clasificar_archivo(origen, elemento, destino, historial)
        elif os.path.isdir(ruta_elemento):
            bytes_movidos += clasificar_carpeta_recursivo(ruta_elemento, destino, historial)

    return bytes_movidos


def contar_archivos_recursivo(ruta):
    """Recorro una carpeta y todas sus subcarpetas para contar cuántos archivos contiene en total.

    Si encuentro una subcarpeta hago una llamada recursiva, y si es un archivo sumo 1.

    Args:
        ruta (str): Ruta de la carpeta a inspeccionar.

    Returns:
        int: Número total de archivos encontrados en la carpeta y subcarpetas.
    """
    if not os.path.exists(ruta) or not os.path.isdir(ruta):
        return 0

    total_archivos = 0

    for elemento in os.listdir(ruta):
        ruta_elemento = os.path.join(ruta, elemento)

        if os.path.isfile(ruta_elemento):
            total_archivos += 1
        elif os.path.isdir(ruta_elemento):
            total_archivos += contar_archivos_recursivo(ruta_elemento)

    return total_archivos
