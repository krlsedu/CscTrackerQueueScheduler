---
project: CscTrackerQueueScheduler
kind: handoff
tier: working
updated_at: 2026-11-21
---

# 🤝 Handoff Ativo — `CscTrackerQueueScheduler`

> **Escopo do Projeto:** Biblioteca Python `csctracker-queue-scheduler` no PyPI para filas normal/prioritária e agendamento periódico de jobs em background.

## 1. Onde Paramos / Contexto Atual (`WIP`)
- **[2026-11-21] Implementação da ID 96 (`Por Publicar`, `6/6` testes offline OK em Python `3.15.2`, sem `flask`/`pytz`):**
  - Removido `pytz~=2023.3.post1` de `requirements.txt` (mantido `schedule>=1.2.2,<2`) e atualizado `setup.py` para `python_requires=">=3.11"`, `encoding="utf-8"` e classifiers `3.11`–`3.15`.
  - Corrigidos `QueueService` (`try/except ImportError` para `flask.g`, `poll_interval`, `queue.task_done()` garantido em `finally:`) e `SchedulerService` (`daemon=True`, guarda de worker único, correção de argumento mutável `services` e guarda `args=None` em `put_in_queue`).
  - Criados testes offline em `tests/test_queue_scheduler.py`, atualizado `.github/workflows/build.yml` (Python `3.15` + testes) e provisionados `.agents/`, `.ai-memory/`, `.junie/` e `notify-cicd.yml`.

## 2. Tentativas Descartadas / O que Falhou (`Failed Approaches`)
- *(Nenhuma falha ativa).*

## 3. Estado dos Arquivos / Branch / Build
- **Fonte Primária:** GitHub (`master`, com espelho `.zip` em `projects/repositorys/CscTrackerQueueScheduler/`; `.pyenv-usr-bin-python3.9/bin/python3.9` pré-existente mantido intocado).
- **Testes offline:** `python -B -m unittest discover -s tests -v` (`6/6` passando em Python `3.15.2`).

## 4. Próximos Passos / Pendências Abertas
- Configurar secret `TOKEN_CSCTRACKER` (e opcionalmente `CICD_WEBHOOK_URL`) no GitHub Actions do repositório para o workflow `notify-cicd.yml`.
- Publicar nova versão de `csctracker-queue-scheduler` no PyPI para desbloquear a **ID 94** (`CscTrackerPyCore`).
