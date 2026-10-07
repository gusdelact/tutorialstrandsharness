"""
Strands harness · 4b · SKILL: documentar un agente de Strands
=============================================================

Variante del ejemplo 4 que muestra la skill `documentar-agente-strands`.

La skill vive en `skills/documentar-agente-strands/SKILL.md` y define cómo
documentar un agente construido con `create_harness`: propósito, tabla de
configuración, herramientas (built-in / propias / MCP), subagentes, seguridad...

Le pasamos al agente la descripción de un agente de Strands (su configuración)
y la skill guía la redacción de la documentación con un formato consistente.

Requisitos
----------
    pip install strands-harness
    export AWS_BEARER_TOKEN_BEDROCK="tu-bedrock-api-key"   # o credenciales AWS

Uso:
    python 4b_skill_documentar_agente.py
"""

import os

from strands_harness import create_harness


AQUI = os.path.dirname(os.path.abspath(__file__))
CARPETA_SKILLS = os.path.join(AQUI, "skills")
MODELO = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"


def main() -> None:
    # El agente elegirá 'documentar-agente-strands' porque la tarea pide
    # documentar un agente de Strands harness.
    agente = create_harness(model=MODELO, skills=[CARPETA_SKILLS])

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
        "\n[Idea] La skill 'documentar-agente-strands' impone un formato de "
        "documentación (propósito, configuración, herramientas, seguridad). El "
        "agente la cargó al reconocer que la tarea encaja con su descripción."
    )


if __name__ == "__main__":
    main()
