# Fraud Apps Finalcode Ashar Arsal

FraudApps-finalcode-Ashar-Arsal is an application for analysing app reviews and potentially fraudulent apps.

![Django](https://img.shields.io/badge/Django-2563EB?style=flat-square) ![SQLite](https://img.shields.io/badge/SQLite-0F172A?style=flat-square)

## Overview

The data model covers `Application`, `AppReview`, `Feedback`.

## Implemented workflows

The source defines these handlers:

- **Penn To Wn** — `penn_to_wn`
- **Analyze Sentiment Sentiwordnet** — `analyze_sentiment_sentiwordnet`
- **Index** — `index`
- **Register** — `register`
- **Login** — `login_view`
- **Logout** — `logout_view`
- **Dashboard** — `dashboard`
- **Add Review** — `add_review`
- **App Detail** — `app_detail`
- **Submit Feedback** — `submit_feedback`

## Getting started

### 1. Get the project

```bash
git clone https://github.com/nasirabbas827/FraudApps-finalcode-Ashar-Arsal.git
cd FraudApps-finalcode-Ashar-Arsal
```

### 2. Prepare Python

Create an isolated environment:

```bash
python -m venv .venv
```

Activate it with `.venv\Scripts\activate` on Windows Command Prompt, or `source .venv/bin/activate` on macOS/Linux.

No requirements file is included. The inspected Python imports indicate these dependencies as a starting point:

```bash
python -m pip install Django nltk Pillow
```

Dependency versions are not pinned in this repository.

### 3. Configure and run

Review [`fake_review_detection/settings.py`](fake_review_detection/settings.py) for database, media, and any email configuration. Use a local copy of the supplied database when available.

```bash
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/. If you need a Django administration account, run `python manage.py createsuperuser`. Application-specific user roles may be managed separately.

## Repository guide

| Path | Purpose |
| --- | --- |
| [`db.sqlite3`](db.sqlite3) | Included SQLite database |
| [`manage.py`](manage.py) | Django command-line entry point |
| [`templates`](templates) | HTML page templates |

## Development notes

These setup instructions are based on the repository source. The application has not been executed as part of this documentation update; verify dependencies and configuration in your local environment.
