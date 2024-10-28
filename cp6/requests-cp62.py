import requests

def menu():
    opcao = -1 #para não entrar em outras opções 
    while opcao >= 1 or opcao <= 5:
        print('--------------------------------------------------------------------------------------------------------------------')
        print('[ 1 ] - Visualizar somente as marcas disponíveis na API pública.')
        print('[ 2 ] - Visualizar marcas e modelos dessa marca.')
        print('[ 3 ] - Visualizar marcas, modelos e anos disponíveis.')
        print('[ 4 ] - Visualizar todas as informações de uma marca e modelo específicos.')
        print('[ 5 ] - Sair da operação')
        
        try:
            opcao = int(input('Digite uma opção: ')) #usuário irá escolher uma opção do print
            if (opcao < 1) or (opcao > 5): # se o usuário escolhe um opção inválida irá retorna para a pergunta
                print('Opção inválida. Escolha um número do MENU')
            else: 
                return opcao # irá retorna a opção que o usuário escolheu
        except ValueError:
            print('Entrada inválida (somente números) você pode digitar. Por favor, digite um número entre 1 a 9.')    
        except  Exception as e:
            print(f'Ocorreu um erro: {e}')

def fazer_requisicao(url):
    try:
        requisicao = requests.get(url)
        json_requisicao = requisicao.json()
        return json_requisicao

    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")
    except Exception as e:
        print(f"Erro: {e}")
        

# Função para obter a lista de marcas
def obter_marcas():
    url = "https://parallelum.com.br/fipe/api/v1/carros/marcas"
    marcas = fazer_requisicao(url)

    if marcas:
        for marca in marcas:
            print(f"Código: {marca['codigo']}, Marca: {marca['nome']}")
    return marcas #retornanda a lista de marcas

# Função para selecionar a marca e obter modelos
def obter_modelos(codigo_marca):
    url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_marca}/modelos"
    modelos = fazer_requisicao(url)

    if modelos:
        for modelo in modelos:
            print(f"Código: {modelo['codigo']}, Modelo: {modelo['nome']}")
    return modelos

# Função para obter os anos do modelo escolhido
def obter_anos(codigo_marca, codigo_modelo):
    url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos"
    anos = fazer_requisicao(url)

    if anos:
        for ano in anos:
            print(f"Código: {ano['codigo']}, Ano: {ano['nome']}\n")
            
    return anos

# Função para obter o valor do carro
def obter_valor(codigo_marca, codigo_modelo, codigo_ano):
    url = f"https://parallelum.com.br/fipe/api/v1/carros/marcas/{codigo_marca}/modelos/{codigo_modelo}/anos/{codigo_ano}"
    valor_carro = fazer_requisicao(url)

    if valor_carro:
        # manipulação do arquivo json (dicionário)
        tipo_veiculo = valor_carro['TipoVeiculo']
        valor = valor_carro['Valor']
        combustivel = valor_carro['Combustivel']
        codigo_fipe = valor_carro['CodigoFipe']
        sigla_combustivel = valor_carro['SiglaCombustivel']

        print(f"Tipo do veículo: {tipo_veiculo}")
        print(f"Valor: {valor}")
        print(f"Marca: {codigo_marca}")
        print(f"Modelo: {codigo_modelo}")
        print(f"Ano: {codigo_ano}")
        print(f"Combustível: {combustivel}")
        print(f"Código Fipe: {codigo_fipe}")
        print(f"Sigla combustível: {sigla_combustivel}")

# Fluxo principal do programa
def main():

    while True:
        opcao = menu()

        if opcao == 1:
            obter_marcas()
        
        elif opcao == 2:
            marcas = obter_marcas()
            if marcas:
                codigo_marca = input("Digite o CÓDIGO da marca do carro: ")

                obter_modelos(codigo_marca)
                
        elif opcao == 3:
            marcas = obter_marcas()
            if marcas:
                codigo_marca = input("Digite o CÓDIGO da marca do carro: ")   

                modelos = obter_modelos(codigo_marca)
                if modelos:
                    codigo_modelo = input("Digite o CÓDIGO do modelo de carro: ")

                    obter_anos(codigo_marca, codigo_modelo)

        elif opcao == 4:
            marcas = obter_marcas()
            if marcas:
                codigo_marca = input("Digite o CÓDIGO da marca do carro: ")

                modelos = obter_modelos(codigo_marca)
                if modelos:
                    codigo_modelo = input("Digite o CÓDIGO do modelo de carro: ")

                    anos = obter_anos(codigo_marca, codigo_modelo)
                    if anos:
                        codigo_ano = input("Digite o CÓDIGO do ano do carro: ")

                        obter_valor(codigo_marca, codigo_modelo, codigo_ano)
#Principal
main()
