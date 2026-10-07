"""
Strands harness · 10b · MCP: servidor de FETCH (traer páginas web)
==================================================================

Segundo ejemplo de MCP (ver también 10_mcp_servers.py, que usa filesystem).

Idea
----
El servidor MCP `fetch` le da al agente la capacidad de hacer peticiones web:
traer una URL y devolver su contenido como texto. Es un buen complemento, porque
Claude en Bedrock no trae búsqueda web nativa; aquí el acceso a la web llega
desde un servidor MCP externo, no desde una tool nativa del modelo.

El harness se conecta con el mismo formato `mcpServers` de cualquier cliente MCP
y añade las tools que descubra (aquí, una tool `fetch`).

    create_harness(mcp_servers={"fetch": {"command": "uvx", "args": ["mcp-server-fetch"]}})

IMPORTANTE sobre el entorno
---------------------------
Este script corre en una TERMINAL (python 10b_mcp_fetch.py), que es donde los
servidores MCP por stdio arrancan bien. Dentro de un notebook de Colab/Jupyter
NO arrancan (el kernel no expone stderr.fileno()); por eso los ejemplos de MCP
viven como scripts, no como celdas de notebook.

Requisitos
----------
    pip install strands-harness
    # uv/uvx instalado (para descargar y correr el servidor fetch)
    export AWS_BEARER_TOKEN_BEDROCK="tu-bedrock-api-key"   # o credenciales AWS

Uso:
    python 10b_mcp_fetch.py
"""

from strands_harness import create_harness


MODELO = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"


def main() -> None:
    # Config MCP inline: el servidor fetch se descarga y corre con uvx.
    # Mismo formato que pondrías en un mcp.json.
    agente = create_harness(
        model=MODELO,
        mcp_servers={
            "fetch": {
                "command": "uvx",
                "args": ["mcp-server-fetch"],
            },
        },
    )

    tarea = (
        "Trae la página https://example.com usando las herramientas disponibles "
        "y dime en una frase de qué trata."
    )
    print(f"Tarea: {tarea}\n")
    print(f"Agente: {agente(tarea)}")

    print(
        "\n[Idea] El agente ganó acceso web desde un servidor MCP externo. "
        "La tool `fetch` se usa igual que cualquier tool local del harness."
    )


if __name__ == "__main__":
    main()
