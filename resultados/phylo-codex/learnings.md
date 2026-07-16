# Aprendizajes de la corrida multiagente

El documento completo y versionable esta en
[`../../docs/phylo-codex-learnings.md`](../../docs/phylo-codex-learnings.md).

Resumen:

- Los ocho roles registrados no demostraron ocho analisis independientes.
- A-D-I fue registrado genericamente y debe pasar a ser por hipotesis.
- Las 20 skills fueron cargadas, pero no hay evidencia suficiente para
  llamarlas semanticamente aplicadas.
- El path handling de `save-run` es un caso prioritario de mejora de data-flow.
- `eval` y `JSON.parse` quedaron como observaciones, no vulnerabilidades
  confirmadas.
- La induccion Python quedo indeterminada por un fallo de carga de modulo.
- La comparacion historica debe incorporar perimetro y versiones de skills y
  agentes.
- Red-team y suite validan Forge, no la seguridad de `phylo`.
