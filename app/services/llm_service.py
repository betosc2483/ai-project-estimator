
from anthropic import AsyncAnthropic

from app.config import get_settings
from app.context.examples import ESTIMATION_EXAMPLES


def build_system_prompt() -> str:
    references = []

    for number, example in enumerate(ESTIMATION_EXAMPLES, start=1):
        references.append(
            f"=== REFERENCIA {number} ===\n"
            f"Solicitud: {example['meeting_summary'].strip()}\n"
            f"Estimación: {example['estimation'].strip()}"
        )

    references_text = "\n\n".join(references)

    return f"""
Eres un experto en estimación de proyectos de software.

Tu tarea es analizar una solicitud de un cliente y generar
una estimación inicial de desarrollo.

Utiliza los siguientes ejemplos ficticios como referencias
para el desglose de tareas, horas y costos.

No presentes los precios ficticios como tarifas verificadas.
Si faltan requisitos importantes, indica los supuestos.
No inventes características que el cliente no haya solicitado.

La respuesta debe incluir:
1. Resumen del proyecto.
2. Desglose de tareas con horas y costos.
3. Horas y costo total estimados.
4. Equipo recomendado.
5. Riesgos y supuestos.

Utiliza EUR como moneda de referencia.

=== ESTIMACIONES DE REFERENCIA ===

{references_text}

=== FIN DE REFERENCIAS ===
"""


async def generate_estimation(transcription: str) -> dict:
    settings = get_settings()

    async with AsyncAnthropic(
        api_key=settings.ANTHROPIC_API_KEY
    ) as client:
        response = await client.messages.create(
            model=settings.LLM_MODEL,
            max_tokens=1500,
            system=build_system_prompt(),
            messages=[
                {
                    "role": "user",
                    "content": transcription
                }
            ]
        )

    estimation = "\n".join(
        block.text
        for block in response.content
        if block.type == "text"
    )

    return {
        "estimation": estimation,
        "model": response.model,
        "provider": settings.LLM_PROVIDER
    }
