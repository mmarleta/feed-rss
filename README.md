# Cyber Inteligente - Monitor de RSS

Script compacto em Python para vigiar feeds de tecnologia/IA, filtrar notícias quentes e (opcionalmente) gerar roteiro curto estilo YouTube Shorts via OpenAI.

## Como rodar

1. Crie e ative um venv (opcional, mas recomendado).
2. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Exporte sua API Key da OpenAI se quiser gerar roteiros:
   ```bash
   export OPENAI_API_KEY="sua_key"
   ```
4. Execute via módulo:
   ```bash
   python -m rss_monitor.main --limit 5
   ```

## O que o script faz

- Lê múltiplos feeds RSS de forma assíncrona.
- Filtra notícias das últimas `--max-age-hours` (padrão 24h).
- Busca palavras-chave.
- Evita duplicados via `data/seen_items.json`.
- Se `OPENAI_API_KEY` estiver setada e `--no-ai` não for usado, chama a OpenAI para gerar o roteiro.
- Imprime cada resultado em JSON e, se definido `SAVE_DIR`, salva um `.json` por notícia.
- Pode enviar o resultado para Telegram/Discord.

## Configuração

A configuração é feita via variáveis de ambiente (`.env` suportado) ou argumentos de linha de comando (que têm prioridade).

### Argumentos CLI
- `--limit`: Máximo de itens por execução.
- `--max-age-hours`: Janela de tempo em horas (padrao 24h).
- `--no-ai`: Desativa geração de roteiro.
- `--feeds`: Caminho para arquivo de feeds.
- `--keywords`: Caminho para arquivo de keywords.
- `--telegram`: Forçar envio para Telegram.
- `--discord`: Forçar envio para Discord.
- `--save-dir`: Diretório para salvar JSONs.

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `FEEDS` | Lista JSON de URLs (se não usar --feeds) | (Lista Default) |
| `KEYWORDS` | Lista JSON de palavras-chave | (Lista Default) |
| `MAX_AGE_HOURS` | Janela de tempo em horas | 24 |
| `LIMIT` | Limite de itens | 10 |
| `MODEL` | Modelo OpenAI | gpt-4o-mini |
| `STATE_FILE` | Arquivo de estado | data/seen_items.json |
| `SAVE_DIR` | Diretório para salvar JSONs | (Vazio = não salvar) |
| `OPENAI_API_KEY` | Chave da API OpenAI | |
| `NO_AI` | Desativa geração de roteiro | False |
| `TELEGRAM_ENABLED` | Habilita envio p/ Telegram | False |
| `TELEGRAM_BOT_TOKEN` | Token do Bot | |
| `TELEGRAM_CHAT_ID` | Chat ID | |
| `DISCORD_ENABLED` | Habilita envio p/ Discord | False |
| `DISCORD_WEBHOOK_URL`| Webhook URL | |
| `LOG_LEVEL` | Nível de log | INFO |

## Customizações rápidas

- Ajuste `Settings` em `rss_monitor/config.py` para mudar defaults.
- Troque o prompt em `rss_monitor/services/ai.py` para mudar estilo/idioma do roteiro.
- Integre com Telegram/Discord/YouTube em `rss_monitor/services/notification.py` ou `rss_monitor/main.py`.

## Entrega em Telegram / Discord

Telegram:
```bash
export TELEGRAM_ENABLED=True
export TELEGRAM_BOT_TOKEN="123:abc"
export TELEGRAM_CHAT_ID="999999"
python -m rss_monitor.main
```

Discord:
```bash
export DISCORD_ENABLED=True
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
python -m rss_monitor.main
```

## Execução contínua (cron ou systemd)

Cron (a cada 20 minutos):
```bash
*/20 * * * * cd /path/to/project && /usr/bin/python3 -m rss_monitor.main --limit 10 >> rss.log 2>&1
```

Systemd:
Ver exemplo em `ops/rss-monitor.service.example`.

## Próximos passos sugeridos

- Adicionar scraping do link completo quando o resumo do RSS for curto.
- Criar um endpoint ou job no cron/PM2/systemd para rodar continuamente.
- Salvar os roteiros em um banco (SQLite/Firestore) para curadoria manual.
- Incluir TTS e geração de vídeo após o payload JSON.
