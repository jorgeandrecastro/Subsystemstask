# 📁 PROJECT EXPORT FOR LLMs

## 📊 Project Information

- **Project Name**: `config`
- **Generated On**: 2026-03-11 17:24:37 (Europe/Paris / GMT+01:00)
- **Total Files Processed**: 1
- **Export Tool**: Easy Whole Project to Single Text File for LLMs v1.1.0
- **Tool Author**: Jota / José Guilherme Pandolfi

### ⚙️ Export Configuration

| Setting | Value |
|---------|-------|
| Language | `en` |
| Max File Size | `1 MB` |
| Include Hidden Files | `false` |
| Output Format | `both` |

## 🌳 Project Structure

```
└── 📄 mosquitto.conf (323 B)
```

## 📑 Table of Contents

**Project Files:**

- [📄 mosquitto.conf](#📄-mosquitto-conf)

---

## 📈 Project Statistics

| Metric | Count |
|--------|-------|
| Total Files | 1 |
| Total Directories | 0 |
| Text Files | 1 |
| Binary Files | 0 |
| Total Size | 323 B |

### 📄 File Types Distribution

| Extension | Count |
|-----------|-------|
| `.conf` | 1 |

## 💻 File Code Contents

### <a id="📄-mosquitto-conf"></a>📄 `mosquitto.conf`

**File Info:**
- **Size**: 323 B
- **Extension**: `.conf`
- **Language**: `text`
- **Location**: `mosquitto.conf`
- **Relative Path**: `root`
- **Created**: 2026-03-11 17:24:28 (Europe/Paris / GMT+01:00)
- **Modified**: 2026-03-11 17:24:36 (Europe/Paris / GMT+01:00)
- **MD5**: `45c0739c51183cef84b173bf2ea6cd4b`
- **SHA256**: `452330c06cb2fbccc8d98696a88cd1e7e04be15f47a78e2bf402f194f957f73f`
- **Encoding**: UTF-8

**File code content:**

```text
# Port MQTT standard
listener 1883

# Port WebSocket
listener 9001

# Autoriser les connexions anonymes (pour les tests)
allow_anonymous true

# Configuration des logs
log_dest file /mosquitto/log/mosquitto.log
log_type all

# Persistance des données
persistence true
persistence_location /mosquitto/data/

```

---

