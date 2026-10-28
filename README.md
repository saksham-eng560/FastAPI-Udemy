# FastAPI-Udemy

My hands-on practice project while following a FastAPI course on Udemy. It contains small example apps, a Postman workspace, and a structured set of study notes exported as a PDF.

## Project structure

| Path | What it is |
|---|---|
| `main.py` | First app: a single `GET /` route with custom docs/OpenAPI URLs |
| `main1.py` | Second app: tags, docstrings, decorator metadata, and the `Request` object |
| `notes/fastapi_notes.md` | Source of my notes, organised by chapter |
| `build_notes_pdf.py` | Script that turns the notes into a PDF |
| `FastAPI_Notes.pdf` | Generated notes (rebuilt whenever I update the notes) |
| `postman/`, `.postman/` | Postman collections/specs linked to my workspace |
| `requirements.txt` | Python dependencies |

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload     # first app
uvicorn main1:app --reload    # second app
```

Then open:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- OpenAPI schema: http://127.0.0.1:8000/openapi.json

## Endpoints

**main.py**
- `GET /` - hello message

**main1.py**
- `GET /` - sample nested JSON response
- `GET /request` - echoes headers, URL, method, path and query params
- `GET /MoreInfo` - same as above, showing decorator-level documentation

## Notes PDF

The notes live in `notes/fastapi_notes.md`. To regenerate the PDF:

```bash
pip install reportlab
python3 build_notes_pdf.py
```

## Topics covered so far

Virtual environments, creating a FastAPI app, route decorators, OpenAPI metadata, tags, docstrings, the `Request` object, sync vs async handlers, Swagger/ReDoc, Postman.
