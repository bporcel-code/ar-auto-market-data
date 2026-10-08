# Inventario de fuentes de datos

> Versión 1.0 · Octubre 2026
> Estados: ✅ **verificado** (revisado directamente) · 🔎 **a verificar** (existe, pero falta confirmar cobertura, formato o acceso) · 💡 **candidata** (todavía no se revisó)

---

## 1. Mercado de vehículos — DNRPA (fuente principal)

Organismo: Dirección Nacional de los Registros Nacionales de la Propiedad del Automotor y de Créditos Prendarios (Ministerio de Justicia).
Portal: [datos.jus.gob.ar](https://datos.jus.gob.ar/dataset?organization=dnrpa-direccion-nacional-del-registro-de-la-propiedad-automotor-y-creditos-prendarios) · Licencia: Creative Commons Attribution 4.0.

| Fuente | Qué trae | Tipo | Formato | Frecuencia | Desde | Capa | Estado |
|---|---|---|---|---|---|---|---|
| [Estadística de trámites de **motovehículos**](https://datos.jus.gob.ar/tr/dataset/estadistica-de-tramites-de-motovehiculos) | Inscripciones iniciales y transferencias de motos por año, mes y provincia | Agregado | CSV / ZIP | Mensual | 2007-01 (hasta 2026-08) | 1 y 2 | ✅ |
| [Estadística de trámites de **automotores**](https://datos.jus.gob.ar/sq/dataset/estadistica-de-tramites-de-automotores) | Ídem, para autos | Agregado | CSV (a confirmar) | Mensual | A confirmar (¿2007?) | 1 y 2 | 🔎 |
| [Inscripciones iniciales de autos](https://datos.jus.gob.ar/dataset/inscripciones-iniciales-de-autos) | Una fila por 0 km inscripto, con los datos del vehículo y del primer titular | Microdato | CSV mensual / anual | Mensual | A confirmar (¿2018?) | 3 | 🔎 |
| [Transferencias de autos](https://datos.jus.gob.ar/dataset/transferencias-de-autos) | Una fila por transferencia de usado | Microdato | CSV mensual / anual | Mensual | A confirmar (¿2018?) | 3 | 🔎 |
| [Prendas de autos](https://datos.jus.gob.ar/dataset/prendas-de-autos) | Una fila por prenda inscripta (25 columnas: fechas, provincia, marca, modelo, origen, año del modelo, titular) | Microdato | CSV UTF-8 mensual (`dnrpa-prendas-autos-AAAAMM.csv`) y ZIP anual | Mensual | 2018-01 | 3 | ✅ |
| [Metadatos en GitHub](https://github.com/datos-justicia-argentina) | Diccionario de columnas de cada dataset (`*-metadata.md`) | Documentación | Markdown | — | — | — | ✅ (prendas) |

### Acceso automatizado: API de catálogo

El portal tiene una **API de catálogo** (CKAN) que devuelve en JSON la lista de archivos de cada dataset con su URL de descarga.

```
https://datos.jus.gob.ar/api/3/action/package_show?id=<id-del-dataset>
```

- ✅ Verificado con `inscripciones-iniciales-de-autos`: responde `"success": true`, con `metadata_modified` del 2026-09-11.
- Campo clave: `result.resources[]` → cada recurso tiene `name`, `format`, `last_modified` y `url`.
- **No** es una API de datos: no permite consultar registros. Sirve para descubrir y descargar archivos.

### Columnas relevantes (prendas, del archivo de metadatos)

| Columna | Uso en el proyecto |
|---|---|
| `tramite_fecha` | Fecha de la prenda → mes del hecho |
| `fecha_inscripcion_inicial` | Junto con `tramite_fecha` → `antiguedad_financiada` (0 km vs. usado) |
| `registro_seccional_provincia` | Dimensión provincia |
| `automotor_origen` | Nacional / importado / Protocolo 21 |
| `automotor_marca_descripcion`, `automotor_modelo_descripcion` | Dimensión marca y modelo |
| `automotor_tipo_descripcion` | Segmento (sedán, pick-up, etc.) |
| `titular_tipo_persona` | Persona física vs. jurídica |

---

## 2. Variables macroeconómicas

| Variable | Fuente | Serie | Desde | Estado | Observaciones |
|---|---|---|---|---|---|
| Tasa BADLAR (bancos privados) | BCRA | Tasa de interés por depósitos a plazo fijo de más de 1 millón (BADLAR) | — | 💡 | Confirmar el endpoint en la API de estadísticas del BCRA |
| Tipo de cambio oficial | BCRA | Com. A3500 (mayorista) | — | 💡 | Promedio mensual |
| Stock de préstamos prendarios | BCRA | Préstamos prendarios al sector privado, en pesos | — | 💡 | Deflactar con el IPC |
| Dólar MEP / CCL | argentinadatos.com | Cotizaciones históricas | A confirmar | 🔎 | Ya se usa en PWOS. Confirmar desde qué año cubre |
| IPC | INDEC | IPC nacional | 2016-12 | 🔎 | ⚠️ **2007-2015: período de intervención, serie no confiable.** Se necesita una serie alternativa o un empalme (decisión pendiente, ADR) |
| EMAE | INDEC | Estimador Mensual de Actividad Económica | A confirmar | 💡 | Usar la serie desestacionalizada y la original |
| Salario (RIPTE) | Secretaría de Seguridad Social | Remuneración Imponible Promedio de los Trabajadores Estables | A confirmar | 💡 | Es un **nivel en pesos** (no un índice), por eso se puede dolarizar directamente |
| Agregador | datos.gob.ar | API de Series de Tiempo | — | 💡 | Puede concentrar varias series (IPC, EMAE, BCRA) en una sola API. Evaluar |

---

## 3. Fuentes secundarias (validación)

| Fuente | Qué trae | Uso | Estado |
|---|---|---|---|
| ACARA | Patentamientos mensuales agregados por marca, modelo y segmento | **Reconciliación:** comparar los totales mensuales del pipeline contra ACARA como test de calidad | 💡 |

---

## 4. Fuentes descartadas

| Fuente | Motivo |
|---|---|
| Scraping de autotest.com.ar / lamoto.com.ar | Frágil, con riesgo legal, y son datos de segunda mano (republican ACARA) |
| Dataset de precios de MercadoLibre (Kaggle, 2023) | Scraping, una foto puntual de 2023, sin historia. Queda para la v2 si aparece una fuente de precios |

---

## 5. Pendientes de verificación

- [ ] Fecha de inicio real de la estadística agregada de **automotores**
- [ ] Fecha de inicio de los microdatos de inscripciones y transferencias de autos
- [ ] Endpoints de la API del BCRA para BADLAR, A3500 y préstamos prendarios
- [ ] Cobertura histórica del MEP / CCL en argentinadatos
- [ ] Serie alternativa de IPC para 2007-2016
- [ ] Cobertura y formato del RIPTE y del EMAE
