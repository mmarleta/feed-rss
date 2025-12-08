import json
import logging
from pathlib import Path
from typing import Set, Iterable

class StateService:
    def __init__(self, state_file: str):
        self.state_path = Path(state_file)

    def load_seen_ids(self) -> Set[str]:
        if not self.state_path.exists():
            return set()
        try:
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
            return set(data.get("seen_ids", []))
        except Exception:
            logging.exception("Erro ao ler arquivo de estado, começando vazio.")
            return set()

    def save_seen_ids(self, seen_ids: Iterable[str]) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(
            json.dumps({"seen_ids": list(seen_ids)}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
