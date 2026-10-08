# Project Brief — AR Auto Market Data

> Versión 1.0 · Octubre 2026 · Autor: Bruno Porcel
> Estado: **borrador aprobado para comenzar la ingesta**. Este documento se actualiza a medida que avanza el proyecto.

---

## 1. Pregunta principal

**¿Cómo responde el mercado argentino de autos y motos (0 km y usados) a los ciclos económicos, en particular a las condiciones de tasas, liquidez, tipo de cambio e inflación?**

## 2. Punto de partida (antecedente que se continúa)

Todesca y Engelman (2026, *Palermo Business Review* n.º 33) observan que en el primer semestre de 2026 los patentamientos de autos cayeron 9,9% y los de motos crecieron 42,4%. Lo interpretan como una estrategia de **sustitución** de los hogares en un contexto de contracción del consumo. El análisis es descriptivo, cubre 2024-2026 y usa cifras agregadas de ACARA. **No relaciona esos movimientos con variables macroeconómicas.**

Este proyecto construye el pipeline de datos necesario para:

1. verificar esas cifras con datos oficiales de la DNRPA;
2. testear si el patrón se repite en las crisis anteriores (2008-09, 2012, 2014, 2018-19, 2020, 2023-24);
3. relacionarlo con indicadores de tasas, liquidez, tipo de cambio, inflación, actividad e ingreso.

Detalle completo en [`antecedentes.md`](antecedentes.md).

## 3. Hipótesis a testear

Son **hipótesis**, no conclusiones. El proyecto existe para confirmarlas o descartarlas.

| # | Hipótesis | Canal |
|---|---|---|
| H1 | En las fases recesivas, la moto funciona como **sustituto** del auto: crece la participación de las motos sobre el total de vehículos 0 km | Ingreso / sustitución |
| H2 | Con **tasa real negativa**, aumentan los patentamientos financiados, porque endeudarse en pesos para comprar un bien que conserva valor es conveniente | Costo del crédito |
| H3 | Con **brecha cambiaria alta**, el 0 km funciona como **reserva de valor**: los patentamientos se sostienen o suben aunque la actividad caiga | Tipo de cambio |
| H4 | El **crédito prendario** anticipa los patentamientos: los cambios en las prendas preceden a los cambios en las ventas | Liquidez |
| H5 | El **salario medido en dólares** explica mejor la demanda de 0 km que el salario real en pesos, porque los vehículos se valúan de hecho en dólares | Poder de compra |
| H6 | En las crisis, la relación **usados / 0 km** sube: la demanda se desplaza hacia el mercado de usados | Ingreso / sustitución |
| H7 | Las subas del **riesgo país** anticipan caídas de los patentamientos de 0 km: cuando empeoran las expectativas, se postergan las compras de bienes durables | Expectativas / confianza |

## 4. Métricas (definición exacta)

### Mercado de vehículos (DNRPA)

| Métrica | Definición | Fórmula |
|---|---|---|
| `inscripciones_0km` | Cantidad de inscripciones iniciales en el mes | conteo, por tipo de vehículo (auto / moto) |
| `transferencias_usados` | Cantidad de transferencias de dominio en el mes | conteo, por tipo de vehículo |
| `ratio_usados_0km` | Usados vendidos por cada 0 km | `transferencias_usados / inscripciones_0km` |
| `participacion_motos_0km` | Peso de las motos en el total de 0 km | `motos_0km / (autos_0km + motos_0km)` |
| `prendas` | Cantidad de prendas inscriptas en el mes | conteo (autos; desde 2018) |
| `antiguedad_financiada` | Antigüedad del vehículo al momento de prendarse | `tramite_fecha − fecha_inscripcion_inicial`, en años |

### Variables macroeconómicas

| Métrica | Definición | Fórmula |
|---|---|---|
| `inflacion_mensual` | Variación mensual del IPC | `IPC_t / IPC_{t-1} − 1` |
| `tasa_real_mensual` | Tasa BADLAR (bancos privados) descontada la inflación | `(1 + BADLAR_mensualizada) / (1 + inflacion_mensual) − 1` |
| `credito_prendario_real` | Stock de préstamos prendarios a precios constantes | `stock_prendarios_nominal / IPC × IPC_base` |
| `tc_oficial` | Tipo de cambio mayorista oficial (Com. A3500), promedio mensual | — |
| `brecha_cambiaria` | Diferencia entre el dólar MEP y el oficial | `tc_mep / tc_oficial − 1` |
| `emae_var_ia` | Variación interanual de la actividad económica | `EMAE_t / EMAE_{t-12} − 1` |
| `salario_usd_oficial` | Salario promedio medido en dólares oficiales | `RIPTE / tc_oficial` |
| `salario_usd_mep` | Salario promedio medido en dólares MEP | `RIPTE / tc_mep` |
| `riesgo_pais` | Spread de los bonos argentinos en dólares sobre los del Tesoro de EE.UU. (índice EMBI, en puntos básicos), promedio mensual | — |
| `fase_ciclo` | Fase del ciclo económico en cada mes: **expansión** o **recesión** | Se define a partir de los picos y valles del EMAE desestacionalizado (ver sección 5.1) |

> **Convención:** todas las series se llevan a frecuencia **mensual**. Para las tasas y el tipo de cambio, se usa el **promedio del mes**. Cualquier cambio a esta convención se documenta como decisión (ADR).

## 5. Granularidad y período

El análisis se arma en **tres capas**, de lo macro a lo micro:

| Capa | Grano | Período | Fuente principal |
|---|---|---|---|
| **1 — Nacional** | país × mes × tipo de vehículo | 2007 → hoy | DNRPA, estadísticas agregadas |
| **2 — Provincial** | provincia × mes × tipo de vehículo | 2007 → hoy | DNRPA, estadísticas agregadas |
| **3 — Micro** | trámite individual (marca, segmento, origen, antigüedad) | 2018 → hoy | DNRPA, microdatos |

El período exacto de inicio se confirma en [`sources.md`](sources.md) al verificar la cobertura real de cada fuente.

### 5.1 Cómo se identifican los ciclos económicos

Para comparar el comportamiento del mercado en cada crisis, primero hay que **fechar los ciclos**: definir en qué mes empieza y termina cada recesión.

- **Indicador base:** EMAE desestacionalizado (actividad económica mensual).
- **Método v1:** identificar los **picos** (máximos antes de una caída) y los **valles** (mínimos antes de una recuperación) de la serie. Cada mes queda clasificado como **expansión** o **recesión** (`fase_ciclo`).
- **Validación:** comparar el fechado propio con cronologías publicadas de los ciclos argentinos. Las diferencias se documentan.
- **Indicadores que acompañan el ciclo:** el **riesgo país** (expectativas y acceso al financiamiento), la **brecha cambiaria** (tensión cambiaria) y la **tasa real** (condiciones monetarias). Juntos permiten describir *qué tipo* de crisis fue cada una: cambiaria, financiera, sanitaria (2020), etc.

Con esto, cada crisis se puede analizar como un **episodio**: qué pasó con autos, motos, 0 km y usados antes, durante y después.

## 6. Fuera de alcance (v1)

- **Precios de vehículos:** no hay una fuente oficial con historia larga. Candidata para la v2.
- **Modelo de proyección** (*forecasting*): queda para la **v2**. La v1 deja la base sobre la que se construye: datos validados e **indicadores adelantados** identificados (ver sección 9).
- **Causalidad formal** (econometría avanzada): la v1 muestra relaciones y rezagos y lo dice con honestidad. No afirma causalidad.
- **Scraping de sitios** (MercadoLibre, autotest, etc.): solo fuentes oficiales o APIs.
- **Camiones, maquinaria agrícola y otros vehículos**: solo autos y motos.

## 7. Supuestos y riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| **El IPC del INDEC entre 2007 y 2015 no es confiable** (período de intervención). El IPC nacional actual empieza en diciembre de 2016 | Las tasas reales, el crédito real y el salario real de 2007-2016 quedan distorsionados | Usar una serie alternativa o un empalme reconocido para ese período y documentarlo como ADR. Es una decisión pendiente |
| La DNRPA cambia el formato de los archivos o las URLs | El pipeline se rompe | Usar la API de catálogo para encontrar las URLs. Validar el esquema en cada ingesta |
| Las cifras de la DNRPA no coinciden con las de ACARA | Dudas sobre la calidad de los datos | Reconciliar los totales mensuales contra ACARA como **test de calidad**, con un margen de tolerancia documentado |
| Cambios regulatorios que alteran el mercado (impuesto a los autos de alta gama, cepo, restricciones a la importación) | Pueden confundirse con efectos macroeconómicos | Registrar una **línea de tiempo de eventos regulatorios** y marcar esos períodos en el análisis |
| Rezagos en la publicación de las series (INDEC, BCRA) | El último mes queda incompleto | El pipeline solo cierra un mes cuando están todas sus fuentes |
| Correlación no es causalidad | Conclusiones exageradas | Presentar los resultados como relaciones, con limitaciones explícitas |

## 8. Entregables de la v1

1. **Pipeline reproducible:** descarga, limpieza y modelo analítico (bronze → silver → gold).
2. **Modelo de datos** documentado, con tablas de hechos y dimensiones.
3. **Tests de calidad de datos**, incluida la reconciliación contra ACARA.
4. **Fechado de los ciclos económicos** 2007 → hoy.
5. **Informe de análisis:** respuesta a H1-H7 con sus limitaciones, más la lista de **indicadores adelantados** encontrados.
6. **Documentación:** README en inglés, ADRs y notas de aprendizaje.

## 9. Hoja de ruta del estudio

El objetivo de largo plazo es **publicar** el estudio y **proyectar** el mercado. Se avanza por etapas, y cada etapa se apoya en la anterior:

| Versión | Pregunta que responde | Tipo de análisis | Publicación posible |
|---|---|---|---|
| **v1** | ¿Qué pasó y con qué se relaciona? | **Descriptivo y explicativo:** episodios de crisis, relaciones con rezagos, indicadores adelantados | Artículo 1: *"Autos y motos en los ciclos económicos argentinos, 2007-2026"* |
| **v2** | ¿Qué es probable que pase? | **Predictivo:** modelo de proyección de patentamientos a 3, 6 y 12 meses, evaluado contra datos reales (*backtesting*) | Artículo 2: proyección del mercado con escenarios |
| **v3** | (abierta) | Extensiones: precios, segmentos, provincias, actualización mensual automática | Tablero público actualizado |

**Por qué este orden:** un modelo de proyección solo es confiable si los datos están validados y si se sabe qué variables anticipan al mercado y con cuántos meses de ventaja. La v1 produce exactamente eso. Saltear la v1 lleva a proyecciones que nadie puede defender.

### Requisitos para publicar

- Todas las fuentes citadas, respetando la licencia **CC BY 4.0** de los datos de la DNRPA (atribución obligatoria).
- Metodología y limitaciones explícitas.
- Resultados **reproducibles**: el link al repositorio permite a cualquier persona verificarlos.

## 10. Documentos relacionados

- [`sources.md`](sources.md) — inventario de fuentes de datos
- [`antecedentes.md`](antecedentes.md) — relevamiento de trabajos previos
- [`aprendizaje/`](aprendizaje/) — notas de aprendizaje del proceso
