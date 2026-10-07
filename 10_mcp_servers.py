"""
Strands harness · 10 · CONECTAR SERVIDORES MCP
==============================================

MCP (Model Context Protocol) deja que el agente use herramientas servidas por
un servidor externo. El harness se conecta a esos servidores a partir de una
config `mcpServers` con el MISMO formato que usan otros clientes MCP, y añade
TODAS las herramientas que descubra a la lista de tools del agente.

`mcp_servers` acepta:
    - la ruta a un archivo JSON:   create_harness(mcp_servers="./mcp.json")
    - o el mapping directamente (inline), como en este ejemplo

Formato (igual que el de otros clientes MCP):
    {
      "nombre_servidor": {
        "command": "...",
        "args": ["...", "..."]
      }
    }

Robustez: si un servidor falla al arrancar, por defecto el harness simplemente
no obtiene sus tools (no se cae). Y si dos servidores exponen una tool con el
mismo nombre, puedes ponerle un "prefix" a uno en la config para que no choquen.

Este ejemplo conecta el servidor MCP de sistema de archivos (vía npx) y le pide
al agente que lo use. Necesitas Node.js instalado (para `npx`).

Requisitos
----------
    pip install strands-harness
    # Node.js instalado (para npx)
    export AWS_BEARER_TOKEN_BEDROCK="tu-bedrock-api-key"   # o credenciales AWS

Uso:
    python 10_mcp_servers.py
"""

from strands_harness import create_harness


def main() -> None:
    # Config MCP inline: un servidor de archivos que opera sobre el directorio
    # actual ("."). Es el mismo formato que pondrías en un mcp.json.
    agente = create_harness(
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        mcp_servers={
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
            },
        },
    )

    tarea = "Lista los archivos de este proyecto usando las herramientas disponibles."
    print(f"Tarea: {tarea}\n")
    print(f"Agente: {agente(tarea)}")

    print(
        "\n[Idea] El agente ahora tiene, además de sus tools built-in, las que "
        "expone el servidor MCP de archivos. Para él, una tool de MCP se usa "
        "igual que una tool local."
    )


if __name__ == "__main__":
    main()
