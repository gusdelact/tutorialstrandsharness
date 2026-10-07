"""
Strands harness · 10c · MCP: servidor de SQLite (consultar una base de datos)
=============================================================================

Tercer ejemplo de MCP (ver también 10_mcp_servers.py y 10b_mcp_fetch.py).

Idea
----
Aquí el agente consulta una base de datos SQLite real a través de MCP: responde
preguntas en lenguaje natural traduciéndolas a SQL contra TUS datos, sin que tú
escribas una sola consulta. Es el ejemplo más "tangible" de MCP: conecta al
agente con un sistema real, no solo con archivos de texto.

Diferencia con los otros dos ejemplos de MCP
--------------------------------------------
En 10 (filesystem) y 10b (fetch) usamos servidores MCP ya hechos, descargados
con `uvx`. Aquí definimos NUESTRO PROPIO servidor MCP de sqlite, en este mismo
repo (archivo servidor_sqlite_mcp.py), por dos razones didácticas:

  1. Los servidores de sqlite publicados (mcp-server-sqlite, mcp-sqlite) usan una
     API vieja de la librería `mcp` y hoy fallan con las versiones nuevas. Un
     servidor propio con la API actual (FastMCP) evita ese problema.
  2. Así ves MCP desde los DOS lados: el servidor que EXPONE tools y el agente
     que las CONSUME. Antes solo habíamos visto el lado del cliente.

El servidor vive en `servidor_sqlite_mcp.py` (junto a este archivo) y expone dos
tools: `listar_tablas` y `consultar_sql`. Lo lanzamos con el mismo mecanismo
`mcp_servers={...}` del harness.

IMPORTANTE sobre el entorno
---------------------------
Corre en una TERMINAL (python 10c_mcp_sqlite.py). Los servidores MCP por stdio
no arrancan dentro de un notebook de Colab/Jupyter (limitación del kernel), por
eso los ejemplos de MCP son scripts.

Requisitos
----------
    pip install strands-harness
    export AWS_BEARER_TOKEN_BEDROCK="tu-bedrock-api-key"   # o credenciales AWS

Uso:
    python 10c_mcp_sqlite.py
"""

import os
import sqlite3
import sys

from strands_harness import create_harness


AQUI = os.path.dirname(os.path.abspath(__file__))
MODELO = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
DB = os.path.join(AQUI, "tienda.db")
SERVIDOR = os.path.join(AQUI, "servidor_sqlite_mcp.py")


def preparar_base() -> None:
    """Crea una base de datos de ejemplo con una tabla de productos."""
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS productos ("
        "sku TEXT PRIMARY KEY, nombre TEXT, precio REAL, stock INTEGER)"
    )
    cur.execute("DELETE FROM productos")
    cur.executemany(
        "INSERT INTO productos VALUES (?, ?, ?, ?)",
        [
            ("A-100", "Teclado", 199.0, 42),
            ("B-200", "Mouse", 49.5, 0),
            ("C-300", "Monitor", 1299.0, 7),
            ("D-400", "Audífonos", 349.0, 15),
        ],
    )
    con.commit()
    con.close()
    print(f"Base de datos lista con 4 productos.\n")


def main() -> None:
    preparar_base()

    # Lanzamos NUESTRO servidor MCP de sqlite (servidor_sqlite_mcp.py), pasándole
    # la ruta de la base como argumento. Mismo mecanismo mcp_servers del harness.
    agente = create_harness(
        model=MODELO,
        mcp_servers={
            "sqlite": {
                # sys.executable = el mismo Python que corre este script, para
                # que el servidor tenga disponibles los mismos paquetes.
                "command": sys.executable,
                "args": [SERVIDOR, DB],
            },
        },
    )

    pregunta = (
        "En la tabla productos, ¿cuál es el producto más caro y cuáles están "
        "agotados (stock 0)? Usa las herramientas de la base de datos y responde "
        "en una frase."
    )
    print(f"Usuario: {pregunta}\n")
    print(f"Agente: {agente(pregunta)}")

    print(
        "\n[Idea] El agente usó las tools de NUESTRO servidor MCP para consultar "
        "la base real. Viste MCP desde los dos lados: el servidor que expone las "
        "tools y el agente que las consume."
    )


if __name__ == "__main__":
    main()
