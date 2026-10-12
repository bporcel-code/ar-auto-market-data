# ADR-001 — Capa raw versionada por fecha de descarga, con retención de 12 descargas

- **Estado:** Aceptado
- **Fecha:** 2026-10-12
- **Decisor:** Bruno Porcel

## Contexto

La DNRPA publica cada mes un archivo nuevo con **toda la historia** (por ejemplo, `...-2007-01-2026-09.csv`). El nombre del archivo cambia mes a mes, y nada garantiza que los datos de meses anteriores se mantengan iguales: la fuente puede **corregir el pasado** sin avisar.

Hay que decidir qué hace el pipeline con la descarga anterior cuando llega una nueva.

## Opciones evaluadas

| Opción | Ventaja | Desventaja |
|---|---|---|
| A. Pisar: un solo archivo, siempre el último | Simple, ocupa poco | Se pierde la versión anterior. No se pueden detectar ni auditar correcciones de la fuente |
| **B. Versionar: una carpeta por fecha de descarga** | Historial completo. Respeta el principio de **raw inmutable** | Ocupa más espacio. Hay que definir qué versión usa el pipeline |

## Decisión

**Opción B**, con una **política de retención**.

- Estructura: `data/raw/<fuente>/<AAAA-MM-DD>/<archivo original>`
  - Ejemplo: `data/raw/motos/2026-10-12/estadistica-inscripciones-iniciales-motovehiculos-2007-01-2026-09.csv`
- Los archivos se guardan **tal cual llegan** (bytes sin modificar).
- La descarga es **idempotente**: si el archivo ya existe en la carpeta del día, no se vuelve a descargar.
- **Retención:** se conservan las **últimas 12 descargas** por fuente; las más antiguas se eliminan. *(Pendiente de implementar.)*
- Las capas siguientes (silver/gold) leen la **descarga más reciente**.

## Consecuencias

- ✅ Si la DNRPA corrige datos históricos, se puede comparar contra versiones anteriores y documentar la diferencia.
- ✅ Cualquier resultado se puede reproducir con la versión exacta de los datos que lo generó.
- ⚠️ Para los datos agregados (cientos de KB) el costo de almacenamiento es despreciable. Para los **microdatos** (mucho más pesados) la retención se vuelve importante y puede revisarse.
- ⚠️ Hay que implementar la lógica de retención y la selección de la "versión vigente".

## Origen de la decisión

Bruno eligió la opción B para tener "el crudo de todos los meses por cualquier ocurrencia" y propuso limitar la tenencia a un año para no acumular archivos sin control.
