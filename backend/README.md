# TaloFood Backend — Session 6

## Run

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health

Product data is persisted in `data/products.json`. Images are served from `data_images/` at `/images/*`.
