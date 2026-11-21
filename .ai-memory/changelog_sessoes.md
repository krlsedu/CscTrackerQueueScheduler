---
project: CscTrackerQueueScheduler
kind: changelog
tier: episodic
updated_at: 2026-11-21
---

# 📜 Changelog de Sessões — `CscTrackerQueueScheduler`

## 2026-11-21 — ID 96: Python 3.15, Remoção de `pytz` Travado, `daemon=True` e `task_done()` Seguro
- Removido `pytz~=2023.3.post1` não utilizado e atualizado `schedule>=1.2.2,<2` + `setup.py` (`python_requires=">=3.11"`, classifiers até `3.15`).
- Garantido `daemon=True` e worker único no `SchedulerService`, `queue.task_done()` em `finally:` no `QueueService` e import opcional de `flask.g`.
- Adicionados testes unitários offline em `tests/test_queue_scheduler.py`, atualizado `.github/workflows/build.yml` e provisionada governança (`/csctracker`).
