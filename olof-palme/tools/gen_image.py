"""Project-local Gemini image adapter: one request, no retries, 16:9, multiple image refs.
usage: gen_image.py MODEL PROMPT_FILE OUT.png REF1 [REF2 ...]   (key from GEMINI_API_KEY)"""
import sys, os, json, base64, mimetypes, urllib.request, urllib.error
model, prompt_file, out, *refs = sys.argv[1:]
parts = [{"text": open(prompt_file).read()}]
for r in refs:
    parts.append({"inline_data": {"mime_type": mimetypes.guess_type(r)[0] or "image/png",
                                  "data": base64.b64encode(open(r, "rb").read()).decode()}})
body = {"contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"], "imageConfig": {"aspectRatio": "16:9"}}}
req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
    data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
try:
    d = json.load(urllib.request.urlopen(req, timeout=240))
except urllib.error.HTTPError as e:
    err = json.loads(e.read() or b"{}").get("error", {})
    print("HTTP", e.code, err.get("status"), (err.get("message") or "")[:300]); sys.exit(2)
for c in d.get("candidates", []):
    for p in c.get("content", {}).get("parts", []):
        if "inlineData" in p:
            open(out, "wb").write(base64.b64decode(p["inlineData"]["data"])); print("saved", out); sys.exit(0)
print("no image; finish:", [c.get("finishReason") for c in d.get("candidates", [])], d.get("promptFeedback")); sys.exit(3)
