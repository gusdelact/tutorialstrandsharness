"""
Strands harness · 9 · APROBAR LLAMADAS A TOOLS (interventions)
==============================================================

Una "intervención" decide si una llamada a herramienta se ejecuta o no. Por
defecto NO hay ninguna: todas las llamadas proceden. Con `interventions` pones
un guardia que pide aprobación (o aplica una política) antes de ejecutar.

Formas de `interventions`:
    - "ask"                      pide aprobación para CADA llamada a tool
    - "smart"                    un clasificador marca solo las llamadas riesgosas
    - "<regla en lenguaje natural>"  tú describes qué vigilar; el modelo juzga
      cada llamada contra tu regla y escala las que la cumplan
    - "<archivo>.cedar"          una política Cedar (autorización programática)

    create_harness(interventions="ask")
    create_harness(interventions="Pide permiso antes de borrar archivos.")

Por qué importa: el agente por defecto puede correr comandos de shell y editar
archivos. Las interventions son el freno de mano para que no haga algo
irreversible sin tu visto bueno. Además, el subagente integrado hereda esta
política, así que no puede saltarse el guardia.

Cómo se ve al ejecutar
----------------------
Cuando una llamada queda "gated", el agente se detiene y pide tu aprobación.
En una terminal interactiva responderás a esa solicitud; en este ejemplo lo
importante es VER que el agente se frena a pedir permiso en vez de actuar directo.

Requisitos
----------
    pip install strands-harness
    export AWS_BEARER_TOKEN_BEDROCK="tu-bedrock-api-key"   # o credenciales AWS

Uso (mejor en una terminal interactiva):
    python 9_interventions.py
"""

from strands_harness import create_harness


def main() -> None:
    # Regla en lenguaje natural: el agente pedirá permiso antes de acciones
    # destructivas o de red, pero no para cosas inofensivas (leer, listar).
    agente = create_harness(
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        interventions="Pide aprobación antes de borrar archivos o ejecutar comandos de shell.",
    )

    print(
        "Agente creado con una política de aprobación.\n"
        "Si le pides una acción riesgosa (p. ej. borrar algo), debería "
        "detenerse a pedir permiso en lugar de hacerlo directo.\n"
    )

    # Una tarea inofensiva: no debería requerir aprobación.
    print("--- Tarea inofensiva (no debería pedir permiso) ---")
    print(agente("¿Qué día es hoy?"))

    print(
        "\n[Prueba tú] En una terminal interactiva, pídele algo como "
        "'borra el archivo temp.txt' y observa cómo pide aprobación.\n"
        "Alternativas: interventions='ask' (pide para TODO) o "
        "interventions='smart' (solo lo riesgoso)."
    )


if __name__ == "__main__":
    main()
