"""
Strands harness · 4a · SKILL: notas de versión
===============================================

Variante del ejemplo 4 que muestra UNA skill en concreto: `notas-de-version`.

La skill vive en `skills/notas-de-version/SKILL.md` y define el formato exacto de
unas release notes (secciones ✨ Nuevo / 🐛 Correcciones / ⚡ Mejoras). El agente
ve su descripción y carga sus instrucciones solo cuando la tarea encaja.

Recuerda (formato agentskills.io, igual que las Skills de Claude):
    - El modelo ve primero los METADATOS (name + description del front-matter).
    - Carga el CUERPO completo del SKILL.md solo cuando la tarea lo amerita.

Requisitos
----------
    pip install strands-harness
    export AWS_BEARER_TOKEN_BEDROCK="tu-bedrock-api-key"   # o credenciales AWS

Uso:
    python 4a_skill_notas_version.py
"""

import os

from strands_harness import create_harness


AQUI = os.path.dirname(os.path.abspath(__file__))
CARPETA_SKILLS = os.path.join(AQUI, "skills")
MODELO = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"


def main() -> None:
    # Apuntamos a la carpeta de skills. El agente elegirá 'notas-de-version'
    # porque la tarea (escribir release notes) encaja con su descripción.
    agente = create_harness(model=MODELO, skills=[CARPETA_SKILLS])

    tarea = (
        "Redacta las notas de versión para la v2.1.0: se añadió inicio de sesión "
        "con Google, se corrigió un error en el carrito y se mejoró la velocidad "
        "de carga."
    )
    print(f"Tarea: {tarea}\n")
    print(f"Agente: {agente(tarea)}")

    print(
        "\n[Idea] La skill 'notas-de-version' define el formato; el agente la "
        "cargó bajo demanda al reconocer que la tarea encaja con su descripción."
    )


if __name__ == "__main__":
    main()
