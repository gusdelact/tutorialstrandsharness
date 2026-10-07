"""
Servidor MCP de SQLite (para el ejemplo 10c)
============================================

Este archivo NO se ejecuta directamente por el alumno: lo lanza 10c_mcp_sqlite.py
como servidor MCP. Muestra el OTRO lado de MCP: cómo se escribe un servidor que
EXPONE herramientas para que un agente las consuma.

Está escrito con la API actual del SDK de MCP (mcp 2.x), donde el servidor es
`MCPServer` (antes se llamaba FastMCP). Define dos tools sencillas sobre una base
SQLite:

    - listar_tablas()        -> qué tablas hay y sus columnas
    - consultar_sql(sql)     -> ejecuta un SELECT y devuelve las filas

Recibe la ruta de la base como primer argumento de línea de comandos y habla por
stdio (el transporte estándar de MCP para procesos locales).

Uso (lo hace 10c por ti):
    python servidor_sqlite_mcp.py /ruta/a/tienda.db
"""

import sqlite3
import sys

from mcp.server.mcpserver import MCPServer


# Ruta de la base: primer argumento de línea de comandos.
DB = sys.argv[1] if len(sys.argv) > 1 else "tienda.db"

servidor = MCPServer(name="sqlite")


@servidor.tool()
def listar_tablas() -> str:
    """Lista las tablas de la base de datos y las columnas de cada una."""
    con = sqlite3.connect(DB)
    try:
        tablas = con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        lineas = []
        for (nombre,) in tablas:
            cols = con.execute(f"PRAGMA table_info({nombre})").fetchall()
            nombres = ", ".join(c[1] for c in cols)
            lineas.append(f"{nombre}({nombres})")
        return "\n".join(lineas) if lineas else "No hay tablas."
    finally:
        con.close()


@servidor.tool()
def consultar_sql(sql: str) -> str:
    """Ejecuta una consulta SQL de solo lectura (SELECT) y devuelve las filas.

    Args:
        sql: una sentencia SELECT. No se permiten escrituras.
    """
    # Guardarraíl simple: solo SELECT (este servidor es de solo lectura).
    if not sql.strip().lower().startswith("select"):
        return "Solo se permiten consultas SELECT."
    con = sqlite3.connect(DB)
    try:
        cur = con.execute(sql)
        columnas = [d[0] for d in cur.description] if cur.description else []
        filas = cur.fetchall()
        if not filas:
            return "Sin resultados."
        encabezado = " | ".join(columnas)
        cuerpo = "\n".join(" | ".join(str(v) for v in fila) for fila in filas)
        return f"{encabezado}\n{cuerpo}"
    except sqlite3.Error as e:
        return f"Error de SQL: {e}"
    finally:
        con.close()


if __name__ == "__main__":
    # Habla por stdio: así lo lanza el harness como servidor MCP.
    servidor.run(transport="stdio")
