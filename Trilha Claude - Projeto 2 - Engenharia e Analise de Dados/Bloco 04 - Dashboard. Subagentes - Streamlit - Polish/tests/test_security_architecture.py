import os
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent

def test_gitignore_protects_env():
    gitignore_path = ROOT_DIR / ".gitignore"
    assert gitignore_path.exists(), "Arquivo .gitignore deve existir"
    content = gitignore_path.read_text(encoding="utf-8")
    assert ".env" in content, ".gitignore deve conter .env"

def test_env_file_format():
    env_path = ROOT_DIR / ".env"
    assert env_path.exists(), "Arquivo .env deve existir no projeto"
    content = env_path.read_text(encoding="utf-8")
    assert "SUPABASE_URL=" in content
    assert "SUPABASE_KEY=" in content

def test_env_example_has_no_secrets():
    example_path = ROOT_DIR / ".env.example"
    assert example_path.exists(), ".env.example deve existir"
    content = example_path.read_text(encoding="utf-8")
    assert "eyJhbGciOi" not in content, ".env.example não deve conter chaves reais JWT"

def test_no_hardcoded_keys_in_code():
    """Garante que nenhum script Python contém chaves JWT hardcoded."""
    jwt_prefix = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    for py_file in ROOT_DIR.rglob("*.py"):
        if "tests" in py_file.parts or ".venv" in py_file.parts:
            continue
        code = py_file.read_text(encoding="utf-8")
        assert jwt_prefix not in code, f"Chave hardcoded detectada no arquivo {py_file.name}!"
