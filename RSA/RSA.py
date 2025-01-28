# Large Prime Generation for RSA
import random
import sys
import hashlib
import base64
 
# Pre generated primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]
 
def mdc(p, q):
    while q != 0:
        p, q = q, p % q
    return p

def nBitRandom(n):
    return random.getrandbits(n)
 
def getLowLevelPrime(n):
    '''Generate a prime candidate divisible 
    by first primes'''
    while True:
        # Obtain a random number
        pc = nBitRandom(n)
 
        # Test divisibility by pre-generated
        # primes
        for divisor in first_primes_list:
            if pc % divisor == 0 and divisor**2 <= pc:
                break
        else:
            return pc
 
 
def isMillerRabinPassed(mrc):
    '''Run 20 iterations of Rabin Miller Primality test'''
    maxDivisionsByTwo = 0
    ec = mrc-1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwo += 1
    assert(2**maxDivisionsByTwo * ec == mrc-1)
 
    def trialComposite(round_tester):
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2**i * ec, mrc) == mrc-1:
                return False
        return True
 
    # Set number of trials here
    numberOfRabinTrials = 20
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, mrc)
        if trialComposite(round_tester):
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
        print("*/*//*/*/*/*/*/*/*/*/*/*/*/*/*/**/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*")
        #print(p)
        #print(q)
        n = p*q
        f = open("entrada.txt", "r")
        test = f.read()
        message = base64.b64encode(test.encode())
        print(message)
        print(base64.b64decode(message))
        teste = hashlib.sha3_256(message).digest()
        print(teste)
        teste2 = int.from_bytes(teste)
        print(teste2)
        print(teste2.to_bytes(32))
        print('----------------------------------------------------------------')
        phi = (p-1)*(q-1)
        cipher = rsa_encrypt(teste2, 23, n)
        print('----------------------------------------------------------------')
        print(cipher)
        print(cipher.bit_length())
        aux = message + cipher.to_bytes(256)
        print(aux)
        print('----------------------------------------------------------------')
        message2 = aux[:len(aux) - 256]
        encoded_hash_bytes = aux[len(aux) - 256:]
        print(encoded_hash_bytes)
        encoded_hash = int.from_bytes(encoded_hash_bytes)
        print('----------------------------------------------------------------')
        print(encoded_hash)
        hash = rsa_decrypt(encoded_hash, 23, phi, n)
        print('----------------------------------------------------------------')
        print(hash)
        if hash == teste2:
            print(teste2)
            print(base64.b64decode(message2).decode())
        break
    else:
        continue