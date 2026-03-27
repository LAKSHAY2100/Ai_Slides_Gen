# AI Slides Gen

AI Slides Gen is a Django-based web app that generates presentation slide outlines and slide images from a topic or an uploaded document. It also supports user authentication, slide sharing by code, and document-aware slide generation using a retrieval pipeline.

## Features

- Generate five-slide presentation outlines from a topic and slide type.
- Generate slide images for each title.
- Upload source documents to guide slide generation.
- Support for `.pdf`, `.csv`, and `.docx` uploads.
- Share slide decks with a short share code.
- Local authentication plus Google sign-in through `django-allauth`.
- Simple landing, story, and slide builder pages.

## Tech Stack

- Django 5
- PostgreSQL
- Django Allauth
- Google GenAI SDK
- LangChain
- FAISS
- Ollama embeddings
- Groq chat model
- Unstructured and docx2txt-based document loading

## Requirements

- Python 3.12 or newer
- PostgreSQL
- Ollama running locally for embeddings
- API keys for Google, Groq, and Pollinations

## Setup

1. Create and activate a virtual environment.
2. Install the project dependencies.
3. Copy `.env.example` to `.env` and fill in the values.
4. Make sure PostgreSQL is available and the database settings in `aislides/settings.py` match your environment.
5. Run migrations.
6. Start the development server.

```bash
python manage.py migrate
python manage.py runserver
```

## Environment Variables

The app expects these values in `.env`:

```env
GOOGLE_API_KEY=
GROQ_API_KEY=
POLLINATIONS_API_KEY=
GOOGLE_OAUTH_CLIENT_ID=
GOOGLE_OAUTH_CLIENT_SECRET=
```

## How It Works

1. Enter a topic and slide type, or upload a document.
2. The app extracts text from the uploaded file when provided.
3. The text is chunked and stored in a FAISS index.
4. A retrieval chain uses Groq to summarize the content into slide titles.
5. Slide images are generated for each title.
6. The resulting slide deck can be shared with a generated code.

## Supported Uploads

- `.pdf` files are parsed with `PyPDFLoader`.
- `.csv` files are parsed with `CSVLoader`.
- `.docx` files are parsed with `Docx2txtLoader`.

`.doc` files are not supported.

## Routes

- `/` - Story landing page
- `/slides/` - Slide builder
- `/story/` - Story page
- `/api/generate_slides/` - Generate slides
- `/api/share/` - Save and share slides
- `/view/<code>/` - View a shared slide deck
- `/auth/` - Login, register, logout, and dashboard routes

## Project Structure

- `aislides/` - Django project settings and URL routing
- `slides/` - Slide generation models, views, and URLs
- `auth_app/` - Login, registration, logout, and dashboard views
- `templates/` - HTML templates
- `static/` - Images, scripts, and generated assets

## Notes

- The app relies on Ollama being available for embeddings.
- If a document upload fails, the API returns the underlying error message to help with debugging.
- The repository currently uses PostgreSQL settings in `aislides/settings.py`.

