---
project: CscTrackerQueueScheduler
kind: gotchas
tier: semantic
updated_at: 2026-11-21
---

# ⚠️ Armadilhas Conhecidas (`Gotchas`) — `CscTrackerQueueScheduler`

- **Thread não-daemon em `SchedulerService.__worker` trava testes/CI:** Sem `daemon=True`, o processo Python imprime `OK` no `unittest` e fica pendurado indefinidamente.
- **Vazamento de `unfinished_tasks` em exceção de job:** Antes da ID 96, `queue.task_done()` só rodava se `func_` não lançasse exceção, travando `queue.join()` e o drain do `GracefulShutdown` até o `SHUTDOWN_TIMEOUT`.
- **Argumento mutável `services: list = []` em `SchedulerService.init()`:** Usar `services: list = None` e inicializar `[]` dentro da função.
- **`pytz` não é utilizado:** Nunca reintroduzir `pytz~=...` em `requirements.txt` sem uso real no código, pois trava atualizações no ecossistema.
- **`python -m build` exige `MANIFEST.in`:** O `build` cria o `wheel` a partir do `sdist`. Sem `MANIFEST.in` listando `version.py`, `version.txt`, `requirements.txt`, `README.md` e `LICENSE`, o build falha com `ModuleNotFoundError: No module named 'version'`. Manter também `description_file = README.md` (underscore) no `setup.cfg` para evitar aviso do `setuptools>=84`.
