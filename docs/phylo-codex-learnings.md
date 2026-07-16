# Aprendizajes de la auditoria multiagente de `phylo`

Fecha: 2026-07-16  
Repositorio: `/home/labestiadevigia/phylo`  
Revision auditada: `26cfd2d22c0d22b5a1a883922909989476579804`  
Artefactos: [`resultados/phylo-codex/`](../resultados/phylo-codex/)

## Resumen

La corrida cumplio correctamente el comportamiento abstencionista de Forge:
red-team 8/8, suite completa 150/150, sello verificado, repositorio auditado
sin modificaciones y estado final `ABSTAINED`.

El aprendizaje principal es que el modo multiagente todavia no equivale a una
deliberacion multiagente independiente. Se registraron ocho roles y protocolos
A-D-I, pero los resultados de los agentes fueron esencialmente protocolos
genericos copiados desde el mismo contexto. No hay evidencia suficiente de que
cada agente haya producido hipotesis, pruebas, contradicciones o decisiones
independientes.

La corrida es valida como prueba de limites, integridad y abstencion; no es
todavia una demostracion de agentes especialistas autonomos.

## Evidencia de la corrida

- 33 modulos detectados: 24 `CONNECTED_ALIVE`, 6 `DEAD_WEIGHT` y 3
  `FOSSIL_HIGH_RISK`.
- Lenguajes detectados: TypeScript, JavaScript y Python.
- Python: analisis AST efectivo.
- JavaScript/TypeScript: scan web acotado, no auditoria completa del lenguaje.
- Excluidos: dependencias, virtualenvs, `.git`, `.gitignore`, caches, builds,
  binarios, codigo generado, minificados y artefactos grandes.
- Siete observaciones: tres criticas y cuatro medias.
- Cero resultados confirmados por induccion dinamica.
- ARGOS no disponible y declarado como abstencion.
- El sello demuestra integridad del artefacto, no correccion de los hallazgos.

## 1. Los roles no prueban agentes independientes

Los ocho roles registrados fueron:

- `coordinator`
- `scope_triage`
- `python_security`
- `web_security`
- `integrity_numeric`
- `abduction_hypotheses`
- `adversarial_redteam`
- `independent_reviewer`

Sin embargo, los archivos de `agent-results/` contienen casi exclusivamente el
mismo A-D-I generico, las mismas referencias a `verification-manifest.json` y
`audit-trace.json`, y el mismo catalogo de 20 skills. No hay evidencia material
de analisis propio por rol.

El `independent_reviewer` tampoco aporta una revision independiente material.
La ausencia de contradicciones no demuestra independencia cuando no existe una
salida independiente que comparar.

### Cambio requerido

Cada agente debe entregar un resultado propio con entradas observadas,
hipotesis, deducciones falsables, pruebas o abstenciones, decision epistemica,
evidencia y desacuerdos con otros agentes. El coordinador debe rechazar un run
si los resultados son solo copias del protocolo comun.

## 2. A-D-I existe como contrato, no todavia como conducta

Todos los agentes registraron los mismos estados:

- abduccion: `PLAUSIBLE_HYPOTHESIS`;
- deduccion: `PREDICTION_REQUIRED`;
- induccion: `UNDETERMINED`.

Esto demuestra que el esquema esta presente, pero no que cada agente haya
realizado una abduccion o deduccion especifica. El ledger debe ser por
hipotesis, no solo por agente.

Cada entrada A-D-I debe contener una afirmacion concreta, un falsificador
concreto y la evidencia que cambio su estado.

## 3. Las skills se cargan, pero se sobredeclaran como aplicadas

Las 20 skills aparecen como `APPLIED`, pero la accion registrada es basicamente
“cargar la politica Markdown y registrar su aplicacion”. Eso prueba carga
documental, no aplicacion semantica.

La metrica de calidad informa `contract_coverage: covered 0 / total 1` y
`skill_versions: {}`. Por eso la mayoria de las skills no tienen aun un
checker ejecutable ni una obligacion verificable.

### Cambio requerido

Crear un `skill_obligation_ledger` con skill, obligacion concreta, agente,
etapa A-D-I, evidencia esperada, evidencia encontrada y estado
`APPLIED`, `REJECTED` o `UNDETERMINED`. `APPLIED` debe significar que la skill
afecto una decision observable, no simplemente que fue leida.

## 4. El path handling descubrio una limitacion real

Forge marco `app/api/save-run/route.ts:107` como path traversal critico porque
vio `writeFile(join(dir, filename), ...)`. Pero `filename` deriva de un `slug`
sanitizado mediante reemplazos restrictivos en las lineas anteriores.

La sanitizacion esta distribuida en una expresion multilinea y el analizador
no propaga correctamente esa evidencia hasta el uso final. No debe llamarse
automaticamente false positive: la clasificacion actual correcta es
“observacion con explicacion benigna plausible, pendiente de verificacion”.

### Cambio requerido

Implementar propagacion conservadora para asignaciones multilinea, variables
derivadas de nombres sanitizados, `basename`, `normalize`, `resolve`,
validaciones de extension, concatenaciones y templates antes de usos en
`join`, `writeFile`, `readFile`, `unlink` y `rm`.

## 5. `eval` es frontera observada, no vulnerabilidad confirmada

Las observaciones en `app/api/sandbox/javascript/route.ts` muestran ejecucion
de codigo mediante `eval`. Es evidencia real de una frontera datos-a-codigo,
pero no demuestra escape del sandbox, control del proceso servidor, acceso a
secretos ni explotacion remota.

Clasificacion correcta: observado si; riesgo de diseno plausible; explotacion
confirmada no; induccion abstinente.

Forge debe separar presencia de una frontera peligrosa, controlabilidad de la
entrada y explotabilidad.

## 6. La induccion Python fallo al cargar el modulo

La hipotesis sobre `json.loads` en `tools/evolution_bundle.py:548` quedo como
plausible porque la carga del modulo en contexto de paquete fallo con:

`AttributeError: 'NoneType' object has no attribute '__dict__'`

Esto es una abstencion de infraestructura, no evidencia sobre la seguridad del
modulo.

Se necesita un loader de induccion que construya el contexto de paquete
correcto, use harnesses aislados de solo lectura y distinga “harness no
disponible” de “harness fallo”.

## 7. La comparacion historica debe comparar perimetros

La comparacion informo siete hallazgos previos, siete actuales y siete sin
cambios. Eso sirve como comparacion de entradas, pero el `coverage_delta` usa
un denominador trivial de 1 y no demuestra equivalencia de cobertura.

Las comparaciones futuras deben incluir hashes o versiones de revision del
repositorio, Forge, skills, manifest de scope, configuracion de agentes,
archivos auditables y harnesses disponibles.

## 8. Red-team y suite validan Forge, no `phylo`

Los resultados `8 passed` y `150 passed` prueban que las pruebas de Forge
pasaron. No prueban que `phylo` sea seguro ni que los siete hallazgos sean
explotables. Esta separacion debe conservarse en los informes HTML y en el
estado final.

## Backlog priorizado

### P0: necesario antes de llamar multiagente al modo

- Salidas independientes por agente.
- Ledger A-D-I por hipotesis.
- Revisor independiente con evidencia propia.
- Fallo cerrado si los resultados son protocolos genericos.
- Skills con obligaciones verificables.

### P1: calidad de hallazgos

- Data-flow multilinea para sanitizacion.
- Separacion entre patron, controlabilidad y explotabilidad.
- Loader seguro para induccion Python.
- Parser o analisis estructural real para JS/TS.
- Severidad basada en flujo de entrada y evidencia, no solo en familia AST.

### P2: comparacion y operacion

- Cobertura efectiva sobre el perimetro auditable.
- Comparacion historica con scope hash.
- Versionado de skills y contratos ejecutables.
- Metricas de independencia y desacuerdo entre agentes.
- Integracion o abstencion formal de ARGOS.

## Criterio de exito de la proxima corrida

La proxima corrida debe demostrar que cada agente produjo analisis materialmente
distinto, cada hipotesis tiene A-D-I propio, cada skill aplicada tiene evidencia
concreta, el revisor puede contradecir al coordinador y los artefactos permiten
reproducir quien decidio que y por que.
