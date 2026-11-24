# Estimador CAG — LIDR AI Engineering

## Descripción

Microservicio desarrollado con Python, FastAPI y Anthropic Claude para generar estimaciones preliminares de proyectos de software utilizando arquitectura CAG (Cache-Augmented Generation).

El sistema recibe una descripción o transcripción de una reunión con un cliente, incorpora estimaciones históricas ficticias como contexto y genera una propuesta con tareas, horas, costos, equipo recomendado y riesgos.

**Este proyecto es un ejercicio académico. Las estimaciones no representan cotizaciones comerciales verificadas.**

## Tecnologías

- Python 3.13
- FastAPI
- Uvicorn
- Pydantic y Pydantic Settings
- Anthropic Claude Haiku 4.5
- uv (gestor de dependencias)

## Arquitectura

```text
estimador-cag/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── estimations.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── llm_service.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── estimation.py
│   └── context/
│       ├── __init__.py
│       └── examples.py
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

### Responsabilidades

- `main.py`: inicializa FastAPI, registra las rutas y expone el endpoint de salud.
- `config.py`: carga y valida la configuración mediante variables de entorno.
- `routers/estimations.py`: recibe solicitudes HTTP y delega el trabajo al servicio.
- `services/llm_service.py`: construye el system prompt, incorpora los ejemplos CAG y llama a Claude.
- `schemas/estimation.py`: valida los formatos de entrada y salida mediante Pydantic.
- `context/examples.py`: almacena las estimaciones ficticias utilizadas como referencias.

## Instalación

### 1. Requisitos

Tener Python y uv instalados.

### 2. Instalar las dependencias

Desde la raíz del proyecto:

```powershell
uv sync
```

En Windows, si aparecen errores relacionados con hardlinks, utilizar:

```powershell
$env:UV_LINK_MODE = "copy"
uv sync
```

### 3. Configurar las variables de entorno

Crear un archivo `.env` a partir de `.env.example` y completar los valores:

```dotenv
ANTHROPIC_API_KEY=tu_clave_privada
LLM_PROVIDER=anthropic
LLM_MODEL=claude-haiku-4-5-20251001
APP_ENV=development
LOG_LEVEL=DEBUG
```

**Seguridad:** nunca publicar `.env` ni compartir las claves API. Este archivo está excluido mediante `.gitignore`.

## Ejecutar la aplicación

Desde la raíz del proyecto:

```powershell
uv run uvicorn app.main:app --reload
```

Servidor local:

http://127.0.0.1:8000

Documentación Swagger:

http://127.0.0.1:8000/docs

## Endpoints

### GET /health

Comprueba que la aplicación está funcionando.

Respuesta esperada:

```json
{
  "status": "healthy"
}
```

### POST /api/v1/estimate

Recibe una descripción de un proyecto y genera una estimación mediante Claude.

**Ejemplo de solicitud:**

```json
{
  "transcription": "En la reunión, el cliente explicó que necesita desarrollar un sistema CRM para gestionar contactos, oportunidades de ventas, seguimiento comercial y reportes. Requiere autenticación para 20 vendedores y un dashboard para los gerentes."
}
```

**Formato de respuesta:**

```json
{
  "estimation": "Estimación generada por Claude...",
  "model": "claude-haiku-4-5-20251001",
  "provider": "anthropic"
}
```

La transcripción debe contener al menos 50 caracteres. Las solicitudes que no cumplan esta regla reciben HTTP 422.

## Arquitectura CAG

El proyecto utiliza tres estimaciones ficticias de referencia:

1. Sistema de gestión de inventarios.
2. Sitio web corporativo.
3. CRM empresarial.

Estas referencias están definidas en `app/context/examples.py`.

El servicio las incorpora al system prompt junto con las instrucciones de estimación antes de llamar a Claude.

Esta primera implementación envía el contexto mediante la API; no implementa una base de datos vectorial ni un KV-cache persistente propio.

## Pruebas manuales realizadas

- Inicio del servidor FastAPI: correcto.
- `GET /health`: HTTP 200.
- Acceso a Swagger `/docs`: HTTP 200.
- `POST /api/v1/estimate` con una solicitud de CRM: HTTP 200 y estimación generada mediante Claude.
- `POST /api/v1/estimate` con menos de 50 caracteres: HTTP 422.

## Próximos pasos

- Configurar la ejecución automática de pruebas mediante CI.
- Registrar el consumo de tokens por solicitud.
- Evaluar la coherencia de las estimaciones y verificar los cálculos.
- Mejorar los ejemplos de contexto y el system prompt.
- Explorar la evolución hacia RAG en módulos posteriores del programa.

## Estado

**Versión:** 0.1.0

**Etapa:** ejercicio funcional de arquitectura CAG — LIDR AI Engineering.