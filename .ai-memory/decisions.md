---
project: CscTrackerQueueScheduler
kind: decisions
tier: semantic
pinned: true
updated_at: 2026-11-21
---

# 🏛️ Decisões Arquiteturais — `CscTrackerQueueScheduler` (`csctracker-queue-scheduler`)

## Cláusulas Pétreas `[PINNED]`
- **Suporte Mínimo Python `>=3.11` (Validado até `3.15`):** `setup.py` exige `python_requires=">=3.11"` e não trava `pytz` no `requirements.txt` (mantendo apenas `schedule>=1.2.2,<2`).
- **Threads `daemon=True` Obrigatórias:** Todas as threads internas (`QueueService` e `SchedulerService.__worker` / `__start_scheduler`) DEVEM ser `daemon=True`, e `SchedulerService.__worker` deve iniciar no máximo uma vez, evitando travamento de encerramento em testes/CI.
- **`queue.task_done()` Garantido em `finally:`:** Em `QueueService.__run_job`, `queue.task_done()` DEVE estar em bloco `finally:` para não deixar `unfinished_tasks > 0` quando um job falhar (pré-requisito para o `GracefulShutdown` do `CscTrackerPyCore`).
- **Sem Dependência Obrigatória de Flask:** O import de `flask.g` em `QueueService` deve permanecer protegido com `try/except ImportError` para permitir uso/importação independente.
- **Testes Offline:** Executar via `python -B -m unittest discover -s tests -v`.
