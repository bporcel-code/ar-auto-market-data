# Antecedentes (prior art)

> Relevamiento realizado en octubre de 2026 en GitHub, Kaggle, Google Scholar y repositorios académicos argentinos. Límite de tiempo: 2 horas.

---

## 1. Trabajos relevados

| Nombre / link | Tipo | Qué hace | Datos que usa | Actualización | ¿Qué me sirve? | ¿Qué le falta? |
|---|---|---|---|---|---|---|
| [Todesca y Engelman — *Consumo, bienestar y distinción social en la Argentina* (PBR n.º 33)](https://www.palermo.edu/negocios/cbrs/pdf/pbr33/PBR-33-01.pdf) | Artículo académico | Analiza la reconfiguración del consumo en 2024-2026. Señala que en el 1.er semestre de 2026 los patentamientos de autos cayeron 9,9% y los de motos crecieron 42,4%, y lo interpreta como **sustitución** | ICP-UP, INDEC, ACARA, BCRA | Julio 2026 | **Es el antecedente que este proyecto continúa.** Plantea la hipótesis de sustitución auto → moto | Es descriptivo y cubre solo 2024-2026, con datos agregados de ACARA. **No relaciona** los movimientos con tasas, tipo de cambio, inflación ni crédito |
| [tomipiqueras/criterio-motor-dashboard](https://github.com/tomipiqueras/criterio-motor-dashboard) | Repo de GitHub (web) | Dashboard en React con estadísticas del mercado automotor y de motos | ACARA, más scraping de autotest.com.ar y lamoto.com.ar | Reciente (9 commits) | Confirma el interés en el tema. Me hizo conocer **ACARA** como fuente de validación. Ideas para la visualización | README genérico, sin documentación de fuentes. Depende de scraping frágil. No usa microdatos oficiales. Sin análisis macroeconómico |
| [datos-justicia-argentina/dnrpa-prendas-autos](https://github.com/datos-justicia-argentina/dnrpa-prendas-autos) | Repo oficial de documentación | Diccionario de datos del dataset de prendas | DNRPA | — | No es un antecedente sino una **fuente** → ver `sources.md`. Permite calcular la antigüedad del vehículo financiado | — |
| [pawelpinkowicz — Car Sales Analysis (Kaggle)](https://www.kaggle.com/code/pawelpinkowicz/car-sales-analysis) | Notebook de Kaggle | Análisis de ventas de autos | No comparte el dataset | Antiguo | Referencia de tipos de análisis | **No es reproducible**: el dataset no está disponible |
| [marinagrabelli — Precios de venta de autos en Argentina (Kaggle)](https://www.kaggle.com/code/marinagrabelli/precios-de-venta-de-autos-en-argentina-1-2023) | Notebook de Kaggle | Análisis de precios de autos usados | Scraping de MercadoLibre (2023) | 2023 | Único hallazgo con **precios**, una variable que no tienen las fuentes oficiales | Una foto puntual sin historia, obtenida con scraping → backlog v2 |
| [Cantarella, Katz y de Guzmán (2008) — *La industria automotriz argentina* (UNGS)](https://cdi.mecon.gob.ar/bases/doc/ungs/littec/dt2008-1.pdf) | Documento de trabajo | Estudia la integración local de autopartes, 1992-2007 | AFAC, ADEFA, INDEC | 2008 | Contexto sobre la estructura de la industria | **No aplica**: estudia la oferta y la importación de partes, no la demanda |
| [Lódola (2018) — Ingresos Brutos en la cadena automotriz (UNLP)](https://sedici.unlp.edu.ar/handle/10915/146296) | Informe | Impacto del impuesto a los Ingresos Brutos en el precio final, año 2016 | Datos fiscales provinciales | 2018 | Contexto: los impuestos influyen en el precio final | **No aplica**: tema fiscal, un solo año |
| [Arcuri (2017) — Política Automotriz Común Argentina-Brasil (Siglo 21)](https://repositorio.21.edu.ar/server/api/core/bitstreams/343e6b7e-3543-406d-b61b-c79ed28b0d21/content) | Tesis de grado | Evalúa los términos comerciales de la PAC, 1988-2016 | INDEC, IBGE, ADEFA, ANFAVEA | 2017 | Contexto sobre comercio exterior automotriz | **No aplica**: comercio bilateral, no demanda interna |

---

## 2. Conclusión

### ¿Existe algo igual a lo que quiero hacer?
**No.** No apareció ningún trabajo ni repositorio que:
- use los **microdatos y estadísticas oficiales de la DNRPA** con un pipeline reproducible;
- abarque un **período largo** (2007 → hoy) con varios ciclos económicos;
- cruce **autos y motos, 0 km y usados**, con variables de **tasas, liquidez, tipo de cambio, inflación, actividad e ingreso**.

Los antecedentes existentes son descriptivos, de un período corto, dependen de scraping o no son reproducibles.

### ¿Qué puedo reutilizar o tomar como referencia?
- La **hipótesis de sustitución** auto → moto de Todesca y Engelman (2026), como punto de partida del análisis (H1).
- **ACARA** como fuente de validación de los totales.
- Los **archivos de metadatos oficiales** de la DNRPA en GitHub como diccionario de datos.

### ¿Qué hace único a este proyecto?
1. **Datos oficiales y reproducibles:** cualquier persona puede correr el pipeline y obtener los mismos resultados.
2. **Horizonte largo:** casi dos décadas, que permiten comparar varias crisis.
3. **Tres niveles de análisis:** nacional → provincial → micro (marca, origen, antigüedad).
4. **Lectura económica con criterio local:** tasa real, brecha cambiaria y salario en dólares como variables explicativas.
5. **Continuación explícita** de un trabajo académico publicado en 2026.

---

## 3. Lecciones del relevamiento

- **GitHub** sirve para encontrar código y documentación de datos. **Kaggle**, para análisis y datasets. **Scholar y los repositorios universitarios**, para tesis y papers.
- Descartar trabajos también es un resultado: 3 de los 4 trabajos académicos no aplicaban a la pregunta.
- Un análisis que no comparte sus datos no se puede verificar → la **reproducibilidad** es un requisito de este proyecto.
- Antes de confiar en un dataset de terceros, hay que revisar **de dónde vienen los datos** (*provenance*).
