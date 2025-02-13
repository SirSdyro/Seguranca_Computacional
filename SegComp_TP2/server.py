import http.server
import ssl
from io import BytesIO

#Definindo o endereco e a porta do servidor
server_address = ('127.0.0.1', 5900)

#Classe que lida com os request HTTP
class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

#Cria o server HTTP
httpd = http.server.HTTPServer(server_address, SimpleHTTPRequestHandler)

#Aplicando o protocolo SSL na socket
httpd.socket = ssl.wrap_socket(
    httpd.socket,
    server_side=True,
    certfile='cert.pem',
    keyfile='key.pem',
    ssl_version=ssl.PROTOCOL_TLS
)

print(f"HTTPS Server running on https://{server_address[0]}:{server_address[1]}")
print(f"Servidor utilizando protocolo de seguranca TLS com certificados")
httpd.serve_forever()