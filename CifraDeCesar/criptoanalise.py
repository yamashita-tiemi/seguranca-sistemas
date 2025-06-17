"""
Criptoanálise da Cifra de César usando Análise de Frequência de Letras
Quebra cifras de César sem conhecer a chave, baseado nas frequências das letras em português.
"""

import collections
import string

# Frequências das letras em português brasileiro (%)
FREQUENCIA_PORTUGUES = {
    'a': 14.63, 'e': 12.57, 'o': 10.73, 's': 7.81, 'r': 6.53,
    'i': 6.18, 'n': 5.05, 'd': 4.99, 'm': 4.74, 'u': 4.63,
    't': 4.34, 'c': 3.88, 'l': 2.78, 'p': 2.52, 'v': 1.67,
    'g': 1.30, 'h': 1.28, 'q': 1.20, 'b': 1.04, 'f': 1.02,
    'z': 0.47, 'j': 0.40, 'x': 0.21, 'k': 0.02, 'w': 0.01,
    'y': 0.01
}

def cifra_cesar_decriptar(texto_cifrado, chave):
    """
    Decripta um texto cifrado com Cifra de César.
    
    Args:
        texto_cifrado (str): Texto cifrado
        chave (int): Chave de deslocamento (1-25)
    
    Returns:
        str: Texto decriptado
    """
    chave = chave % 26
    resultado = ""
    
    for caractere in texto_cifrado:
        if caractere.isalpha():
            ascii_base = 65 if caractere.isupper() else 97
            indice = ord(caractere) - ascii_base
            novo_indice = (indice - chave) % 26
            novo_caractere = chr(novo_indice + ascii_base)
            resultado += novo_caractere
        else:
            resultado += caractere
    
    return resultado

def calcular_frequencia_texto(texto):
    """
    Calcula a frequência percentual de cada letra no texto.
    
    Args:
        texto (str): Texto para análise
    
    Returns:
        dict: Frequências percentuais das letras
    """
    # Remove caracteres não-alfabéticos e converte para minúsculas
    texto_limpo = ''.join(c.lower() for c in texto if c.isalpha())
    
    if len(texto_limpo) == 0:
        return {letra: 0 for letra in string.ascii_lowercase}
    
    # Conta ocorrências
    contador = collections.Counter(texto_limpo)
    total_letras = len(texto_limpo)
    
    # Calcula frequências percentuais
    frequencias = {}
    for letra in string.ascii_lowercase:
        count = contador.get(letra, 0)
        frequencias[letra] = (count / total_letras) * 100
    
    return frequencias

def calcular_chi_quadrado(freq_observada, freq_esperada):
    """
    Calcula o valor chi-quadrado entre frequências observadas e esperadas.
    Menor valor indica melhor correspondência com o padrão esperado.
    
    Args:
        freq_observada (dict): Frequências observadas no texto
        freq_esperada (dict): Frequências esperadas (padrão português)
    
    Returns:
        float: Valor chi-quadrado
    """
    chi_quadrado = 0
    
    for letra in string.ascii_lowercase:
        observada = freq_observada.get(letra, 0)
        esperada = freq_esperada.get(letra, 0)
        
        if esperada > 0:
            chi_quadrado += ((observada - esperada) ** 2) / esperada
    
    return chi_quadrado

def criptoanalise_cesar(texto_cifrado, mostrar_processo=True):
    """
    Realiza criptoanálise da Cifra de César usando análise de frequência.
    
    Args:
        texto_cifrado (str): Texto cifrado para quebrar
        mostrar_processo (bool): Se deve mostrar o processo de análise
    
    Returns:
        list: Lista de tuplas (chave, pontuacao, texto_decriptado) ordenada por probabilidade
    """
    if mostrar_processo:
        print("=== CRIPTOANÁLISE POR FREQUÊNCIA DE LETRAS ===")
        print(f"Texto cifrado: {texto_cifrado}")
        texto_limpo = ''.join(c for c in texto_cifrado if c.isalpha())
        print(f"Total de letras: {len(texto_limpo)}")
        
        if len(texto_limpo) < 50:
            print("⚠️  AVISO: Texto curto. Análise pode ser imprecisa.")
        
        print("\nTestando todas as chaves possíveis...\n")
    
    resultados = []
    
    # Testa todas as chaves de 1 a 25
    for chave in range(1, 26):
        # Decripta com a chave atual
        texto_decriptado = cifra_cesar_decriptar(texto_cifrado, chave)
        
        # Calcula frequências do texto decriptado
        freq_observadas = calcular_frequencia_texto(texto_decriptado)
        
        # Calcula chi-quadrado (menor = melhor)
        pontuacao = calcular_chi_quadrado(freq_observadas, FREQUENCIA_PORTUGUES)
        
        resultados.append((chave, pontuacao, texto_decriptado))
        
        if mostrar_processo:
            preview = texto_decriptado[:60] + "..." if len(texto_decriptado) > 60 else texto_decriptado
            print(f"Chave {chave:2d}: χ² = {pontuacao:7.2f} | {preview}")
    
    # Ordena por pontuação (menor chi-quadrado = melhor)
    resultados.sort(key=lambda x: x[1])
    
    return resultados

def mostrar_resultados_detalhados(resultados, top_n=5):
    """
    Mostra os melhores resultados da criptoanálise de forma detalhada.
    
    Args:
        resultados (list): Lista de resultados da criptoanálise
        top_n (int): Número de melhores resultados para mostrar
    """
    print(f"\n=== TOP {top_n} MELHORES RESULTADOS ===")
    print("-" * 70)
    
    for i, (chave, pontuacao, texto) in enumerate(resultados[:top_n]):
        print(f"\n{i+1}º LUGAR - Chave {chave} (χ² = {pontuacao:.2f}):")
        print(f"'{texto}'")
        
        if i == 0:
            print("👆 RESULTADO MAIS PROVÁVEL")

def analisar_frequencias_detalhadas(texto):
    """
    Mostra análise detalhada das frequências de um texto.
    
    Args:
        texto (str): Texto para análise
    """
    freq_observadas = calcular_frequencia_texto(texto)
    
    print("\n=== ANÁLISE DETALHADA DE FREQUÊNCIAS ===")
    print(f"Texto: {texto[:100]}{'...' if len(texto) > 100 else ''}")
    
    texto_limpo = ''.join(c for c in texto if c.isalpha())
    print(f"Total de letras analisadas: {len(texto_limpo)}")
    
    print("\n" + "="*55)
    print("| Letra | Observada | Esperada | Diferença |")
    print("="*55)
    
    # Ordena por frequência observada (decrescente)
    letras_ordenadas = sorted(freq_observadas.items(), key=lambda x: x[1], reverse=True)
    
    for letra, freq_obs in letras_ordenadas:
        if freq_obs > 0:  # Só mostra letras que aparecem
            freq_esp = FREQUENCIA_PORTUGUES[letra]
            diferenca = freq_obs - freq_esp
            status = "✓" if abs(diferenca) < 2 else "⚠" if abs(diferenca) < 5 else "✗"
            
            print(f"|   {letra}   |   {freq_obs:5.2f}%  |  {freq_esp:5.2f}%  |  {diferenca:+6.2f}% {status} |")
    
    print("="*55)
    print("✓ = Diferença pequena | ⚠ = Diferença média | ✗ = Diferença grande")

def quebrar_cifra_cesar(texto_cifrado):
    """
    Função principal para quebrar uma Cifra de César.
    
    Args:
        texto_cifrado (str): Texto cifrado
    
    Returns:
        tuple: (melhor_chave, melhor_texto, todos_resultados)
    """
    resultados = criptoanalise_cesar(texto_cifrado)
    mostrar_resultados_detalhados(resultados)
    
    melhor_chave, _, melhor_texto = resultados[0]
    
    return melhor_chave, melhor_texto, resultados

# Exemplo de uso
if __name__ == "__main__":
    print("CRIPTOANÁLISE DA CIFRA DE CÉSAR")
    print("=" * 50)
    
    while True:
        print("\n1. Quebrar cifra (criptoanálise)")
        print("2. Analisar frequências de um texto")
        print("3. Exemplo de demonstração")
        print("0. Sair")
        
        try:
            opcao = int(input("\nEscolha uma opção: "))
            
            if opcao == 0:
                print("Encerrando...")
                break
                
            elif opcao == 1:
                texto_cifrado = input("\nDigite o texto cifrado: ")
                chave, texto_original, _ = quebrar_cifra_cesar(texto_cifrado)
                
                print(f"\n🔓 CIFRA QUEBRADA!")
                print(f"Chave mais provável: {chave}")
                print(f"Texto original: '{texto_original}'")
                
            elif opcao == 2:
                texto = input("\nDigite o texto para análise: ")
                analisar_frequencias_detalhadas(texto)
                
            elif opcao == 3:
                # Exemplo de demonstração
                print("\n=== EXEMPLO DE DEMONSTRAÇÃO ===")
                
                # Texto original
                texto_original = "Esta é uma mensagem secreta que precisa ser decifrada usando análise de frequência"
                print(f"Texto original: {texto_original}")
                
                # Simula encriptação com chave 7
                from random import randint
                chave_real = randint(1, 25)
                
                # Encripta manualmente para demonstração
                texto_cifrado = ""
                for c in texto_original:
                    if c.isalpha():
                        base = 65 if c.isupper() else 97
                        novo = chr((ord(c) - base + chave_real) % 26 + base)
                        texto_cifrado += novo
                    else:
                        texto_cifrado += c
                
                print(f"Texto cifrado (chave {chave_real}): {texto_cifrado}")
                
                # Quebra a cifra
                chave_encontrada, texto_decifrado, _ = quebrar_cifra_cesar(texto_cifrado)
                
                print(f"\n🎯 RESULTADO:")
                print(f"Chave real: {chave_real}")
                print(f"Chave encontrada: {chave_encontrada}")
                print(f"Sucesso: {'✅ SIM' if chave_real == chave_encontrada else '❌ NÃO'}")
                
            else:
                print("Opção inválida!")
                
        except ValueError:
            print("Digite um número válido!")
        except KeyboardInterrupt:
            print("\nEncerrando...")
            break