# Histórico de auditorías Forge — `phylo`

Este directorio conserva la evolución de las corridas sin sobrescribir
resultados anteriores. `../phylo-demo/` es el baseline legado de la primera
demo y se conserva con ese nombre histórico; la corrida nueva usa el nombre
neutral `run-20260716T010234Z`.

## 2026-07-16 — corrida actual

- Repositorio inspeccionado: `/home/labestiadevigia/phylo`
- Revisión auditada: `26cfd2d22c0d22b5a1a883922909989476579804`
- Invocación exacta: `python3 -m forge audit /home/labestiadevigia/phylo --output-dir /home/labestiadevigia/forge/resultados/phylo/run-20260716T010234Z --max-connected 100`
- Stacks detectados: TypeScript, Python y JavaScript.
- Módulos detectados: 33; `CONNECTED_ALIVE`: 24; `FOSSIL_HIGH_RISK`: 3; `DEAD_WEIGHT`: 6; `FOSSIL_LOW_RISK`: 0; duplicados: 0.
- Módulos analizados: 26 archivos AST parseables; 9 módulos quedaron fuera por límite de alcance no conectado.
- Hallazgos: 7 observaciones: 3 CRITICAL y 4 MEDIUM; 6 `CODE FACT` y 1 `PLAUSIBLE HYPOTHESIS`/inferencia. No hay resultados confirmados por inducción dinámica.
- Distribución por agente: `web_auditor` 6, `bug_investigator` 1. No se auditó JavaScript/TypeScript como lenguaje confirmado: se detectó y se analizaron 14 archivos soportados por el auditor web; el resto quedó explícitamente fuera o no analizado según cobertura.
- Candidatos descartados: 0. Por tanto no se usa “false positive” como etiqueta: las observaciones no fueron demostradas falsas; las limitaciones se mantienen como observaciones, inferencias o indeterminaciones.
- Límites exactos: `.git`, dependencias (`node_modules`, `vendor`, `site-packages`, `dependencies`), entornos virtuales (`.venv`, `venv`, `.tox`, `.nox`), caches, build/dist/target y `.gitignore` son `excluded_by_policy`; los manifiestos permanecen como evidencia de stack. La cobertura los enumera para explicar el límite, no para auditarlos. 9 módulos no conectados quedaron fuera.
- Integridad: manifiesto sellado generado; la comparación MCP verificó ambos runs (`ok: true`).
- Red-team: 8/8 pruebas adversariales pasaron antes de considerar la auditoría verde. Suite completa: 150/150; ambos resultados son del código Forge usado para esta corrida.
- Reproducibilidad: Forge `0.1.0`, Python 3.12.3, Linux; snapshot SHA-256 `6576700de9e634e50a72cd0d7c08e639f9e6eb40bede9e5ae5a8979471654ead`. La corrida quedó degradada honestamente a `ABSTAIN_INSUFFICIENT_SCOPE` por cobertura parcial; no se presenta como auditoría completa del repositorio.
- Protocolo de agentes: los 8 roles runtime registrados tienen las tres etapas A-D-I y el catálogo de 20 skills. ARGOS: no aplicable/no conectado en esta corrida; el cross-check independiente ejecutado fue `mcp__forge__compare_audits`.

Artefactos completos: [`run-20260716T010234Z/`](run-20260716T010234Z/), incluyendo `report.md`, `metrics.json`, `coverage-report.json`, `audit-trace.json` y el manifiesto sellado.

## Comparación contra el baseline legado

La comparación MCP (`resultados/phylo-demo` → `run-20260716T010234Z`) informó:

- 12 hallazgos previos frente a 7 actuales.
- 5 resueltos, 0 nuevos y 7 sin cambios.
- La reducción no se interpreta automáticamente como corrección de código ni como falsos positivos: refleja la diferencia de alcance/evidencia y los cambios de Forge; cada entrada conserva su estatus epistemológico.
- El denominador de cobertura cambió de 1.828 a 7.312 y el numerador de 5 a 13; no es una comparación porcentual directa sin normalizar el perímetro.

El resultado machine-readable del cross-check está en
[`comparison-mcp.json`](comparison-mcp.json).
