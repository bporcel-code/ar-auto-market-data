# 03 — Primera ingesta con Python, debugging y versiones con Git

> Sesiones: 11-12 de octubre de 2026 · Proyecto: `ar-auto-market-data`
> Resultado: entorno virtual, script de descarga idempotente de los datos de motos (DNRPA), ADR-001 y primera versión `v0.1.0`.

---

## 1. Entorno virtual (`venv`)

**Qué es:** una caja de herramientas propia del proyecto. Las librerías que se instalan ahí no se mezclan con las de otros proyectos (por ejemplo, PWOS).

| Comando | Qué hace |
|---|---|
| `python -m venv .venv` | Crea el entorno en la carpeta `.venv` (ignorada en `.gitignore`) |
| `.venv\Scripts\Activate.ps1` | Lo activa. Aparece `(.venv)` al principio de la línea |
| `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` | Una sola vez, si Windows bloquea la activación |
| VS Code: `Ctrl+Shift+P` → *Python: Select Interpreter* → `.venv` | Para que VS Code use ese entorno |

**Regla:** cada vez que se abre el proyecto, activar el entorno. Sin `(.venv)` se está usando el Python general de la PC.

## 2. Librerías y `requirements.txt`

- **Librería:** herramientas extra escritas por otras personas que se instalan cuando hacen falta.
- `pip install requests` → instala la librería.
- `pip freeze | Set-Content -Encoding utf8 requirements.txt` → guarda la **receta** del entorno, con las versiones exactas.
- Otra persona recrea el entorno con `pip install -r requirements.txt` → **reproducibilidad**.
- `Set-Content -Encoding utf8` evita el problema de UTF-16 de PowerShell.

## 3. `requests`: hablar con internet desde Python

```python
respuesta = requests.get(URL, timeout=30)
respuesta.raise_for_status()
datos = respuesta.json()
```

| Parte | Qué hace |
|---|---|
| `requests.get(URL)` | Hace el pedido, igual que pegar la URL en Chrome |
| `timeout=30` | Si en 30 segundos no responde, corta. Sin esto el programa podría esperar para siempre |
| `respuesta.status_code` | **200** = OK · **404** = no existe · **500** = error del servidor |
| `respuesta.raise_for_status()` | **Control de calidad:** si el código es de error (4xx o 5xx), frena el programa con un mensaje claro. Si es 200, no hace nada |
| `respuesta.json()` | Convierte el JSON en un **diccionario** de Python |

**Principio:** *fail fast*. Es mejor que un pipeline falle con un error claro a que siga funcionando con datos malos.

## 4. Conceptos de Python que aparecieron

| Concepto | Ejemplo | Qué es |
|---|---|---|
| `import` | `import requests`, `from pathlib import Path` | Traer herramientas |
| Variable / constante | `URL = "..."` | Un nombre que guarda un valor. En mayúsculas si no cambia |
| Diccionario | `datos["result"]["resources"]` | Datos con etiquetas. Se accede por clave, como abrir un cajón por su nombre |
| Bucle `for` | `for recurso in recursos:` | Repite el bloque para cada elemento de la lista |
| **Sangría** | 4 espacios | Le indica a Python qué líneas están dentro del bucle o del `if`. No es estética |
| `if` / `!=` | `if recurso["format"] != "CSV":` | Condición. `!=` = "distinto de" |
| `continue` | dentro del `for` | Saltear este elemento y pasar al siguiente |
| `.split("/")[-1]` | sobre la URL | Cortar un texto en partes y quedarse con la última |
| f-string | `f"({len(x):,} bytes)"` | Texto con cálculos adentro de `{}`. `:,` agrega separadores de miles |

## 5. Rutas de archivo con `pathlib`

```python
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_DESTINO = CARPETA_PROYECTO / "data" / "raw" / "motos" / date.today().isoformat()
CARPETA_DESTINO.mkdir(parents=True, exist_ok=True)
```

- `__file__` = la ruta del propio script. Cada `.parent` sube una carpeta.
- La `/` entre `Path` **une carpetas**, igual en Windows y en Linux.
- **Por qué:** el script se corre desde `src/`. Con rutas relativas (`data/raw`) crearía las carpetas en el lugar equivocado. Calculando desde `__file__`, funciona desde cualquier carpeta.
- `mkdir(parents=True, exist_ok=True)` crea las carpetas intermedias y no da error si ya existen.

## 6. Idempotencia y raw inmutable

```python
if ruta_archivo.exists():
    print("Ya existe, se omite:", nombre_archivo)
    continue
...
ruta_archivo.write_bytes(descarga.content)
```

- **Idempotente:** correr el script dos veces da el mismo resultado y no duplica nada.
- **Cómo se prueba:** corriéndolo dos veces. La segunda vez dice "Ya existe, se omite".
- `write_bytes` guarda el archivo **tal cual llegó**, sin interpretarlo → capa raw **inmutable**.

## 7. Cómo leer un error (traceback)

1. **De abajo hacia arriba:** la última línea dice qué falló (`JSONDecodeError`).
2. **Buscar la línea de tu código** entre las de las librerías (`explorar_api.py, line 12`).
3. **Buscar la causa, no el síntoma:** el `404` de más arriba. La URL estaba mal escrita, el servidor devolvió una página de error HTML y por eso falló la lectura del JSON.

> Es como el testigo de check engine: el testigo no es la falla, te avisa que hay una.

## 8. Explorar antes de programar

- Primero **imprimir el dato** (`print(recurso["format"])`) y **después** escribir la condición (`!= "CSV"`).
- En Python, `"CSV"` y `"csv"` son distintos.
- La API devolvió 4 recursos: 2 CSV (sirven), 1 ZIP (duplicado) y 1 Tableau (página web).

## 9. Primer perfilado del CSV de motos

- **Grano:** año × mes × provincia.
- `provincia_id` viene **entre comillas** (`"06"`): es **texto**. Leído como número perdería el cero, como el bug de Ecovalores en PWOS.
- Para unir con otras fuentes, el **código** de provincia es más confiable que el nombre.
- El archivo trae **toda la historia** (2007 → hoy) y su nombre cambia cada mes → decisión de diseño (ADR-001).

## 10. ADR-001: raw versionado y retención

- Una carpeta por **fecha de descarga**: `data/raw/motos/2026-10-12/`.
- Se conservan las **últimas 12 descargas** (*política de retención*). Pendiente de implementar.
- **Motivo:** si la fuente corrige el pasado, se puede ver qué cambió.

## 11. Git: commits separados, deshacer y versiones

### Prefijos (Conventional Commits)
| Prefijo | Uso |
|---|---|
| `feat:` | Funcionalidad nueva |
| `fix:` | Corrección de un error |
| `docs:` | Solo documentación |
| `chore:` | Mantenimiento (dependencias, configuración) |
| `refactor:` | Reordenar el código sin cambiar lo que hace |
| `test:` | Pruebas |

Si un cambio mezcla tipos → **dividirlo en varios commits**.

### Separar commits
```
git add <archivo>  →  git status (en verde solo eso)  →  git commit -m "..."
```
Repetir por cada grupo. Al final, **un solo** `git push`.

### Deshacer
| Comando | Qué hace |
|---|---|
| `git reset --soft HEAD~N` | Deshace los últimos N commits **conservando los cambios**. Solo antes del push |
| `git restore --staged <archivo>` o `.` | Saca de la caja sin perder nada |
| ⚠️ `git reset --hard` | **Borra los cambios.** No usar |

Lo que ya está subido a GitHub **no se reescribe**.

### Versiones (tags)
| Comando | Qué hace |
|---|---|
| `git tag -a v0.1.0 -m "..."` | Pega la "oblea del service" sobre el último commit (en la PC) |
| `git push origin v0.1.0` | Sube la etiqueta. `git push` común **no** sube tags |
| `git tag` | Lista las etiquetas |

**Versionado semántico:** `vMAYOR.MENOR.PARCHE`. Mientras está en construcción, `0.x`.

### Leer el historial
```
commit 5f26909... (HEAD -> main, tag: v0.1.0, origin/main)
```
- `HEAD -> main` = dónde estás parado.
- `tag: v0.1.0` = la etiqueta está sobre este commit.
- `origin/main` = GitHub está en el mismo commit → todo subido.

### Otros
- Git **desde la raíz del proyecto**: desde `src/` muestra rutas relativas (`../`, `./`).
- **Tab** autocompleta nombres de archivo y evita errores de tipeo (`requeriment.txt`).
- `LF will be replaced by CRLF`: aviso inofensivo por los finales de línea de Windows y Linux.

## 12. Errores de esta etapa

| Error | Causa | Lección |
|---|---|---|
| `404` + `JSONDecodeError` | URL mal tipeada | Leer el traceback buscando la causa. Usar `raise_for_status()` |
| `pathspec 'requeriment.txt' did not match` | Error de tipeo en el nombre | Usar Tab para autocompletar |
| Mezclar `feat` y `chore` en un commit | `add` de varias cosas juntas | `add` por grupo + `git status` antes de cada commit |
| Saltearse el `git restore --staged .` | Todo seguía en la caja | Verificar con `git status` que el estado sea el esperado |

## 13. Próximo paso

**Perfilado con Python:** cantidad de filas, las 24 provincias, meses faltantes, valores vacíos o negativos y duplicados por mes y provincia.
