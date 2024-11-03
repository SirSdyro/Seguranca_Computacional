#include <iostream>
#include <string>
#include <algorithm>
#include <list>
#include <tuple>

typedef std::string string;

bool compare (const std::tuple<char,int>& first, const std::tuple<char,int>& second){
    if (std::get<1>(first) > std::get<1>(second)){
        return true;
    } 
    else if (std::get<1>(first) < std::get<1>(second)){
        return false;
    }
    return false;
}

char Relocate(int letter, int key){
    if (letter >= 'A' && letter <= 'Z') {
        return char((letter - 'A' - key + 26) % 26 + 'A');
    }
    if (letter >= 'a' && letter <= 'z') {
        return char((letter - 'a' - key + 26) % 26 + 'a');
    }
    return letter;
}

string lowerCase(string text){
    string lowerString;
    for(char& c : text){
        lowerString += tolower(c);
    }
    return lowerString;
}

void analiseFreq(const string& ciphertext){
    string freq = "aeosirdntcmuplvgbfqhjzxkwy";
    string cipher = lowerCase(ciphertext);
    string plaintext;
    std::list<std::tuple<char,int>> freqCipher;
    for(char& c : cipher){
        std::string::difference_type n = std::count(cipher.begin(), cipher.end(), c);
        auto tupla = std::make_tuple(c,n);
        if(std::find(freqCipher.begin(), freqCipher.end(), tupla) == freqCipher.end()){
            freqCipher.push_back(tupla);
        }
    }
    freqCipher.sort(compare);
    int escolha = 0;
    for (auto t : freqCipher){
        char letra = std::get<0>(t);
        for (char& c : freq){
            plaintext.clear();
            for(int j = 0; j < cipher.length(); j++){
                plaintext += Relocate(int(cipher[j]),abs(int(letra) - int(c)));
            }
            std::cout << plaintext << " chave: " << abs(int(letra) - int(c)) << std::endl;
            std::cout << "Digite 1 para mensagem correta \nDigite 2 para mensagem errada" << std::endl;
            std::cin >> escolha;
            if (escolha == 2){
                continue;
            }
            else if (escolha == 1){
                break;
            }
        if (escolha == 1){
            break;
        }
        }
    if (escolha == 1){
        break;
    }
    }
}

void bruteForce(const string& ciphertext){
    string plaintext;
    for(int i = 0; i < 26; i++){
        plaintext.clear();
        for(int j = 0; j < ciphertext.length(); j++){
            plaintext += Relocate(int(ciphertext[j]),i);
        }
        std::cout << plaintext << " chave: " << i << std::endl;
    }
}

int main(){
    string ciphertext;
    int escolha;
    std::cout << "1 - forca bruta \n2 - Analise de frequencia" << std::endl;
    std::cin >> escolha;
    if(escolha == 1){
        std::cin.ignore();
        std::getline(std::cin, ciphertext);
        bruteForce(ciphertext);
    }
    else if(escolha == 2){
        std::cin.ignore();
        std::getline(std::cin, ciphertext);
        analiseFreq(ciphertext);
    }
    else{
        std::cout << "não válido" << std::endl;
    }
    return 0;
}