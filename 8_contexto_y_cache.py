"""
Strands harness · 8 · CONTEXTO Y CACHÉ
======================================

Dos defaults que mantienen una conversación larga coherente y barata. Los dos
vienen activados y, para el caso común, no necesitas configurar nada.

1) GESTIÓN DE CONTEXTO
   El modelo solo puede leer cierta cantidad de texto a la vez (su "ventana de
   contexto"). Conforme la charla crece, el agente:
     - resume los turnos viejos para no desbordar la ventana, y
     - "descarga" los resultados de herramienta muy grandes: deja un resumen
       corto + una referencia, y guarda el contenido completo aparte, que el
       agente recupera con `retrieve_context` solo si de verdad lo necesita.

   Opción: context_manager = "auto" (default) | "agentic" | off

2) CACHÉ DE PROMPTS (prompt caching)
   Reutiliza las partes del mensaje que NO cambian entre turnos (el system
   prompt, las definiciones de tools, la conversación previa). Eso hace que el
   prefijo estable de una charla larga sea más rápido y barato de procesar.

   Opción: caching = True (default) | False
   (En OpenAI/Google el caché es automático del lado del servidor; en Bedrock y
    Anthropic el harness lo configura por ti.)

Para los alumnos: lo importante es ENTENDER que estas dos cosas ya ocurren solas.
Casi nunca las vas a tocar; se muestran aquí para que sepan que existen.

Requisitos
----------
    pip install strands-harness
    export AWS_BEARER_TOKEN_BEDROCK="tu-bedrock-api-key"   # o credenciales AWS

Uso:
    python 8_contexto_y_cache.py
"""

from strands_harness import create_harness


def main() -> None:
    # Caso común: no tocas contexto ni caché (ya están activos). Solo fijamos
    # el modelo que vamos a usar.
    agente = create_harness(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

    print("Agente creado con los defaults: contexto 'auto' y caché activada.\n")

    # Una charla normal; por debajo, el harness ya gestiona la ventana y cachea
    # el prefijo estable entre turnos.
    print(agente("En una frase, ¿para qué sirve gestionar la ventana de contexto?"))

    print(
        "\n--- Variantes de configuración (solo referencia) ---\n"
        '  create_harness(context_manager="agentic")  # otra estrategia\n'
        "  create_harness(context_manager=False)      # apagar gestión de contexto\n"
        "  create_harness(caching=False)              # apagar la caché\n"
        "\n[Idea] Son defaults 'production-ready': normalmente no los tocas."
    )


if __name__ == "__main__":
    main()
