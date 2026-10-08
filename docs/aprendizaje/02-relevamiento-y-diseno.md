# 02 — Relevamiento de antecedentes y diseño del proyecto

> Sesiones: 4-8 de octubre de 2026 · Proyecto: `ar-auto-market-data`
> Resultado: antecedentes relevados; `project-brief.md` (v1.1), `sources.md` y `antecedentes.md` publicados en el repo.

---

## 1. Por qué se investiga antes de construir

Antes de escribir código se releva qué existe (*prior art*). Sirve para:
- no reconstruir algo que ya está hecho;
- encontrar fuentes de datos y enfoques que no se nos habían ocurrido;
- **definir el aporte propio**: lo que les falta a los trabajos existentes.

Regla: **ponerle un límite de tiempo** (en este caso, 2 horas). Una búsqueda sin límite no termina nunca.

---

## 2. Dónde buscar cada cosa

| Lugar | Qué se encuentra | Para qué sirve |
|---|---|---|
| **GitHub** | Código, pipelines, documentación de datasets | Ver cómo otros procesaron los datos. Es el **portfolio** de un Data Engineer |
| **Kaggle** | Datasets y notebooks de análisis | Ideas de análisis. Es el portfolio de analistas y científicos de datos |
| **Google Scholar** | Papers y tesis | Preguntas, métodos y conclusiones académicas |
| **Repositorios universitarios** (RDU-UNC, SEDICI-UNLP, FCE-UBA) | Tesis argentinas | Cuando Scholar no alcanza |
| **Informes sectoriales** (ACARA, ADEFA, BCRA) | Cifras oficiales del sector | Validar resultados |

### Cómo buscar en GitHub
- Barra superior **"Type / to search"**, o la URL `https://github.com/search?q=PALABRA&type=repositories`.
- Filtros: **Repositories** y **Language** (Python / Jupyter Notebook).
- Orden: **Recently updated** o **Most stars**.

### Cómo buscar en Google Scholar
- `scholar.google.com` → filtrar por año en la columna izquierda ("Desde 2018").
- **[PDF]** a la derecha = descarga gratuita. **"Citado por N"** = relevancia. **"Artículos relacionados"** = seguir el hilo.

---

## 3. Cómo evaluar lo que se encuentra

### Repositorio de GitHub (en 30 segundos)
| Qué mirar | Qué indica |
|---|---|
| README | Qué hace. Un README genérico o ausente es mala señal |
| Último commit | Si está vivo o abandonado |
| Estrellas | Interés de la comunidad (no aplica a repos oficiales de documentación) |
| Archivos | Si hay código real o solo datos |

### Dataset de Kaggle
| Qué mirar | Qué indica |
|---|---|
| Usability (0-10) | Calidad de la documentación |
| Updated | Si está vigente |
| **Provenance** | **De dónde salen los datos.** Si no lo dice, desconfiar |
| Pestaña Code | Los análisis que otros hicieron |

### Trabajo académico
- ¿Responde **mi** pregunta o solo habla del mismo sector?
- ¿Qué período cubre? ¿Qué datos usa? ¿Cuál es su conclusión? ¿Qué le falta?

> **Descartar también es un resultado.** De 4 trabajos académicos, 3 hablaban del sector automotor pero no de la demanda (autopartes, impuestos, comercio con Brasil).

---

## 4. Antecedente vs. fuente

| | Antecedente | Fuente |
|---|---|---|
| Qué es | Un **trabajo** que otra persona hizo con datos | **De dónde salen** los datos |
| Ejemplo | Todesca y Engelman (2026); el dashboard Criterio Motor | DNRPA, BCRA, INDEC |
| Dónde se documenta | `antecedentes.md` | `sources.md` |

El repo `datos-justicia-argentina/dnrpa-prendas-autos` parece un antecedente, pero es una **fuente**: es la documentación oficial del dataset.

---

## 5. Lecciones de los hallazgos

| Hallazgo | Lección |
|---|---|
| Criterio Motor usa scraping de autotest y lamoto | **Scraping:** frágil (se rompe si cambia la web), con riesgo legal (`robots.txt`, términos de uso) y con datos de segunda mano. Regla: fuente oficial o API primero; scraping como último recurso |
| Criterio Motor usa ACARA | Una fuente agregada e independiente sirve para **reconciliar** (test de calidad de datos), como comparar los saldos de PWOS con la app de cada broker |
| Notebook de Kaggle sin dataset | **Sin datos no hay reproducibilidad**, y sin reproducibilidad el resultado no se puede verificar |
| Todo lo encontrado es viejo o descriptivo | **Ese hueco es el aporte del proyecto** |
| Todesca y Engelman (2026) observan la sustitución auto → moto sin modelo macro | Un trabajo para **continuar**: testear la hipótesis con datos oficiales, un período largo y variables económicas |

---

## 6. Formas de obtener datos

| Tipo | Cómo funciona | Ejemplo |
|---|---|---|
| **API de datos** | Se piden registros puntuales y responde en JSON | BCRA, dolarapi |
| **Descarga de archivos** | Se baja el archivo entero y se procesa | CSV de la DNRPA |
| **API de catálogo** | Devuelve la **lista de archivos** de un dataset y sus URLs | `datos.jus.gob.ar/api/3/action/package_show?id=...` |
| **Scraping** | Se lee el HTML de una web | Criterio Motor |

### Leer JSON en el navegador
- Chrome en español: casilla **"Impresión con formato estilístico"** (en inglés, *Pretty-print*).
- Estructura de la respuesta de la API de catálogo:
  - `success: true` → respondió bien;
  - `result.resources[]` → lista de archivos, cada uno con `name`, `format`, `last_modified` y **`url`**.
- El script de ingesta va a recorrer esa lista y descargar las URLs.

### Datos agregados vs. microdatos
| | Agregados | Microdatos |
|---|---|---|
| Qué son | Totales (por ejemplo, cantidad por mes y provincia) | Una fila por hecho (cada trámite) |
| Ejemplo | Estadística de motovehículos, 2007-2026 | Prendas de autos, 2018-2026 |
| Ventaja | Historia larga, livianos | Detalle (marca, origen, antigüedad) |

---

## 7. Conceptos de diseño

**Grano (*grain*):** el nivel de detalle de una tabla, es decir, qué representa cada fila. Para comparar fuentes, hay que llevarlas al **mismo grano**. Acá: mes × provincia × tipo de vehículo.

**Análisis en capas, de lo macro a lo micro:** nacional → provincial → microdatos.

**Canales de transmisión:** organizar las variables económicas según el mecanismo por el que afectan la compra:

| Canal | Indicador |
|---|---|
| Costo del crédito | Tasa real (BADLAR − inflación) |
| Liquidez | Crédito prendario real, cantidad de prendas |
| Precios | IPC |
| Tipo de cambio | Oficial y brecha con el MEP |
| Actividad | EMAE |
| Poder de compra | Salario (RIPTE) en dólares |
| Expectativas | Riesgo país |

**Variables reales vs. nominales:** en Argentina una tasa nominal sola no dice nada. Lo que importa es la **tasa real** (tasa − inflación).

**Fechado de ciclos:** para comparar crisis hay que definir cuándo empieza y termina cada una. Se hace con los **picos y valles** del EMAE desestacionalizado.

**Riesgo de calidad conocido:** el IPC del INDEC entre 2007 y 2015 no es confiable (período de intervención). Detectar este tipo de problemas **antes** de construir es parte del trabajo.

---

## 8. Niveles de análisis

| Nivel | Pregunta | Versión del proyecto |
|---|---|---|
| Descriptivo | ¿Qué pasó? | v1 |
| Explicativo | ¿Con qué se relaciona? | v1 |
| Predictivo | ¿Qué va a pasar? | v2 (requiere *backtesting*: proyectar el pasado y medir el error) |

---

## 9. Las tres acepciones de "modelado"

| Quién | Significado |
|---|---|
| **Data Engineer** | **Modelado de datos:** diseñar las tablas (modelo estrella: hechos + dimensiones). Es lo que pide una oferta que dice *data modeling* |
| **dbt** | **"Models":** cada archivo SQL que transforma una tabla en otra |
| **Analista / economista** | **Modelo estadístico o predictivo:** una ecuación que relaciona o proyecta variables |

El modelado de datos es **una etapa** del pipeline, no el pipeline completo:

```
Fuentes → Ingesta (raw) → Limpieza (silver) → Modelado de datos (gold) → Análisis
```

**Respuesta para una entrevista:** *"El modelado de datos es diseñar la estructura de las tablas analíticas, por ejemplo un modelo estrella con hechos y dimensiones, para que el negocio consulte los datos de forma simple y eficiente. Es una etapa del pipeline, después de la ingesta y la limpieza."*

---

## 10. Git en esta etapa

- Commits hechos de forma autónoma: `d90dcc4` (documentos de diseño) y `3442280` (ciclos económicos en el brief).
- **Mejora pendiente:** mantener el formato *Conventional Commits* en inglés, igual que los primeros commits.
  - ✅ `docs: add project brief, sources and prior art`
  - ⚠️ `armado de primeros documentos del proyecto`
- **No se reescribe historia ya subida** a GitHub para corregir un mensaje. Se aplica la convención de acá en adelante.

---

## 11. Próximo paso

**Python: primer script de ingesta.** Va a leer la API de catálogo de la DNRPA y descargar los CSV a `data/raw/`.
