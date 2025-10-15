import json
import os
from datetime import datetime
from uuid import uuid4

# --- Constantes ---
ARQUIVO_DADOS = "dados_estoque.json"

# --- Classes do Core do Sistema ---

class Produto:
    """Representa um produto no sistema de estoque."""
    def __init__(self, codigo, nome, descricao, quantidade_inicial=0, estoque_maximo=100):
        if not all([codigo, nome]):
            raise ValueError("Código e Nome são campos obrigatórios.")
        if quantidade_inicial < 0 or estoque_maximo <= 0:
            raise ValueError("Quantidade inicial e estoque máximo devem ser positivos.")
            
        self.codigo = codigo
        self.nome = nome
        self.descricao = descricao
        self.quantidade = quantidade_inicial
        self.estoque_maximo = estoque_maximo
        self.data_criacao = datetime.now().isoformat()
        self.ultima_atualizacao = self.data_criacao

    def atualizar_quantidade(self, quantidade_para_adicionar):
        """Atualiza a quantidade em estoque, positiva para entrada, negativa para saída."""
        nova_quantidade = self.quantidade + quantidade_para_adicionar
        if nova_quantidade < 0:
            raise ValueError(f"Não há estoque suficiente para a saída de {abs(quantidade_para_adicionar)} unidades do produto '{self.nome}'.")
        if nova_quantidade > self.estoque_maximo:
            raise ValueError(f"Estoque máximo de {self.estoque_maximo} para o produto '{self.nome}' foi excedido.")
            
        self.quantidade = nova_quantidade
        self.ultima_atualizacao = datetime.now().isoformat()
        return True

    def to_dict(self):
        """Converte o objeto Produto para um dicionário serializável."""
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        """Cria uma instância de Produto a partir de um dicionário."""
        produto = cls(data['codigo'], data['nome'], data['descricao'])
        produto.__dict__.update(data)
        return produto

class Movimentacao:
    """Representa uma movimentação de entrada ou saída de estoque."""
    def __init__(self, codigo_produto, tipo, quantidade, motivo=""):
        if tipo not in ["entrada", "saida"]:
            raise ValueError("Tipo de movimentação deve ser 'entrada' ou 'saida'.")
        if quantidade <= 0:
            raise ValueError("Quantidade da movimentação deve ser positiva.")

        self.id_movimentacao = str(uuid4())
        self.codigo_produto = codigo_produto
        self.tipo = tipo
        self.quantidade = quantidade
        self.motivo = motivo
        self.data_movimentacao = datetime.now().isoformat()

    def to_dict(self):
        """Converte o objeto Movimentacao para um dicionário serializável."""
        return self.__dict__

class Estoque:
    """Gerencia o conjunto de produtos e suas movimentações."""
    def __init__(self):
        self.produtos = {}  # {codigo: objeto_produto}
        self.historico_movimentacoes = []

    def adicionar_produto(self, produto):
        """Adiciona um novo produto ao estoque."""
        if produto.codigo in self.produtos:
            raise ValueError(f"Produto com código '{produto.codigo}' já existe.")
        self.produtos[produto.codigo] = produto
        print(f"\n✅ Produto '{produto.nome}' adicionado com sucesso!")

    def registrar_movimentacao(self, codigo_produto, tipo, quantidade, motivo=""):
        """Registra uma entrada ou saída e atualiza a quantidade do produto."""
        if codigo_produto not in self.produtos:
            raise ValueError(f"Produto com código '{codigo_produto}' não encontrado.")

        produto = self.produtos[codigo_produto]
        quantidade_ajustada = quantidade if tipo == 'entrada' else -quantidade

        produto.atualizar_quantidade(quantidade_ajustada)
        
        movimentacao = Movimentacao(codigo_produto, tipo, quantidade, motivo)
        self.historico_movimentacoes.append(movimentacao)
        print(f"\n✅ Movimentação de {tipo} para o produto '{produto.nome}' registrada com sucesso.")

    def consultar_produto(self, codigo_produto):
        """Retorna os detalhes de um produto específico."""
        return self.produtos.get(codigo_produto)

    def gerar_relatorio_estoque(self):
        """Imprime um relatório do estado atual de todos os produtos."""
        print("\n--- Relatório de Estoque Atual ---")
        if not self.produtos:
            print("Nenhum produto cadastrado.")
            return

        print(f"{'Código':<15} | {'Nome':<25} | {'Quantidade':<12} | {'Ocupação':<15} | {'Estoque Máximo':<15}")
        print("-" * 85)
        for produto in self.produtos.values():
            ocupacao_percent = (produto.quantidade / produto.estoque_maximo) * 100
            print(f"{produto.codigo:<15} | {produto.nome:<25} | {produto.quantidade:<12} | {ocupacao_percent:,.2f}%{'':<11} | {produto.estoque_maximo:<15}")
        print("-" * 85)

    def gerar_relatorio_movimentacoes(self, codigo_produto=None):
        """Imprime o histórico de movimentações, opcionalmente filtrado por produto."""
        print("\n--- Histórico de Movimentações ---")
        movimentacoes = self.historico_movimentacoes
        if codigo_produto:
            if codigo_produto not in self.produtos:
                print(f"Produto com código '{codigo_produto}' não encontrado.")
                return
            movimentacoes = [m for m in self.historico_movimentacoes if m.codigo_produto == codigo_produto]
            print(f"Filtrando por produto: {self.produtos[codigo_produto].nome}\n")

        if not movimentacoes:
            print("Nenhuma movimentação registrada.")
            return
            
        print(f"{'Data/Hora':<28} | {'Cód. Produto':<15} | {'Tipo':<10} | {'Quantidade':<12} | {'Motivo'}")
        print("-" * 90)
        for m in sorted(movimentacoes, key=lambda x: x.data_movimentacao, reverse=True):
            data_formatada = datetime.fromisoformat(m.data_movimentacao).strftime('%d-%m-%Y %H:%M:%S')
            print(f"{data_formatada:<28} | {m.codigo_produto:<15} | {m.tipo.capitalize():<10} | {m.quantidade:<12} | {m.motivo}")
        print("-" * 90)

    def calcular_ocupacao_total(self):
        """Calcula e exibe a ocupação total do armazém."""
        if not self.produtos:
            print("\nEstoque vazio. A ocupação é 0%.")
            return
            
        total_armazenado = sum(p.quantidade for p in self.produtos.values())
        capacidade_total = sum(p.estoque_maximo for p in self.produtos.values())
        
        ocupacao_geral = (total_armazenado / capacidade_total) * 100 if capacidade_total > 0 else 0
        
        print("\n--- Ocupação Geral do Estoque ---")
        print(f"Total de itens armazenados: {total_armazenado}")
        print(f"Capacidade total de armazenamento: {capacidade_total}")
        print(f"Taxa de ocupação geral: {ocupacao_geral:.2f}%")
        print("---------------------------------")
        
    def to_dict(self):
        """Converte todo o objeto Estoque para um dicionário."""
        return {
            'produtos': {code: p.to_dict() for code, p in self.produtos.items()},
            'historico_movimentacoes': [m.to_dict() for m in self.historico_movimentacoes]
        }

    @classmethod
    def from_dict(cls, data):
        """Cria uma instância de Estoque a partir de um dicionário."""
        estoque = cls()
        for codigo, prod_data in data.get('produtos', {}).items():
            estoque.produtos[codigo] = Produto.from_dict(prod_data)
        
        mov_data = data.get('historico_movimentacoes', [])
        for mov in mov_data:
            movimentacao = Movimentacao(mov['codigo_produto'], mov['tipo'], mov['quantidade'], mov['motivo'])
            movimentacao.__dict__.update(mov)
            estoque.historico_movimentacoes.append(movimentacao)
            
        return estoque

# --- Funções de Persistência ---

def salvar_dados(estoque):
    """Salva o estado atual do estoque em um arquivo JSON."""
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(estoque.to_dict(), f, indent=4, ensure_ascii=False)
    print("\n💾 Dados do estoque salvos com sucesso!")

def carregar_dados():
    """Carrega os dados do estoque de um arquivo JSON. Se não existir, cria um novo."""
    if not os.path.exists(ARQUIVO_DADOS):
        return Estoque()
    try:
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            return Estoque.from_dict(dados)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Arquivo de dados corrompido ou não encontrado. Iniciando um novo estoque.")
        return Estoque()

# --- Interface de Linha de Comando (CLI) ---

def limpar_tela():
    """Limpa o terminal para melhorar a legibilidade."""
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_principal():
    """Exibe o menu principal e retorna a escolha do usuário."""
    print("\n===== Sistema de Gestão de Estoque =====")
    print("1. Adicionar Novo Produto")
    print("2. Registrar Entrada de Produto")
    print("3. Registrar Saída de Produto")
    print("4. Relatório de Estoque Atual")
    print("5. Histórico de Movimentações")
    print("6. Consultar Ocupação Geral do Estoque")
    print("7. Salvar e Sair")
    print("========================================")
    return input("Escolha uma opção: ")

def main():
    """Função principal que executa o loop do programa."""
    estoque = carregar_dados()
    print("Bem-vindo ao Sistema de Gestão de Estoque!")
    
    while True:
        escolha = menu_principal()
        limpar_tela()
        
        try:
            if escolha == '1':
                print("--- Adicionar Novo Produto ---")
                codigo = input("Código do produto: ")
                nome = input("Nome do produto: ")
                descricao = input("Descrição: ")
                estoque_maximo = int(input("Capacidade máxima de estoque: "))
                novo_produto = Produto(codigo, nome, descricao, estoque_maximo=estoque_maximo)
                estoque.adicionar_produto(novo_produto)
                
            elif escolha == '2':
                print("--- Registrar Entrada de Produto ---")
                codigo = input("Código do produto: ")
                quantidade = int(input("Quantidade de entrada: "))
                motivo = input("Motivo (ex: Compra, Devolução): ")
                estoque.registrar_movimentacao(codigo, 'entrada', quantidade, motivo)

            elif escolha == '3':
                print("--- Registrar Saída de Produto ---")
                codigo = input("Código do produto: ")
                quantidade = int(input("Quantidade de saída: "))
                motivo = input("Motivo (ex: Venda, Perda): ")
                estoque.registrar_movimentacao(codigo, 'saida', quantidade, motivo)
                
            elif escolha == '4':
                estoque.gerar_relatorio_estoque()

            elif escolha == '5':
                codigo_filtro = input("Digite o código do produto para filtrar ou deixe em branco para ver tudo: ")
                estoque.gerar_relatorio_movimentacoes(codigo_filtro if codigo_filtro else None)

            elif escolha == '6':
                estoque.calcular_ocupacao_total()

            elif escolha == '7':
                salvar_dados(estoque)
                print("\nObrigado por usar o sistema. Até logo!\n")
                break
                
            else:
                print("\n❌ Opção inválida! Por favor, tente novamente.")
                
        except (ValueError, TypeError) as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Ocorreu um erro inesperado: {e}")

        input("\nPressione Enter para continuar...")
        limpar_tela()

# --- Ponto de Entrada do Programa ---
if __name__ == "__main__":
    main()