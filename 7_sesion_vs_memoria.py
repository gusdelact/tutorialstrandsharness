"""
Strands harness · 7 · SESIÓN vs. MEMORIA DE LARGO PLAZO
=======================================================

Esta es la confusión más común, así que vale la pena dejarla clarísima. El
agente tiene DOS formas de "recordar", y responden a preguntas distintas:

    SESIÓN (checkpoint)                 MEMORIA DE LARGO PLAZO
    -------------------                 ----------------------
    Reanuda UNA conversación            Lleva HECHOS entre conversaciones
    concreta tras reiniciar.            distintas (no relacionadas).
    Se reproduce solo cuando            Se consulta SIEMPRE, en toda
    retomas ese id.                     charla, con o sin sesión.
    create_harness(session={"id":...})  create_harness()  (ya viene ON)

Son independientes (ortogonales). Puedes tener:

    ninguno    -> tarea de una sola vez, sin dejar rastro
                  create_harness(session=False, memory=False)
    solo sesión-> retomar una tarea, pero sin recordar entre tareas
    solo memoria-> recordar hechos, pero sin reanudar una charla concreta
    ambos      -> una tarea reanudable Y con conocimiento acumulado
                  create_harness(session={"id": ...})   # memoria ON por defecto

Analogía rápida:
    - La SESIÓN es como guardar la partida de un videojuego: continúas ESA
      partida justo donde la dejaste.
    - La MEMORIA es como lo que el agente "aprende de ti" y aplica en cualquier
      partida nueva.

Tabla de decisión (de la documentación):

    ¿Quieres...?                                   Usa          Cómo
    reanudar una tarea donde la dejaste            sesión       session={"id": ...}
    llevar hechos entre tareas distintas           memoria      (ON por defecto)
    las dos cosas                                  ambas        session={"id": ...} + memoria ON
    una tarea sin dejar rastro                     ninguna      session=False, memory=False

Este archivo no ejecuta un agente: es la explicación conceptual con ejemplos de
configuración. Para verlos en acción, corre `5_sesiones.py` y
`6_memoria_largo_plazo.py`.

Requisitos
----------
    pip install strands-harness
"""

from strands_harness import create_harness


def ejemplos_de_configuracion():
    """Las cuatro combinaciones, solo como referencia (no se invocan)."""

    modelo = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"

    # 1) Ninguno: tarea de una sola vez, sin dejar rastro en disco.
    _sin_rastro = lambda: create_harness(model=modelo, session=False, memory=False)

    # 2) Solo sesión: reanuda esta charla, pero no recuerda entre tareas.
    _solo_sesion = lambda: create_harness(model=modelo, session={"id": "mi-tarea"}, memory=False)

    # 3) Solo memoria: recuerda hechos, sin reanudar una charla concreta.
    _solo_memoria = lambda: create_harness(model=modelo, session=False)  # memoria ON por defecto

    # 4) Ambas: tarea reanudable y con conocimiento acumulado.
    _ambas = lambda: create_harness(model=modelo, session={"id": "mi-tarea"})  # memoria ON

    return _sin_rastro, _solo_sesion, _solo_memoria, _ambas


def main() -> None:
    print(__doc__)
    print(
        "Resumen de una frase:\n"
        "  - SESIÓN = continuar ESTA conversación.\n"
        "  - MEMORIA = recordar hechos en CUALQUIER conversación."
    )


if __name__ == "__main__":
    main()
