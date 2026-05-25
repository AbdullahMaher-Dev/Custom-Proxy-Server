from flask import Flask, render_template, request, Response # type: ignore
import requests # type: ignore
import time
import hashlib

# --- Caching ---
cache_storage = {}
CACHE_TTL = 60  # seconds

def get_cache(key):
    if key in cache_storage:
        data, timestamp = cache_storage[key]
        if time.time() - timestamp < CACHE_TTL:
            return data
        else:
            del cache_storage[key]
    return None

def set_cache(key, data):
    cache_storage[key] = (data, time.time())

# --- Content Filtering ---
BLOCKED_KEYWORDS = ["facebook", "porn", "banned"]

def is_blocked(url):
    for word in BLOCKED_KEYWORDS:
        if word in url:
            return True
    return False

# --- Bandwidth Throttling ---
THROTTLE_SPEED = 100  # bytes per second

def throttle_speed(size):
    delay = size / THROTTLE_SPEED
    print(f"\n[NETWORK CONTROL] Throttling active: Data size is {size} bytes. Delaying response by {round(delay, 2)} seconds...\n")
    time.sleep(delay)

# --- Flask App ---
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/proxy', methods=['GET', 'POST'])
def proxy():
    url = request.args.get('url')
    if not url:
        return "Missing URL. Use /proxy?url=http://example.com"

    if is_blocked(url):
        # --- صفحة التحذير الشيك --
        return """
        <body style="background-color: #1a1a1a; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
            <div style="text-align: center; border: 2px solid #d9534f; padding: 40px; border-radius: 15px; background-color: #222; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
                <div style="font-size: 5em; margin-bottom: 20px;">⚠️</div>
                <h1 style="color: #d9534f; font-size: 3em; margin: 0 0 15px 0;">ACCESS DENIED</h1>
                <p style="font-size: 1.5em; margin: 0 0 10px 0;">This URL has been blocked by</p>
                <p style="font-size: 1.5em; font-weight: bold; color: #5bc0de;">Abdullah Maher PROXY FIREWALL</p>
                <p style="color: #888; margin-top: 25px; font-size: 0.9em;">Reason: Restricted Keyword Detected</p>
            </div>
        </body>
        """, 403

    cache_key = hashlib.md5((url + request.method).encode()).hexdigest()
    cached_response = get_cache(cache_key)
    if cached_response:
        return Response(cached_response['content'], status=200, headers=cached_response['headers'])

    try:
        if request.method == 'GET':
            response = requests.get(url)
        else:
            response = requests.post(url, data=request.data)

        throttle_speed(len(response.content))

        set_cache(cache_key, {
            'content': response.content,
            'headers': response.headers
        })

        return Response(response.content, status=response.status_code, content_type=response.headers.get('Content-Type'))
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    print("Proxy server running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
