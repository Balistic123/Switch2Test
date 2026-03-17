import http.server
import socketserver
import datetime
import os

PORT = 80
FILE_PATH = r"C:\Users\Aiden\Documents\LOLAL\index.html"

class RawMonitor(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [CONN] Switch requested index.html")
        try:
            with open(FILE_PATH, "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read())
        except Exception as e:
            print(f"Error reading file: {e}")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        raw_data = self.rfile.read(content_length)
        
        # Check if this is the 3160-byte System Environment Table
        if content_length == 3160:
            filename = f"system_dump_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.bin"
            with open(filename, "wb") as f:
                f.write(raw_data)
            print(f"\033[92m[{datetime.datetime.now().strftime('%H:%M:%S')}] [!!! SUCCESS !!!] Captured 3160 bytes to {filename}\033[0m")
        else:
            # Fallback to your original string logging for other messages
            try:
                post_data = raw_data.decode('utf-8', errors='ignore')
                if "STAGE_2" in post_data:
                    print(f"\033[93m[{datetime.datetime.now().strftime('%H:%M:%S')}] [PUNCTURE] {post_data}\033[0m")
                else:
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [LOG] {post_data}")
            except:
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [DATA] Received {content_length} bytes of binary data.")

        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args): return

print("--- RAW FORENSIC MONITOR ACTIVE (WIFI DUMP ENABLED) ---")
socketserver.TCPServer.allow_reuse_address = True
try:
    with socketserver.TCPServer(("", PORT), RawMonitor) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nShutting down...")