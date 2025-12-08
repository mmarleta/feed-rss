import json
import logging
from datetime import datetime
from pathlib import Path
from rss_monitor.models import ProcessedItem

def render_result(processed: ProcessedItem) -> None:
    # Pydantic model_dump
    payload = processed.model_dump(mode='json')
    print(json.dumps(payload, ensure_ascii=False, indent=2))

def save_result_to_file(processed: ProcessedItem, save_dir: Path) -> None:
    if not save_dir:
        return
    
    try:
        import hashlib
        safe_title = processed.news.title[:50].replace("/", "_").replace("\\", "_")
        # Add hash to avoid collision in same second
        hash_input = f"{processed.news.title}{processed.news.id}"
        title_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_title}_{title_hash}.json"
        
        payload = processed.model_dump(mode='json')
        (save_dir / filename).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        logging.info("Salvo em: %s", save_dir / filename)
    except Exception as e:
        logging.error(f"Erro ao salvar arquivo: {e}")
