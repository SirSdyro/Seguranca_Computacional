#include <iostream>
#include <string>

//Funcao utilizada para realizar o deslocamento das letras, baseado se estao na forma maiuscula ou minuscula
char Deslocate(int letter, int key){
    if (letter >= 'A' && letter <= 'Z') {
        return char((letter + key) % (26 + 'A'));
    }
    if (letter >= 'a' && letter <= 'z') {
        return char((letter + key) % (26 + 'a'));
    }
    return letter;
}

int main(){
    int key;
    std::string plaintext, ciphertext;
    std::cin >> key; //chave do deslocamento
    std::cin.ignore();
    std::getline(std::cin,plaintext); //entrada do texto plano
    for (int i = 0;i < plaintext.length(); i++){
        if (plaintext[i] != ' '){
        ciphertext += Deslocate(int(plaintext[i]),key);
        }
        else{
        ciphertext += plaintext[i];   
        }
    }
    std::cout << ciphertext; //saida do texto cifrado
}
