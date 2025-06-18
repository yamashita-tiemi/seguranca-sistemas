## Segurança em Sistemas Computacionais (Cibersegurança)

Este repositório contém implementações práticas e esstudos desenvolvidos durante a disciplina Segurança em Sistemas Computacionais (DCC075) da Universidade Federal de Juiz de Fora (UFJF).

Para algumas atividades, foram utilizadas ferramentas de inteligência artificial como apoio para agilizar o desenvolvimento inicial. No entanto, as soluções passaram por revisão, testes e ajustes com base no entendimento dos conceitos estudados.

### Conteúdo do Projeto – Parte 1

- [Role-Based Access Control (RBAC):](./RBAC.py) Define permissões com base nos papéis atribuídos aos usuários.

- [OAuth2:](./OAuth2) Protocolo de autorização que permite acesso limitado a recursos de um usuário por meio de tokens.

- [Cifra de César:](./CifraDeCesar) Realiza uma substituição simples de letras, deslocando cada caractere do texto original por um número fixo de posições no alfabeto.

- [Cifra de Feistel:](./Feistel.py) Estrutura de cifra de bloco que divide o texto em partes e aplica múltiplas rodadas de transformação (usou-se 16 rodadas).

- AES (Advanced Encryption Standard): Algoritmo de criptografia simétrica amplamente usado para proteger dados com segurança.

- Modos de Operação em Cifras de Bloco: Define formas diferentes de processar blocos de dados ao usar cifragem por blocos como o AES.

- [Blum Blum Shub + Testes com a Suite do NIST:](./BlumBlumShub) Gera sequências pseudoaleatórias com base em teoria dos números e realiza testes estatísticos de qualidade (usou-se [este site](https://mzsoltmolnar.github.io/random-bitstream-tester/)).

- [Protocolo de Troca de Chaves Diffie-Hellman (DH):](./DiffieHellman.py) Permite que duas partes estabeleçam uma chave secreta compartilhada por um canal inseguro.

#### Execução dos arquivos

Clone este repositório. Acesse o diretório do projeto.

Execute o arquivo desejado com Python: ```python nome_do_arquivo.py```
