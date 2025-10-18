faturamento = 1000
custo = 199.99 #float

imposto = 0.15 * faturamento  #float
lucro = faturamento - custo - imposto
print("Faturamento:", faturamento)
print("custo:", custo)
print("Lucro", faturamento - custo - imposto)
print("Imposto: ", imposto)

# int = números inteiros
# float = números com cacas decimais
# strings = textos e cadeias de caracteres
# boolean = True or false

mensagem = "Olá, o faturamento da loja foi de 1000"

margem_lucro = lucro / faturamento

print("Margem de Lucro: ", margem_lucro)