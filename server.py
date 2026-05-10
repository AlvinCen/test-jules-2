import http.server
import socketserver

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        with open("orchestrator_hostname.txt", "wb") as f:
            f.write(post_data)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

with socketserver.TCPServer(("", 8001), Handler) as httpd:
    httpd.serve_forever()
