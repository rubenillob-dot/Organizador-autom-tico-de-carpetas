# Módulo: Programación en Python (optativo) - CFGS en Desarrollo de Aplicaciones Multiplataforma
## Práctica evaluable: Organizador automático de carpetas

**Resultado de aprendizaje evaluado:**
RA3. Escribe código utilizando programación modular. Conoce la diferencia entre el paso de parámetros por valor y por referencia.

*   **Lenguaje de referencia:** Python 3
*   **Librería externa requerida:** `rich`
*   **Otras librerías utilizadas:** `os` y `shutil` (módulos de la biblioteca estándar de Python; no requieren instalación adicional).

---

## 1. Enunciado

Crea un programa en Python que automatice la organización de los archivos de una carpeta.

El programa pedirá al usuario una carpeta de origen y una carpeta de destino, y moverá a la carpeta de destino todos los archivos de la carpeta de origen, incluidos los que estén dentro de subcarpetas (a cualquier nivel de profundidad), clasificándolos en subcarpetas de la carpeta de destino según su extensión (por ejemplo, todas las imágenes JPG en una subcarpeta `jpg`, todos los documentos PDF en `pdf`, etc.). 

Al terminar, generará un pequeño informe con el número de archivos movidos, el espacio total que ocupan (mostrado en una unidad legible: bytes, KB, MB o GB según corresponda), cuántos archivos quedan en la carpeta de origen y cuántos hay en total en la carpeta de destino.

Toda la interacción con el usuario (cabecera del programa, petición de datos, avisos de error, seguimiento de la clasificación e informe final) debe presentarse mediante una consola enriquecida creada con la librería **`rich`**: texto en colores, paneles y tablas.

El programa debe resolverse mediante funciones definidas por el programador, cada una con una responsabilidad concreta, aplicando lo estudiado en esta unidad sobre paso de parámetros y sobre recursividad. Las funciones que calculan o actúan sobre los archivos no deben mostrar nada por pantalla: solo devuelven resultados o modifican sus parámetros; la presentación con `rich` se encarga a otras funciones y al programa principal.

---

## 2. Requisitos funcionales y técnicos

El programa debe cumplir, como mínimo, los siguientes requisitos:

1.  **Consola y cabecera.** Al inicio del programa se debe crear un único objeto `Console` (`from rich.console import Console`), que se utilizará en lugar de `print()` para toda la salida por pantalla. Mediante una función `mostrar_cabecera(consola)` se mostrará el título del programa dentro de un `Panel`.
2.  **Carpetas de origen y de destino.** El programa debe pedir por teclado, utilizando `Prompt.ask()` (`from rich.prompt import Prompt`) con un texto de petición en color, la ruta de la carpeta de origen y la ruta de la carpeta de destino. Antes de continuar deben realizarse tres comprobaciones y, si alguna falla, el programa debe avisar con un mensaje en rojo (por ejemplo, dentro de un `Panel` con `border_style="red"`) y finalizar sin dar error:
    *   La carpeta de origen debe existir y ser una carpeta (`os.path.isdir()`).
    *   Si la ruta de destino ya existe, debe ser una carpeta (`os.path.isdir()`); si no existe, se creará automáticamente al clasificar el primer archivo.
    *   La carpeta de origen y la de destino no pueden ser la misma ni estar una dentro de la otra, para evitar volver a procesar archivos ya clasificados.
3.  **Función `obtener_extension(nombre_archivo)`.** Debe devolver, en minúsculas y sin el punto, la extensión de un nombre de archivo (por ejemplo, `"Informe.PDF"` $\rightarrow$ `"pdf"`), apoyándose en `os.path.splitext()`. Si el archivo no tiene extensión, debe devolver el texto `"sin_extension"`.
4.  **Función `tamano_legible(tamano_bytes)`.** Debe resolver un problema de cálculo elemental: convertir un tamaño en bytes a la unidad más adecuada (bytes, KB, MB o GB), dividiendo sucesivamente entre 1024 mientras el valor lo permita, y devolver el resultado como una cadena de texto ya formateada (por ejemplo, `"2.35 MB"`). El cálculo debe programarse a mano: no se puede usar `rich.filesize` ni utilidades automáticas.
5.  **Función `una_dentro_de_otra(ruta_a, ruta_b)`.** Debe devolver `True` si las dos rutas son la misma carpeta o si una de ellas está dentro de la otra, y `False` en caso contrario. Se comparan las rutas absolutas (`os.path.abspath()`) a las que se les añade `os.sep` al final, y se usa `.startswith()` en ambos sentidos.
6.  **Función `nombre_disponible(ruta_destino, nombre_archivo)`.** Debe devolver un nombre que no exista todavía en `ruta_destino`. Si `nombre_archivo` ya existe, se probará con `nombre_1.ext`, `nombre_2.ext`, etc. (separando nombre y extensión con `os.path.splitext()` y comprobando con `os.path.exists()` dentro de un bucle `while`), hasta encontrar uno libre.
7.  **Función `clasificar_archivo(ruta_origen, nombre_archivo, ruta_destino, historial)`.** Debe mover un archivo a la subcarpeta correspondiente según su extensión, obteniendo un nombre libre con `nombre_disponible()` y moviendo el archivo con `shutil.move()`. Además, debe añadir a `historial` mediante `append()` un texto que describa el movimiento. El parámetro `historial` debe ser una lista modificada por referencia. La función devolverá con `return` el tamaño en bytes del archivo movido.
8.  **Función recursiva `clasificar_carpeta_recursivo(ruta_origen, ruta_destino, historial)`.** Debe recorrer la carpeta de origen y todas sus subcarpetas, a cualquier profundidad, clasificando todos los archivos que encuentre usando un bucle `for` con `os.listdir()`. Cuando sea subcarpeta, se llamará a sí misma. No se puede usar `os.walk()`.
9.  **Función recursiva `contar_archivos_recursivo(ruta)`.** Debe recorrer una carpeta y todas sus subcarpetas, devolviendo el número total de archivos que contiene (sin `os.walk()`).
10. **Programa principal e informe final con tablas.** El programa principal pedirá las carpetas, creará la lista `historial` y llamará a `clasificar_carpeta_recursivo()`. Al terminar, el informe se mostrará mediante `mostrar_informe(...)`, construyendo tablas de `rich.table.Table`.
11. **Separación entre cálculo y presentación.** Solo las funciones de presentación y el programa principal pueden utilizar `rich`.
12. **Documentación del código.** El archivo debe incluir un *docstring* de módulo, un *docstring* en cada función definida, y comentarios en los bloques principales.

### Restricciones importantes
*   **No se puede usar `os.walk()`** ni utilidades automáticas de recursividad.
*   **La librería `rich` no puede sustituir los cálculos** (no usar `rich.filesize` ni `rich.tree`).
*   **El objeto `Console` se creará una sola vez** y se pasará como parámetro.

---

## 3. Entrega

1. Crear un proyecto en el IDE (VS Code), con su propio entorno virtual, e instalar `rich` (`pip install rich`).
2. Crear el fichero `requirements.txt`.
3. Crear una carpeta de pruebas independiente con varios archivos y subcarpetas.
4. Probar el programa con varios casos de uso distintos (incluyendo casos límite).
5. Realizar el desarrollo utilizando tu propio repositorio en GitHub.
6. La entrega se realizará en el Aula Virtual indicando la URL de GitHub y adjuntando un vídeo de demostración.

### 3.1. Condiciones relativas a la entrega
1. Trabajo individual.
2. Desarrollo supervisado en el aula.
3. Defensa oral breve ante el profesor.
4. Historial de desarrollo (GitHub).
5. Comprobación de similitud entre entregas.
6. Uso de asistentes de IA generativa no autorizado para escribir el código principal.

---

## 4. Rúbrica de evaluación

### 4.1. Requisitos previos de entrega (obligatorios)

| Cód. | Requisito | Cumple |
|---|---|---|
| **E1** | URL de GitHub accesible con el código. | Sí / No |
| **E2** | Repositorio contiene `requirements.txt` y el programa funciona. | Sí / No |
| **E3** | Historial de commits refleja desarrollo incremental. | Sí / No |
| **E4** | Carpeta de pruebas pedida creada correctamente. | Sí / No |
| **E5** | Vídeo adjunto con las cuatro ejecuciones solicitadas. | Sí / No |
| **E6** | Superación de la defensa oral. | Sí / No |
| **E7** | Condiciones de autoría cumplidas. | Sí / No |

*(Para el detalle completo de la rúbrica de corrección, revisa las tablas detalladas de los apartados 4.2 a 4.5 en el documento original).*