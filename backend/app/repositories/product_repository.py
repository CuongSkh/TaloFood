import json
from pathlib import Path
from fastapi import HTTPException
from app.core.config import DATA_FILE

class ProductRepository:
    def __init__(self, data_file: Path = DATA_FILE):
        self.data_file = data_file
        self.data_file.parent.mkdir(parents=True, exist_ok=True)

    def read_all(self) -> list[dict]:
        if not self.data_file.exists():
            self.write_all([])
            return []
        try:
            text = self.data_file.read_text(encoding="utf-8").strip()
            if not text:
                return []
            data = json.loads(text)
            if not isinstance(data, list):
                raise ValueError("Product data must be a JSON array")
            return data
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            raise HTTPException(status_code=500, detail="Không thể đọc dữ liệu món ăn") from exc

    def write_all(self, products: list[dict]) -> None:
        try:
            temp_file = self.data_file.with_suffix(".json.tmp")
            temp_file.write_text(json.dumps(products, ensure_ascii=False, indent=2), encoding="utf-8")
            temp_file.replace(self.data_file)
        except OSError as exc:
            raise HTTPException(status_code=500, detail="Không thể lưu dữ liệu món ăn") from exc
