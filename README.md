# Curso: agentes con Strands harness

Ejemplos para aprender **Strands harness** desde cero, sin conocimientos previos.
Siguen el orden de la [documentación oficial](https://strandsagents.com/docs/user-guide/harness/)
y cada archivo enseña **un concepto** con el mínimo de código.

## ¿Qué es Strands harness?

Un agente de IA completo que creas con **una sola línea**:

```python
from strands_harness import create_harness
agente = create_harness()
agente("Investiga X y escríbelo en un archivo")
```

No tienes que ensamblar nada. El agente ya viene con buenos defaults: un modelo,
un system prompt afinado, herramientas de shell/archivos/web, gestión de
contexto, memoria y sesiones. Tú solo cambias las perillas que te interesen.

Cada perilla se activa con **un argumento** de `create_harness(...)`. Ese es el
hilo conductor del curso.

## Los ejemplos (en orden)

| # | Archivo | Concepto | Argumento clave |
|---|---------|----------|-----------------|
| 0 | `0_hola_agente.py` | El agente en una línea | — |
| 1 | `1_modelo_y_razonamiento.py` | Elegir modelo y cuánto "piensa" | `model`, `effort` |
| 2 | `2_tools_e_instrucciones.py` | Darle identidad y capacidades propias | `instructions`, `tools` |
| 3 | `3_subagentes.py` | Delegar en agentes especialistas | `tools=[agente.as_tool()]` |
| 4 | `4_agent_skills.py` | Paquetes de instrucciones (`SKILL.md`): el agente elige entre varias | `skills` |
| 4a | `4a_skill_notas_version.py` | Variante: solo la skill `notas-de-version` | `skills` |
| 4b | `4b_skill_documentar_agente.py` | Variante: solo la skill `documentar-agente-strands` | `skills` |
| 4c | `4c_skill_business_canvas.py` | Variante: solo la skill `business-model-canvas` | `skills` |
| 5 | `5_sesiones.py` | Retomar una conversación tras reiniciar | `session={"id": ...}` |
| 6 | `6_memoria_largo_plazo.py` | Recordar hechos entre conversaciones | `memory` |
| 7 | `7_sesion_vs_memoria.py` | La diferencia (¡la confusión típica!) | — (conceptual) |
| 8 | `8_contexto_y_cache.py` | Que la charla larga no desborde ni cueste de más | `context_manager`, `caching` |
| 9 | `9_interventions.py` | Pedir aprobación antes de acciones riesgosas | `interventions` |
| 10 | `10_mcp_servers.py` | Conectar herramientas externas (MCP): filesystem | `mcp_servers` |
| 10b | `10b_mcp_fetch.py` | MCP: servidor `fetch` (traer páginas web) | `mcp_servers` |
| 10c | `10c_mcp_sqlite.py` | MCP: servidor de SQLite propio (consultar una BD) | `mcp_servers` |
| 11 | `11_built_in_tools.py` | Elegir/limitar las herramientas de fábrica | `builtin_tools` |
| 12 | `12_shell.py` | La tool `shell` con `mkdir`, `cat`, `mv`, `rm`, `rmdir` | `shell` (built-in) |

> **Agent Skills y el `SKILL.md`:** el ejemplo 4 usa el formato
> [agentskills.io](https://agentskills.io), el **mismo** que las Skills de Claude
> y otros agentes: un `SKILL.md` con front-matter (nombre + descripción) que el
> modelo ve primero y cuyas instrucciones carga solo cuando la tarea encaja.
>
> La carpeta `skills/` trae **tres** skills de muestra:
> - `notas-de-version` — redacta release notes con un formato fijo.
> - `documentar-agente-strands` — documenta un agente de Strands harness.
> - `business-model-canvas` — genera un lienzo de modelo de negocio (9 bloques).
>
> `4_agent_skills.py` muestra cómo el agente **elige** la skill correcta entre
> las tres según la descripción. Los archivos `4a`/`4b`/`4c` aíslan cada skill,
> útil para explicarlas de una en una.

> **Ejemplos de MCP (`10`, `10b`, `10c`):** conectan al agente con herramientas
> externas vía `mcp_servers`. `10` usa el servidor de filesystem, `10b` el de
> fetch (ambos descargados con `uvx`/`npx`), y `10c` lanza un **servidor MCP
> propio** de SQLite (`servidor_sqlite_mcp.py`) para ver MCP desde los dos lados:
> el servidor que expone tools y el agente que las consume. Importante: los
> servidores MCP por stdio funcionan en **terminal**, no dentro de un notebook de
> Colab/Jupyter (limitación del kernel), por eso son scripts.

## Requisitos

```bash
pip install strands-harness
```

El agente usa **Amazon Bedrock**. Todos los ejemplos fijan el modelo
`us.anthropic.claude-sonnet-4-5-20250929-v1:0` en la llamada a
`create_harness(model=...)`. Dale credenciales:

```bash
export AWS_BEARER_TOKEN_BEDROCK="tu-bedrock-api-key"   # o credenciales AWS
export AWS_REGION="us-east-1"
```

Habilita el acceso a ese modelo en la consola de Bedrock (Model access). Si usas
otro modelo, cambia el id en el `create_harness(model=...)` de cada archivo.
Los ejemplos de MCP necesitan además: **Node.js** (`npx`) para el 10 (filesystem)
y **uv/uvx** para el 10b (fetch). El 10c (SQLite) usa un servidor propio en
Python, sin descargas extra.

## Cómo ejecutar

Cada archivo es independiente:

```bash
python 0_hola_agente.py
python 1_modelo_y_razonamiento.py
python 2_tools_e_instrucciones.py
python 3_subagentes.py
python 4_agent_skills.py        # el agente elige entre varias skills
python 4a_skill_notas_version.py       # solo notas-de-version
python 4b_skill_documentar_agente.py   # solo documentar-agente-strands
python 4c_skill_business_canvas.py     # solo business-model-canvas
python 5_sesiones.py            # ejecútalo DOS veces para ver la sesión
python 6_memoria_largo_plazo.py
python 7_sesion_vs_memoria.py   # explicación conceptual (no llama al modelo)
python 8_contexto_y_cache.py
python 9_interventions.py       # mejor en una terminal interactiva
python 10_mcp_servers.py        # MCP filesystem (requiere Node.js/npx)
python 10b_mcp_fetch.py         # MCP fetch (requiere uv/uvx)
python 10c_mcp_sqlite.py        # MCP sqlite con servidor propio
python 11_built_in_tools.py
python 12_shell.py              # usa shell en una carpeta temporal aislada
```

## Avisos

- Este agente trae **shell y file tools reales** y las usa. Varios ejemplos
  crean archivos o carpetas: `0`/`4b` escriben archivos, `5`/`6` usan `./.agent/`,
  y `10c` genera `tienda.db`. Ejecútalos en una carpeta donde eso no te moleste.
- El ejemplo 9 (`interventions`) es el freno de mano para acciones riesgosas;
  pruébalo en una terminal interactiva para ver cómo pide aprobación.

## ¿Y después? (más control con el SDK)

Lo que `create_harness()` te devuelve es un agente estándar de Strands. Cuando
quieras controlar cada pieza a mano (en vez de usar los defaults), existe el
**Strands Harness SDK**, la capa de más abajo. Pero para empezar, no hace falta:
con el harness ya puedes construir agentes útiles. Dejamos el SDK para más
adelante.
