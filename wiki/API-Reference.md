# API Reference

Complete documentation for TubeNova's backend REST API.

## Base URL

- **Local Development:** `http://127.0.0.1:5000`
- **Production:** Your deployed backend URL (e.g., `https://tubenova.onrender.com`)

## Endpoints

### 1. Health Check

Check if the backend is running.

**Endpoint:** `GET /api/health`

**Response:**

```json
{
  "status": "ok"
}
```

**Example:**

```bash
curl http://127.0.0.1:5000/api/health
```

---

### 2. Get Video Info

Fetch metadata for a YouTube video or Short.

**Endpoint:** `GET /api/info`

**Query Parameters:**

| Parameter | Type   | Required | Description           |
|-----------|--------|----------|-----------------------|
| `url`     | string | Yes      | YouTube video URL     |

**Success Response (200):**

```json
{
  "id": "dQw4w9WgXcQ",
  "title": "Rick Astley - Never Gonna Give You Up (Official Video)",
  "uploader": "Rick Astley",
  "duration": 212,
  "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
  "webpage_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "formats": [
    {
      "format_id": "18",
      "label": "360p",
      "filesize": 12345678,
      "ext": "mp4",
      "type": "video"
    },
    {
      "format_id": "140",
      "label": "128k",
      "filesize": 3456789,
      "ext": "m4a",
      "type": "audio"
    }
  ]
}
```

**Error Response (400):**

```json
{
  "error": "Missing url parameter"
}
```

```json
{
  "error": "DownloadError",
  "detail": "Video unavailable"
}
```

**Error Response (500):**

```json
{
  "error": "ServerError",
  "detail": "Internal error message"
}
```

**Example:**

```bash
curl "http://127.0.0.1:5000/api/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**Supported URL Formats:**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/shorts/VIDEO_ID`
- `https://m.youtube.com/watch?v=VIDEO_ID`

---

### 3. Download Media

Stream video or audio file without storing on server.

**Endpoint:** `GET /api/download`

**Query Parameters:**

| Parameter   | Type   | Required | Description                        |
|-------------|--------|----------|------------------------------------|
| `url`       | string | Yes      | YouTube video URL                  |
| `format_id` | string | Yes      | Format ID from `/api/info` response|

**Success Response (200 or 206):**

- **Content-Type:** `video/mp4`, `audio/mp4`, `audio/mpeg`, etc.
- **Content-Disposition:** `attachment; filename="Title_720p.mp4"`
- **Content-Length:** File size in bytes (when available)
- **Content-Range:** Byte range for partial downloads (206 response)

**Features:**
- ✅ Streams file directly (no server storage)
- ✅ Supports HTTP Range requests (partial downloads)
- ✅ Automatic filename generation with quality label
- ✅ Correct MIME type detection
- ✅ Proper cache headers

**Error Response (400):**

```json
{
  "error": "Missing url or format_id"
}
```

**Error Response (404):**

```json
{
  "error": "FormatNotFound"
}
```

**Example:**

```bash
curl "http://127.0.0.1:5000/api/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ&format_id=18" \
  -o video.mp4
```

**Range Request Example:**

```bash
curl "http://127.0.0.1:5000/api/download?url=https://youtu.be/dQw4w9WgXcQ&format_id=18" \
  -H "Range: bytes=0-1048575" \
  -o partial.mp4
```

---

## Format Selection

### Video Formats

Available quality labels returned by `/api/info`:

| Label  | Resolution | Typical Bitrate | Container |
|--------|-----------|-----------------|-----------|
| 144p   | 256×144   | ~100 kbps       | mp4/webm  |
| 240p   | 426×240   | ~250 kbps       | mp4/webm  |
| 360p   | 640×360   | ~500 kbps       | mp4/webm  |
| 480p   | 854×480   | ~1 Mbps         | mp4/webm  |
| 720p   | 1280×720  | ~2.5 Mbps       | mp4/webm  |
| 1080p  | 1920×1080 | ~5 Mbps         | mp4/webm  |

### Audio Formats

| Label | Bitrate  | Container | Codec      |
|-------|----------|-----------|------------|
| 128k  | 128 kbps | m4a       | AAC        |
| 320k  | 320 kbps | m4a       | AAC        |

---

## CORS Configuration

The backend supports CORS for cross-origin requests.

**Environment Variable:**

```bash
export YDL_ALLOWED_ORIGINS="https://umeshcode1.github.io,http://localhost:8000"
```

**Default:** `*` (all origins)

---

## Rate Limiting

Currently, there is no rate limiting. For production:

1. Use a reverse proxy (Nginx, Cloudflare)
2. Implement rate limiting middleware
3. Consider caching video metadata

---

## Error Handling

### Common Error Types

| Error Code | Error Type      | Description                        |
|------------|----------------|------------------------------------|
| 400        | DownloadError  | YouTube extraction failed          |
| 400        | Missing params | Required parameter not provided    |
| 404        | FormatNotFound | Requested quality not available    |
| 500        | ServerError    | Internal server error              |

### Error Response Format

```json
{
  "error": "ErrorType",
  "detail": "Human-readable description"
}
```

---

## Examples

### Python

```python
import requests

# Get video info
response = requests.get(
    "http://127.0.0.1:5000/api/info",
    params={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
)
info = response.json()

# Download video
format_id = info["formats"][0]["format_id"]
response = requests.get(
    "http://127.0.0.1:5000/api/download",
    params={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "format_id": format_id},
    stream=True
)

with open("video.mp4", "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
```

### JavaScript

```javascript
// Get video info
const response = await fetch(
  `http://127.0.0.1:5000/api/info?url=${encodeURIComponent(videoUrl)}`
);
const info = await response.json();

// Download with progress
const dlResponse = await fetch(
  `http://127.0.0.1:5000/api/download?url=${encodeURIComponent(videoUrl)}&format_id=${formatId}`
);

const reader = dlResponse.body.getReader();
const contentLength = +dlResponse.headers.get('Content-Length');

let receivedLength = 0;
const chunks = [];

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  chunks.push(value);
  receivedLength += value.length;
  
  console.log(`Progress: ${(receivedLength / contentLength * 100).toFixed(2)}%`);
}

const blob = new Blob(chunks);
```

---

## Next Steps

- [Frontend Architecture](Frontend-Architecture) - How the UI calls the API
- [CORS Configuration](CORS-Configuration) - Set up cross-origin
- [Deploy Backend](Deploy-Backend-Render) - Host your API

---

[← Back to Wiki Home](Home)
