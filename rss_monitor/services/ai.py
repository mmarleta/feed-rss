import logging
from typing import Optional
from openai import AsyncOpenAI
from rss_monitor.models import NewsItem

class AIService:
    def __init__(self, api_key: str, model: str):
        self.client = AsyncOpenAI(api_key=api_key) if api_key else None
        self.model = model
        if not self.client:
            logging.warning("AI Service inicializado sem API Key.")

    async def generate_script(self, item: NewsItem) -> Optional[str]:
        if not self.client:
            return None

        system_prompt = (
            "Você é roteirista do canal Cyber Inteligente. "
            "Crie roteiros para YouTube Shorts de até 50 segundos, em português claro e direto. "
            "Tom energético, futurista, sem enrolação. "
            "Formato: (1) Gancho em 1 frase; (2) Essência em 3-5 frases curtas; (3) CTA com pergunta."
        )
        user_prompt = (
            f"Notícia:\n"
            f"Título: {item.title}\n"
            f"Resumo: {item.summary or 'sem resumo'}\n"
            f"Link: {item.link}\n\n"
            "Entregue apenas o texto do roteiro. "
            "Use frases curtas que cabem em fala rápida. "
            "Se não houver informações suficientes, seja transparente e peça mais contexto."
        )

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                temperature=0.6,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"Erro ao gerar roteiro para {item.title}: {e}")
            return None
