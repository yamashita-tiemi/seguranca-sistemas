def cifra_cesar_encriptar(texto, chave):
    """
    Encripta um texto utilizando a Cifra de César com a chave especificada.
    
    Args:
        texto (str): O texto a ser encriptado
        chave (int): O valor de deslocamento (1 a N)
    
    Returns:
        str: O texto encriptado
    """
    # Garantir que é um número positivo
    chave = abs(chave)
    
    resultado = ""
    
    for caractere in texto:
        if caractere.isalpha():
            # Determinar o código ASCII base (65 para maiúsculas, 97 para minúsculas)
            ascii_base = 65 if caractere.isupper() else 97
            indice = ord(caractere) - ascii_base
            novo_indice = (indice + chave) % 26
            novo_caractere = chr(novo_indice + ascii_base)
            
            resultado += novo_caractere
        else:
            resultado += caractere
    
    return resultado

def cifra_cesar_decriptar(texto_cifrado, chave):
    """
    Decripta um texto que foi encriptado com a Cifra de César usando a chave especificada.
    
    Args:
        texto_cifrado (str): O texto cifrado a ser decriptado
        chave (int): O valor de deslocamento usado na encriptação
    
    Returns:
        str: O texto original decriptado
    """
    chave_inversa = 26 - (chave % 26)
    return cifra_cesar_encriptar(texto_cifrado, chave_inversa)


def mostrar_menu():
    """
    Exibe o menu de opções para o usuário.
    """
    print("\n-- MENU --")
    print("1. Encriptar uma mensagem")
    print("2. Decriptar uma mensagem")
    print("0. Sair")

if __name__ == "__main__":
    print("Cifra de César – Desloca letras do texto por um número fixo de posições no alfabeto")
    while True:
        mostrar_menu()
        try:
            opcao = int(input("\nEscolha uma opção: "))
            
            if opcao == 0:
                print("\nEncerrando o programa...")
                break
                
            elif opcao == 1:
                mensagem = input("\nDigite a mensagem a ser encriptada: ")
                while True:
                    try:
                        chave = int(input("Digite a chave de deslocamento (1-25): "))
                        if 1 <= chave <= 25:
                            break
                        else:
                            print("Número fora do range aceito")
                    except ValueError:
                        print("Valor inválido")
                
                resultado = cifra_cesar_encriptar(mensagem, chave)
                print(f"Mensagem original: {mensagem}")
                print(f"Mensagem cifrada: {resultado}")
                
                opcao_decriptar = input("\nDeseja decriptar esta mensagem? (s/n): ").lower()
                if opcao_decriptar == 's' or opcao_decriptar == 'sim':
                    mensagem_decriptada = cifra_cesar_decriptar(resultado, chave)
                    print(f"Mensagem decifrada: {mensagem_decriptada}")
                
            elif opcao == 2:
                mensagem_cifrada = input("\nDigite a mensagem a ser decriptada: ")
                while True:
                    try:
                        chave = int(input("Digite a chave de deslocamento (1-25): "))
                        if 1 <= chave <= 25:
                            break
                        else:
                            print("Número fora do range aceito")
                    except ValueError:
                        print("Valor inválido.")
                
                resultado = cifra_cesar_decriptar(mensagem_cifrada, chave)
                print(f"Mensagem inserida: {mensagem_cifrada}")
                print(f"Mensagem decifrada: {resultado}")
                
            else:
                print("\nOpção inválida")
                
        except ValueError:
            print("\nValor válido.")
    
        except KeyboardInterrupt:
            print("\nEncerrando o programa...")
            break