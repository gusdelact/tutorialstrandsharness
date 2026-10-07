"""
Strands harness · 6 · MEMORIA DE LARGO PLAZO
=============================================

La memoria de largo plazo deja que el agente recuerde HECHOS durables entre
conversaciones distintas, sin que se los vuelvas a decir.

Viene activada por defecto. Por debajo, el harness:
    - destila hechos importantes de la conversación en archivos (en ./.agent/memory)
    - antes de cada turno busca ahí y mete en el contexto lo más relevante
    - te da además una herramienta `search_memory` para buscar a propósito
    - hace la extracción en segundo plano, con un modelo pequeño (cuesta poco)

    create_harness()                       # memoria ON por defecto
    create_harness(memory=False)           # apagarla
    create_harness(memory={"dir": "..."})  # cambiar dónde se guarda

Importante: la memoria son archivos independientes de las sesiones, así que
sobrevive aunque las sesiones estén apagadas y vale entre charlas no relacionadas.

Un detalle práctico (flush)
---------------------------
La extracción corre en segundo plano, así que una corrida muy corta puede
terminar antes de escribir lo último. Usar el agente como context manager
(`with ... as agente:`) asegura que al salir del bloque se vacíe lo pendiente.

Requisitos
----------
    pip install strands-harness
    export AWS_BEARER_TOKEN_BEDROCK="tu-bedrock-api-key"   # o credenciales AWS

Uso:
    python 6_memoria_largo_plazo.py
"""

from strands_harness import create_harness


def main() -> None:
    # Memoria activada por defecto. Usamos `with` para que, al salir, el agente
    # vacíe a disco cualquier hecho pendiente de guardar.
    with create_harness(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0") as agente:
        # Le damos un dato durable sobre el usuario.
        m1 = "Para que lo tengas presente: soy alérgico a los cacahuates."
        print(f"Usuario: {m1}\n")
        print(f"Agente: {agente(m1)}\n")

        # Una tarea donde ese hecho debería influir, aunque no lo repitamos.
        m2 = "Sugiéreme un snack para llevar al cine."
        print(f"Usuario: {m2}\n")
        print(f"Agente: {agente(m2)}")

    print(
        "\n[Idea] El dato de la alergia queda en ./.agent/memory. En una charla "
        "FUTURA y distinta, el agente puede recordarlo sin que se lo repitas. "
        "Eso es lo que distingue a la memoria de una sesión."
    )


if __name__ == "__main__":
    main()
