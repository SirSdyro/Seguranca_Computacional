import random
import sys
import hashlib
import base64
 
#Lista de numeros primos iniciais
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]
 
#Funcao que encontra o mdc de dois numeros
def mdc(p, q):
    while q != 0:
        p, q = q, p % q
    return p

#Funcao que gera um numero aleatorio de n bits
def nBitRandom(n):
    return random.getrandbits(n)
 
#Funcao que testa se um numero e divisivel por uma lista de numeros primos iniciais
def getLowLevelPrime(n):
    while True:
        n = nBitRandom(n)
 
        for divisor in first_primes_list:
            if n % divisor == 0 and divisor**2 <= n:
                break
        else:
            return n
 
#Funcao que realiza o teste de primalidade Miller-Rabin
def isMillerRabinPassed(n):
    expoente_dois = 0
    aux = n-1
    while aux % 2 == 0:
        aux >>= 1
        expoente_dois += 1
    assert(2**expoente_dois * aux == n-1)
 
    def trialComposite(numero_teste):
        if pow(numero_teste, aux, n) == 1:
            return False
        for i in range(expoente_dois):
            if pow(numero_teste, 2**i * aux, n) == n-1:
                return False
        return True
 
    rodadas = 20
    for i in range(rodadas):
        numero_teste = random.randrange(2, n)
        if trialComposite(numero_teste):
            return False
    return True

#Funcao que gera uma mascara dado um numero aleatorio e o tamanho da saida em bytes 
def MFG1_sha3_256(seed, length):
    hlen = hashlib.sha3_256().digest_size
    if length > (hlen << 32):
        print("mascara muito longa")
        return
    T = b""
    counter = 0
    while len(T) < length:
        C = int.to_bytes(counter, 4, "big")
        T += hashlib.sha3_256(seed + C).digest()
        counter += 1
    return T[:length]

#Funcao que checa se uma string de bytes possui apenas zeros
def contains_zeroes(string):
    for i in string:
        if i != 0:
            return False
    return True

#Funcao responsavel por realizar o padding de acordo com o esquema OPTICAL ASSYMETRIC ENCRYPTION PADDING (OAEP)
def OAEP(message):
    k = int(2048/8) # Tamanho em bytes do modulo do RSA
    hLen = 32 # Tamanho do hash em bytes feito pela funcao sha3_256
    mLen = 32 # Tamanho da mensagem em bytes
    lHash = hashlib.sha3_256("".encode()).digest() # Hash do label, no caso uma string vazia
    PS = b'\x00' *(k - mLen - 2*hLen - 2) # Geracao da string de padding, no caso uma feita sรณ de zeros
    DB = lHash + PS + b'\x01' + message.to_bytes(32) # Geracao do bloco de dados 
    randNumber = random.getrandbits(hLen*8) # Geracao de um numero aleatorio de 256 bits
    dbMask = MFG1_sha3_256(randNumber.to_bytes(32), k - hLen - 1) # Geracao da mascara do bloco de dados DB
    maskedDB = bytes(a ^ b for a, b in zip(DB, dbMask)) # Mascarando o bloco de dados DB com sua mascara
    seedMask = MFG1_sha3_256(maskedDB, hLen) # Geracao da mascara do numero aleatorio
    maskedSeed = bytes(a ^ b for a, b in zip(randNumber.to_bytes(32), seedMask)) # Mascarando o numero aleatorio
    return b'\x00' + maskedSeed + maskedDB # Retornando a mensagem com padding

#Funcao responsavel por remover o padding de acordo com o esquema OPTICAL ASSYMETRIC ENCRYPTION PADDING (OAEP)
def OAEP_unpad(padded):
    k = int(2048/8) # Tamanho em bytes do modulo do RSA
    hLen = 32 # Tamanho do hash em bytes feito pela funcao sha3_256
    lHash = hashlib.sha3_256("".encode()).digest() # Hash do label, no caso uma string vazia
    empty_bit = padded[:1] # Separacao da mensagem preenchida
    maskedSeed = padded[1:hLen+1] # Separacao da mensagem preenchida
    maskedDB = padded[hLen+1:] # Separacao da mensagem preenchida
    seedMask = MFG1_sha3_256(maskedDB, hLen) # Geracao da mascara do numero aleatorio 
    seed = bytes(a ^ b for a, b in zip(maskedSeed, seedMask)) # Obtencao do numero aleatorio original
    dbMask = MFG1_sha3_256(seed, k - hLen - 1) # Geracao da mascara do bloco de dados
    DB = bytes(a ^ b for a, b in zip(maskedDB, dbMask)) # Obtencao do bloco de dados original
    lHash_padded = DB[:32] # Separacao do bloco de dados
    PS = DB[32:DB.find(b'\x01')] # Separacao do bloco de dados
    M = DB[DB.find(b'\x01')+1:] # Separacao do bloco de dados
    #Checagem para ver se o padding e valido
    if lHash == lHash_padded and contains_zeroes(PS) and padded[:1] == b'\x00':
        return M
    else:
        print("Invalid padding")
        return 0

#Funcao que realiza a encriptacao RSA com OAEP
def rsa_encrypt(message, e, n):
    message = int.from_bytes(OAEP(message))
    return pow(message, e, n)

#Funcao que realiza a decriptacao RSA com OAEP
def rsa_decrypt(cipher, e, phi, n):
    d = pow(e, -1, phi) 
    padded_plaintext = pow(cipher, d, n)
    plaintext = OAEP_unpad(padded_plaintext.to_bytes(256))
    return int.from_bytes(plaintext)

random.seed(3041735568637125599) #Semente para reprodutibilidade do resultado
while True:
    n = 1024
    #p = getLowLevelPrime(n)
    p = 142540984084842373528554216101328477512272737825818698707193218342253704337743113222120862588334006659016214636470679525454328398350902118574574279272175942622860010891899344762580914002429512531804592383470319857040194550806309372990137960475620696728015784367986815264669262155544976950446379847608840328683
    #q = getLowLevelPrime(n)
    q = 134752603881357130257014875736430163121202348030624673249908034547345341113325144628769101811033291842265197240947782054734048588039759699511244221312827419395596182234386251220889669882451203118878633826930494948130757978548132978633484056553220292888880325490420759361144641801231821860476072244435805462513
    if isMillerRabinPassed(p) and isMillerRabinPassed(q):
        #seed = random.randrange(sys.maxsize)
        #rng = random.Random(seed)
        #print("Seed was:", seed)
        print("-------------------------------------------------------------------")
        print("GERACAO DAS CHAVES, PREPARACAO DA MENSAGEM E DO HASH","\n")
        print("p =",p,"\n")
        print("q =",q,"\n")
        n = p*q
        print("p*q =",n,"\n")
        f = open("entrada.txt", "r")
        test = f.read()
        print("Mensagem:")
        print(test, "\n")
        message = base64.b64encode(test.encode())
        print("Mensagem codificada em BASE64:")
        print(message, "\n")
        hash = hashlib.sha3_256(message).digest()
        print("Hash da mensagem em bytes:")
        print(hash, "\n")
        hash_int = int.from_bytes(hash)
        print("Hash da mensagem em numero inteiro:")
        print(hash_int, "\n")
        print("-------------------------------------------------------------------")
        print("CIFRACAO RSA COM OAEP","\n")
        cipher = rsa_encrypt(hash_int, 23, n)
        print("Hash com padding cifrado:")
        print(cipher, "\n")
        aux = message + cipher.to_bytes(256)
        print("Mensagem concatenada com a assinatura:")
        print(aux, "\n")
        print("-------------------------------------------------------------------")
        print("DECIFRACAO RSA COM OAEP","\n")
        message2 = aux[:len(aux) - 256]
        print("Mensagem separada da assinatura:")
        print(message2, "\n")
        encoded_hash_bytes = aux[len(aux) - 256:]
        print("Assinatura separada da messagem:")
        print(encoded_hash_bytes, "\n")
        encoded_hash = int.from_bytes(encoded_hash_bytes)
        print("Assinatura em numero inteiro:")
        print(encoded_hash, "\n")
        phi = (p-1)*(q-1)
        print("phi(n) = (p-1)*(q-1):")
        print(phi, "\n")
        hash = rsa_decrypt(encoded_hash, 23, phi, n)
        print("Assinatura sem padding decifrada:")
        print(hash, "\n")
        hash_teste = int.from_bytes(hashlib.sha3_256(message2).digest())
        print("Hash da mensagem:")
        print(hash_teste, "\n")
        if hash == hash_teste:
            print("Mensagem decodificada em BASE64:")
            print(base64.b64decode(message2).decode())
        input()
        break
    else:
        continue
