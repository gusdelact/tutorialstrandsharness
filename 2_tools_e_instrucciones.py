"""
Strands harness · 2 · TOOLS E INSTRUCCIONES
===========================================

Dos perillas para adaptar el agente a tu caso:

  - `instructions`: le dicen QUIÉN es y PARA QUÉ sirve (su identidad y alcance).
    Se AÑADEN al system prompt afinado que ya trae el harness; no lo reemplazan.
    Por eso tú solo escribes lo específico de tu caso, no las reglas generales
    de "cómo comportarse como agente".

  - `tools`: le dan capacidades PROPIAS tuyas. Conviven con las built-in
    (shell, archivos, web). Se definen con el decorador `@tool`.

    create_harness(instructions="...", tools=[mi_tool])

Regla útil: el nombre de cada tool debe ser único. Si tu tool choca con una
built-in, el harness falla al construir y te dice cuáles chocaron (nada
desaparece en silencio).

Requisitos
----------
    pip install strands-harness
    export AWS_BEARER_TOKEN_BEDROCK="tu-bedrock-api-key"   # o credenciales AWS

Uso:
    python 2_tools_e_instrucciones.py
"""

from strands import tool
from strands_harness import create_harness


# Una tool propia. El docstring es importante: es lo que el modelo lee para
# saber cuándo y cómo usarla.
@tool
def estado_pedido(numero_pedido: str) -> str:
    """Consulta el estado de un pedido por su número.

    Args:
        numero_pedido: identificador del pedido, por ejemplo "PED-123".
    """
    pedidos = {
        "PED-123": "En camino, llega mañana.",
        "PED-456": "Entregado el lunes.",
        "PED-789": "Procesando, sale hoy.",
    }
    return pedidos.get(
        numero_pedido.upper().strip(),
        "No encontré ese pedido. Revisa el número.",
    )


def main() -> None:
    agente = create_harness(
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        # Identidad y alcance: lo específico de ESTE agente.
        instructions=(
            "Eres el asistente de una tienda en línea. Atiendes dudas sobre "
            "pedidos. Para consultar el estado de un pedido usa la herramienta "
            "estado_pedido. Sé breve y amable."
        ),
        # Nuestra tool se suma a las built-in del harness.
        tools=[estado_pedido],
    )

    pregunta = "Hola, ¿me dices cómo va mi pedido PED-123?"
    print(f"Usuario: {pregunta}\n")
    print(f"Agente: {agente(pregunta)}")


if __name__ == "__main__":
    main()
