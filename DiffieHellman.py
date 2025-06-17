# Valores usados no exemplo:
# p = 9973
# g = 7
# a = 38, b = 69
# A = 8957
# B = 2537
# s = 5295

def mod_exp(base, exp, mod):
    """Exponenciação modular eficiente: (base^exp) mod mod"""
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

def diffie_hellman():
    """Implementação simplificada do Diffie-Hellman com primo grande"""
    print("-- Diffie-Hellman --\n")
    
    # Parâmetros públicos (primo menor que 10000)
    p = 9973 
    g = 7
    
    print(f"Parâmetros públicos:")
    print(f"p = {p:,} (primo menor que 10.000)")
    print(f"g = {g}")
    
    # Chaves privadas (secretas)
    a = 38       # Chave privada de Alice (2 dígitos)
    b = 69        # Chave privada de Bob (2 dígitos)
    
    print(f"\nChaves privadas:")
    print(f"a (Alice) = {a}")
    print(f"b (Bob) = {b}")
    
    # Chaves públicas
    A = mod_exp(g, a, p)  # A = g^a mod p
    B = mod_exp(g, b, p)  # B = g^b mod p
    
    print(f"\nChaves públicas:")
    print(f"A = {g}^{a} mod {p} = {A}")
    print(f"B = {g}^{b} mod {p} = {B}")
    
    # Segredo compartilhado
    s_alice = mod_exp(B, a, p)  # Alice: s = B^a mod p
    s_bob = mod_exp(A, b, p)    # Bob: s = A^b mod p
    
    print(f"\nSegredo compartilhado:")
    print(f"Alice: s = {B}^{a} mod {p} = {s_alice}")
    print(f"Bob: s = {A}^{b} mod {p} = {s_bob}")
    
    return p, g, a, b, A, B, s_alice

def exemplo_didatico():
    """Exemplo didático com números menores para visualizar o processo"""
    print("\n-- Exemplo Didático (números menores) --")
    
    # Parâmetros menores para visualização
    p = 23
    g = 5
    a = 6
    b = 15
    
    print(f"p = {p}, g = {g}")
    print(f"a = {a}, b = {b}")
    
    # Cálculos passo a passo
    A = mod_exp(g, a, p)
    B = mod_exp(g, b, p)
    
    print(f"A = {g}^{a} mod {p} = {A}")
    print(f"B = {g}^{b} mod {p} = {B}")
    
    s_alice = mod_exp(B, a, p)
    s_bob = mod_exp(A, b, p)
    
    print(f"Alice: s = {B}^{a} mod {p} = {s_alice}")
    print(f"Bob: s = {A}^{b} mod {p} = {s_bob}")
    
    return p, g, a, b, A, B, s_alice

if __name__ == "__main__":
    # Exemplo principal com primo grande
    p1, g1, a1, b1, A1, B1, s1 = diffie_hellman()
    
    # Exemplo didático
    # p2, g2, a2, b2, A2, B2, s2 = exemplo_didatico()
