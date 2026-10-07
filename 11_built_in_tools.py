"""
Strands harness · 11 · HERRAMIENTAS INTEGRADAS (built-in tools)
===============================================================

El agente ya trae, de fábrica y activadas, estas herramientas:

    shell                    ejecuta comandos de terminal
    read                     lee un archivo
    write                    crea/sobrescribe un archivo
    edit                     reemplaza un texto exacto dentro de un archivo
    web_fetch                lee una página web y la resume
    web_search               busca en la web
    programmatic_tool_caller el modelo escribe código que llama a otras tools
    subagent                 el ayudante general "generalist"

Puedes elegir cuáles quedan activas con `builtin_tools`:

    create_harness(builtin_tools=["read", "shell"])  # solo estas dos
    create_harness(builtin_tools=[])                 # ninguna (traes las tuyas)
    create_harness(builtin_tools={"subagent": False})# apaga solo el subagente

Un nombre desconocido falla al construir y te lista los válidos (no se traga
errores en silencio).

Detalles que conviene saber de algunas built-in:
    - `shell` es SIN estado: cada llamada es una terminal nueva. Si necesitas
      un directorio o variable, encadénalo en el mismo comando: `cd build && make`.
    - `read`/`write`/`edit` usan rutas ABSOLUTAS y rechazan `..`.
    - `web_fetch` no te devuelve la página cruda: la resume y te da la respuesta,
      para no inundar el contexto.

Este ejemplo crea un agente "de solo lectura/consulta": le dejamos leer archivos
y buscar en la web, pero le QUITAMOS shell, write y edit, así no puede modificar
nada en tu máquina.

Requisitos
----------
    pip install strands-harness
    export AWS_BEARER_TOKEN_BEDROCK="tu-bedrock-api-key"   # o credenciales AWS

Uso:
    python 11_built_in_tools.py
"""

from strands_harness import create_harness


def main() -> None:
    # Agente limitado: solo puede LEER archivos y LEER páginas web.
    # Sin shell, sin write, sin edit -> no puede cambiar nada en el disco.
    #
    # Nota: usamos 'web_fetch' (leer una URL) en vez de 'web_search' porque la
    # búsqueda web nativa depende del proveedor y Claude en Bedrock no la trae;
    # si pides 'web_search' explícitamente con un modelo que no la soporta, el
    # harness lanza un error (en vez de ignorarlo en silencio).
    agente = create_harness(
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        builtin_tools=["read", "web_fetch"],
        instructions=(
            "Eres un asistente de solo consulta. Puedes leer archivos y leer "
            "páginas web, pero no modificas nada."
        ),
    )

    print(
        "Agente creado SOLO con las tools 'read' y 'web_fetch'.\n"
        "No tiene shell, write ni edit, así que no puede modificar archivos.\n"
    )

    pregunta = "¿Qué herramientas tienes disponibles y cuáles NO para modificar archivos?"
    print(f"Usuario: {pregunta}\n")
    print(f"Agente: {agente(pregunta)}")

    print(
        "\n[Idea] Limitar las built-in es una forma simple de acotar lo que el "
        "agente puede hacer. Útil para un agente de consulta o análisis que no "
        "debe tocar tu sistema."
    )


if __name__ == "__main__":
    main()
