#include <iostream>
#include <string>
#include <list>
#include <algorithm>

typedef std::string string;

string lowerCase(string text){
    string lowerString;
    for(char& c : text){
        lowerString += tolower(c);
    }
    return lowerString;
}

std::list<int> Chave(const string& x){
    string key = lowerCase(x);
    string chave;
    std::list<int> coluna;
    int index, dist;
    while (coluna.size() < key.size()){
        dist = 27;
        index = -1;
        for (int i = 0; i < key.size(); i++) {
            if (std::find(coluna.begin(), coluna.end(), i) == coluna.end()) {
                if (key[i] - 'a' < dist) {
                    dist = key[i] - 'a';
                    index = i;
                }
            }
        }
        if (index != -1) {
            coluna.push_back(index);
        }
    }
    return coluna;
}

string cifraTranspo(string chave, string mensagem){
    std::list<int> key = Chave(chave);
    string alphabet = "abcdefghijklmnopqrstuvwxyz";
    string ciphertext;
    int index_1 = -1;
    int index_2 = -1;
    while (mensagem.size() % key.size() != 0){
        index_1++;
        mensagem += alphabet[index_1];
    }
    for(int n : key){
        index_2 = n;
        while(index_2 < mensagem.size()){
            ciphertext += mensagem[index_2];
            index_2 += key.size();
        }
    }
    return ciphertext;

}

void permuteRec(string ciphertext, int index)
{
    std::list<string> trigrafos = {"que","ent","nte","ado","ade","ode","ara","est","res","con","com","sta","dos","cao","par","aca","men","sde","ica","ese","aco","ada","por","nto","ose","des","ase","era","oes","uma","tra","ida","dad","ant","are","ont","pre","ist","ter","ais"};
    
    for(string trig : trigrafos){
        if(ciphertext.find(trig) != std::string::npos){
            if (index == ciphertext.size() - 1) {
                std::cout << ciphertext << std::endl;
                return;
            }
        }
    }

    for (int i = index; i < ciphertext.size(); i++) {
      
        // Swapping 
        std::swap(ciphertext[index], ciphertext[i]);

        // First idx+1 characters fixed
        permuteRec(ciphertext, index + 1);

        // Backtrack
        std::swap(ciphertext[index], ciphertext[i]);
    }
}

void decryptTranspo(string ciphertext) {
    permuteRec(ciphertext, 0);
}

int main(){
    int i;
    std::cout << "Digite 1 para criptografar \nDigite 2 para descriptografar" << std::endl;
    std::cin >> i;
    if (i == 1){
        string chave, plaintext;
        std::cout << "chave: " << std::endl;
        std::cin.ignore();
        std::getline(std::cin,chave);
        std::cout << "mensagem: " << std::endl;
        std::cin.ignore();
        std::getline(std::cin,plaintext);
        string x = cifraTranspo(chave,plaintext);
        std::cout << x;  
    }
    if (i == 2){
        string ciphertext;
        std::cout << "texto cifrado: " << std::endl;
        std::cin.ignore();
        std::getline(std::cin,ciphertext);
        decryptTranspo(ciphertext);
    }
    return 0;
}