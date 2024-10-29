import requests
import json


def menu():
    opcao = -1 #para não entrar em outras opções 
    while opcao >= 1 or opcao <= 6:
        print("------- Menu de CRUD -----")
        print("1. Listar todos os carros")
        print("2. Inserir um carro")
        print("3. Atualizar um carro")
        print("4. Deletar um carro")
        print("5. Exportar dados para JSON")
        print("6. Sair")
        
        try:
            opcao = int(input('Digite uma opção: ')) 
            if (opcao < 1) or (opcao > 10): 
                print('Opção inválida. Escolha um número do MENU')
            else: 
                return opcao 
        except ValueError:
            print('Entrada inválida (somente números) você pode digitar. Por favor, digite um número entre 1 a 9.')    
        except  Exception as e:
            print(f'Ocorreu um erro: {e}')

def listar_todos():
    response = requests.get('http://localhost:5000/carros')
    data = response.json()
    for carro in data:
        print(json.dumps(carro, indent=4, ensure_ascii=False))
    return data


def perguntas_inserir():
    marca = input("Digite a marca: ")
    modelo = input("Digite o modelo: ")
    ano = int(input("Digite o ano do carro: "))
    quilometragem = float(input("Digite a quilometragem do seu carro: "))
    return marca, modelo, ano, quilometragem

def inserir(marca, modelo, ano, quilometragem):
    carro = {
        "marca": marca,
        "modelo": modelo,
        "ano": ano,
        "quilometragem": quilometragem
    }
    response = requests.post('http://localhost:5000/carros', json=carro)
    print(response.json())

def perguntas_atualizar():
    id_carro = input("Digite o ID do carro que você deseja atualizar: ")
    marca_nova = input("Digite a nova marca ou a antiga: ")
    modelo_nova = input("Digite o novo modelo ou a antiga: ")
    ano_nova = int(input("Digite o novo ano do carro ou a antiga: "))
    quilometragem_nova = float(input("Digite a nova quilometragem do seu carro ou a antiga: "))
    return id_carro, marca_nova, modelo_nova, ano_nova, quilometragem_nova

def update(id_carro, marca_nova, modelo_nova, ano_nova, quilometragem_nova):
    carro = {
        "marca": marca_nova,
        "modelo": modelo_nova,
        "ano": ano_nova,
        "quilometragem": quilometragem_nova
    }
    response = requests.put(f'http://localhost:5000/carros/{id_carro}', json=carro)
    print(response.json())

def deletar():
    id_carro = input("ID do carro: ")

    response = requests.delete(f'http://localhost:5000/carros/{id_carro}')
    print(response.json())    

def exportar_dados():
    dados = listar_todos()
    with open('carros.json', 'w') as f:
        json.dump(dados, f)
    print("Dados exportados para carros.json")    

#----------------------------- Avaliacao ------------------------



def main():
    while True:
        opcao = menu()
        if opcao == 1:
            listar_todos()
        elif opcao == 2:
            marca, modelo, ano, quilometragem = perguntas_inserir()
            inserir(marca, modelo, ano, quilometragem)
        elif opcao == 3:
            id_carro, marca_nova, modelo_nova, ano_nova, quilometragem_nova = perguntas_atualizar()
            update(id_carro, marca_nova, modelo_nova, ano_nova, quilometragem_nova)
        elif opcao == 4:
            deletar()
        elif opcao == 5:
            exportar_dados()
        elif opcao == 6:
            print("Fim do programa")
            break
        else:
            print("Opção inválida")







#Principal
main()