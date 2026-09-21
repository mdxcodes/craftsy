<div align="center">

# Craftsy

### Where Artisan Hands Meet Digital Markets

**An AI-powered companion that transforms a single photo and a spoken sentence into a professional, fairly-priced, bilingual product listing — purpose-built for India's rural artisans.**

*Smart India Hackathon 2026 · PS-90 · Heritage & Culture*

[![Flutter](https://img.shields.io/badge/Mobile-Flutter-02569B?logo=flutter&logoColor=white)](https://flutter.dev)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Supabase](https://img.shields.io/badge/Data-Supabase-3FCF8E?logo=supabase&logoColor=white)](https://supabase.com)
[![ChromaDB](https://img.shields.io/badge/Vector%20Store-ChromaDB-purple)](https://www.trychroma.com)
[![Offline First](https://img.shields.io/badge/Design-Offline--First-orange)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](#license)

</div>

---

## The Gap We Address

India's artisan economy — 7 million+ craftspeople — remains largely invisible to digital commerce. Government initiatives like Shilp Samagam and Surajkund Mela provide seasonal exposure, but the moment the fair ends, the sales stop.

The barriers are not effort or talent. They are:

- **Technical friction** — e-commerce demands studio photography, English SEO descriptions, and typing-heavy onboarding
- **Language exclusion** — most platforms assume Hindi or English fluency, leaving regional-language artisans behind
- **Pricing exploitation** — without market awareness, artisans consistently undervalue their work or lose margins to intermediaries
- **Connectivity poverty** — rural clusters often lack reliable internet, making cloud-only apps useless

**Craftsy was designed from day one to work in zero-connectivity environments, in any Indian language, with zero typing required.**

---

## What Craftsy Does

### One Photo → Studio-Quality Product Shot

The artisan points their phone camera at their craft. A 10-stage computer vision pipeline removes cluttered backgrounds, corrects lighting, auto-crops to square format, and compresses for fast upload — producing an e-commerce-ready asset from a budget phone photo.

### One Voice Note → Bilingual Listing

The artisan speaks naturally in their regional language. Speech-to-text transcribes, translation models clean up, and an LLM structures the output into a bilingual (English + Hindi) product listing with title, description, SEO tags, and category — then reads it back aloud for confirmation.

### Fair Pricing, Not Predatory Pricing

A dual-layer pricing engine combines a mathematical cost floor (materials + labour + transport + overhead) with market-reference data from indexed handicraft listings. The result: a suggested price range with transparent reasoning the artisan can accept, adjust, or override.

### Offline-First, Always

Every photo, voice note, and draft is stored locally on the device. When connectivity returns, a background sync queue drains automatically with exponential backoff. Nothing is ever lost waiting for a signal.

### Human-in-the-Loop

Every AI decision — image, listing, and price — is read aloud via on-device bilingual TTS and requires the artisan's manual approval before going live. The AI assists; the artisan decides.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Flutter Mobile Client                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Camera  │  │  Voice   │  │  Local   │  │  TTS     │   │
│  │  Capture │  │  Record  │  │  Queue   │  │  Readback│   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │              │              │              │         │
│       └──────────────┴──────────────┴──────────────┘         │
│                          │                                    │
│                    ┌─────┴─────┐                             │
│                    │  Drift +  │                             │
│                    │  Hive DB  │                             │
│                    └─────┬─────┘                             │
└──────────────────────────┼──────────────────────────────────┘
                           │ (sync on reconnect)
                    ┌──────┴──────┐
                    │  FastAPI    │
                    │  Backend    │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐
    │  Image      │ │  Voice      │ │  Pricing    │
    │  Pipeline   │ │  Pipeline   │ │  Engine     │
    │  rembg+OpenCV│ │  Whisper+   │ │  Cost Floor │
    │  +Pillow    │ │  IndicTrans │ │  +ChromaDB  │
    └─────────────┘ └─────────────┘ └─────────────┘
```

---

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Mobile** | Flutter 3.x, Dart | Cross-platform, offline-capable local storage |
| **State** | Riverpod 2.x | Reactive, decoupled state propagation |
| **Local DB** | Drift (SQLite), Hive | Offline queue, persistent storage |
| **Background sync** | WorkManager | Automatic drain on reconnect |
| **Backend** | FastAPI, SQLAlchemy 2.0 | Async REST API |
| **Database** | Supabase | Postgres + auth + object storage |
| **Vector store** | ChromaDB | Embedding-based market comparables |
| **Image pipeline** | rembg (U²-Net), OpenCV, Pillow | Background removal, auto-crop, correction |
| **Speech-to-text** | Whisper / Bhashini ASR | Regional dialect transcription |
| **Translation** | IndicTrans2 / Bhashini | 22 scheduled Indian languages |
| **LLM** | Groq Cloud (primary), Gemini (fallback) | Bilingual listing generation, chat |
| **Deployment** | Railway (PaaS) | Continuous cloud deployment |

---

## Getting Started

### Prerequisites

- [Flutter SDK](https://flutter.dev/docs/get-started/install) (3.x)
- [Python 3.11+](https://www.python.org/downloads/)
- [Supabase](https://supabase.com) account (free tier)
- [Groq API key](https://console.groq.com) (free tier)

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your GROQ_API_KEY and SUPABASE credentials
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend
flutter pub get
flutter run
```

### Build APK

```bash
cd frontend
flutter build apk --release --no-tree-shake-icons
```

---

## Project Structure

```
craftsy/
├── frontend/              # Flutter mobile app
│   ├── lib/
│   │   ├── core/          # Theme, routing, offline sync, TTS
│   │   ├── data/          # Services, models, API clients
│   │   └── features/      # Screens & widgets per feature
│   ├── assets/            # Images, translations, fonts
│   └── test/              # Widget & unit tests
├── backend/               # FastAPI service
│   ├── routers/           # API endpoints
│   ├── services/          # Business logic
│   ├── models/            # Pydantic schemas & DB models
│   └── tests/             # Integration tests
├── ML/                    # Standalone ML pipelines
│   ├── image_pipeline/    # rembg, OpenCV, Pillow
│   ├── voice_pipeline/    # Whisper, Bhashini, glossary
│   └── pricing/           # Cost floor + ChromaDB RAG
├── docs/                  # Architecture, research, ideas
├── submission/            # SIH submission materials
└── README.md
```

---

## Design Philosophy

Craftsy's visual identity is built on **Indigo Loom** — a deep, premium indigo base with warm amber accents, inspired by the rich dyes of Indian textile traditions. The geometric logo evokes a loom's warp and weft, with a central diamond representing the artisan's craft at the heart of the system.

Every design decision prioritizes:

- **Accessibility first** — large touch targets, high contrast, voice-first interaction
- **Trust through transparency** — every AI output is shown, read aloud, and approved
- **Resilience** — works fully offline, syncs automatically, never loses data
- **Dignity** — the artisan is the decision-maker; the AI is the assistant

---

## Research Foundation

This project builds on established ICTD (ICT for Development) research:

- Patel et al., *["Experiences Designing a Voice Interface for Rural India" (Avaaj Otalo)](https://dl.acm.org/doi/10.1145/1998249.1998258)* — voice input paired with confirmation buttons
- Medhi et al., *"Designing Mobile Interfaces for Novice and Low-Literacy Users" (VideoKheti)* — human-in-the-loop review safeguards
- Gala, Chitale et al., *["IndicTrans2," TMLR 2023](https://github.com/AI4Bharat/IndicTrans2)* — translation across 22 Indian languages
- Qin et al., *"U²-Net: Going Deeper with Nested U-Structure for Salient Object Detection," Pattern Recognition 2020* — background removal model

---

## Impact

- **Year-round income** — converts seasonal fair exposure into continuous digital storefront
- **Fair pricing** — cost-floor model protects artisans from information asymmetry
- **Financial inclusion** — timestamped sales history as alternative credit signal
- **Women artisan empowerment** — voice-first design overcomes mobility and literacy barriers
- **DPI alignment** — designed to plug into ONDC, GeM, and Bhashini

---

## License

Licensed under the [MIT License](LICENSE).

---

<div align="center">
<sub>Craftsy — Dignity through technology, not charity.</sub>
</div>
