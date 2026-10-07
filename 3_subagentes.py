"""
Strands harness · 3 · SUBAGENTES
================================

Un subagente es un agente al que el agente principal puede llamar como si fuera
una herramienta. Sirve para delegar una subtarea autocontenida: el trabajo
intermedio del subagente NO ensucia la conversación principal; solo vuelve su
respuesta final.

Dos formas:

  1. Tus propios especialistas: creas un `Agent`, le pones nombre y descripción
     (eso le dice al principal cuándo usarlo) y lo pasas como tool con `.as_tool()`.

  2. El subagente integrado `generalist`: ya viene activado. Es un ayudante
     de propósito general que hereda la configuración del principal y corre en
     segundo plano. Úsalo para subtareas que inundarían el contexto (buscar en
     muchos archivos, exploración abierta) cuando solo te interesa la conclusión.

Este ejemplo muestra la forma 1: un especialista "traductor" que el agente
principal invoca cuando hace falta.

Requisitos
----------
    pip install strands-harness
    export AWS_BEARER_TOKEN_BEDROCK="tu-bedrock-api-key"   # o credenciales AWS

Uso:
    python 3_subagentes.py
"""

from strands import Agent
from strands_harness import create_harness


def main() -> None:
    # Un especialista. El `name` y la `description` son la "lógica de ruteo":
    # el agente principal decide usarlo leyendo esa descripción.
    traductor = Agent(
        name="traductor",
        description="Traduce texto a otro idioma con calidad profesional.",
        system_prompt=(
            "Eres traductor profesional. Devuelve solo la traducción, sin "
            "comentarios."
        ),
    )

    # El especialista entra como una tool más, vía .as_tool().
    agente = create_harness(
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        instructions=(
            "Eres un asistente que ayuda con textos. Cuando el usuario pida una "
            "traducción, delega en el especialista traductor."
        ),
        tools=[traductor.as_tool()],
    )

    pregunta = "¿Me traduces al inglés la frase 'más vale tarde que nunca'?"
    print(f"Usuario: {pregunta}\n")
    print(f"Agente: {agente(pregunta)}")

    print(
        "\n[Nota] Cada vez que se llama al subagente, este arranca con una "
        "conversación en blanco: no acumula estado entre llamadas. Y recuerda "
        "que el agente ya trae un subagente integrado, 'generalist', para "
        "subtareas de propósito general."
    )


if __name__ == "__main__":
    main()
