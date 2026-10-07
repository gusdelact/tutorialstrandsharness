"""
Strands harness · 1 · MODELO Y RAZONAMIENTO
===========================================

El agente corre sobre un modelo, y puedes elegir cuál con un solo argumento.
Lo mejor: TODO lo demás del agente (tools, memoria, contexto, prompt) se queda
igual. Solo cambias el motor.

    create_harness(model="proveedor/nombre")

Formas de `model`:
    - "bedrock/..."     Amazon Bedrock  (el default si no pasas nada)
    - "anthropic/..."   Anthropic
    - "openai/..."      OpenAI
    - "google/..."      Google
    - "ollama/..."      modelos locales (sin API key)

Y con `effort` controlas cuánto "piensa" el modelo antes de responder:
    - "auto"   (default) el nivel recomendado por el proveedor
    - "low" / "medium" / "high"
    - "off"    sin razonamiento extendido

Credenciales según el proveedor
-------------------------------
    bedrock (default) : AWS_BEARER_TOKEN_BEDROCK  (o credenciales AWS)
    anthropic         : ANTHROPIC_API_KEY
    openai            : OPENAI_API_KEY
    google            : GEMINI_API_KEY
    ollama            : ninguna (corre `ollama serve` y `ollama pull llama3.1`)

Requisitos
----------
    pip install strands-harness

Uso:
    python 1_modelo_y_razonamiento.py
"""

from strands_harness import create_harness


def main() -> None:
    # Ejemplo A: nuestro modelo de Bedrock, pasado como id "pelón"
    # (sin prefijo de proveedor), que es una de las formas que acepta `model`.
    print("=== Agente con Claude Sonnet 4.5 en Bedrock ===")
    agente = create_harness(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")
    print(agente("Explica en una frase qué es un agente de IA."))

    # Ejemplo B: otro proveedor + razonamiento alto, cambiando SOLO el argumento.
    # (Descomenta si tienes credenciales de Anthropic en ANTHROPIC_API_KEY.)
    #
    # print("\n=== Mismo agente, otro motor: Anthropic con effort alto ===")
    # agente_anthropic = create_harness(
    #     model="anthropic/claude-sonnet-5",
    #     effort="high",
    # )
    # print(agente_anthropic("Explica en una frase qué es un agente de IA."))

    print(
        "\n[Idea] Cambiar de modelo es cambiar un argumento. El resto del "
        "andamiaje del agente no se toca."
    )


if __name__ == "__main__":
    main()
