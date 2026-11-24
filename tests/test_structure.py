
from pathlib import Path


def test_project_structure():
    project_root = Path(__file__).resolve().parent.parent

    required_files = [
        "app/main.py",
        "app/config.py",
        "app/routers/estimations.py",
        "app/services/llm_service.py",
        "app/schemas/estimation.py",
        "app/context/examples.py",
        "pyproject.toml",
        ".env.example",
        ".gitignore",
        "README.md",
    ]

    for file in required_files:
        assert (project_root / file).is_file(), (
            f"Falta el archivo: {file}"
        )
