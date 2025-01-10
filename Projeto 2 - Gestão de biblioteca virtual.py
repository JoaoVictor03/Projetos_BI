##### Mini projeto 2 - Gestão de uma biblioteca virtual ####
#Adicionar livros, buscar informações, remover livros, listar livros cadastrados

#Começar criando um dicionário vazio para armazenar os livros
livros = {}

#Criar função para adicionar livros
def adicionar_livro():
    isbn = input("Adicione o ISBN do livro: ")
    
    #Checar se o livro já está nesse dicionário
    if isbn in livros:
        print("\n Este livro já está na biblioteca. ")
    else:
        nome = input("Digite o nome do livro: ")
        autor = input("Digite o nome do autor: ")
        ano = input("Digite o ano do livro: ")

        #Agora, adicionar as informações na biblioteca
        livros[isbn] = {"Título: ": nome, "Autor": autor, "Ano": ano}
        print(f"Livro {nome} publicado por {autor} em {ano} adicionado com sucesso")

def achar_livro():
    isbn = input("Digite o ISBN do livro que deseja buscar: ")

    #Checar se o livro estiver na biblioteca:
    if isbn in livros:
        livro = livros[isbn]
        print("### Seguem informações do livro ###")
        
        #Iterar sobre cada uma das informações do livro
        for chave, valor in livro.items():
            print(f"{chave}: {valor}")
    
    else:
        print("Livro não encontrado")



adicionar_livro()

achar_livro()