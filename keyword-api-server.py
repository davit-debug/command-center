#!/usr/bin/env python3
"""
10XSEO Keyword Research API Proxy Server
Protects DataForSEO credentials from frontend exposure.
Run: python3 keyword-api-server.py
"""

import http.server
import json
import urllib.request
import urllib.error
import base64
import time
import os
import mimetypes
from urllib.parse import urlparse, parse_qs
from collections import defaultdict

# ============ CONFIGURATION ============
PORT = 3001
DATAFORSEO_LOGIN = "davit@10xseo.ge"
DATAFORSEO_PASSWORD = "fb35fc357556204b"
DATAFORSEO_AUTH = base64.b64encode(f"{DATAFORSEO_LOGIN}:{DATAFORSEO_PASSWORD}".encode()).decode()

CACHE_TTL = 3600  # 1 hour
RATE_LIMIT = 30   # requests per minute per IP
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))

# ============ IN-MEMORY STORES ============
cache = {}  # key -> {"data": ..., "expires": timestamp}
rate_limits = defaultdict(list)  # ip -> [timestamps]

# ============ ALLOWED ORIGINS ============
ALLOWED_ORIGINS = [
    "http://localhost:3001",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3000",
    "https://10xseo.ge",
    "https://www.10xseo.ge",
    "http://10xseo.ge",
    "null",  # for file:// protocol
]


def get_cors_headers(origin=None):
    """Return CORS headers."""
    allowed = "*"
    if origin and origin in ALLOWED_ORIGINS:
        allowed = origin
    return {
        "Access-Control-Allow-Origin": allowed,
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "86400",
    }


def check_rate_limit(ip):
    """Return True if request is allowed, False if rate limited."""
    now = time.time()
    # Clean old entries
    rate_limits[ip] = [t for t in rate_limits[ip] if now - t < 60]
    if len(rate_limits[ip]) >= RATE_LIMIT:
        return False
    rate_limits[ip].append(now)
    return True


def get_cache(key):
    """Get cached response if not expired."""
    if key in cache and cache[key]["expires"] > time.time():
        return cache[key]["data"]
    if key in cache:
        del cache[key]
    return None


def set_cache(key, data):
    """Cache response with TTL."""
    cache[key] = {"data": data, "expires": time.time() + CACHE_TTL}


def dataforseo_request(endpoint, payload):
    """Make a request to DataForSEO API."""
    url = f"https://api.dataforseo.com/v3/{endpoint}"
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Basic {DATAFORSEO_AUTH}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else "{}"
        return {"error": f"HTTP {e.code}", "detail": body}
    except Exception as e:
        return {"error": str(e)}


def search_keyword(keyword, location_code=2268):
    """Search keyword volume and related keywords."""
    cache_key = f"{keyword.lower().strip()}:{location_code}"
    cached = get_cache(cache_key)
    if cached:
        return cached, True

    # Call both endpoints
    volume_payload = [{
        "keywords": [keyword],
        "location_code": location_code,
        "sort_by": "search_volume"
    }]

    related_payload = [{
        "keywords": [keyword],
        "location_code": location_code,
        "sort_by": "search_volume",
        "limit": 50
    }]

    volume_result = dataforseo_request(
        "keywords_data/google_ads/search_volume/live", volume_payload
    )
    related_result = dataforseo_request(
        "keywords_data/google_ads/keywords_for_keywords/live", related_payload
    )

    # Parse volume data
    main_kw = {}
    try:
        tasks = volume_result.get("tasks", [{}])
        if tasks and tasks[0].get("status_code") == 20000:
            results = tasks[0].get("result", [])
            if results and results[0]:
                r = results[0]
                main_kw = {
                    "keyword": r.get("keyword", keyword),
                    "searchVolume": r.get("search_volume") or 0,
                    "cpc": r.get("cpc") or 0,
                    "competition": r.get("competition"),
                    "competitionIndex": r.get("competition_index"),
                    "lowTopOfPageBid": r.get("low_top_of_page_bid") or 0,
                    "highTopOfPageBid": r.get("high_top_of_page_bid") or 0,
                    "monthlySearches": r.get("monthly_searches") or [],
                }
    except Exception as e:
        main_kw = {"error": f"Volume parse error: {str(e)}"}

    if not main_kw.get("keyword"):
        main_kw["keyword"] = keyword
    if "searchVolume" not in main_kw:
        main_kw["searchVolume"] = 0
        main_kw["monthlySearches"] = []

    # Parse related keywords
    related_keywords = []
    try:
        tasks = related_result.get("tasks", [{}])
        if tasks and tasks[0].get("status_code") == 20000:
            results = tasks[0].get("result", [])
            for r in (results or []):
                if r is None:
                    continue
                kw_name = r.get("keyword", "")
                if kw_name.lower().strip() == keyword.lower().strip():
                    continue  # Skip the original keyword
                related_keywords.append({
                    "keyword": kw_name,
                    "searchVolume": r.get("search_volume") or 0,
                    "cpc": r.get("cpc") or 0,
                    "competition": r.get("competition"),
                    "competitionIndex": r.get("competition_index"),
                })
    except Exception as e:
        pass

    main_kw["relatedKeywords"] = related_keywords
    main_kw["totalRelated"] = len(related_keywords)

    # Cache result
    set_cache(cache_key, main_kw)
    return main_kw, False


class KeywordAPIHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for keyword research API."""

    def log_message(self, format, *args):
        """Custom logging."""
        print(f"[{time.strftime('%H:%M:%S')}] {self.client_address[0]} - {format % args}")

    def send_json(self, data, status=200):
        """Send JSON response."""
        origin = self.headers.get("Origin", "*")
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")

        self.send_response(status)
        for key, val in get_cors_headers(origin).items():
            self.send_header(key, val)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        origin = self.headers.get("Origin", "*")
        self.send_response(204)
        for key, val in get_cors_headers(origin).items():
            self.send_header(key, val)
        self.end_headers()

    def do_GET(self):
        """Handle GET requests — static files + health endpoint."""
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            self.send_json({
                "status": "ok",
                "cacheSize": len(cache),
                "port": PORT,
            })
            return

        # Serve static files
        if path == "/":
            path = "/keyword-research.html"

        file_path = os.path.join(STATIC_DIR, path.lstrip("/"))
        file_path = os.path.realpath(file_path)

        # Security: prevent directory traversal
        if not file_path.startswith(os.path.realpath(STATIC_DIR)):
            self.send_error(403, "Forbidden")
            return

        if os.path.isfile(file_path):
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = "application/octet-stream"

            try:
                with open(file_path, "rb") as f:
                    content = f.read()

                self.send_response(200)
                origin = self.headers.get("Origin", "*")
                for key, val in get_cors_headers(origin).items():
                    self.send_header(key, val)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404, "File not found")

    def do_POST(self):
        """Handle POST requests — API endpoints."""
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/keyword-search":
            self.handle_keyword_search()
        elif path == "/api/cache-clear":
            cache.clear()
            self.send_json({"status": "ok", "message": "Cache cleared"})
        else:
            self.send_json({"error": "Not found"}, 404)

    def handle_keyword_search(self):
        """Handle keyword search request."""
        # Rate limit check
        client_ip = self.client_address[0]
        if not check_rate_limit(client_ip):
            self.send_json({"error": "Rate limit exceeded. Max 30 requests/minute."}, 429)
            return

        # Read body
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 1048576:  # 1MB limit
                self.send_json({"error": "Request too large"}, 413)
                return
            body = self.rfile.read(content_length)
            data = json.loads(body.decode("utf-8"))
        except (json.JSONDecodeError, Exception) as e:
            self.send_json({"error": f"Invalid JSON: {str(e)}"}, 400)
            return

        keyword = data.get("keyword", "").strip()
        if not keyword:
            self.send_json({"error": "Missing 'keyword' field"}, 400)
            return

        location_code = data.get("location_code", 2268)

        # Search
        try:
            result, from_cache = search_keyword(keyword, location_code)
            if from_cache:
                self.log_message("CACHE HIT: %s", keyword)
            else:
                self.log_message("API CALL: %s (volume=%s, related=%s)",
                    keyword,
                    result.get("searchVolume", "?"),
                    result.get("totalRelated", "?"))
            self.send_json(result)
        except Exception as e:
            self.send_json({"error": f"Server error: {str(e)}"}, 500)


def main():
    server = http.server.HTTPServer(("0.0.0.0", PORT), KeywordAPIHandler)
    print(f"""
╔══════════════════════════════════════════════════╗
║   10XSEO Keyword Research API Proxy Server       ║
║   Port: {PORT}                                      ║
╠══════════════════════════════════════════════════╣
║   Endpoints:                                     ║
║   POST /api/keyword-search                       ║
║   GET  /api/health                               ║
║   POST /api/cache-clear                          ║
║                                                  ║
║   Static files served from:                      ║
║   {STATIC_DIR[:46]:46} ║
║                                                  ║
║   Open: http://localhost:{PORT}/keyword-research.html ║
╚══════════════════════════════════════════════════╝
    """)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()


if __name__ == "__main__":
    main()
