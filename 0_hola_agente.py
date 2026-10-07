"""
Strands harness · 0 · HOLA, AGENTE
==================================

Esto es **Strands harness**: un agente completo y listo para usar que creas con
UNA sola línea. No tienes que ensamblar nada; las decisiones difíciles (qué
tools, cómo gestionar el contexto, qué system prompt usar) ya vienen tomadas.

    agente = create_harness()

Sin configurar nada, el agente que obtienes ya trae:
    - un modelo (Amazon Bedrock por defecto) con razonamiento activado
    - un system prompt afinado: explora primero, actúa después, confirma antes
      de algo irreversible y verifica antes de dar por terminada una tarea
    - herramientas de shell y archivos (leer, escribir, editar)
    - acceso a la web
    - gestión automática del contexto y memoria

Requisitos
----------
    pip install strands-harness
    # Bedrock es el default; dale credenciales:
    export AWS_BEARER_TOKEN_BEDROCK="tu-bedrock-api-key"   # o credenciales AWS
    export AWS_REGION="us-east-1"

Uso:
    python 0_hola_agente.py

OJO: este agente trae shell y file tools REALES. La tarea de abajo escribe un
archivo (bases_de_datos.md) en el directorio actual. Ejecútalo en una carpeta
donde eso no te moleste.
"""

from strands_harness import create_harness


def main() -> None:
    # Una línea: un agente completo, listo para trabajar.
    # Pasamos el modelo de Bedrock al que tenemos acceso.
    agente = create_harness(model="us.anthropic.claude-sonnet-4-5-20250929-v1:0")

    # Le damos una tarea en lenguaje natural. El agente decide solo qué
    # herramientas usar: buscará en la web y escribirá el resultado en un archivo.
    tarea = (
        "Investiga las tres bases de datos vectoriales más populares, compara "
        "sus precios y límites, y escribe el resumen en bases_de_datos.md"
    )
    print(f"Tarea: {tarea}\n")

    respuesta = agente(tarea)
    print(f"\nAgente: {respuesta}")


if __name__ == "__main__":
    main()
