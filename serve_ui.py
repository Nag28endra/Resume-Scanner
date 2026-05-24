#!/usr/bin/env python3
"""
Simple HTTP server to serve the Resume Scanner UI.
Run this script from the ui/ directory.
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 3000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow API calls
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    # Change to ui directory
    ui_dir = Path(__file__).parent / 'ui'
    os.chdir(ui_dir)

    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Serving Resume Scanner UI at http://localhost:{PORT}")
        print("Make sure the API server is running on port 8000")
        print("Press Ctrl+C to stop the server")

        # Open browser automatically
        webbrowser.open(f"http://localhost:{PORT}")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            httpd.shutdown()

if __name__ == "__main__":
    main()