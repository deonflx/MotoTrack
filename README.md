# 🏍️ MotoSync — AI-Powered Motorcycle Touring & Geospatial Convoy Platform

[![Django](https://img.shields.io/badge/Django-6.0.5-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![GeoDjango](https://img.shields.io/badge/GeoDjango-PostGIS-2C6E49?style=for-the-badge&logo=postgresql&logoColor=white)](https://docs.djangoproject.com/en/6.0/ref/contrib/gis/)
[![React 19](https://img.shields.io/badge/React-19.2.8-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-8.3.0-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![PostGIS](https://img.shields.io/badge/PostGIS-3.4-006400?style=for-the-badge&logo=postgis&logoColor=white)](https://postgis.net/)
[![Redis](https://img.shields.io/badge/Redis-7.4-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Google Gemini](https://img.shields.io/badge/Gemini-3.8_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![Clerk Auth](https://img.shields.io/badge/Clerk-RS256_JWT-6C47FF?style=for-the-badge&logo=clerk&logoColor=white)](https://clerk.com/)

An intelligent expedition management, highway route intelligence, and live convoy coordination system engineered specifically for long-distance motorcycle touring riders.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Key Features](#-key-features)
  - [1. Predictive 70% Fuel Range & Expanding Petrol Station Search](#1-predictive-70-fuel-range--expanding-petrol-station-search)
  - [2. Spatial Highway Corridor & Co-Traveler Matching](#2-spatial-highway-corridor--co-traveler-matching)
  - [3. Real-Time Multi-Rider Convoy Radar & HUD](#3-real-time-multi-rider-convoy-radar--hud)
  - [4. Dual-Tier AI Co-Pilot with Automated Fallback](#4-dual-tier-ai-co-pilot-with-automated-fallback)
  - [5. Micro-Climate Multi-Point Route Weather](#5-micro-climate-multi-point-route-weather)
  - [6. Stateless RS256 JWT Authentication & Object Security](#6-stateless-rs256-jwt-authentication--object-security)
  - [7. Hybrid PostGIS + Redis Storage Architecture](#7-hybrid-postgis--redis-storage-architecture)
- [Repository Structure](#-repository-structure)
- [Database Schema & Models](#-database-schema--models)
- [Redis Caching Schema](#-redis-caching-schema)
- [REST API Reference](#-rest-api-reference)
- [Prerequisites](#-prerequisites)
- [Local Setup & Installation](#-local-setup--installation)
  - [1. Clone Repository & Setup Environment](#1-clone-repository--setup-environment)
  - [2. PostGIS & Redis Setup via Docker](#2-postgis--redis-setup-via-docker)
  - [3. Backend Setup (GeoDjango & GDAL)](#3-backend-setup-geodjango--gdal)
  - [4. Frontend Setup (React 19 + Vite)](#4-frontend-setup-react-19--vite)
- [Environment Configuration](#-environment-configuration)
- [Production Deployment (Render Blueprint)](#-production-deployment-render-blueprint)
- [Documentation & Deep Dives](#-documentation--deep-dives)

---

## 🌟 Overview

Long-distance motorcycle expeditions demand proactive fuel planning, micro-climate weather tracking, and real-time coordination among dispersed group riders.

**MotoSync** solves three core highway touring challenges:
1. **Fuel Range Anxiety:** Predicts the exact 70% tank threshold point along highway driving polylines and dynamically surfaces nearby petrol stations before the rider runs out of fuel.
2. **Convoy Isolation:** Detects co-travelers riding proximate routes using computational road corridor buffering (~1.6 km) and vector cosine similarity.
3. **Distributed Group Sync:** Aggregates live GPS telemetry across all accepted convoy members, computes physical road distance gaps in real time, and renders a synchronized radar map with single-click viewport focus and WhatsApp convoy chat integration.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           CLIENT TIER (React 19 SPA)                            │
│  React Leaflet Maps • Live Telemetry Radar • Clerk Auth Bridge • Axios Client   │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │ HTTPS / REST (RS256 JWT Bearer)
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     API GATEWAY & SECURITY LAYER (Django 6.0)                   │
│  Gunicorn • WhiteNoise • CORS Headers • Clerk JWKS Token Verifier (RS256)      │
│  Object-Level Permissions (IsOwnerOrReadOnly, IsSessionOwner, IsParticipant)    │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        APPLICATION & SERVICE ENGINE                             │
│  ┌───────────────────────┬───────────────────────┬───────────────────────────┐  │
│  │   BikeTripViewSet     │  TripSessionViewSet   │ ConnectionRequestViewSet  │  │
│  ├───────────────────────┴───────────────────────┴───────────────────────────┤  │
│  │                     Geospatial & Service Modules                          │  │
│  │ • Nominatim Geocoding            • OSRM Driving Polyline Generator        │  │
│  │ • 70% Fuel Point Interpolation   • Overpass Expanding Radius Fuel Search  │  │
│  │ • Corridor Buffer Intersection   • Vector Dot-Product Direction Analysis  │  │
│  │ • Open-Meteo Multi-Point Weather • Multi-Model AI Fallback Orchestrator   │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────┬───────────────────────┘
                        │                                 │
           Spatial & Relational Writes             Key-Value Read/Write Cache
                        ▼                                 ▼
┌───────────────────────────────────────┐   ┌─────────────────────────────────────┐
│       POSTGRESQL 16 + POSTGIS         │   │              REDIS 7.4              │
│  • BikeTrip (Point & LineString)      │   │  • trip:<id>:fuel_stops (JSON)      │
│  • TripSession (Live GPS Points)      │   │  • trip:<id>:ai_summary (HTML)      │
│  • RouteWeather (Spatial Points)      │   │  • trip:<id>:ai_tips (HTML)         │
│  • ConnectionRequest (Convoy Graph)   │   │  • trip:<id>:ai_weather (Text)      │
│  • GIST R-Tree Spatial Indexes        │   │  • 7-Day TTL with Invalidation Hooks │
└───────────────────────────────────────┘   └─────────────────────────────────────┘
```

---

## ⚡ Key Features

### 1. Predictive 70% Fuel Range & Expanding Petrol Station Search
- **Proactive Safety Reserve:** Rather than waiting for the low-fuel indicator, the platform computes:
  $$\text{Max Range} = \text{Tank Capacity (L)} \times \text{Average Mileage (km/l)}$$
  $$\text{Refuel Target} = \text{Max Range} \times 0.70$$
- **Road Geometry Interpolation:** GeoDjango GEOS walks the exact turn-by-turn OSRM driving polyline (`LineStringField`) to locate the exact 70% coordinate point on the highway.
- **Expanding POI Radius Search:** Queries the OpenStreetMap Overpass API for `amenity=fuel` in stepped increments:
  $$2\text{ km} \longrightarrow 5\text{ km} \longrightarrow 10\text{ km} \longrightarrow 20\text{ km} \longrightarrow \text{up to } 100\text{ km}$$
  Stops at the earliest radius with viable fuel stations and sorts candidates by Haversine distance. Results are cached in Redis with a 7-day TTL.

### 2. Spatial Highway Corridor & Co-Traveler Matching
Matches riders on shared routes without requiring identical coordinate timestamps or discrete waypoint equality:
1. **Destination Proximity:** PostGIS `ST_Distance(destination_point, candidate.destination_point) <= 50 km` or city name substring match.
2. **Direction Vector Cosine Similarity:** Start and destination coordinates form displacement vectors $\vec{v}_A$ and $\vec{v}_B$. The system verifies:
   $$\cos \theta = \frac{\vec{v}_A \cdot \vec{v}_B}{\|\vec{v}_A\| \|\vec{v}_B\|} \ge 0.0$$
   Eliminates opposing-direction traffic (e.g. Bangalore $\to$ Mysore vs. Mysore $\to$ Bangalore).
3. **Geometric Road Corridor Buffering:** Dilates Path A using GEOS `path.buffer(0.015°)` (~$1.6\text{ km}$ road corridor) and intersects Path B.
4. **Match Threshold:** Classified as matching co-travelers if:
   $$\text{Shared Distance} \ge 5\text{ km} \quad \text{OR} \quad (\text{Overlap} \ge 20\% \text{ AND Shared Distance} \ge 2\text{ km})$$

### 3. Real-Time Multi-Rider Convoy Radar & HUD
- **Hardware Telemetry Streaming:** Active riders emit GPS breadcrumbs via `navigator.geolocation.watchPosition` through `PATCH /api/sessions/<id>/`.
- **Spatial Telemetry Aggregation:** The backend queries all accepted connection partners in the pack, computes real-time distance gaps (`gap_km`) to each companion using the Haversine formula, and returns live pack metrics.
- **Dual-Sync Latency Engine:** Immediate push payload on each GPS transmission + a 4-second background poller loop.
- **Interactive Multi-User Map:**
  - **Self Pin:** Pulsing blue radar marker (`pulse-ring`).
  - **Partner Pins:** Emerald-green radar pins displaying companion initials (e.g. `'D'`, `'A'`) and distance popups.
  - **Pack Radar HUD:** Real-time distance leaderboard, active live counts (e.g. `3/3 Live`), and a **"Focus Pack"** button that dynamically fits Leaflet map bounds around all distributed convoy members.
  - **Convoy Group Chat:** Quick-access button to the pack's dedicated WhatsApp group invite link.

### 4. Dual-Tier AI Co-Pilot with Automated Fallback
Engineered for zero downtime and low latency:
```
[User Input Motorcycle Name]
             │
             ▼
[Curated Dataset Matching] ──▶ 100_popular_bikes_india.csv (instant specs lookup)
             │ (if bike not found or CSV missing)
             ▼
[Google Gemini 3.8 Flash] ──▶ High-speed model via google-genai SDK
             │ (if rate-limited or unavailable)
             ▼
[Google Gemini 3.5 Lite]  ──▶ Lightweight fallback
             │ (if unavailable)
             ▼
[OpenAI GPT-4o-mini]     ──▶ High-availability secondary provider
             │ (if all external APIs fail)
             ▼
[Deterministic Defaults] ──▶ 15.0 L tank capacity | 35.0 km/l mileage
```
- **Expedition Advisory:** Generates fuel consumption estimates (including a 10% detour margin), fuel costs (at ₹113/L), riding time calculations, break schedules, and weather-conditioned safety warnings.

### 5. Micro-Climate Multi-Point Route Weather
- Samples weather at 3 geographic points along the route: **Origin**, **Midpoint**, and **Destination**.
- Fetches real-time temperature, wind speed, precipitation probability, and WMO weather codes via the Open-Meteo API.
- Persists observations in PostGIS [`RouteWeather`](file:///c:/Users/DEON/OneDrive/Desktop/bike/bike_project/bike_app/models.py#L78-L94) records to enable spatial caching and route-wide weather reusability.

### 6. Stateless RS256 JWT Authentication & Object Security
- **Stateless Decoupled Auth:** Frontend signs in via Clerk SDK; Axios injects short-lived JWT tokens as `Bearer <token>`.
- **Asymmetric In-Memory Verification:** Django backend [`ClerkAuthentication`](file:///c:/Users/DEON/OneDrive/Desktop/bike/bike_project/bike_app/authentication.py#L11-L100) fetches public keys from Clerk's JWKS endpoint using `PyJWKClient` (1-hour cache), cryptographically validating RS256 signatures in memory without outbound network calls per request.
- **Just-In-Time (JIT) Provisioning:** Resolves Clerk `sub` ID to Django's native `auth.User`.
- **Strict Object Permissions:**
  - [`IsOwnerOrReadOnly`](file:///c:/Users/DEON/OneDrive/Desktop/bike/bike_project/bike_app/permissions.py#L5-L16): Only trip owners can modify or delete expeditions.
  - [`IsSessionOwnerOrReadOnly`](file:///c:/Users/DEON/OneDrive/Desktop/bike/bike_project/bike_app/permissions.py#L19-L38): Only trip owners can transmit live GPS telemetry (`PATCH`). Spectators have public read access.
  - [`IsConnectionParticipant`](file:///c:/Users/DEON/OneDrive/Desktop/bike/bike_project/bike_app/permissions.py#L41-L54): Only sender or receiver can view/cancel invitations; only the receiver can accept or decline.

### 7. Hybrid PostGIS + Redis Storage Architecture
| Data Entity | Store | Model / Structure | Reason |
|---|---|---|---|
| Route endpoints & paths | **PostGIS** | `BikeTrip.starting_point`, `destination_point`, `route_path` | Spatial queries, line buffering, GIST R-Tree indexing |
| Live GPS telemetry | **PostGIS** | `TripSession.current_location` | Geospatial point updates, proximity calculation |
| Multi-point route weather | **PostGIS** | `RouteWeather.location`, `description` | Spatially reusable and queryable along highway corridors |
| Convoy connections | **PostgreSQL** | `ConnectionRequest` | Relational integrity, foreign key cascading, unique constraints |
| 70% refuel point & petrol stops | **Redis** | `trip:<id>:fuel_stops` (JSON String) | Sub-millisecond payload caching, 7-day TTL |
| AI route advisory & tips | **Redis** | `trip:<id>:ai_summary`, `trip:<id>:ai_tips` (HTML) | <15ms response time, shields LLM API quotas |
| Route weather text | **Redis** | `trip:<id>:ai_weather` (Text) | Cached weather context for prompt generation |

---

## 📁 Repository Structure

```
bike/
├── 100_popular_bikes_india.csv       # Curated motorcycle dataset (capacity, mileage, specs)
├── docker-compose.yml               # Local PostGIS 16 Docker service definition
├── render.yaml                      # Production blueprint for Render (Django + Redis)
├── PROJECT_ABSTRACT.md              # Architectural design document & interview guide
├── implementation_plan.md           # Engineering implementation plan
├── bike_project/                    # Django 6.0 Backend with GeoDjango
│   ├── manage.py                    # Django management CLI
│   ├── requirements.txt             # Python dependencies
│   ├── build.sh                     # Production build script (migrate + collectstatic)
│   ├── bike_project/                # Backend settings & configuration
│   │   ├── settings.py              # Settings, PostGIS, Clerk, Redis, GDAL paths
│   │   ├── urls.py                  # Root URL configuration
│   │   ├── wsgi.py                  # WSGI entrypoint for Gunicorn
│   │   └── asgi.py                  # ASGI entrypoint
│   └── bike_app/                    # Core application logic
│       ├── models.py                # BikeTrip, TripSession, RouteWeather, ConnectionRequest
│       ├── api_views.py             # DRF ViewSets (trips, sessions, weather, connections)
│       ├── serializers.py           # GeoJSON & spatial DRF serializers
│       ├── services.py              # Nominatim geocoding, OSRM routing, Overpass fuel query
│       ├── ai_helper.py             # Dual-engine LLM fallback (Gemini -> OpenAI) + CSV parser
│       ├── redis_client.py          # Centralized Redis client & caching utilities
│       ├── authentication.py       # Custom Clerk RS256 JWKS JWT authentication backend
│       ├── permissions.py          # Granular object-level permissions
│       └── urls.py                  # REST API router endpoints
└── frontend/                        # React 19 + Vite Frontend SPA
    ├── package.json                 # Node dependencies (@clerk/clerk-react, leaflet, etc.)
    ├── vite.config.js               # Vite configuration
    ├── index.html                   # HTML template with Google Fonts (Inter, Outfit)
    └── src/
        ├── main.jsx                 # ClerkProvider initialization & root routing
        ├── App.jsx                  # Navigation, Expedition Logbook, Slide-over modal
        ├── TripDetail.jsx           # Interactive Leaflet map, refuel stops, AI summary, co-travelers
        ├── LiveTracking.jsx         # Live GPS radar HUD, multi-rider markers, WhatsApp convoy sync
        ├── Invitations.jsx          # Connection request manager (incoming, sent, accepted)
        ├── api.js                   # Axios client with automatic Clerk JWT token injection
        ├── App.css                  # Cyber-touring aesthetic styles, pulsing radar animations
        └── index.css                # Base design tokens and CSS variables
```

---

## 🗄️ Database Schema & Models

### [`BikeTrip`](file:///c:/Users/DEON/OneDrive/Desktop/bike/bike_project/bike_app/models.py#L6-L47)
- `user`: Foreign key to `auth.User` (owner of the trip).
- `bikename`: Motorcycle make and model string (e.g. `"Royal Enfield Himalayan 450"`).
- `capacity`: Fuel tank capacity in liters (`FloatField`).
- `mileage`: Real-world mileage in km/l (`FloatField`).
- `starting_name` / `destination_name`: Human-readable location labels.
- `starting_point` / `destination_point`: Geocoded `gis_models.PointField(srid=4326)` coordinates.
- `route_path`: `gis_models.LineStringField(srid=4326)` representing the full driving polyline.
- `whatsapp_group_link`: Optional WhatsApp convoy group invite link (`URLField`).
- `created_at`: Creation timestamp.

### [`TripSession`](file:///c:/Users/DEON/OneDrive/Desktop/bike/bike_project/bike_app/models.py#L48-L76)
- `bike_trip`: Foreign key to `BikeTrip`.
- `status`: State machine status (`'active'` | `'completed'`).
- `current_location`: Real-time GPS coordinate `gis_models.PointField(srid=4326)`.
- `started_at` / `updated_at`: Live timestamps.

### [`RouteWeather`](file:///c:/Users/DEON/OneDrive/Desktop/bike/bike_project/bike_app/models.py#L78-L94)
- `bike_trip`: Foreign key to `BikeTrip`.
- `location`: Exact GPS point of the weather observation `gis_models.PointField(srid=4326)`.
- `description`: Formatted weather observation string (temperature, wind, condition).
- `recorded_at`: Timestamp for cache freshness validation.

### [`ConnectionRequest`](file:///c:/Users/DEON/OneDrive/Desktop/bike/bike_project/bike_app/models.py#L95-L128)
- `sender`: User initiating the convoy invitation.
- `receiver`: User receiving the convoy invitation.
- `bike_trip`: Reference to the shared `BikeTrip`.
- `status`: Invitation status (`'pending'` | `'accepted'` | `'rejected'`).
- Unique constraint: `unique_together = ('sender', 'receiver', 'bike_trip')`.

---

## ⚡ Redis Caching Schema

All cached items are configured with a **7-Day TTL (604,800 seconds)** and automatic invalidation hooks via [`delete_trip_cache(trip_id)`](file:///c:/Users/DEON/OneDrive/Desktop/bike/bike_project/bike_app/redis_client.py#L151-L165):

| Redis Key | Data Type | Content Description |
|---|---|---|
| `trip:<id>:fuel_stops` | String (JSON) | Pre-calculated 70% refuel coordinates, total route distance, and nearby petrol stations. |
| `trip:<id>:ai_summary` | String (HTML) | Cached route summary, estimated fuel liters consumed, cost in INR, and driving time. |
| `trip:<id>:ai_tips` | String (HTML) | Detailed markdown-rendered safety advice, highway warnings, and break schedule. |
| `trip:<id>:ai_weather` | String (Text) | Cached pipe-separated multi-point weather text for quick prompt assembly. |

---

## 📡 REST API Reference

Base URL: `http://localhost:8000/api`

### Expeditions & Routing (`/api/trips/`)

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `GET` | `/api/trips/` | No | List all logged expeditions. |
| `POST` | `/api/trips/` | **Yes (JWT)** | Log a new expedition (auto-geocodes, queries AI specs, computes fuel stops). |
| `GET` | `/api/trips/<id>/` | No | Retrieve detailed expedition data (coordinates, specs, route path). |
| `PUT` / `PATCH` | `/api/trips/<id>/` | **Yes (Owner)** | Update expedition metadata or bike model. |
| `DELETE` | `/api/trips/<id>/` | **Yes (Owner)** | Delete expedition and purge related Redis cache. |
| `GET` | `/api/trips/my_expeditions/` | **Yes (JWT)** | Filter expeditions belonging strictly to the signed-in user. |
| `GET` | `/api/trips/<id>/fuel_stops/` | No | Fetch pre-cached 70% refuel target and nearby petrol pumps (append `?refresh=true` to force). |
| `POST` | `/api/trips/<id>/generate_summary/`| No | Generate or retrieve cached AI route & fuel cost advisory. |
| `POST` | `/api/trips/<id>/ai_tips/` | No | Generate detailed motorcycle safety advice & break schedule. |
| `GET` | `/api/trips/<id>/co_travelers/` | No | Discover matching riders along the highway corridor or proximate destination. |
| `POST` | `/api/trips/<id>/start_session/` | **Yes (Owner)** | Launch or resume an active GPS live tracking session. |
| `POST` | `/api/trips/<id>/set_whatsapp_link/`| **Yes (Owner)** | Set or update the WhatsApp group invite URL for the convoy. |

### Live GPS Tracking Sessions (`/api/sessions/`)

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `GET` | `/api/sessions/<id>/` | No | Public / spectator read of real-time GPS coordinates and active convoy members. |
| `PATCH` | `/api/sessions/<id>/` | **Yes (Owner)** | Transmit live GPS coordinates: `{"lat": 12.9716, "lng": 77.5946}`. |
| `POST` | `/api/sessions/<id>/end_session/` | **Yes (Owner)** | Transition tracking session status to `'completed'`. |
| `DELETE` | `/api/sessions/<id>/` | **Yes (Owner)** | Remove tracking session record. |
| `POST` | `/api/sessions/<id>/set_whatsapp_link/`| **Yes (Owner)** | Update shared WhatsApp link via active session. |

### Convoy Connections & Invitations (`/api/connections/`)

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| `GET` | `/api/connections/` | **Yes (JWT)** | View invitations (filters: `?type=incoming`, `?type=sent`, `?type=accepted`). |
| `POST` | `/api/connections/` | **Yes (JWT)** | Send a ride invitation: `{"receiver": <user_id>, "bike_trip": <trip_id>}`. |
| `POST` | `/api/connections/<id>/respond/`| **Yes (Recipient)**| Accept or decline an invitation: `{"action": "accept"}` or `{"action": "reject"}`. |
| `DELETE` | `/api/connections/<id>/` | **Yes (Participant)**| Cancel or withdraw an invitation. |

---

## 💻 Prerequisites

Ensure you have the following installed locally:
- **Python 3.12+**
- **Node.js 18+ & npm**
- **Docker & Docker Compose** (for running PostGIS & Redis)
- **OSGeo4W / GDAL C-Libraries** (only if running GeoDjango natively on Windows without Docker)
- API Keys:
  - **Google Gemini API Key** (from [Google AI Studio](https://aistudio.google.com/))
  - **OpenAI API Key** (optional, fallback from [OpenAI Platform](https://platform.openai.com/))
  - **Clerk Publishable & Secret Keys** (from [Clerk Dashboard](https://dashboard.clerk.com/))

---

## 🚀 Local Setup & Installation

### 1. Clone Repository & Setup Environment

```bash
git clone https://github.com/your-username/bike.git
cd bike
```

---

### 2. PostGIS & Redis Setup via Docker

Start the containerized PostGIS 16 spatial database using the included [`docker-compose.yml`](file:///c:/Users/DEON/OneDrive/Desktop/bike/docker-compose.yml):

```bash
docker compose up -d
```

> **Note:** The container runs on port `5433` (`5433:5432`) to prevent conflicts with any local PostgreSQL instance installed on default port 5432.

If you don't have a local Redis instance installed, run Redis in a container as well:
```bash
docker run -d --name redis-cache -p 6379:6379 redis:7-alpine
```

---

### 3. Backend Setup (GeoDjango & GDAL)

#### A. Create Python Virtual Environment
```bash
cd bike_project
python -m venv .venv

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# On macOS/Linux:
source .venv/bin/activate
```

#### B. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### C. Windows OSGeo4W / GDAL Configuration (Windows Only)
GeoDjango requires GDAL, GEOS, and PROJ C-libraries. On Windows:
1. Download and run the **OSGeo4W Network Installer** from [OSGeo4W](https://trac.osgeo.org/osgeo4w/).
2. Select **Express Install** with GDAL and PROJ packages installed into `C:\OSGeo4W`.
3. The project [`settings.py`](file:///c:/Users/DEON/OneDrive/Desktop/bike/bike_project/bike_project/settings.py#L27-L37) automatically configures the library paths when running on Windows (`os.name == 'nt'`).

#### D. Configure Environment Variables
Create a `.env` file inside `bike_project/.env`:
```env
# AI Providers
GOOGLE_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Database (connecting to local Docker PostGIS on port 5433)
DB_NAME=gisdb
DB_USER=postgres
DB_PASSWORD=9f324689154c4a17b3b2151126d073e4
DB_HOST=localhost
DB_PORT=5433

# Redis Cache
REDIS_URL=redis://localhost:6379

# Django
DEBUG=True
SECRET_KEY=your-django-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Clerk Authentication (Optional local JWKS URL)
CLERK_SECRET_KEY=sk_test_...
CLERK_PUBLISHABLE_KEY=pk_test_...
```

#### E. Run Migrations & Start Server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8000
```
Backend API will be running at `http://127.0.0.1:8000/api/`.

---

### 4. Frontend Setup (React 19 + Vite)

#### A. Install Node Dependencies
```bash
cd ../frontend
npm install
```

#### B. Configure Frontend Environment Variables
Create a `.env` file inside `frontend/.env`:
```env
VITE_API_URL=http://127.0.0.1:8000/api
VITE_CLERK_PUBLISHABLE_KEY=pk_test_your_clerk_key_here
VITE_CARTO_API_KEY=cb1_3yu3_1_95c86b8e5ae70fdb821e4cc2
```

#### C. Run Vite Development Server
```bash
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## ⚙️ Environment Configuration

### Backend (`bike_project/.env`)
| Variable | Description | Default / Example |
|---|---|---|
| `GOOGLE_API_KEY` | Google Gemini API Key | Required for AI specs & route analysis |
| `OPENAI_API_KEY` | OpenAI API Key | Fallback LLM provider |
| `DB_NAME` | PostGIS database name | `gisdb` |
| `DB_USER` | Database username | `postgres` |
| `DB_PASSWORD` | Database password | Password defined in Docker / Supabase |
| `DB_HOST` | Database host | `localhost` (or cloud host) |
| `DB_PORT` | Database port | `5433` (Docker) or `5432` |
| `REDIS_URL` | Redis connection URI | `redis://localhost:6379` |
| `SECRET_KEY` | Django cryptographic secret | Django secret string |
| `DEBUG` | Enable debug mode | `True` (dev) / `False` (prod) |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `*` or `localhost,127.0.0.1` |
| `CLERK_PUBLISHABLE_KEY` | Clerk Frontend Publishable Key | `pk_test_...` |
| `CLERK_SECRET_KEY` | Clerk Backend Secret Key | `sk_test_...` |
| `CLERK_JWKS_URL` | Explicit JWKS URL (optional) | Auto-discovered from issuer domain |

### Frontend (`frontend/.env`)
| Variable | Description | Example |
|---|---|---|
| `VITE_API_URL` | Backend REST API root | `http://127.0.0.1:8000/api` |
| `VITE_CLERK_PUBLISHABLE_KEY` | Clerk Frontend Key | `pk_test_...` |
| `VITE_CARTO_API_KEY` | CartoDB map tile key | Map tile access token |

---

## ☁️ Production Deployment (Render Blueprint)

The repository includes a ready-to-deploy [`render.yaml`](file:///c:/Users/DEON/OneDrive/Desktop/bike/render.yaml) blueprint configuring:
1. **Django Web Service:** Running Python 3.12, Gunicorn with 3 workers, WhiteNoise static asset serving, and automatic HTTPS.
2. **Managed Redis Instance:** Low-latency caching instance with `allkeys-lru` eviction policy.

### Deployment Steps:
1. Push your repository to GitHub.
2. Log into [Render](https://render.com/) and navigate to **Blueprints**.
3. Connect your repository and select [`render.yaml`](file:///c:/Users/DEON/OneDrive/Desktop/bike/render.yaml).
4. Fill in the sensitive environment variables in the Render Dashboard:
   - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` (pointing to PostGIS on Supabase or Neon).
   - `GEMINI_API_KEY`, `OPENAI_API_KEY`.
5. Render will automatically execute [`bike_project/build.sh`](file:///c:/Users/DEON/OneDrive/Desktop/bike/bike_project/build.sh), install dependencies, run migrations, collect static files, and launch the service.

---

## 📖 Documentation & Deep Dives

For comprehensive architecture analyses, algorithmic justifications, and technical interview preparation notes:
- **[PROJECT_ABSTRACT.md](file:///c:/Users/DEON/OneDrive/Desktop/bike/PROJECT_ABSTRACT.md):** 600+ lines covering the mathematical derivation of corridor matching, stateless RS256 JWT security, real-time telemetry fan-out, and technical interview Q&A.
- **[implementation_plan.md](file:///c:/Users/DEON/OneDrive/Desktop/bike/implementation_plan.md):** Architectural split between PostGIS spatial fields and Redis sub-millisecond key-value stores.

---

## 📄 License

This project is licensed under the MIT License — see the LICENSE file for details.
