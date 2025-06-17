import random
import math
import os
from typing import Tuple

class BlumBlumShub:
    def __init__(self, min_prime=10000):
        """
        Inicializa o gerador BBS encontrando automaticamente p, q e s adequados
        """
        self.min_prime = min_prime
        
        # Gera automaticamente p e q e calcula n
        self.p, self.q = self.generate_suitable_primes()
        self.n = self.p * self.q
        
        # Gera automaticamente o seed s
        self.s = self.generate_seed()
        
        # Estado inicial
        self.current_state = (self.s * self.s) % self.n
        
        # Estatísticas
        self.bits_generated = 0
        
        self.print_parameters()
    
    def is_prime(self, n: int) -> bool:
        """Teste de primalidade otimizado"""
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True
    
    def find_next_prime_congruent_3_mod_4(self, start: int) -> int:
        """
        Encontra o próximo primo p tal que p ≡ 3 (mod 4) e p >= start
        """
        candidate = start
        if candidate % 2 == 0:
            candidate += 1
        
        while True:
            if candidate % 4 == 3 and self.is_prime(candidate):
                return candidate
            candidate += 2  # Só testa números ímpares
    
    def generate_suitable_primes(self) -> Tuple[int, int]:
        """
        Gera dois primos p e q adequados para BBS com melhor segurança:
        - p, q > min_prime
        - p ≡ 3 (mod 4) e q ≡ 3 (mod 4)
        - p ≠ q
        - Diferença significativa entre p e q para melhor segurança
        """
        print("Procurando primos adequados para BBS...")
        
        # Encontra p
        p = self.find_next_prime_congruent_3_mod_4(self.min_prime + 1)
        
        # Encontra q com diferença significativa de p
        # Isso melhora a qualidade criptográfica
        min_diff = max(100, p // 100)  # Diferença mínima entre p e q
        q_start = p + min_diff
        q = self.find_next_prime_congruent_3_mod_4(q_start)
        
        # Verifica se os primos são adequados
        while abs(p - q) < min_diff:
            q = self.find_next_prime_congruent_3_mod_4(q + 2)
        
        print(f"Primos encontrados: p = {p}, q = {q}")
        print(f"Diferença: |p - q| = {abs(p - q)}")
        print(f"Verificação: p mod 4 = {p % 4}, q mod 4 = {q % 4}")
        
        return p, q
    
    def generate_seed(self) -> int:
        """
        Gera um seed s adequado com melhor distribuição:
        - 1 < s < n
        - gcd(s, n) = 1
        - s deve ser escolhido de forma criptograficamente segura
        """
        print("Gerando seed adequado...")
        
        # Usa diferentes estratégias para encontrar um bom seed
        max_attempts = 10000
        
        for attempt in range(max_attempts):
            # Estratégia 1: números aleatórios grandes (primeiros 70% das tentativas)
            if attempt < max_attempts * 0.7:
                # Gera um número grande próximo a n/2 para melhor distribuição
                min_val = self.n // 4
                max_val = (3 * self.n) // 4
                s = random.randint(min_val, max_val)
            else:
                # Estratégia 2: números menores mas ainda adequados
                s = random.randint(self.n // 10, self.n - 1)
            
            # Verifica se é coprimo com n
            if math.gcd(s, self.n) == 1:
                # Verifica se não é um quadrado perfeito
                sqrt_s = int(math.sqrt(s))
                if sqrt_s * sqrt_s != s:
                    # Teste adicional: verifica se o seed inicial produz boa distribuição
                    x0 = (s * s) % self.n
                    if x0 > self.n // 10:  # Evita valores muito pequenos
                        print(f"Seed encontrado após {attempt + 1} tentativas: s = {s}")
                        print(f"Verificações: gcd(s, n) = {math.gcd(s, self.n)}, x₀ = {x0}")
                        return s
        
        raise ValueError("Não foi possível encontrar um seed adequado após muitas tentativas")
    
    def print_parameters(self):
        """Imprime os parâmetros gerados"""
        print("\n-- Parâmetros Gerados --")
        print(f"p = {self.p}")
        print(f"q = {self.q}")
        print(f"n = p × q = {self.n}")
        print(f"s (seed) = {self.s}")
        print(f"x₀ = s² mod n = {self.current_state}")
        print(f"Tamanho de n: {self.n.bit_length()} bits")
    
    def next_bit(self) -> int:
        """
        Gera o próximo bit pseudoaleatório usando BBS com melhor extração
        """
        # x_{i+1} = x_i^2 mod n
        self.current_state = pow(self.current_state, 2, self.n)
        
        # Para melhor qualidade estatística, podemos usar diferentes estratégias de extração
        # Estratégia 1: LSB (padrão BBS)
        bit = self.current_state & 1
        
        # Estratégia 2: Para alguns casos, usar outros bits pode ser melhor
        # Descomente a linha abaixo se quiser testar com bit de paridade
        # bit = bin(self.current_state).count('1') & 1
        
        self.bits_generated += 1
        return bit
    
    def generate_bytes(self, num_bytes: int) -> bytearray:
        """
        Gera uma sequência de bytes usando BBS
        """
        result = bytearray()
        
        for _ in range(num_bytes):
            byte_val = 0
            # Gera 8 bits para formar um byte
            for bit_pos in range(8):
                bit = self.next_bit()
                byte_val = (byte_val << 1) | bit
            
            result.append(byte_val)
        
        return result
    
    def generate_bitstream_file(self, filename: str, num_bits: int = 100000, format_type: str = "txt"):
        """
        Gera um arquivo de texto ou binário para teste
        
        Args:
            filename: Nome do arquivo a ser criado
            num_bits: Número de bits a gerar
            format_type: "txt" para texto ou "bin" para binário
        """
        
        if format_type == "txt":
            self.generate_text_file(filename, num_bits)
        else:
            self.generate_binary_file(filename, num_bits)
    
    def generate_text_file(self, filename: str, num_bits: int):
        """
        Gera um arquivo de texto com bits em uma única linha contínua
        """
        print(f"\nGerando arquivo de texto: {filename}")
        print(f"Número de bits: {num_bits:,}")
        print("Gerando dados...")
        
        with open(filename, 'w') as f:
            bits_written = 0
            
            while bits_written < num_bits:
                bit = self.next_bit()
                f.write(str(bit))
                bits_written += 1
                
                # Mostra progresso
                # if bits_written % 10000 == 0 or bits_written == num_bits:
                #     progress = (bits_written / num_bits) * 100
                #     print(f"Progresso: {progress:.1f}% ({bits_written:,}/{num_bits:,} bits)")
        
        print(f"\nArquivo de texto gerado com sucesso: {filename}")
        print(f"Total de bits gerados: {self.bits_generated:,}")
        print(f"Tamanho do arquivo: {os.path.getsize(filename):,} bytes")
    
    def generate_binary_file(self, filename: str, num_bits: int):
        """
        Gera um arquivo binário (método original)
        """
        num_bytes = (num_bits + 7) // 8  # Arredonda para cima
        
        print(f"\nGerando arquivo binário: {filename}")
        print(f"Número de bits: {num_bits:,} ({num_bytes:,} bytes)")
        print("Gerando dados...")
        
        # Gera os dados em chunks para economizar memória
        chunk_size = 64 * 1024  # 64KB por vez
        bytes_written = 0
        
        with open(filename, 'wb') as f:
            while bytes_written < num_bytes:
                # Calcula quantos bytes gerar neste chunk
                remaining = num_bytes - bytes_written
                current_chunk_size = min(chunk_size, remaining)
                
                # Gera o chunk
                chunk_data = self.generate_bytes(current_chunk_size)
                
                # Escreve no arquivo
                f.write(chunk_data)
                bytes_written += len(chunk_data)
                
                # Mostra progresso
                progress = (bytes_written / num_bytes) * 100
                if bytes_written % (chunk_size * 10) == 0 or bytes_written == num_bytes:
                    print(f"Progresso: {progress:.1f}% ({bytes_written:,}/{num_bytes:,} bytes)")
        
        # Estatísticas finais
        print(f"\nArquivo binário gerado com sucesso: {filename}")
        print(f"Total de bits gerados: {self.bits_generated:,}")
        print(f"Tamanho do arquivo: {os.path.getsize(filename):,} bytes")
    
    def analyze_first_bytes(self, num_bytes: int = 16):
        """Analisa os primeiros bytes gerados para verificação"""
        print(f"\nAnálise dos primeiros {num_bytes} bytes:")
        
        # Salva o estado atual
        saved_state = self.current_state
        saved_bits_count = self.bits_generated
        
        # Reinicia para análise
        self.current_state = (self.s * self.s) % self.n
        self.bits_generated = 0
        
        for i in range(num_bytes):
            byte_val = 0
            bits = []
            
            for bit_pos in range(8):
                bit = self.next_bit()
                bits.append(str(bit))
                byte_val = (byte_val << 1) | bit
            
            print(f"Byte {i+1:2d}: {byte_val:3d} (0x{byte_val:02X}) "
                  f"(binário: {''.join(bits)})")
        
        # Restaura o estado
        self.current_state = saved_state
        self.bits_generated = saved_bits_count

def main():
    """Função principal que demonstra o uso do BBS"""
    
    # Cria o gerador BBS
    print("Inicializando Gerador Blum Blum Shub...")
    bbs = BlumBlumShub(min_prime=10000)
    
    bbs.analyze_first_bytes(4)
    
    # Configurações para geração do arquivo
    filename_txt = "bbs_random_data.txt"
    
    # Para passar nos testes estatísticos, precisa de mais bits
    # Testes como Universal Statistical requerem pelo menos 387,840 bits
    num_bits = 1000000  # 1 milhão de bits para testes robustos
    
    print("\n-- Geração do arquivo --")
    print(f"ATENÇÃO: Gerando {num_bits:,} bits para testes estatísticos rigorosos")
    print("   Isso pode demorar alguns minutos...")
    
    try:
        # Gera o arquivo de texto
        bbs.generate_bitstream_file(filename_txt, num_bits, format_type="txt")
        
    except Exception as e:
        print(f"Erro ao gerar arquivo: {e}")

if __name__ == "__main__":
    main()