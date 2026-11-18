
import sqlite3
import pytest
import app as sistema


# Prepara um banco temporário para os testes
@pytest.fixture
def cliente(tmp_path, monkeypatch):
    banco_teste = tmp_path / "teste.db"

    def conectar_banco_teste():
        return sqlite3.connect(banco_teste)

    monkeypatch.setattr(
        sistema,
        "conectar_banco",
        conectar_banco_teste
    )

    sistema.criar_banco()
    sistema.app.config["TESTING"] = True

    with sistema.app.test_client() as cliente:
        yield cliente


# Testa a página inicial
def test_pagina_inicial(cliente):
    resposta = cliente.get("/")
    assert resposta.status_code == 200


# Testa a página de cadastro
def test_pagina_cadastro(cliente):
    resposta = cliente.get("/cadastro")
    assert resposta.status_code == 200


# Testa o cadastro com dados válidos
def test_cadastro_valido(cliente):
    resposta = cliente.post("/cadastro", data={
        "consultora": "Maria",
        "iniciativa": "Crer Para Ver",
        "ciclo": "2026",
        "data": "2026-11-17",
        "situacao": "Ativa"
    })

    assert resposta.status_code == 200
    assert "Adesão cadastrada com sucesso!".encode() in resposta.data


# Testa o cadastro com dados inválidos
def test_cadastro_invalido(cliente):
    resposta = cliente.post("/cadastro", data={
        "consultora": "Maria",
        "iniciativa": "Iniciativa inválida",
        "ciclo": "2026",
        "data": "2026-11-17",
        "situacao": "Ativa"
    })

    assert resposta.status_code == 200
    assert "Preencha todos os campos com valores válidos.".encode() in resposta.data


# Testa a consulta das adesões cadastradas
def test_consultar_adesoes(cliente):
    cliente.post("/cadastro", data={
        "consultora": "Maria",
        "iniciativa": "Crer Para Ver",
        "ciclo": "2026",
        "data": "2026-11-17",
        "situacao": "Ativa"
    })

    resposta = cliente.get("/adesoes")

    assert resposta.status_code == 200
    assert b"Maria" in resposta.data
