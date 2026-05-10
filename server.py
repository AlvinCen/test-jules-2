import http.server
import socketserver

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        with open("exfiltrated_data.txt", "ab") as f:
            f.write(post_data + b"\n===\n")
        self.send_response(200)
        self.end_headers()

with socketserver.TCPServer(("", 8080), Handler) as httpd:
    httpd.serve_forever()
