import asyncio
import argparse
import logging
from pathlib import Path
import aiohttp

from rss_monitor.config import settings
from rss_monitor.models import ProcessedItem
from rss_monitor.services.state import StateService
from rss_monitor.services.feed import FeedService
from rss_monitor.services.filter import FilterService
from rss_monitor.services.ai import AIService
from rss_monitor.services.notification import NotificationService
from rss_monitor.utils import render_result, save_result_to_file

def parse_args():
    parser = argparse.ArgumentParser(description="Monitor de RSS (Modular)")
    parser.add_argument("--limit", type=int, help="Override limite de itens")
    parser.add_argument("--max-age-hours", type=int, help="Override janela de tempo (horas)")
    parser.add_argument("--no-ai", action="store_true", help="Desativar IA")
    parser.add_argument("--feeds", help="Arquivo de feeds")
    parser.add_argument("--keywords", help="Arquivo de keywords")
    parser.add_argument("--telegram", action="store_true", help="Forçar Telegram")
    parser.add_argument("--discord", action="store_true", help="Forçar Discord")
    parser.add_argument("--save-dir", help="Pasta para salvar JSONs")
    return parser.parse_args()

def read_lines_file(path: str) -> list[str]:
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
        return [ln.strip() for ln in lines if ln.strip()]
    except Exception as e:
        logging.error(f"Erro ao ler arquivo {path}: {e}")
        return []

async def main():
    # 0. Parse Args & Override Settings
    args = parse_args()
    
    # Simple overrides. ideally config logic handles this, but manual override is safe here.
    if args.limit is not None:
        settings.LIMIT = args.limit
    if args.max_age_hours is not None:
        settings.MAX_AGE_HOURS = args.max_age_hours
    if args.no_ai:
        settings.NO_AI = True
    if args.feeds:
        settings.FEEDS = read_lines_file(args.feeds)
    if args.keywords:
        settings.KEYWORDS = read_lines_file(args.keywords)
    if args.telegram:
        settings.TELEGRAM_ENABLED = True
    if args.discord:
        settings.DISCORD_ENABLED = True
    if args.save_dir:
        settings.SAVE_DIR = args.save_dir

    # 1. Setup Logging
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format="[%(asctime)s] %(levelname)s: %(message)s",
    )

    # 2. Initialize Services
    state_service = StateService(settings.STATE_FILE)
    feed_service = FeedService(settings.MAX_AGE_HOURS)
    filter_service = FilterService(settings.KEYWORDS)
    ai_service = AIService(settings.OPENAI_API_KEY, settings.MODEL)
    
    telegram_cfg = (settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_CHAT_ID) if settings.TELEGRAM_ENABLED else None
    notification_service = NotificationService(
        telegram_cfg=telegram_cfg,
        discord_webhook=settings.DISCORD_WEBHOOK_URL if settings.DISCORD_ENABLED else None
    )

    # 3. Load State
    seen_ids = state_service.load_seen_ids()
    logging.info(f"Carregados {len(seen_ids)} itens vistos.")

    # 4. Fetch Feeds
    all_items = await feed_service.fetch_all(settings.FEEDS)
    logging.info(f"Encontrados {len(all_items)} itens nos feeds.")

    # 5. Filter (Dedup + Keywords)
    new_items = [item for item in all_items if item.id not in seen_ids]
    relevant_items = filter_service.filter_items(new_items)
    logging.info(f"Itens novos e relevantes: {len(relevant_items)}")

    if not relevant_items:
        logging.info("Nenhuma notícia nova relevante.")
        return

    # Apply Limit
    if settings.LIMIT and len(relevant_items) > settings.LIMIT:
        relevant_items = relevant_items[:settings.LIMIT]
        logging.info(f"Limitando a {settings.LIMIT} itens.")

    # 6. Process Items (AI + Notify + Save)
    save_dir = Path(settings.SAVE_DIR) if settings.SAVE_DIR else None
    
    # Semaphore to limit concurrency (e.g. 5 concurrent processings)
    sem = asyncio.Semaphore(5)

    async with aiohttp.ClientSession() as session:
        async def process_one(item):
            async with sem:
                try:
                    script = None
                    error = None
                    
                    if not settings.NO_AI:
                        script = await ai_service.generate_script(item)
                        if not script:
                            error = "Falha ao gerar roteiro (ver logs)"

                    processed = ProcessedItem(news=item, script=script, error=error)
                    
                    # Output / Notify
                    render_result(processed)
                    if save_dir:
                        save_result_to_file(processed, save_dir)
                    
                    await notification_service.send_all(processed, session)
                    
                    return item.id
                except Exception as e:
                    logging.error(f"Erro crítico processando item {item.id}: {e}")
                    return None

        results = await asyncio.gather(*[process_one(item) for item in relevant_items], return_exceptions=True)
    
    # 7. Update State
    successful_ids = []
    for res in results:
        if isinstance(res, str):
            successful_ids.append(res)
        # We ignore exceptions here because they are caught inside process_one or handled by gather return_exceptions
    
    if successful_ids:
        state_service.save_seen_ids(seen_ids | set(successful_ids))
        logging.info(f"Estado atualizado com {len(successful_ids)} novos itens processados com sucesso.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
