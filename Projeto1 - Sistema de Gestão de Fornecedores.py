# Projeto 1 - Teste de sistema de gestão de fornecedores
# Cada fornecedor possui algumas informações (Categoria, tamanho)


#Podemos iniciar criando um dicionário contendo os nomes dos fornecedores

fornecedores = {
    "FerramentesGerais": {
        "Categoria": "Ferramentas", 
        "Porte": "Grande"
        },
    "Serviços Brasil":{
        "Categoria":"Manuteção",
        "Porte": "Médio"}
}

#Definir uma função que irá permitir que o usuário adicione novos fornecedores à essa lista
def adicionar_fornecedor(fornecedores):
    nome_empresa = input("\n Escreva o nome da nova empresa: ")
    categoria = input("Digite a categoria que essa empresa se enquadra: ")
    porte = input("Digite o porte dessa empresa: ")

    #Adicionar as informações ao dicionário já existente
    fornecedores[nome_empresa] = {"Categoria": categoria, "Porte": porte}
    print("\n Fornecedor adicionado com sucesso da base de dados!")


    #Exibir o dicionário com os fornecedores atualizado
    for fornecedor, informacao in fornecedores.items():
        print(f"\n{fornecedor}: {informacao}")
    print("\n Obrigado!")


print("######################### Seja Bem Vindo ao mini sistema de gestão de Fornecedores ##################################")
print("\n A lista de atual de fornecedores é a seguinte: ", fornecedores)

#Checar se o usuário deseja incluir uma nova empresa
adicionar = input("\n Você deseja adicionar uma nova empresa à base de dados(s/n)? ")

if adicionar == "s":
    adicionar_fornecedor(fornecedores)
else:
    print("\n Obrigado! \n")