---
name: documentar-agente-strands
description: Genera la documentación de un agente construido con Strands harness (create_harness). Úsala cuando el usuario pida documentar, describir o escribir el README de un agente de Strands, o explicar su configuración (modelo, instructions, tools, memoria, sesiones, interventions, MCP).
---

# Cómo documentar un agente de Strands harness

Cuando el usuario pida documentar un agente de Strands, produce un documento en
Markdown con EXACTAMENTE estas secciones, en este orden. Omite una sección solo
si el agente no usa esa capacidad.

## Formato de salida

```
# Agente: <nombre del agente>

## Propósito
<1-2 frases: qué resuelve y para quién>

## Configuración (create_harness)
| Parámetro | Valor | Nota |
|-----------|-------|------|
| model | <id o "provider/name"> | <proveedor> |
| effort | <auto/low/medium/high/off> | razonamiento |
| instructions | <resumen de la identidad/alcance> | se añade al prompt del harness |
| session | <id / False> | reanudar conversación |
| memory | <on / off / dir> | hechos entre conversaciones |
| context_manager | <auto/agentic/off> | gestión de ventana |
| interventions | <ask/smart/regla/cedar/—> | gate de aprobación |

## Herramientas
### Built-in activas
<lista de builtin_tools: shell, read, write, edit, web_fetch, web_search, programmatic_tool_caller, subagent>
### Tools propias
<por cada @tool: nombre, qué hace, parámetros>
### Servidores MCP
<por cada servidor en mcp_servers: nombre, qué expone>

## Subagentes
<generalist y/o especialistas con as_tool(): nombre + cuándo se usa>

## Agent Skills
<skills cargadas, si las hay>

## Cómo ejecutarlo
<comando + variables de entorno necesarias (credenciales del proveedor)>

## Consideraciones de seguridad
<qué puede tocar el agente (shell/archivos), gates aplicados, datos sensibles>
```

## Reglas

1. Rellena cada fila/sección a partir de la información o el código que te dé el usuario. Si falta un dato, escribe `(no especificado)` en vez de inventarlo.
2. Para el modelo, indica el proveedor cuando se pueda deducir del id (p. ej. un id que empieza con `us.anthropic...` es Amazon Bedrock).
3. En "Herramientas", recuerda la distinción: las built-in vienen del harness; las propias se definen con `@tool`; las MCP las aporta un servidor externo vía `mcp_servers`.
4. En "Consideraciones de seguridad", si el agente tiene `shell`, `write` o `edit` activas, menciónalo explícitamente y señala si hay `interventions` que lo acoten.
5. Sé conciso y técnico. No repitas el código completo; descríbelo.
6. Si el usuario te da el archivo .py del agente, léelo y extrae los valores reales de `create_harness(...)` en vez de suponerlos.
