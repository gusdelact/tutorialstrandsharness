"""
Strands harness · 12 · LA HERRAMIENTA SHELL (mkdir, cat, mv, rm, rmdir)
=======================================================================

La herramienta `shell` (una de las built-in) deja que el agente ejecute comandos
de terminal. Aquí la vemos con los comandos clásicos de archivos:

    mkdir   crear carpeta
    cat     ver contenido de un archivo
    mv      mover / renombrar
    rm      borrar archivo
    rmdir   borrar carpeta vacía

DOS cosas importantes que enseña este ejemplo
---------------------------------------------
1) `shell` es SIN ESTADO (stateless). Cada llamada abre una terminal NUEVA: no
   se conserva el directorio de trabajo ni las variables entre llamadas. Por eso,
   si necesitas entrar a una carpeta y luego actuar, debes encadenarlo en UN solo
   comando con `&&`:

       cd mi_carpeta && cat archivo.txt        ✅  (un solo comando)
       cd mi_carpeta                            ❌  (y en otra llamada: cat ...;
                                                     el `cd` ya se perdió)

2) `rm` y `rmdir` son DESTRUCTIVOS. El agente por defecto puede borrar sin pedir
   permiso. Para acciones peligrosas conviene combinar `shell` con
   `interventions` (ver ejemplo 9), de modo que el agente pida aprobación antes
   de borrar. La función `demo_con_aprobacion()` de abajo lo muestra.

SEGURIDAD
---------
Para que NADIE borre algo importante por accidente, todo este ejemplo trabaja
dentro de una carpeta TEMPORAL aislada (algo como /tmp/clase_shell_xxxx). Al
agente se le indica explícitamente que no salga de ahí, y al final se limpia.

Requisitos
----------
    pip install strands-harness
    export AWS_BEARER_TOKEN_BEDROCK="tu-bedrock-api-key"   # o credenciales AWS

Uso:
    python 12_shell.py
"""

import os
import shutil
import tempfile

from strands_harness import create_harness


MODELO = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"


def demo_basica(carpeta: str) -> None:
    """Recorrido seguro: mkdir -> escribir -> cat -> mv -> rm -> rmdir."""
    agente = create_harness(
        model=MODELO,
        instructions=(
            "Eres un asistente que trabaja en una terminal. Usa la herramienta "
            f"shell para ejecutar comandos. Trabaja SOLO dentro de la carpeta "
            f"'{carpeta}'. Nunca toques nada fuera de ahí. Recuerda que cada "
            "comando shell corre en una terminal nueva, así que si necesitas "
            "entrar a una subcarpeta encadena los comandos con '&&' en una sola "
            "llamada (por ejemplo: cd ruta && cat archivo)."
        ),
    )

    # Una tarea que recorre todo el ciclo de vida de archivos con shell.
    tarea = (
        f"Dentro de la carpeta '{carpeta}', haz lo siguiente paso a paso con la "
        "herramienta shell y ve mostrándome la salida de cada paso:\n"
        "1. Crea una subcarpeta llamada 'notas' (mkdir).\n"
        "2. Dentro de 'notas', crea un archivo saludo.txt con el texto "
        "'Hola clase' (puedes usar echo con redirección).\n"
        "3. Muestra el contenido de saludo.txt (cat).\n"
        "4. Renombra saludo.txt a bienvenida.txt (mv).\n"
        "5. Borra bienvenida.txt (rm).\n"
        "6. Borra la carpeta 'notas' ya vacía (rmdir).\n"
        "Al final, confirma que la carpeta quedó limpia."
    )
    print(f"Tarea:\n{tarea}\n")
    print(f"Agente: {agente(tarea)}")


def demo_con_aprobacion(carpeta: str) -> None:
    """Igual que arriba, pero pidiendo aprobación antes de borrar (interventions).

    Mejor pruébala en una terminal INTERACTIVA: el agente se detendrá a pedir
    permiso antes de ejecutar rm/rmdir.
    """
    agente = create_harness(
        model=MODELO,
        interventions="Pide aprobación antes de borrar archivos o carpetas (rm, rmdir).",
        instructions=(
            f"Trabaja con la herramienta shell SOLO dentro de '{carpeta}'. "
            "Encadena comandos con '&&' cuando necesites un directorio concreto."
        ),
    )
    tarea = (
        f"En '{carpeta}', crea un archivo temporal.txt con echo, muéstralo con "
        "cat y luego bórralo con rm."
    )
    print(f"Tarea:\n{tarea}\n")
    print(f"Agente: {agente(tarea)}")


def main() -> None:
    # Carpeta temporal aislada: nada de lo que haga el agente afecta tu proyecto.
    carpeta = tempfile.mkdtemp(prefix="clase_shell_")
    print(f"[sandbox] Trabajando en carpeta temporal: {carpeta}\n")

    try:
        print("=== DEMO BÁSICA: mkdir, cat, mv, rm, rmdir ===\n")
        demo_basica(carpeta)

        # Descomenta para ver el agente pidiendo permiso antes de borrar.
        # Hazlo en una terminal interactiva.
        #
        # print("\n\n=== DEMO CON APROBACIÓN (interventions) ===\n")
        # demo_con_aprobacion(carpeta)

    finally:
        # Limpieza: borramos la carpeta temporal pase lo que pase.
        shutil.rmtree(carpeta, ignore_errors=True)
        print(f"\n[limpieza] Carpeta temporal eliminada: {carpeta}")

    print(
        "\n[Idea] La tool shell ejecuta comandos reales, pero es SIN ESTADO: "
        "encadena con '&&' lo que dependa de un directorio. Y para comandos "
        "destructivos (rm/rmdir), combínala con interventions para pedir permiso."
    )


if __name__ == "__main__":
    main()
