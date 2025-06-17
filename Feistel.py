class FeistelCipher:
    def __init__(self, key="FEDCBA9876543210"):
        """
        Inicializa a cifra Feistel com chave de 64 bits (16 hex chars)
        """
        self.key = key
        self.rounds = 16
        self.subkeys = self._generate_subkeys()
    
    def _generate_subkeys(self):
        """
        Gera 16 subchaves de 32 bits a partir da chave principal
        Implementação simples: rotação circular da chave
        """
        subkeys = []
        key_int = int(self.key, 16)
        
        for i in range(self.rounds):
            # Rotação circular para gerar subchaves diferentes
            rotated = ((key_int << (i * 4)) | (key_int >> (64 - (i * 4)))) & 0xFFFFFFFFFFFFFFFF
            # Pega os 32 bits menos significativos como subchave
            subkey = rotated & 0xFFFFFFFF
            subkeys.append(subkey)
        
        return subkeys
    
    def _f_function(self, right_half, subkey):
        """
        Função F da estrutura Feistel
        Implementação simples: XOR com expansão e substituição básica
        """
        # Expansão: duplica alguns bits para criar confusão
        expanded = ((right_half << 1) | (right_half >> 31)) & 0xFFFFFFFF
        
        # XOR com a subchave
        xor_result = expanded ^ subkey
        
        # Substituição simples (S-box básica)
        substituted = 0
        for i in range(8):
            # Pega 4 bits por vez
            nibble = (xor_result >> (i * 4)) & 0xF
            # Substituição simples: inversão dos bits + XOR
            new_nibble = ((~nibble) ^ 0x5) & 0xF
            substituted |= (new_nibble << (i * 4))
        
        # Permutação final
        permuted = ((substituted << 7) | (substituted >> 25)) & 0xFFFFFFFF
        
        return permuted
    
    def _feistel_round(self, left, right, subkey):
        """
        Executa uma rodada da estrutura Feistel
        """
        new_left = right
        new_right = left ^ self._f_function(right, subkey)
        return new_left, new_right
    
    def _pad_text(self, text):
        """
        Adiciona padding ao texto para completar blocos de 64 bits (16 chars hex)
        """
        # Se o comprimento não é múltiplo de 16, adiciona padding
        remainder = len(text) % 16
        if remainder != 0:
            padding_needed = 16 - remainder
            text += '0' * padding_needed
        return text
    
    def _encrypt_block(self, block):
        """
        Encripta um único bloco de 16 caracteres hexadecimais (64 bits)
        """
        # Converte para inteiro e divide em duas metades
        plain_int = int(block, 16)
        left = (plain_int >> 32) & 0xFFFFFFFF  # 32 bits mais significativos
        right = plain_int & 0xFFFFFFFF         # 32 bits menos significativos
        
        # 16 rodadas de encriptação
        for round_num in range(self.rounds):
            left, right = self._feistel_round(left, right, self.subkeys[round_num])
        
        # Combina as metades finais (inverte a ordem - característica Feistel)
        ciphertext_int = (right << 32) | left
        return f"{ciphertext_int:016X}"
    
    def encrypt(self, plaintext):
        """
        Encripta o texto usando a estrutura Feistel
        plaintext: string hexadecimal de qualquer tamanho
        """
        print(f"Texto original: {plaintext}")
        print(f"Tamanho: {len(plaintext)} caracteres")
        
        # Adiciona padding se necessário
        padded_text = self._pad_text(plaintext)
        if len(padded_text) != len(plaintext):
            print(f"Texto com padding: {padded_text}")
        
        # Processa em blocos de 16 caracteres (64 bits cada)
        ciphertext = ""
        num_blocks = len(padded_text) // 16
        
        print(f"\nProcessando {num_blocks} bloco(s) de 64 bits cada:")
        print("\n--- Processo de Encriptação ---")
        
        for i in range(num_blocks):
            start = i * 16
            end = start + 16
            block = padded_text[start:end]
            
            print(f"\nBloco {i + 1}: {block}")
            
            # Mostra o processo detalhado apenas para o primeiro bloco
            if i == 0:
                plain_int = int(block, 16)
                left = (plain_int >> 32) & 0xFFFFFFFF
                right = plain_int & 0xFFFFFFFF
                print(f"L0: {left:08X}, R0: {right:08X}")
                
                for round_num in range(self.rounds):
                    left, right = self._feistel_round(left, right, self.subkeys[round_num])
                    print(f"Rodada {round_num + 1:2d}: L{round_num + 1} = {left:08X}, R{round_num + 1} = {right:08X}")
                
                encrypted_block = f"{((right << 32) | left):016X}"
            else:
                encrypted_block = self._encrypt_block(block)
            
            print(f"Bloco cifrado: {encrypted_block}")
            ciphertext += encrypted_block
        
        return ciphertext
    
    def _decrypt_block(self, block):
        """
        Decripta um único bloco de 16 caracteres hexadecimais (64 bits)
        """
        # Converte para inteiro e divide em duas metades
        cipher_int = int(block, 16)
        left = (cipher_int >> 32) & 0xFFFFFFFF  # 32 bits mais significativos
        right = cipher_int & 0xFFFFFFFF         # 32 bits menos significativos
        
        # 16 rodadas de decriptação (usando subchaves em ordem reversa)
        for round_num in range(self.rounds):
            subkey_index = self.rounds - 1 - round_num
            left, right = self._feistel_round(left, right, self.subkeys[subkey_index])
        
        # Combina as metades finais (inverte a ordem)
        plaintext_int = (right << 32) | left
        return f"{plaintext_int:016X}"
    
    def decrypt(self, ciphertext):
        """
        Decripta o texto usando a estrutura Feistel
        ciphertext: string hexadecimal de qualquer tamanho (múltiplo de 16)
        """
        if len(ciphertext) % 16 != 0:
            raise ValueError("Ciphertext deve ter tamanho múltiplo de 16 caracteres hexadecimais")
        
        print(f"\nTexto cifrado: {ciphertext}")
        print(f"Tamanho: {len(ciphertext)} caracteres")
        
        # Processa em blocos de 16 caracteres (64 bits cada)
        plaintext = ""
        num_blocks = len(ciphertext) // 16
        
        print(f"\nProcessando {num_blocks} bloco(s) de 64 bits cada:")
        print("\n--- Processo de Decriptação ---")
        
        for i in range(num_blocks):
            start = i * 16
            end = start + 16
            block = ciphertext[start:end]
            
            print(f"\nBloco {i + 1}: {block}")
            
            # Mostra o processo detalhado apenas para o primeiro bloco
            if i == 0:
                cipher_int = int(block, 16)
                left = (cipher_int >> 32) & 0xFFFFFFFF
                right = cipher_int & 0xFFFFFFFF
                print(f"L0: {left:08X}, R0: {right:08X}")
                
                for round_num in range(self.rounds):
                    subkey_index = self.rounds - 1 - round_num
                    left, right = self._feistel_round(left, right, self.subkeys[subkey_index])
                    print(f"Rodada {round_num + 1:2d}: L{round_num + 1} = {left:08X}, R{round_num + 1} = {right:08X}")
                
                decrypted_block = f"{((right << 32) | left):016X}"
            else:
                decrypted_block = self._decrypt_block(block)
            
            print(f"Bloco decifrado: {decrypted_block}")
            plaintext += decrypted_block
        
        return plaintext
    
def run_test(cipher, test_number, plaintext, description):
    """
    Executa um teste específico da cifra Feistel
    """
    print(f"\n-- TESTE {test_number}: {description} --")

    print("\n-- ENCRIPTAÇÃO --")
    ciphertext = cipher.encrypt(plaintext)
    print(f"\nResultado da encriptação:")
    print(f"Texto original:  {plaintext}")
    print(f"Texto cifrado:   {ciphertext}")
    
    print("\n-- DECRIPTAÇÃO --")
    decrypted = cipher.decrypt(ciphertext)
    print(f"\nResultado da decriptação:")
    print(f"Texto original:  {plaintext}")
    print(f"Texto decifrado: {decrypted}")
    
    
    original_padded = cipher._pad_text(plaintext)
    
    # Mostra se houve padding
    if len(plaintext) != len(original_padded):
        print(f"Nota: Padding adicionado - Original: {len(plaintext)} chars, Com padding: {len(original_padded)} chars")

def main():
    print("Cifra de Feistel - 16 rodadas\n")
    
    cipher = FeistelCipher()
    print(f"Chave utilizada: {cipher.key}")
    print(f"Número de rodadas: {cipher.rounds}")
    
    # Teste com diferentes tamanhos de entrada
    test_cases = [
        ("0123456789ABCDEF", "1 bloco exato (16 chars)"),
        ("0123456789ABCDEF01234567", "1.5 blocos com padding (24 chars)"),
        ("123ABC", "Texto pequeno com padding (6 chars)"),
        ("0123456789ABCDEF0123456789ABCDEF", "2 blocos exatos (32 chars)"),
    ]
    
    while True:
        print("\n-- MENU --")
        
        # Mostra opções de teste
        for i, (plaintext, description) in enumerate(test_cases, 1):
            if i <= 4:
                print(f"{i}. {description}")
                print(f"   Entrada: '{plaintext}'")
            else:
                print(f"{i}. {description}")
        
        print("0. Sair")
        
        try:
            escolha = input(f"\nEscolha uma opção (0-{len(test_cases)}): ").strip()
            
            if escolha == "0":
                print("\nEncerrando o programa...")
                break
            elif escolha in ["1", "2", "3", "4"]:
                # Teste pré-definido
                index = int(escolha) - 1
                plaintext, description = test_cases[index]
                run_test(cipher, int(escolha), plaintext, description)
            else:
                print("\nOpção inválida")
                
        except KeyboardInterrupt:
            print("\nEncerrando o programa...")
            break
        except Exception as e:
            print(f"ERRO: {e}")

if __name__ == "__main__":
    main()