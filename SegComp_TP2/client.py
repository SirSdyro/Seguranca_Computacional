import http.client
import ssl

#Criando uma conexao HTTPS
context = ssl.create_default_context(cafile='cert.pem')
print(context.get_ca_certs())
conn = http.client.HTTPSConnection('localhost', 5900, context=context)
conn.connect()
print("Versão do protocolo :",conn.sock.version())
#Enviando um request GET
conn.request('GET', '/')

#Recebendo a resposta do server
response = conn.getresponse()
print(response.msg)
print(f"Status: {response.status}")
print(f"Response: {response.read().decode()}")

#Enviando um request POST com o body 'Testando essa budega'
conn.request('POST', '/', "Testando essa budega")

#Recebendo a resposta do server
response = conn.getresponse()
print(response)
print(f"Status: {response.status}")
print(f"Response: {response.read().decode()}")

#Encerrando a conexão
conn.close()

#Criando uma conexao HTTPS com certificado errado
context = ssl.create_default_context(cafile='wrong_cert.pem')
print(context.get_ca_certs())
conn = http.client.HTTPSConnection('localhost', 5900, context=context)

#Enviando um request GET
conn.request('GET', '/')

#Recebendo a resposta do server
response = conn.getresponse()
print(response.msg)
print(f"Status: {response.status}")
print(f"Response: {response.read().decode()}")

#Enviando um request POST com o body 'Testando essa budega'
conn.request('POST', '/', "Testando essa budega")

#Recebendo a resposta do server
response = conn.getresponse()
print(response)
print(f"Status: {response.status}")
print(f"Response: {response.read().decode()}")

#Encerrando a conexão
conn.close()
