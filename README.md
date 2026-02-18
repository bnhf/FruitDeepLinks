# 🍎 FruitDeepLinks

**Universal Sports Aggregator for Channels DVR**

FruitDeepLinks leverages Apple TV's Sports aggregation APIs to build a unified sports EPG with deeplinks to 24+ streaming services. One guide to rule them all.

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

## 🎯 The Problem

Sports streaming is fragmented:

- NFL on Prime Video (Thursday), ESPN+ (Monday), Peacock (Sunday)
- MLS exclusively on Apple TV
- College sports scattered across ESPN+, Paramount+, Peacock, etc.
- You have multiple subscriptions but need to check multiple apps just to find games

## ✨ The Solution

FruitDeepLinks creates virtual TV channels in Channels DVR with deeplinks that launch directly into your streaming apps.

**One EPG. All your sports. All your services.**

---

## 🆕 What's New

### Latest Features (February 2026)

**🎬 Prismcast Output (Documented)**
- Full support for Prismcast's white-label streaming platform
- Generates M3U and XMLTV exports compatible with Prismcast's schedule expectations
- Deeplinks properly formatted for embedded Prismcast playback
- Includes sport/league categorization for Prismcast channel organization
- Multi-service playable support for Prismcast environments
- Foundation for broader OTT platform expansion

**🆕 Experimental NESN Support**
- **NESN** (New England Sports Network) - Regional baseball, hockey, and basketball for Boston area
- Event data successfully scraped from Apple TV Sports API
- Deeplink format under investigation for optimal playback compatibility
- Marked EXPERIMENTAL while deeplink pattern is refined
- Expected stabilization with community feedback and testing

**Previously Added (January 2026)**

**🛒 Amazon Channel Integration**
- Advanced scraping system identifies which Amazon Prime Video Channel is required for each event
- Discovers NBA League Pass, Peacock Premium, DAZN, FOX One, ViX Premium, Max, and 10+ other channels
- Tracks channel requirements in new `amazon_channels` database table
- `v_amazon_playables_with_channels` view provides comprehensive channel mapping
- Async/parallel scraping with smart 7-day caching for performance
- Detects "stale" events (404s) to maintain data accuracy
- Foundation for future user-selectable Amazon channel filtering

**Four New Streaming Services (Experimental)**
- **Victory+** - Regional college sports content
- **Fanatiz Soccer** - International soccer leagues
- **beIN Sports** - International soccer, rugby, motorsports  
- **Gotham Sports** - NYC regional sports (Knicks, Rangers, Islanders, Devils, Yankees, Nets)
- Note: These services are marked EXPERIMENTAL - deeplink formats still being discovered
- Event data scraped successfully, seeking community help to identify working deeplink patterns

**Enhanced Title Formatting**
- ESPN-style league/sport prefixes for better event organization
- Consistent title formatting across all export types
- Improved metadata presentation in EPG

**Genre Normalization**
- Automatic cleanup of malformed categories
- Prevents bad genre data from affecting filters
- More reliable sports/league classification

**Performance Improvements**
- Hybrid scraping approach (Selenium + HTTP) for faster data collection
- Improved `--skip-scrape` flag handling for rapid refreshes
- Better provider detection in exports
- 5,000 line log buffer (up from 500) for better debugging

### Core Features

**🔥 ESPN Watch Graph API Integration**
- Fixes ESPN deeplink compatibility with Fire TV and Android TV devices
- Automatically enriches ESPN events with Fire TV-compatible deeplinks
- Scrapes ESPN's Watch Graph API daily (2,000+ events, 14 days forward)
- 71.7% match rate for current ESPN events
- Works across all export types: ADB lanes, virtual lanes, and direct channels
- Falls back to Apple TV deeplinks for unmatched events

**🎬 CDVR Detector - Automatic App Launching**
- Tune to a Fruit Lane in Channels DVR → streaming app launches automatically!
- Detects which device is watching and launches the correct service (ESPN+, Peacock, etc.)
- Supported on Apple TV, Fire TV, and Android TV
- No manual app switching required

**📊 Standards-Compliant XMLTV Exports**
- Proper `<live/>` and `<new/>` tags for EPG consumers
- Structured category taxonomy (Provider, Sport, League, "Sports Event")
- Sport/league metadata from Apple's classification system
- Clean placeholders with no unnecessary tags
- Shared `xmltv_helpers.py` module for consistent tagging across all exporters

**🌏 Kayo Sports Integration**
- Full Australian sports streaming support (Cricket, AFL, NRL, etc.)
- Web-based deeplink generation
- Integrated into multi-provider selection

### Enhanced Multi-Provider Support

- **Enhanced Apple scrape** preserves richer service metadata and captures multiple playable/deeplink options per event
- **User-adjustable service priority** - control which provider wins when multiple options exist
- **Multi-service selection helpers** to identify events available on multiple services
- **Improved ADB compatibility** for Android/Fire workflows
- **Improved HTTP fallback generation** for cases where native schemes aren't usable
- **Metadata/labeling fixes** - categories/descriptions match the chosen provider accurately

---

## 🚀 Quick Start (Portainer – Recommended)

These steps assume you already have **Docker** and **Portainer** running on your server.

### 1. Add a Git-backed stack in Portainer

1. Open Portainer in your browser.
2. Go to **Stacks → Add stack**.
3. Choose the **Repository** method.
4. Fill in:
   - **Name:** `fruitdeeplinks`
   - **Repository URL:** `https://github.com/kineticman/FruitDeepLinks.git`
   - **Repository reference:** `main` (or whatever branch you want)
   - **Compose path:** `docker-compose.yml`

Portainer will clone the repo and use `docker-compose.yml` plus the included `Dockerfile` to build the container image locally.

### 2. Set environment variables in Portainer

Scroll down to the **Environment variables** section for the stack.

Most people only need to set these four values:

```env
# REQUIRED (typical setup for Channels DVR)
SERVER_URL=http://192.168.86.80:6655
FRUIT_HOST_PORT=6655
CHANNELS_DVR_IP=192.168.86.80
TZ=America/New_York
```

If you want extra automation / features, you can add these as well:

```env
# OPTIONAL (only if you want extra automation/features)

# Auto Channels DVR guide refresh
CHANNELS_SOURCE_NAME=fruitdeeplinks-direct  # must match your Channels "Custom Channels" source name

# Chrome Capture / Channels4Chrome (BETA) – only if you use CC4C/AH4C or CH4C
CC_SERVER=192.168.86.80
CC_PORT=8020  # Chrome Capture port
CH4C_SERVER=192.168.86.80
CH4C_PORT=8020  # Channels4Chrome port (can be same or different)

# Lanes (BETA) – only needed if you experiment with lane channels
FRUIT_LANES=50
FRUIT_LANE_START_CH=9000

# Direct lanes channel numbering – separates direct lanes from virtual lanes in your guide
FRUIT_DIRECT_START_CH=5000

# Prismcast output (optional) – if using Prismcast platform integration
PRISMCAST_OUTPUT=true
```

Notes:

- If you **omit** an env var, Docker uses the default from `docker-compose.yml` (the part after `:-`).
- Most users only need to set the four **REQUIRED** values.
- `CHANNELS_DVR_IP` should be the IP/hostname of your Channels DVR server.
- `CHANNELS_SOURCE_NAME` is only needed if you want FruitDeepLinks to auto-refresh a specific Channels "Custom Channels" source.
- `CC_SERVER` / `CC_PORT` and `CH4C_SERVER` / `CH4C_PORT` are only needed if you're using **Chrome Capture (CC4C/AH4C)** or **Channels4Chrome (CH4C)**. Both can share the same host/port if desired.
- `SERVER_URL` is the base URL embedded in generated links (it should be reachable by your playback devices).
- `FRUIT_HOST_PORT` is the host port Docker exposes; it should match the port in `SERVER_URL`.
- Scheduling/refresh runs via **APScheduler** inside the container (no cron).
- Lanes (`FRUIT_LANES`, `FRUIT_LANE_START_CH`, etc.) are only used if you experiment with the **BETA** lane features.
- `FRUIT_DIRECT_START_CH` controls the starting channel number for direct lanes (default: 5000), keeping them separate from virtual lanes in your channel guide.
- `PRISMCAST_OUTPUT` generates Prismcast-compatible M3U and XMLTV files in addition to standard Channels DVR exports.

### 3. Deploy the stack

1. Click **Deploy the stack**.
2. Wait for Portainer to pull the repo, build the image, and start the container.
3. Open the dashboard in your browser:

```text
http://<LAN-IP>:<FRUIT_HOST_PORT>
# example: http://192.168.86.80:6655
```

You should see the FruitDeepLinks web UI.

---

## ➕ Alternative: Docker Compose (without Portainer)

If you prefer bare Docker Compose on the host (Windows PowerShell):

```powershell
git clone https://github.com/kineticman/FruitDeepLinks.git
cd FruitDeepLinks

Copy-Item .env.example .env
# Edit .env to match your LAN IP, timezone, Channels DVR IP, etc.

docker compose up -d

# Web UI: http://localhost:6655
```

Portainer and Docker Compose both use the same `docker-compose.yml`. The only difference is where you manage the environment variables.

---

## 📡 Add to Channels DVR

### Direct Channels (recommended & stable)

Direct channels expose **one channel per event** (great for browsing specific games). This is the most tested and stable path today.

1. In Channels DVR, go to **Settings → Sources → Add Source → Custom Channels**.
2. Create a new source named e.g. `fruitdeeplinks-direct` (if you enable auto-refresh, set `CHANNELS_SOURCE_NAME` to this exact name):
   - **M3U URL:** `http://your-server-ip:6655/direct.m3u`
   - **XMLTV URL:** `http://your-server-ip:6655/direct.xml`
3. In that **direct** source's settings, set **Stream Format** to **`STRMLINK`**.  
   This is required so Channels passes the deeplink URL through to your device.
4. Refresh guide data.

To enable automatic guide refresh, make sure the **Custom Channels source name in Channels DVR** exactly matches `CHANNELS_SOURCE_NAME` (default: `fruitdeeplinks-direct`).

### Lanes & ADB Provider Lanes (BETA)

> Lanes and ADB provider lanes are **BETA / upcoming features**. API and behavior may still change.

**Lane Channels (multisource_lanes – BETA)**

1. (Optional) Create another Custom Channels source named e.g. `fruitdeeplinks-lanes`.
2. Use:
   - **M3U URL (lanes, BETA):** `http://your-server-ip:6655/multisource_lanes.m3u`
   - **XMLTV URL (lanes, BETA):** `http://your-server-ip:6655/multisource_lanes.xml`

---

## 📋 Supported Streaming Services

FruitDeepLinks aggregates sports from **24+ streaming services**:

### Tier 1: Fully Integrated (Stable)

| Service | Deeplink Status | Notable Content |
|---------|-----------------|-----------------|
| **ESPN+** | ✅ Stable | MLS, most college sports, select UFC |
| **Peacock** | ✅ Stable | Premier League, NBC Sports, many college sports |
| **Paramount+** | ✅ Stable | Champions League, college football, NFL |
| **Max** | ✅ Stable | HBO Sports, selected events |
| **Apple TV** | ✅ Stable | MLS (exclusive), select Apple TV+ events |
| **Prime Video** | ✅ Stable | Thursday Night Football, select sports |
| **Kayo Sports** | ✅ Stable | Cricket, AFL, NRL (Australia) |
| **ViX** | ✅ Stable | Liga MX, Copa América, international soccer |
| **DAZN** | ✅ Stable | Combat sports, select leagues (regional) |
| **NBA League Pass** | ✅ Stable (via Prime) | NBA regular season & playoffs |
| **WNBA League Pass** | ✅ Stable (via Prime) | WNBA |
| **NHL.tv** | ✅ Stable | Hockey (direct service) |
| **Bravo** | ✅ Stable | WWE events |
| **TUDN** | ✅ Stable | Soccer, select sports (Spanish) |
| **Pluto TV** | ✅ Stable | Free sports content |
| **Tubi** | ✅ Stable | Free/ad-supported sports |
| **YouTube TV** | ✅ Stable | Multi-service aggregator |
| **Sling TV** | ✅ Stable | Multi-service aggregator |
| **Fubo** | ✅ Stable | Multi-service aggregator |
| **YouTube** | ✅ Stable | Free sports content & official streams |

### Tier 2: Experimental (Deeplink Discovery In Progress)

| Service | Status | Notable Content |
|---------|--------|-----------------|
| **Victory+** | 🧪 Experimental | Regional college sports |
| **Fanatiz Soccer** | 🧪 Experimental | International soccer leagues |
| **beIN Sports** | 🧪 Experimental | Soccer, rugby, motorsports |
| **Gotham Sports** | 🧪 Experimental | NYC regional (Knicks, Rangers, Islanders, Yankees, Nets) |
| **NESN** | 🧪 Experimental | Boston regional (Red Sox, Bruins, Celtics) |

> **Experimental Services:** Event discovery works; deeplink patterns being researched. Community feedback welcome!

### Tier 3: Planned (Coming Soon)

- MLB.tv (target: March 2026 before Opening Day)
- FloSports (gymnastics, wrestling, track & field, rugby)
- Optus Sport (Australian sports)
- Tennis Channel Plus

---

## 🛠️ Architecture

### Component Overview

1. **Scraper** (Selenium + async HTTP)
   - Connects to Apple TV Sports API with browser automation
   - Extracts event metadata, playable URLs, and deeplinks
   - Caches ESPN Graph IDs for cross-platform playback
   - Amazon Channel discovery via benefitId analysis
   - Handles multi-page results and authentication
   - Respects rate limits with exponential backoff

2. **Import Engine** (SQLite)
   - Normalizes and deduplicates events from multiple sources
   - Validates deeplinks and filters invalid entries
   - Tracks scraped events and detects stale data
   - Manages Amazon channel mappings
   - Merges ESPN Graph ID enrichment data
   - Transaction-safe batch inserts

3. **Filter Engine**
   - User-configurable service preferences
   - Sport/league selection controls
   - Multi-service priority resolution (e.g., "prefer ESPN+ over YouTube")
   - Handles edge cases: no services remaining, all sports disabled, etc.
   - Database query optimization with prepared statements

4. **Export Engine**
   - Generates standards-compliant XMLTV EPG files
   - Creates M3U playlists with deeplinks
   - Applies ESPN Graph ID corrections during export
   - Builds scheduled lane channels (BETA)
   - Builds provider-specific ADB lanes (BETA)
   - Prismcast-compatible exports (documented format)
   - Uses shared `xmltv_helpers.py` for consistent tagging:
     - Proper `<live/>` and `<new/>` tags
     - Structured categories (Provider, Sport, League)
     - Sport/league from classification_json
     - Conditional tagging (placeholders excluded)

5. **Web Dashboard** (Flask)
   - Real-time configuration interface.
   - Manual refresh controls.
   - System monitoring.
   - Filter management UI.

### Data Flow

```text
Apple TV Sports API ──┐
                      ├──> Scraper (Selenium)
ESPN Watch Graph API ─┘
        ↓
   SQLite Database
   (with ESPN Graph ID enrichment)
        ↓
  Filter Engine (User Preferences)
  (prioritizes ESPN Graph IDs)
        ↓
   Export Scripts
   (applies ESPN corrections)
        ↓
  M3U + XMLTV Files
  (+ Prismcast, Lane variants)
        ↓
   Channels DVR / Prismcast / OTT Platforms
        ↓
Your Streaming Apps (via Deeplinks)
```

---

## 🎯 Filtering Examples

### Example 1: Budget Sports Fan

**Enabled Services:**

- Prime Video (already have)
- Peacock Premium

**Result:** ~200 events filtered down to ~40 events.

### Example 2: Soccer Enthusiast

**Enabled Services:**

- Paramount+ (Champions League)
- ViX (Liga MX)
- Peacock (Premier League)

**Disabled Sports:**

- Basketball, Baseball, Hockey

**Result:** Only soccer events from your services.

### Example 3: Premium Everything

**Enabled Services:** All 24 (including 5 experimental).

**Disabled Leagues:**

- WNBA, Women's Soccer

**Result:** Full coverage minus specific leagues.

---

## 🐛 Troubleshooting

### Container Won't Start

```powershell
# Check logs (Windows PowerShell)
docker logs fruitdeeplinks

# Common issues:
# - Port 6655 already in use
# - Invalid env vars in stack
# - Insufficient memory
```

### No Events Showing

```powershell
# Run manual refresh
docker exec fruitdeeplinks python3 /app/bin/daily_refresh.py

# Check database
docker exec fruitdeeplinks sqlite3 /app/data/fruit_events.db "SELECT COUNT(*) FROM events"

# Verify filtering isn't too aggressive
# Visit http://your-server-ip:6655/filters
```

### Deeplinks Not Working

- Verify the streaming app is installed on your device.
- Check the app is authenticated (logged in).
- Test deeplink manually (Fire TV: `adb shell am start -a android.intent.action.VIEW -d "scheme://..."`).
- Some services require cable/TV provider authentication.

### Web Dashboard Not Loading

```powershell
# Check server is running
docker exec fruitdeeplinks ps aux | grep fruitdeeplinks_server

# Check port mapping
docker port fruitdeeplinks
```

### Prismcast Exports Not Generating

- Verify `PRISMCAST_OUTPUT=true` is set in environment variables
- Check logs for export errors: `docker logs fruitdeeplinks | grep -i prismcast`
- Ensure M3U and XMLTV directories are writable
- Verify Prismcast URL format matches expected schema

---

## 📊 Performance

From real deployment (example):

```text
Database: ~1,500 total events (varies by season)
After filtering: 100-200 events (depends on service selection)
Services available: 24 total (19 stable + 5 experimental)

Scrape time: ~10 minutes (with all services enabled)
Filter apply time: ~10 seconds
Memory usage: ~600MB
Database size: ~18MB
```

---

## 🗓️ Roadmap

### Recently Completed

- [x] **Prismcast Output** - M3U and XMLTV exports compatible with Prismcast white-label platform
- [x] **Experimental NESN Support** - Boston regional sports (Red Sox, Bruins, Celtics)
- [x] **Amazon Channel Integration** - Advanced scraping system identifies which Prime Video Channel events require (NBA League Pass, Peacock, DAZN, FOX One, Max, ViX, and more)
- [x] **Four New Streaming Services (Experimental)** - Victory+, Fanatiz, beIN Sports, Gotham Sports integrations
- [x] **Enhanced Title Formatting** - ESPN-style league/sport prefixes across all exports
- [x] **Genre Normalization** - Automatic cleanup of malformed categories
- [x] **Performance Improvements** - Hybrid scraping (Selenium + HTTP), improved --skip-scrape handling, 5,000 line log buffer
- [x] **ESPN Watch Graph API Integration** - Fire TV-compatible deeplinks for ESPN events (71.7% match rate)
- [x] **Database Event Cleanup** - Automatic removal of old events to improve performance
- [x] **CDVR Detector** - Automatic app launching when tuning to Fruit Lanes
- [x] **XMLTV Standards Compliance** - Proper `<live/>` and `<new/>` tags with structured categories
- [x] **Kayo Sports Integration** - Australian sports streaming support
- [x] **Filter UI Bug Fixes** - JavaScript errors resolved
- [x] **Improved Logical Service Mapping** - Better web-based provider support
- [x] **Sport Name Normalization** - Consistent capitalization

### Coming Soon

- [ ] User-selectable Amazon Prime Video Channel filtering (NBA League Pass, Peacock via Prime, etc.)
- [ ] Complete deeplink discovery for experimental services (Victory+, Fanatiz, beIN, Gotham, NESN)
- [ ] Stabilize Chrome Capture (HTTP deeplink mapping + docs)
- [ ] Team-based filtering
- [ ] Time-of-day filters
- [ ] Multi-user profiles

### Future

- [ ] MLB.tv integration (target: March 2026)
- [ ] FloSports integration (niche sports)
- [ ] Additional streaming sources (Optus Sport, DAZN expansion, etc.)
- [ ] Mobile companion app
- [ ] Plex/Emby support
- [ ] "Red Zone" style auto-switching

See this section (and `ROADMAP.md`, if present) for more details as it evolves.

---

## 🤝 Contributing

This is an active **open beta**. The project evolves regularly with new services and features. Contributions and feedback from the community are welcome.

### Development Setup

```powershell
# Clone repo (Windows PowerShell)
git clone https://github.com/kineticman/FruitDeepLinks.git
cd FruitDeepLinks

# Run locally (no Docker)
pip install -r requirements.txt
python bin/daily_refresh.py

# Or develop in container
docker compose up -d
docker exec -it fruitdeeplinks pwsh  # Or 'bash' for Linux-based container shell
```

---

## 📄 License

MIT License – see `LICENSE` file for details.

---

## 🙏 Acknowledgments

- Apple TV Sports APIs (reverse-engineered).
- Channels DVR community.
- All the streaming services for having deeplink support.

---

## ⚠️ Disclaimer

This project is for personal use only. Users must have legitimate subscriptions to streaming services. FruitDeepLinks does not provide, host, or distribute any copyrighted content – it only aggregates publicly available scheduling data and generates deeplinks to official streaming services.

Use of this software may violate Terms of Service of various platforms. Use at your own risk.

---

## 🔗 Links

- **Repository:** https://github.com/kineticman/FruitDeepLinks
- **Channels DVR:** https://getchannels.com
- **Service Catalog:** `docs/SERVICE_CATALOG.md`

---

**Made with ❤️ for sports fans tired of app-hopping**
