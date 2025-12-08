import logging
import aiohttp
import asyncio
from typing import Optional, Tuple
from rss_monitor.models import ProcessedItem

class NotificationService:
    def __init__(
        self,
        telegram_cfg: Optional[Tuple[str, str]] = None,
        discord_webhook: Optional[str] = None
    ):
        self.telegram_token = telegram_cfg[0] if telegram_cfg else None
        self.telegram_chat_id = telegram_cfg[1] if telegram_cfg else None
        self.discord_webhook = discord_webhook

    def build_message(self, processed: ProcessedItem) -> str:
        news = processed.news
        lines = [
            f"🔥 {news.title}",
            f"🔗 {news.link}",
        ]
        if news.published:
            lines.append(f"🕒 {news.published}")
        if processed.script:
            lines.append("\n📝 Roteiro:")
            lines.append(processed.script)
        elif processed.error:
            lines.append(f"\n⚠️ Erro ao gerar roteiro: {processed.error}")
        return "\n".join(lines)

    async def send_all(self, processed: ProcessedItem, session: aiohttp.ClientSession):
        text = self.build_message(processed)
        await asyncio.gather(
            self.send_telegram(session, text),
            self.send_discord(session, text),
            return_exceptions=True
        )

    async def send_telegram(self, session: aiohttp.ClientSession, text: str):
        if not self.telegram_token or not self.telegram_chat_id:
            return
        
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        try:
            async with session.post(
                url,
                json={
                    "chat_id": self.telegram_chat_id,
                    "text": text,
                    "disable_web_page_preview": True,
                },
                timeout=10,
            ) as resp:
                resp.raise_for_status()
            logging.info("Enviado para Telegram.")
        except Exception as e:
            logging.error(f"Falha ao enviar para Telegram: {e}")

    async def send_discord(self, session: aiohttp.ClientSession, text: str):
        if not self.discord_webhook:
            return
        
        try:
            async with session.post(
                self.discord_webhook,
                json={"content": text},
                timeout=10,
            ) as resp:
                resp.raise_for_status()
            logging.info("Enviado para Discord.")
        except Exception as e:
            logging.error(f"Falha ao enviar para Discord: {e}")
