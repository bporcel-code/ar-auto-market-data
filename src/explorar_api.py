#traer la caja herramienta.
import requests
#guargar la dirección de la API en una variable.
URL = "https://datos.jus.gob.ar/api/3/action/package_show?id=estadistica-de-tramites-de-motovehiculos"

#Hacer el pedido a la API y guardar la respuesta en una variable. timeout=30 significa que si la respuesta tarda más de 30 segundos, se corta la conexión.
respuesta = requests.get(URL,timeout=30)
#respuesta.status_code es el codigo de estado de la respuesta. 200 significa bien, 404 no existe, 500 error del servidor, etc.
print("código de estado:",respuesta.status_code)

#respuesta.json() convierte la respuesta en un diccionario de Python.
datos = respuesta.json()

#datos["success"] saca el valor de la clave "success" del diccionario datos. Si es True, significa que la API respondió correctamente.
print("¿Funcionó?:", datos['success'])

#Bucle repite el código para cada recurso en la lista de recursos que está dentro del diccionario datos.
for recurso in datos ["result"]["resources"]:
    #nombre del recurso o formato y su url.
    print(recurso["format"], "|", recurso["name"])

    