"""Serve the lecture slides on localhost so they can be presented full screen.

    python3 present.py                  # opens http://localhost:8000 in your browser
    python3 present.py --port 8001      # if 8000 is taken
    python3 present.py --deck other.html --no-open

While presenting: F or double-click toggles fullscreen, the arrow keys, Space, Home and End
move between slides, and Ctrl+C in the terminal stops the server.
"""
import argparse
import http.server
import re
import sys
import webbrowser
from pathlib import Path

DEFAULT_DECK = Path(__file__).resolve().parent / "Convolutional Neural Networks.html"

# Added to the page as it's sent to the browser. The HTML file itself is never changed
PRESENTER_SCRIPT = """<script>
(() => {
  // Tell the deck it's being presented: its toolbar then only shows when the mouse moves
  const present = () => window.postMessage({ __omelette_presenting: true }, location.origin);

  // The deck fires "slidechange" on every move, including the first slide on load.
  // Keep the slide number in the address, so a reload lands on the same slide
  document.addEventListener("slidechange", (e) => {
    present();
    history.replaceState(null, "", "#" + (e.detail.index + 1));
  });

  // F or double-click toggles fullscreen
  const toggleFullscreen = () =>
    document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
  window.addEventListener("keydown", (e) => {
    if ((e.key || "").toLowerCase() === "f" && !e.metaKey && !e.ctrlKey && !e.altKey) toggleFullscreen();
  });
  window.addEventListener("dblclick", toggleFullscreen);
})();
</script>
"""


class SlidesHandler(http.server.BaseHTTPRequestHandler):
    deck = DEFAULT_DECK

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return
        if path != "/":
            self.send_error(404, "The slides are at /")
            return

        # Read the file on every request, so a fresh export shows up with a reload
        html = self.deck.read_text(encoding="utf-8")
        head = re.search(r"<head[^>]*>", html, re.IGNORECASE)
        at = head.end() if head else 0
        body = (html[:at] + PRESENTER_SCRIPT + html[at:]).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass  # keep the terminal quiet while presenting


def main():
    parser = argparse.ArgumentParser(description="Present the slides full screen from localhost.")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--deck", type=Path, default=DEFAULT_DECK, help="the exported HTML slides")
    parser.add_argument("--no-open", action="store_true", help="don't open a browser tab")
    args = parser.parse_args()

    if not args.deck.is_file():
        sys.exit(f"Can't find the slides: {args.deck}")
    SlidesHandler.deck = args.deck.resolve()

    # 127.0.0.1 means only this computer can open the page
    try:
        server = http.server.ThreadingHTTPServer(("127.0.0.1", args.port), SlidesHandler)
    except OSError:
        sys.exit(f"Port {args.port} is busy. Try: python3 present.py --port {args.port + 1}")

    url = f"http://localhost:{args.port}/"
    print(f"Presenting {args.deck.name}", flush=True)
    print(f"  {url}", flush=True)
    print("  F = fullscreen, arrows = next/previous, Ctrl+C = stop", flush=True)
    if not args.no_open:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
