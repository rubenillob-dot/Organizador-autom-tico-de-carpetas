# Organizador Automático de Carpetas

Práctica evaluable para el módulo de Programación en Python (CFGS Desarrollo de Aplicaciones Multiplataforma).


## Descripción del proyecto

Este programa es una herramienta de terminal desarrollada en Python diseñada para automatizar la organización y limpieza de directorios.

A partir de una carpeta de origen indicada por el usuario, el script localiza todos los archivos existentes —incluidos aquellos alojados en cualquier nivel de subcarpetas— y los traslada a una carpeta de destino, agrupándolos de forma ordenada en subcarpetas según su formato o extensión (por ejemplo, `jpg`, `pdf`, `txt`, etc.).

Al finalizar el proceso, la aplicación presenta un balance completo con estadísticas sobre los ficheros procesados y el espacio total gestionado.


## Características principales

- Interfaz visual en consola: Toda la interacción con el usuario (cabecera, petición de rutas, advertencias de error y tabla de resultados) se realiza mediante paneles y colores utilizando la librería `rich`.

- Validaciones de seguridad: Antes de mover archivos, el programa verifica que las rutas existan y comprueba que la carpeta de origen y la de destino no coincidan ni estén anidadas entre sí, evitando bucles o pérdidas de datos.

- Exploración recursiva propia: El recorrido del árbol de directorios y el conteo de archivos se realiza mediante funciones recursivas programadas a medida, sin recurrir a utilidades automáticas como `os.walk`.

- Control de colisiones de nombres: Si en el destino ya existe un archivo con el mismo nombre, el programa le asigna automáticamente un sufijo numérico (`archivo_1.ext`, `archivo_2.ext`, etc.) para evitar sobrescrituras accidentales.

- Conversión manual de tamaños: El cálculo de bytes a unidades legibles (bytes, KB, MB, GB) se realiza mediante un algoritmo propio de divisiones sucesivas, sin emplear librerías de formateo automático.

- Tratamiento de archivos sin extensión: Aquellos ficheros que carecen de extensión se clasifican de forma segura en una subcarpeta denominada `sin_extension`.

- Separación de responsabilidades: La lógica que opera con el sistema de archivos (`os`, `shutil`) está desacoplada de las funciones de presentación visual (`rich`).


## Requisitos del sistema

- Python 3.10 o superior.
- Módulos de la biblioteca estándar de Python: `os`, `shutil`.
- Librerías externas: `rich`.


## Instalación

1. Clonar el repositorio o descargar los archivos del proyecto:

```bash
git clone <url-del-repositorio>
cd Organizador-autom-tico-de-carpetas
```

2. Crear y activar un entorno virtual (opcional pero recomendado):

```bash
python3 -m venv env
source env/bin/activate    # En Linux / macOS
# En Windows: env\Scripts\activate
```

3. Instalar las dependencias necesarias:

```bash
pip install -r requirements.txt
```


## Uso

Para iniciar el organizador, ejecuta el archivo principal:

```bash
python main.py
```

Durante la ejecución, el programa solicitará por consola:
1. Ruta de la carpeta de origen.
2. Ruta de la carpeta de destino (si no existe, se creará automáticamente al transferir el primer archivo).

Una vez completada la clasificación, la terminal mostrará un informe final detallado con el historial de movimientos, número total de archivos transferidos, tamaño total gestionado y el balance de archivos en las carpetas de origen y destino.


## Estructura del repositorio

- `main.py`: Script principal con la lógica modular y la interfaz por consola.
- `requirements.txt`: Archivo de dependencias del proyecto (`rich`).
- `Enunciado.md`: Especificación técnica y rúbrica detallada de la práctica.
- `README.md`: Documentación del proyecto.
