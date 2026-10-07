"""
Strands harness · 4 · AGENT SKILLS
==================================

Las Agent Skills son "paquetes de instrucciones" reutilizables que el agente
carga SOLO cuando los necesita. Cada skill es una carpeta con un archivo
`SKILL.md`.

¿Te suena? Es el mismo formato (agentskills.io) que usan Claude y otros agentes:
el modelo ve primero los METADATOS de la skill (nombre + descripción en el
front-matter) y carga las INSTRUCCIONES completas solo cuando una tarea la
amerita. Así no gastas contexto en instrucciones que quizá no se usen.

Dónde busca el agente:
    - Por defecto escanea ./.agent/skills
    - O le pasas tú las carpetas: create_harness(skills=["./mis-skills"])
    - skills=None lo apaga

Un skill en disco se ve así:

    mis-skills/
      notas-de-version/
        SKILL.md          <- front-matter (name, description) + instrucciones

Este ejemplo apunta el agente a la carpeta `skills/` que está junto a este
archivo (ya trae una skill de ejemplo: "notas-de-version").

Requisitos
----------
    pip install strands-harness
    export AWS_BEARER_TOKEN_BEDROCK="tu-bedrock-api-key"   # o credenciales AWS

Uso:
    python 4_agent_skills.py
"""

import os

from strands_harness import create_harness


# Carpeta de skills junto a este archivo (independiente de dónde ejecutes).
AQUI = os.path.dirname(os.path.abspath(__file__))
CARPETA_SKILLS = os.path.join(AQUI, "skills")


def main() -> None:
    # Apuntamos el agente a nuestra carpeta de skills. Hay VARIAS skills ahí
    # (documentar-agente-strands, business-model-canvas, notas-de-version);
    # el agente ve solo sus descripciones y carga la que encaje con la tarea.
    agente = create_harness(
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        skills=[CARPETA_SKILLS],
    )

    # Esta tarea encaja con la skill "documentar-agente-strands".
    tarea = (
        "Documenta este agente de Strands harness: se crea con "
        "create_harness(model='us.anthropic.claude-sonnet-4-5-20250929-v1:0', "
        "instructions='Eres un asistente de soporte de una tienda; atiende dudas "
        "de pedidos', tools=[estado_pedido], interventions='ask'). La tool "
        "estado_pedido consulta el estado de un pedido por su número. Genera su "
        "documentación."
    )
    print(f"Tarea: {tarea}\n")
    print(f"Agente: {agente(tarea)}")

    print(
        "\n[Idea] El agente eligió la skill 'documentar-agente-strands' entre "
        "varias, por su descripción, y cargó sus instrucciones bajo demanda: "
        "igual que las Skills de Claude (metadatos primero, cuerpo solo cuando "
        "hace falta). Prueba otra tarea (p. ej. 'hazme un business model canvas "
        "de una cafetería') y cargará OTRA skill."
    )


if __name__ == "__main__":
    main()
