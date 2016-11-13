
from http.server import HTTPServer, CGIHTTPRequestHandler
# import os
port = 8080

# run_at = os.path.join('/home/zaza/Vídeos')
# os.chdir(run_at)
httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
print("Starting simple_httpd on port: " + str(httpd.server_port))
httpd.serve_forever()

