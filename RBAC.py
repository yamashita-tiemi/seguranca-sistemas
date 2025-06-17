"""
Sistema RBAC (Role-Based Access Control) - Biblioteca
Autor: Demonstração de conceitos RBAC
Cenário: Sistema de gerenciamento de biblioteca com 3 papéis diferentes
"""

from typing import Dict, List, Set
from enum import Enum

class Permissao(Enum):
    """
    Enum que define todas as permissões possíveis no sistema
    """
    # Permissões relacionadas a livros
    VER_LIVROS = "ver_livros"
    ADICIONAR_LIVRO = "adicionar_livro"
    EDITAR_LIVRO = "editar_livro"
    REMOVER_LIVRO = "remover_livro"
    
    # Permissões relacionadas a empréstimos
    EMPRESTAR_LIVRO = "emprestar_livro"
    DEVOLVER_LIVRO = "devolver_livro"
    VER_EMPRESTIMOS = "ver_emprestimos"
    
    # Permissões relacionadas a usuários
    VER_USUARIOS = "ver_usuarios"
    CRIAR_USUARIO = "criar_usuario"
    EDITAR_USUARIO = "editar_usuario"
    REMOVER_USUARIO = "remover_usuario"
    
    # Permissões administrativas
    GERAR_RELATORIOS = "gerar_relatorios"
    CONFIGURAR_SISTEMA = "configurar_sistema"

class Papel:
    """
    Classe que representa um papel (role) no sistema RBAC
    Cada papel tem um nome e um conjunto de permissões
    """
    def __init__(self, nome: str, permissoes: Set[Permissao]):
        self.nome = nome
        self.permissoes = permissoes
    
    def tem_permissao(self, permissao: Permissao) -> bool:
        """
        Verifica se este papel possui uma permissão específica
        """
        return permissao in self.permissoes
    
    def __str__(self):
        return f"Papel: {self.nome}"

class Usuario:
    """
    Classe que representa um usuário do sistema
    Cada usuário tem um nome, ID único e pode ter múltiplos papéis
    """
    def __init__(self, user_id: int, nome: str, papeis: List[Papel] = None):
        self.user_id = user_id
        self.nome = nome
        self.papeis = papeis or []
    
    def adicionar_papel(self, papel: Papel):
        """
        Adiciona um papel ao usuário
        """
        if papel not in self.papeis:
            self.papeis.append(papel)
    
    def remover_papel(self, papel: Papel):
        """
        Remove um papel do usuário
        """
        if papel in self.papeis:
            self.papeis.remove(papel)
    
    def tem_permissao(self, permissao: Permissao) -> bool:
        """
        Verifica se o usuário tem uma permissão específica
        O usuário tem a permissão se pelo menos um de seus papéis a possui
        """
        return any(papel.tem_permissao(permissao) for papel in self.papeis)
    
    def obter_todas_permissoes(self) -> Set[Permissao]:
        """
        Retorna todas as permissões que o usuário possui
        (união de todas as permissões de todos os seus papéis)
        """
        todas_permissoes = set()
        for papel in self.papeis:
            todas_permissoes.update(papel.permissoes)
        return todas_permissoes
    
    def __str__(self):
        papeis_str = ", ".join([papel.nome for papel in self.papeis])
        return f"Usuário: {self.nome} (ID: {self.user_id}) - Papéis: [{papeis_str}]"

class SistemaRBAC:
    """
    Classe principal que gerencia o sistema RBAC
    Responsável por criar e gerenciar usuários, papéis e verificar permissões
    """
    def __init__(self):
        self.usuarios: Dict[int, Usuario] = {}
        self.papeis: Dict[str, Papel] = {}
        self._inicializar_papeis()
    
    def _inicializar_papeis(self):
        """
        Inicializa os papéis padrão do sistema de biblioteca
        """
        # Papel 1: LEITOR - Usuário comum que pode apenas consultar e pegar emprestado
        leitor_permissoes = {
            Permissao.VER_LIVROS,
            Permissao.EMPRESTAR_LIVRO,
            Permissao.DEVOLVER_LIVRO
        }
        papel_leitor = Papel("Leitor", leitor_permissoes)
        
        # Papel 2: BIBLIOTECÁRIO - Pode gerenciar livros e empréstimos
        bibliotecario_permissoes = {
            Permissao.VER_LIVROS,
            Permissao.ADICIONAR_LIVRO,
            Permissao.EDITAR_LIVRO,
            Permissao.EMPRESTAR_LIVRO,
            Permissao.DEVOLVER_LIVRO,
            Permissao.VER_EMPRESTIMOS,
            Permissao.VER_USUARIOS,
            Permissao.GERAR_RELATORIOS
        }
        papel_bibliotecario = Papel("Bibliotecário", bibliotecario_permissoes)
        
        # Papel 3: ADMINISTRADOR - Acesso completo ao sistema
        admin_permissoes = set(Permissao)  # Todas as permissões
        papel_admin = Papel("Administrador", admin_permissoes)
        
        # Adiciona os papéis ao sistema
        self.papeis["Leitor"] = papel_leitor
        self.papeis["Bibliotecário"] = papel_bibliotecario
        self.papeis["Administrador"] = papel_admin
    
    def criar_usuario(self, user_id: int, nome: str, papeis_nomes: List[str] = None) -> Usuario:
        """
        Cria um novo usuário no sistema
        """
        papeis = []
        if papeis_nomes:
            for nome_papel in papeis_nomes:
                if nome_papel in self.papeis:
                    papeis.append(self.papeis[nome_papel])
                else:
                    print(f"Aviso: Papel '{nome_papel}' não encontrado")
        
        usuario = Usuario(user_id, nome, papeis)
        self.usuarios[user_id] = usuario
        return usuario
    
    def obter_usuario(self, user_id: int) -> Usuario:
        """
        Retorna um usuário pelo seu ID
        """
        return self.usuarios.get(user_id)
    
    def verificar_permissao(self, user_id: int, permissao: Permissao) -> bool:
        """
        Verifica se um usuário tem uma permissão específica
        """
        usuario = self.obter_usuario(user_id)
        if not usuario:
            return False
        return usuario.tem_permissao(permissao)
    
    def listar_papeis(self):
        """
        Lista todos os papéis disponíveis no sistema
        """
        print("\n-- PAPÉIS DISPONÍVEIS --")
        for nome_papel, papel in self.papeis.items():
            print(f"\n{papel}:")
            for permissao in papel.permissoes:
                print(f"  - {permissao.value}")
    
    def listar_usuarios(self):
        """
        Lista todos os usuários cadastrados
        """
        print("\n-- USUÁRIOS CADASTRADOS --\n")
        for usuario in self.usuarios.values():
            print(f"{usuario}")

def simular_operacoes(sistema: SistemaRBAC):
    """
    Função que simula algumas operações do sistema para demonstrar o RBAC
    """
    print("\n-- SIMULAÇÃO DE OPERAÇÕES DO SISTEMA --\n")

    operacoes = [
        (1, Permissao.VER_LIVROS, "Consultar catálogo de livros"),
        (1, Permissao.ADICIONAR_LIVRO, "Adicionar novo livro"),
        (1, Permissao.GERAR_RELATORIOS, "Gerar relatório de empréstimos"),
        
        (2, Permissao.VER_LIVROS, "Consultar catálogo de livros"),
        (2, Permissao.ADICIONAR_LIVRO, "Adicionar novo livro"),
        (2, Permissao.REMOVER_USUARIO, "Remover usuário do sistema"),
        
        (3, Permissao.VER_LIVROS, "Consultar catálogo de livros"),
        (3, Permissao.REMOVER_LIVRO, "Remover livro do acervo"),
        (3, Permissao.CONFIGURAR_SISTEMA, "Alterar configurações do sistema")
    ]
    
    for user_id, permissao, descricao in operacoes:
        usuario = sistema.obter_usuario(user_id)
        tem_permissao = sistema.verificar_permissao(user_id, permissao)
        status = "PERMITIDO" if tem_permissao else "NEGADO"
        print(f"{usuario.nome} tentando: {descricao} -> {status}")

def main():
    print("Sistema RBAC - Biblioteca")
    
    sistema = SistemaRBAC()
    sistema.listar_papeis()
    
    print("\ncriando usuários...")
    usuario1 = sistema.criar_usuario(1, "João Silva", ["Leitor"])
    sistema.criar_usuario(2, "Maria Santos", ["Bibliotecário"])
    sistema.criar_usuario(3, "Admin Root", ["Administrador"])
    sistema.criar_usuario(4, "Carlos Oliveira", ["Leitor", "Bibliotecário"])
    
    sistema.listar_usuarios()
    simular_operacoes(sistema)

    print("\n-- DEMONSTRAÇÃO DE MODIFICAÇÃO DE PAPÉIS --")

    print(f"\nAntes: \n{usuario1}")
    permissoes = usuario1.obter_todas_permissoes()
    print("Permissões:")
    for permissao in sorted(permissoes, key=lambda x: x.value):
        print(f"  - {permissao.value}")

    usuario1.adicionar_papel(sistema.papeis["Bibliotecário"])
    print(f"\nApós adicionar papel de Bibliotecário: \n{usuario1}")
    permissoes = usuario1.obter_todas_permissoes()
    print("Permissões:")
    for permissao in sorted(permissoes, key=lambda x: x.value):
        print(f"  - {permissao.value}")

if __name__ == "__main__":
    main()