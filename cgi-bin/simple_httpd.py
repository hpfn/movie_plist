
from http.server import HTTPServer, CGIHTTPRequestHandler
# import os
from conf.global_conf import PORT
port = PORT

# run_at = os.path.join('/home/zaza/Vídeos')
# os.chdir(run_at)
httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
print("Starting simple_httpd on port: " + str(httpd.server_port))
httpd.serve_forever()

