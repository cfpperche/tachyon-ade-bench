# Handoff — Tachyon ADE Bench

Atualizado em 2026-07-21, após o refresh do roster e do dashboard.

## Estado atual

- Branch ativa: `main`.
- Working tree antes deste handoff: limpo.
- Último commit publicado: `4b4e099 chore: refresh competitor and dashboard data`.
- GitHub Pages: deploy do commit `4b4e099` concluído com sucesso.
- O roster contém 13 perfis, incluindo `jetbrains-air`.
- A inclusão catalográfica do JetBrains Air está encerrada na spec 015.

## Evidência de validação

- `python3 harness/bench.py check` passou.
- `python3 scripts/intelligence/check-intelligence.py` passou.
- `python3 scripts/marketing/check-marketing.py` passou.
- `bash scripts/check-suite.sh` passou.
- `npm run dashboard:check` passou com 0 erros, 0 warnings e 0 hints do Astro.
- `npm run dashboard:build` passou e gerou 42 rotas estáticas.
- O build ainda exibe apenas avisos preexistentes de depreciação do Vite e tamanho de chunk.

## Refresh realizado

Foram revalidadas fontes oficiais e atualizados claims/datas dos perfis. Correções factuais relevantes:

- AgentsRoom: download oficial reporta v1.109.0.
- Kandev: release oficial v0.81.0 em 21/07/2026.
- Orca: release público v1.4.35 e 3,8k stars; pacote ainda expõe `1.4.142-rc.7`.
- HiveTerm: site oficial reporta v0.37.0 e downloads para macOS, Windows e Linux.

Os derivados `marketing/current/{ads,campaigns,coverage}.json` foram regenerados.

## Próxima seção — smoke do JetBrains Air

A spec 016 permanece `deferred` por depender de instalação desktop interativa e autenticação.

### Pré-requisitos

1. Instalar JetBrains Toolbox e Air pelo fluxo oficial de Linux.
2. Autenticar o Air e um agente convidado suportado.
3. Registrar Air, agente, modelo, esforço, assinatura, permissões, OS e política de rede.

### Execução

1. Preparar `T001-python-bugfix` para `jetbrains-air`:

   ```sh
   python3 harness/bench.py prepare \
     --product jetbrains-air \
     --task T001-python-bugfix \
     --run-id air-t001-<timestamp>
   ```

2. Abrir somente o worktree gerado como Local Workspace no Air.
3. Fornecer exatamente o `prompt.md`, contar intervenções/aprovações e deixar o agente trabalhar.
4. Executar o verificador canônico:

   ```sh
   python3 harness/bench.py verify runs/air-t001-<timestamp>
   ```

5. Completar o `result.json` com metadados de runtime e atualizar a spec 016.
6. Só promover `benchmarking.readiness` no perfil se o smoke passar; caso contrário, registrar o bloqueio e manter `needs-install`.

## Limites

- `/home/goat/tachyon` é somente leitura.
- Não transformar claims de marketing em evidência de benchmark.
- `runs/` é gitignored; manter evidência local salvo pedido explícito.
- Fazer commit/push somente quando o usuário autorizar.

## Comandos de retomada

```sh
cd /home/goat/tachyon-ade-bench
git status --short
python3 harness/bench.py check
sed -n '1,220p' docs/specs/016-jetbrains-air-smoke/tasks.md
```
