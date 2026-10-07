"""
Strands harness · 5 · PERSISTIR SESIONES
========================================

Una SESIÓN guarda una conversación en disco para poder RETOMARLA después,
aunque cierres el programa y lo vuelvas a abrir.

Las sesiones vienen activadas por defecto: si no das un id, cada agente arranca
con una conversación nueva bajo un id aleatorio. Si TÚ eliges el id, una
ejecución posterior rehidrata la MISMA conversación.

    create_harness(session={"id": "mi-charla"})

    Mismo id  -> retoma la conversación donde quedó.
    Nuevo id  -> empieza limpio.

Por defecto se guarda en ./.agent/sessions (puedes cambiarlo con
session={"id": "...", "dir": "..."}).

Cómo probarlo
-------------
Córrelo DOS veces. La primera siembra el contexto; la segunda hace una pregunta
de seguimiento que solo tiene sentido si recuerda lo anterior:

    python 5_sesiones.py     # 1ª vez: siembra
    python 5_sesiones.py     # 2ª vez: retoma la charla

Requisitos
----------
    pip install strands-harness
    export AWS_BEARER_TOKEN_BEDROCK="tu-bedrock-api-key"   # o credenciales AWS

Uso:
    python 5_sesiones.py
"""

from strands_harness import create_harness


ID_SESION = "clase-sesiones"


def main() -> None:
    # Mismo id -> misma conversación. El harness la retoma si ya existía.
    agente = create_harness(
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        session={"id": ID_SESION},
    )

    # ¿Es la primera vez con ESTA sesión? Si el harness rehidrató una
    # conversación previa con este id, el agente ya trae mensajes. Preguntar
    # por `agente.messages` es más fiable que mirar si existe una carpeta.
    es_primera_vez = len(agente.messages) == 0

    if es_primera_vez:
        print("[1ª vez] No hay sesión previa. Sembrando contexto...\n")
        mensaje = "Mi lenguaje de programación favorito es Python. Recuérdalo."
        print(f"Usuario: {mensaje}\n")
        print(f"Agente: {agente(mensaje)}")
        print("\n[Listo] Vuelve a ejecutar el script para ver cómo retoma la charla.")
    else:
        print("[2ª vez] Retomando la conversación guardada...\n")
        # "mi lenguaje favorito" solo tiene sentido si recordó la 1ª corrida.
        mensaje = "¿Cuál dije que era mi lenguaje de programación favorito?"
        print(f"Usuario: {mensaje}\n")
        print(f"Agente: {agente(mensaje)}")


if __name__ == "__main__":
    main()
