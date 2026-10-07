"""
Strands harness · 4c · SKILL: business model canvas
====================================================

Variante del ejemplo 4 que muestra la skill `business-model-canvas`.

La skill vive en `skills/business-model-canvas/SKILL.md` y define los nueve
bloques del modelo de negocio de Osterwalder (segmentos, propuesta de valor,
canales, relación con clientes, ingresos, recursos, actividades, socios,
costos) más un resumen final.

Le describimos un negocio al agente y la skill guía la generación del lienzo
completo con un formato consistente.

Requisitos
----------
    pip install strands-harness
    export AWS_BEARER_TOKEN_BEDROCK="tu-bedrock-api-key"   # o credenciales AWS

Uso:
    python 4c_skill_business_canvas.py
"""

import os

from strands_harness import create_harness


AQUI = os.path.dirname(os.path.abspath(__file__))
CARPETA_SKILLS = os.path.join(AQUI, "skills")
MODELO = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"


def main() -> None:
    # El agente elegirá 'business-model-canvas' porque la tarea pide un
    # modelo de negocio / lienzo.
    agente = create_harness(model=MODELO, skills=[CARPETA_SKILLS])

    tarea = (
        "Hazme un business model canvas de una cafetería de especialidad en una "
        "zona universitaria."
    )
    print(f"Tarea: {tarea}\n")
    print(f"Agente: {agente(tarea)}")

    print(
        "\n[Idea] La skill 'business-model-canvas' impone los nueve bloques de "
        "Osterwalder. El agente la cargó al reconocer que la tarea encaja con su "
        "descripción."
    )


if __name__ == "__main__":
    main()
