# Projeto 1 - Teste de sistema de gestão de fornecedores
# Cada fornecedor possui algumas informações (Categoria, tamanho)


#Podemos iniciar criando um dicionário contendo os nomes dos fornecedores

fornecedores = {
    "Fornecedor1": {
        "Nome": "Ferramentas Gerais",
        "Categoria": "Ferramentas", 
        "Porte": "Grande"
        },
    "Fornecedor2":{
        "Nome": "Serviços Brasil",
        "Categoria":"Manuteção",
        "Porte": "Médio"}
}

#Definir uma função que irá permitir que o usuário adicione novos fornecedores à essa lista
def adicionar_fornecedor(fornecedores):
    id_fornecedor = input("\n Escreva o id da nova empresa: ")

    #Checar se o fornecedor já está na base
    if id_fornecedor in fornecedores:
        print("\n Ops, esta empresa já está cadastrada! ")
    
    #Caso não esteja cadastrada, aí sim o usuário irá digitar os dados da empresa:
    else:
        nome = input("Digite o nome da empresa: ")
        categoria = input("Digite a categoria da empresa: ")
        porte = input("Digite o porte da empresa: ")

        #Agora que o usuário já digitou os nomes, adicionar as informações no dicionário usando como base a chave primária
        fornecedores[id_fornecedor] = {"Nome": nome, "Categoria": categoria, "Porte": porte}
        print(f"\nFornecedor {nome} de categoria {categoria} e porte {porte} adicionado na base!")

        #Imprimir a lista atual de fornecedores
        fornecedor = fornecedores[id_fornecedor]
        for chave, valor in fornecedor.items():
            print(f"{chave}: {valor}")

print("######################### Seja Bem Vindo ao mini sistema de gestão de Fornecedores ##################################")
print("\n A lista de atual de fornecedores é a seguinte: ", fornecedores)

#Checar se o usuário deseja incluir uma nova empresa
adicionar = input("\n Você deseja adicionar uma nova empresa à base de dados(s/n)? ")

if adicionar == "s":
    adicionar_fornecedor(fornecedores)
else:
    print("\n Obrigado! \n")