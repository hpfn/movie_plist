
from http.server import HTTPServer, CGIHTTPRequestHandler
# import os

# this path must be fixed if this file goes
# to some /home/user dir
# from conf.global_conf import PORT
port = 8123

# run_at = os.path.join('/home/zaza/Vídeos')
# os.chdir(run_at)
httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
print("Starting simple_httpd on port: " + str(httpd.server_port))
httpd.serve_forever()

