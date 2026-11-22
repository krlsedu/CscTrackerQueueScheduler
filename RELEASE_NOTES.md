Release Notes - v26.47.001

Abaixo estão as notas de atualização para a versão v26.47.001. Esta versão foca na modernização do ecossistema de build e suporte de runtime, viabilizando a compatibilidade com o Python 3.15 e atualizando pipelines de CI/CD. Além disso, introduz correções críticas na lógica dos serviços de fila e agendamento, assegurando a correta distribuição de pacotes com manifestos completos de empacotamento e suíte de testes dedicada.

## 🚀 Features
*(Nenhuma alteração desta categoria nesta versão)*

## 🐛 Fixes
* **Queue & Scheduler:** Correção na lógica de processamento e execução assíncrona do serviço de filas e agendamento, ajustando o ciclo de vida das tarefas para prevenir falhas de concorrência ou bloqueios na fila, acompanhada pela expansão da cobertura de testes unitários (`services/queue_service.py`).
  * *Commit: `5aaa582` | Autor: @krlsedu*

## 🔧 Chore
* **Packaging & Build:** Inclusão e configuração do arquivo `MANIFEST.in` junto à atualização do `setup.cfg`, garantindo que todos os arquivos estáticos e metadados essenciais sejam devidamente empacotados na distribuição do pacote Python, prevenindo ausência de artefatos em instalações downstream (`MANIFEST.in`).
  * *Commit: `b532b67` | Autor: @krlsedu*
* **Build & Tooling:** Adequação do ambiente para suportar Python 3.15 no `setup.py` e matrizes do GitHub Actions (`build.yml`), inclusão de fluxo para notificações de CI/CD e estruturação da base de conhecimento com documentações de skills e diretrizes de IA (`setup.py`).
  * *Commit: `5aaa582` | Autor: @krlsedu*