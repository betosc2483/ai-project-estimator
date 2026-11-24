
from fastapi.testclient import TestClient

from app.main import app
from app.routers import estimations
from app.services.llm_service import build_system_prompt


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_short_transcription():
    response = client.post(
        "/api/v1/estimate",
        json={"transcription": "Necesito una página web"}
    )

    assert response.status_code == 422


def test_estimation_with_mock(monkeypatch):

    async def fake_generate_estimation(transcription: str):
        return {
            "estimation": "Estimación simulada: 100 horas",
            "model": "test-model",
            "provider": "anthropic"
        }

    monkeypatch.setattr(
        estimations,
        "generate_estimation",
        fake_generate_estimation
    )

    response = client.post(
        "/api/v1/estimate",
        json={
            "transcription":
            "El cliente necesita desarrollar una aplicación web "
            "para gestionar productos, usuarios y reportes."
        }
    )

    assert response.status_code == 200
    assert response.json()["estimation"] == (
        "Estimación simulada: 100 horas"
    )
    assert response.json()["provider"] == "anthropic"


def test_cag_context():
    prompt = build_system_prompt()

    assert "Sistema de Inventario" in prompt
    assert "Sitio Web Corporativo" in prompt
    assert "CRM Empresarial" in prompt
