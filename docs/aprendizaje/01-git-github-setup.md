# 01 — Repositorio, Git y GitHub desde cero

> Sesión: 3-4 de octubre de 2026 · Proyecto: `ar-auto-market-data`
> Resultado: repo creado en la carpeta correcta, primer commit (`3a58ce5`) y publicado en GitHub.

---

## 1. Conceptos clave

**Repositorio (repo):** una carpeta cuyo historial controla Git. Ese historial vive en una carpeta oculta llamada `.git`.

**Commit:** una "foto" guardada del proyecto en un momento dado. Cada commit tiene:
- un **hash**, que es su número de serie único (por ejemplo, `3a58ce5`);
- un **mensaje** que describe qué cambió.

Con el hash se puede volver a esa foto o deshacerla.

**Local vs. remoto:**
- *Local:* el repo en mi PC.
- *Remoto:* la copia en GitHub. Por convención se llama `origin`.

### Las tres zonas de Git

```
 MI CARPETA               ZONA DE PREPARACIÓN        HISTORIAL                GITHUB
 (working directory)      (staging area)             (repositorio local)      (remoto)
 ┌──────────────┐  add   ┌──────────────┐  commit  ┌──────────────┐  push  ┌────────┐
 │ archivos que │ ─────→ │ lo que va en │ ───────→ │ fotos        │ ─────→ │ origin │
 │ estoy        │        │ el próximo   │          │ guardadas    │        │        │
 │ editando     │        │ commit       │          │              │        │        │
 └──────────────┘        └──────────────┘          └──────────────┘        └────────┘
```

### Analogía logística

| Paso | Logística | Git |
|---|---|---|
| Trabajar | Mercadería en el depósito | Editar archivos |
| `git add` | Elegir qué productos van en esta caja | Elegir qué cambios van en el commit |
| `git commit` | Cerrar la caja, etiquetarla, hacer el remito | Guardar la foto con un mensaje |
| `git log` | Libro de despachos | Historial de commits |
| `git push` | El camión lleva las cajas al centro de distribución | Subir los commits a GitHub |

---

## 2. Estructura del proyecto (y por qué)

```
Datos Mercado Automotor/
├── data/
│   └── raw/        ← datos tal cual se descargan, nunca se modifican (capa bronze)
├── docs/           ← brief, fuentes, decisiones de diseño, notas
├── src/            ← código Python (source = código fuente)
├── .gitignore      ← lo que Git NO debe subir nunca
└── README.md       ← portada del proyecto (en inglés)
```

- **Separación:** código, datos y documentación no se mezclan. Si algo sale mal, borro lo procesado, vuelvo a `raw/` y corro `src/` de nuevo.
- **Por qué `data/` no se sube a GitHub:**
  1. Los archivos de datos son pesados.
  2. El proyecto tiene que ser *reproducible*: el código descarga los datos, no hace falta guardarlos.
- **El README siempre va:** es lo primero que ve cualquiera (por ejemplo, un reclutador) al entrar al repo.
- **¿Todo proyecto arranca así?** Casi siempre, con variantes. Existen plantillas estándar, como *Cookiecutter Data Science*.

### `.gitignore` actual

```
data/
.venv/
__pycache__/
*.db
.env
```

| Línea | Qué ignora |
|---|---|
| `data/` | Datos descargados y procesados |
| `.venv/` | Entorno virtual de Python (se recrea) |
| `__pycache__/` | Archivos temporales que genera Python |
| `*.db` | Bases de datos locales (SQLite) |
| `.env` | Contraseñas y claves. **Nunca** se suben |

---

## 3. Comandos usados

### Terminal (PowerShell)

| Comando | Qué hace |
|---|---|
| `cd "ruta"` | Moverse a una carpeta. Entre comillas si hay espacios o tildes |
| `mkdir docs, src, data\raw` | Crear carpetas (*make directory*) |
| `New-Item archivo.txt` | Crear un archivo vacío |
| `Remove-Item archivo.txt` | Borrar un archivo. **No pasa por la papelera** |
| `Remove-Item -Recurse -Force .git` | Borrar una carpeta oculta con todo su contenido |
| `Test-Path .git` | Verificar si algo existe (`True` / `False`) |

### Git

| Comando | Qué hace | Cuándo |
|---|---|---|
| `git --version` | Muestra la versión de Git instalada | Para verificar la instalación |
| `git config --global user.name "..."` | Configura mi nombre para los commits | Una sola vez por PC |
| `git config --global user.email "..."` | Configura mi email (el mismo de GitHub) | Una sola vez por PC |
| `git init` | Convierte la carpeta actual en repo (crea `.git`) | Una vez por proyecto |
| `git branch -M main` | Le pone `main` a la rama principal | Justo después de `init` |
| `git rev-parse --show-toplevel` | Muestra **en qué repo estoy realmente** | Ante cualquier duda |
| `git status` | Muestra en qué zona está cada archivo (rojo = sin preparar, verde = preparado) | **Siempre**, antes y después de cada paso |
| `git add .` | Prepara todos los cambios (menos lo ignorado) | Antes del commit |
| `git add archivo` | Prepara un solo archivo | Para hacer commits por tema |
| `git commit -m "mensaje"` | Guarda la foto con un mensaje | Después del `add` |
| `git log --oneline` | Muestra el historial, un commit por línea | Para verificar |
| `git remote add origin URL` | Conecta el repo local con GitHub | Una vez por proyecto |
| `git remote -v` | Muestra a qué remoto está conectado | Para verificar |
| `git push -u origin main` | Sube los commits y deja guardado el destino | El primer push |
| `git push` | Sube los commits nuevos | Los siguientes push |

### El ciclo de trabajo de siempre

```
editar → git status → git add → git status → git commit → git log → git push
```

### Mensajes de commit (Conventional Commits)

| Prefijo | Uso | Ejemplo |
|---|---|---|
| `feat:` | Algo nuevo | `feat: add script to count registrations by province` |
| `fix:` | Corrección | `fix: handle empty rows in csv reader` |
| `docs:` | Documentación | `docs: describe project goal and main question` |
| `chore:` | Mantenimiento o estructura | `chore: initial project structure` |

Un buen mensaje dice qué cambió en pocas palabras. ❌ `cambios`, `asdf`, `prueba`.

---

## 4. Errores que tuve (y cómo los resolví)

### Error 1 — El repo se creó en la carpeta equivocada
- **Síntoma:** el `.git` apareció en `AUTOMOCIÓN` (la carpeta de arriba), no en `Datos Mercado Automotor`.
- **Causa:** `git init` se corrió parado en la carpeta padre.
- **Riesgo:** Git busca `.git` subiendo por las carpetas. Un `git add .` hubiera subido **toda mi bóveda de automotores** (PDFs, bibliografía) a un repo público.
- **Diagnóstico antes de corregir:** `git log --oneline` respondió `does not have any commits yet` y `git remote -v` no mostró nada. Conclusión: se había creado ese mismo día y no había nada que perder.
- **Solución:** `Remove-Item -Recurse -Force .git` en la carpeta padre, después `git init` dentro del proyecto y verificación con `git rev-parse --show-toplevel`.
- **Lección:** antes del primer `add`, confirmar dónde está el repo con `git rev-parse --show-toplevel`.

### Error 2 — Espacios al principio de las líneas del `.gitignore`
- **Síntoma:** a simple vista el archivo parecía correcto.
- **Causa:** cada línea empezaba con 3 espacios (`   data/`).
- **Riesgo:** en el `.gitignore`, los espacios del principio forman parte del patrón. Git buscaba una carpeta llamada "`   data/`" y no ignoraba nada.
- **Solución:** borrar los espacios para que cada línea arranque pegada a la izquierda.
- **Verificación:** crear `data\raw\prueba.txt`, correr `git status` y comprobar que `data/` no aparezca. Después borrar el archivo de prueba.
- **Lección:** verificar el **comportamiento**, no solo el aspecto del archivo.

### Error 3 — `src refspec main does not match any`
- **Síntoma:** `git push` falló con ese mensaje.
- **Causa:** intenté hacer push sin haber hecho ningún commit. La rama `main` estaba vacía.
- **Diagnóstico:** `git log --oneline` respondió `does not have any commits yet`.
- **Solución:** hacer el commit primero y el push después. El `git remote add` ya estaba hecho, así que no había que repetirlo (si se repite, da el error `remote origin already exists`).
- **Lección:** el orden es **commit → push**. No se puede despachar una caja que no se cerró.

### Error 4 — Pegar varios comandos juntos
- **Síntoma:** en la terminal aparecía `>>` y los errores se mezclaban entre sí.
- **Causa:** pegué varios comandos a la vez. Si uno fallaba, su error quedaba escondido.
- **Solución:** **un comando a la vez → Enter → leer la respuesta → recién después el siguiente.**
- **Lección:** así fue como encontramos que el commit nunca se había guardado.

### Error 5 (evitado) — `echo` en PowerShell
- PowerShell `echo >>` guarda los archivos en UTF-16 y rompe archivos como el `.gitignore` (me pasó en PWOS).
- **Regla:** crear y editar archivos de texto desde VS Code, no con `echo`.

---

## 5. Checklist para crear un repo nuevo

1. [ ] Abrir **la carpeta del proyecto** en VS Code (no la carpeta de arriba).
2. [ ] `git init` y `git branch -M main`.
3. [ ] `git rev-parse --show-toplevel` → ¿es la carpeta correcta?
4. [ ] Crear la estructura: `data/raw`, `docs`, `src`.
5. [ ] Crear `.gitignore` y `README.md` desde VS Code.
6. [ ] Probar el `.gitignore` con un archivo dentro de `data/` y `git status`.
7. [ ] `git add .` → `git status` (verde) → `git commit -m "chore: initial project structure"`.
8. [ ] `git log --oneline` → ¿aparece el commit?
9. [ ] Crear el repo en GitHub **sin** README ni `.gitignore`.
10. [ ] `git remote add origin URL` → `git push -u origin main`.
11. [ ] Actualizar GitHub en el navegador y verificar.

---

## 6. Principios de trabajo que aparecieron

- **Diagnosticar antes de corregir.** Primero se confirma qué pasó (`git log`, `git remote -v`) y recién después se actúa.
- **Un paso, una verificación.** Cada comando se confirma con `git status` o `git log`.
- **Leer los errores completos.** El mensaje casi siempre dice la causa: hay que traducirlo.
- **No mostrar lo que no hay.** La descripción del repo menciona solo lo que el proyecto ya tiene.

---

## 7. Pendientes

- [ ] Completar el `README.md` cuando avance el proyecto (decidido: más adelante).
- [ ] Paso 2: `docs/project-brief.md` (pregunta, métricas, alcance).
- [ ] Paso 2: `docs/sources.md` (inventario de fuentes).
