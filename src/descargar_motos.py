#datatime es la herramienta para trabajar con fechas y horas. Path es la herramienta para trabajar con rutas de archivos.
from datetime import date
from pathlib import Path

import requests

URL = "https://datos.jus.gob.ar/api/3/action/package_show?id=estadistica-de-tramites-de-motovehiculos"

#path (_file_) es la ruta del archivo actual (misma que explorar_api.py). resolve() convierte la ruta relativa en absoluta. parent.parent sube dos niveles en la ruta.
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
# CARPETA_DESTINO es la ruta donde se guardarán los archivos descargados. date.today().isoformat() devuelve la fecha de hoy en formato YYYY-MM-DD.
CARPETA_DESTINO = CARPETA_PROYECTO / "data" / "raw" / "motos" / date.today().isoformat()

respuesta = requests.get(URL, timeout=30)
# controlar si la respuesta fue exitosa del pedido de la linea anterior. Si no, lanza una excepción y termina el programa.
respuesta.raise_for_status()
datos = respuesta.json()

#mkdir(parents=True, exist_ok=True) crea la carpeta destino y todas las carpetas intermedias si no existen. exist_ok=True significa que si la carpeta ya existe, no lanza un error.
CARPETA_DESTINO.mkdir(parents=True, exist_ok=True)

for recurso in datos["result"]["resources"]:
    #filtro con if para que solo descargue los archivos CSV. continue salta a la siguiente iteración del bucle.
    if recurso["format"] != "CSV":
        # continue salta a la siguiente iteración del bucle, es decir, no ejecuta el resto del código dentro del bucle para este recurso y pasa al siguiente recurso.
        continue

# sino se cumple la condición del if, se ejecuta el resto del código dentro del bucle para este recurso. Se guarda el nombre del archivo y la ruta donde se guardará.
# recurso["url"].split("/")[-1],corta la url por los "/" y toma el último elemento, que es el nombre del archivo. CARPETA_DESTINO / nombre_archivo, une la carpeta destino con el nombre del archivo para obtener la ruta completa donde se guardará el archivo.
    nombre_archivo = recurso["url"].split("/")[-1]
    ruta_archivo = CARPETA_DESTINO / nombre_archivo

# idempotencia: si el archivo ya existe, no se vuelve a descargar. Esto evita descargar el mismo archivo varias veces si se ejecuta el script varias veces en el mismo día.
    if ruta_archivo.exists():
        print("Ya existe, se omite:", nombre_archivo)
        continue

# descargar el archivo y guardarlo en la ruta destino. timeout=120 significa que si la respuesta tarda más de 120 segundos, se corta la conexión. raise_for_status() lanza una excepción si la respuesta no fue exitosa.
    print("Descargando:", nombre_archivo)
    descarga = requests.get(recurso["url"], timeout=120)
    descarga.raise_for_status()
    ruta_archivo.write_bytes(descarga.content) # write_bytes() guarda el contenido del archivo descargado en la ruta destino. descarga.content es el contenido del archivo descargado en bytes.
    print("Guardado:", ruta_archivo, f"({len(descarga.content):,} bytes)") #f"({len(descarga.content):,} bytes)" formatea el tamaño del archivo con comas como separador de miles.