import oracledb
from flask import Flask, request, jsonify


app = Flask(__name__) 


def get_connection():
    connection = oracledb.connect('rm556585/221205@oracle.fiap.com.br:1521/orcl')
    return connection

#--------------------------- Carro ------------------------
@app.route("/carros/<int:id>", methods=["GET"])
def findByIdCarro(id):


    connection = get_connection()  
    cursor = connection.cursor()  

    sql = "SELECT * FROM cha_adicionar_carro WHERE id_carro = :id_carro"
    cursor.execute(sql, {'id_carro': id})  
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return jsonify()


@app.route("/carros", methods=["GET"])
def listar_carro():
    connection = get_connection()  
    cursor = connection.cursor()   #agente que vai executar de fato o código de sql no banco de dados, através deles conseguimos funções para manipular os dados

    sql = 'SELECT * FROM cha_adicionar_carro'
    cursor.execute(sql)

    resultados = cursor.fetchall()  #captura os dados com uma lista de tuplas, porém sem os nomes das tabelas somento os valores || dados bruto do bancos de dados
    

    #Tratamento de dados: converte a lista de tuplas em uma lista de dicionários || Pegando os dados cru e fazendo a lista do formato que eu quero
    lista_carros = []
    for linha in resultados:
        carro = {
            'id': linha[0],
            'marca': linha[1],
            'modelo': linha[2],
            'ano': linha[3],
            'quilometragem': linha[4]
        }
        lista_carros.append(carro)

    cursor.close()  
    connection.close()  

    # Retornando a lista de carros em formato JSON
    return jsonify(lista_carros)

@app.route("/carros", methods=["POST"])
def insert_carro():
    # Pegando os dados enviados no corpo da requisição como JSON
    carro = request.json 
    marca = carro.get('marca') #get é usado para acessar os valores do JSON. Usar get permite retornar None se algum dos campos estiver faltando
    modelo = carro.get('modelo')
    ano = carro.get('ano')
    quilometragem = carro.get('quilometragem')

    connection = get_connection()  
    cursor = connection.cursor()   

    
    sql = 'INSERT INTO cha_adicionar_carro (marca, modelo, ano, quilometragem) VALUES (:marca, :modelo, :ano, :quilometragem)'
    cursor.execute(sql, {'marca': marca, 'modelo': modelo, 'ano': ano, 'quilometragem': quilometragem})
    connection.commit()  

    cursor.close()  
    connection.close()  

    return jsonify(carro) 

@app.route("/carros/<int:id>", methods=["PUT"])
def update_carro(id):  

    carro = request.json
    marca = carro.get('marca')
    modelo = carro.get('modelo')
    ano = carro.get('ano')
    quilometragem = carro.get('quilometragem')
    


    connection = get_connection()  
    cursor = connection.cursor()    

    sql = "UPDATE cha_adicionar_carro SET marca = :marca, modelo = :modelo, ano = :ano, quilometragem = :quilometragem WHERE id_carro = :id_carro"
    cursor.execute(sql, {
        'marca': marca, 
        'modelo': modelo, 
        'ano': ano, 
        'quilometragem': quilometragem, 
        'id_carro': id
    })
    connection.commit()

    cursor.close() 
    connection.close()

    return jsonify(carro)

@app.route("/carros/<int:id>", methods=["DELETE"])
def delete_carro(id):
    connection = get_connection()  
    cursor = connection.cursor()  

    sql = "DELETE FROM cha_adicionar_carro WHERE id_carro = :id_carro"
    cursor.execute(sql, {'id_carro': id})  
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return jsonify({'message': 'Carro deletado com sucesso'})

#--------------- Avaliação Cliente -----------------------
@app.route("/avaliacoes/<int:id>", methods=["GET"])
def listByIdAvaliacao(id):
    connection = get_connection()
    cursor = connection.cursor

    sql = "SELECT FROM cha_avaliacao_cliente WHERE id_avaliacao = :id_avaliacao"
    cursor.execute(sql, {"id_avaliacao" : id})

    cursor.close() 
    connection.close()

    return jsonify()


@app.route("/avalicaoes", methods=["GET"])
def listar_todos_avaliacao():
    connection = get_connection()
    cursor = connection.cursor() #Ele executa os comandos SQL e manipula os resultados ||  o cursor atua como intermediário entre o seu código Python e o banco de dados

    sql = "SELECT * FROM cha_avaliacao_cliente"
    cursor.execute(sql)
    resultados = cursor.fetchall()

    listas_avaliacoes = []
    for avalicao in resultados:
        avaliacaoes = {
            "id" : avaliacao[0],
            "nome_cliente" : avalicao[1],
            "avaliacao" : avalicao[2],
            "comentario" : avalicao[3]
        }
        listas_avaliacoes.append(avaliacaoes)

    cursor.close()
    connection.close()

    return jsonify(listas_avaliacoes) #converte sua lista de dicionários em um objeto JSON que pode ser retornado em uma resposta HTTP.

@app.route("/avaliacoes", methods=["POST"])
def inserir_avaliacao():
    """
    request.json extrai os dados em formato JSON enviados pelo cliente. O cliente envia um objeto 
    JSON que pode incluir muitos dados, e request.json converte isso em um dicionário Python.
    Ao receber uma requisição com um corpo JSON, request.json lê esse corpo e converte em um 
    dicionário Python. A partir daí, get() nos ajuda a pegar valores específicos desse dicionário:
    - avaliacoes.get("nome_cliente") pega o valor associado à chave nome_cliente.
    - Se nome_cliente não estiver presente no JSON, get("nome_cliente") retorna None ao invés de causar um erro.
    """
    connection = get_connection()
    cursor = connection.cursor

    avaliacoes= request.json #avaliacoes é um dicionário que contém todos os dados enviados pelo cliente.
    nome = avaliacoes.get("nome_cliente")
    avaliacao = avaliacoes.get("avaliacao")
    comentario = avaliacoes.get("comentario")

    sql = "INSERT INTO cha_avaliacao_cliente(nome_cliente, avaliacao, comentario) VALUES(:nome_cliente, :avaliacao, :comentario)"
    cursor.execute(sql, {"nome" : nome, "avaliacao" : avaliacao, "comentario" : comentario}) #executa o comando SQL com os dados fornecidos.
    connection.commit()

    cursor.close()
    connection.close()
    return jsonify(avaliacoes) #avaliacoes é o dicionário original, agora sendo retornado como JSON na resposta da API.
    """Esses dados foram enviados pelo cliente como parte do corpo da requisição HTTP em formato JSON. Portanto, quando você retorna jsonify(avaliacoes), 
    você está simplesmente devolvendo ao cliente os dados que ele enviou, confirmando que foram recebidos e processados corretamente
    """

@app.route("/avaliacoes/<int:id>", methods=["PUT"])
def update_avaliacao(id):
    avaliacoes = request.json
    nome = avaliacoes.get("nome_cliente")
    avaliacao = avaliacoes.get("avaliacao")
    comentario = avaliacoes.get("comentario")

    connection = get_connection
    cursor = connection.cursor

    sql = "UPDATE cha_avaliacao_cliente  SET nome_cliente = :nome_cliente, avaliacao = :avaliacao, comentario = comentario WHERE id_avaliacao = :id_avaliacao"
    cursor.execute(sql, {"nome" : nome, "avaliacao" : avaliacao, "comentario" : comentario, "id_avaliacao" : id})
    cursor.commit()

    cursor.close()
    connection.close()

    return jsonify(avaliacoes)

@app.route("/avaliacoes/<int:id>", methods=["DELETE"])
def delete_avaliacao(id):

    connection = get_connection
    cursor = connection.cursor

    sql = "DELETE FROM cha_avaliacao_cliente WHERE id_avaliacao = :id_avaliacao"
    cursor.execute(sql, {"id_avaliacao" : id})
    connection.commit()

    connection.close()
    cursor.close()

    return jsonify({"message" : "Carro deletado com sucesso"})


#--------------- Peca -----------------------------
@app.route("/pecas/<int:id>", methods=["DELETE"])
def findByIdPeca(id):

    connection = get_connection()
    cursor = connection.cursor()

    sql = "SELECT * FROM cha_peca  WHERE id_peca = :id_peca"
    cursor.execute(sql, {"id_peca" : id})
    connection.commit()

    connection.close()
    cursor.close()

    return jsonify()



@app.route("/pecas", methods=["GET"])
def listar_peca():

    connection = get_connection()
    cursor = connection.cursor()

    sql = "SELECT * FROM cha_peca "
    cursor.execute(sql)
    resultados = cursor.fetchall()

    lista_pecas = []
    for peca in resultados:
        pecas = {
            "id_peca" : peca[0],
            "nome_peca" : peca[1],
            "preco_peca" : peca[2]
        }
        lista_pecas.append(pecas)

    return jsonify(lista_pecas)


@app.route("/pecas", methods=["POST"])
def inserir_peca():

    pecas = request.json
    nome = pecas.get("nome_peca")
    preco = pecas.get("preco_peca")

    connection = get_connection()
    cursor = connection.cursor()

    sql = "INSERT INTO cha_peca(nome_peca, preco_peca) VALUES(?,?)"
    cursor.execute(sql, {"nome_peca" : nome, "preco_peca" : preco})

    connection.close()
    cursor.close()

    return jsonify(pecas)

@app.route("/pecas/<int:id>", methods=["PUT"])
def update_peca(id):

    pecas = request.json
    nome = pecas.get("nome_peca")
    preco = pecas.get("preco_peca")

    connection = get_connection()
    cursor = connection.cursor()

    sql = "UPDATE cha_peca SET nome_peca = :nome_peca, preco_peca = :preco_peca WHERE id_peca = :id_peca"
    cursor.execute(sql, {"nome_peca" : nome, "preco_peca" : preco, "id_peca" : id})

    connection.close()
    cursor.close()

    return jsonify(pecas)


@app.route("/pecas/<int:id>", methods=["DELETE"])
def delete_peca(id):

    connection = get_connection()
    cursor = connection.cursor()

    sql = "DELETE FROM cha_peca WHERE id_peca = :id_peca"
    cursor.execute(sql, {"id_peca" : id})
    connection.commit()

    connection.close()
    cursor.close()

    return jsonify({"message" : "Carro deletado com sucesso"})

# ---------------- Cadastro ------------------
@app.route("/usuarios/<int:id>", methods=["GET"])
def listbyIdCadastro(id):
    
    connection = get_connection()
    cursor = connection.cursor
    
    sql = "SELECT * FROM chacadastrocliente WHERE id_cliente = :id_cliente"
    cursor.execute(sql, {"id_cliente" : id})
    
    cursor.close() 
    connection.close()

    return jsonify()


@app.route("/usuarios", methods=["GET"])
def listar_cadastro():
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = "SELECT * FROM chacadastrocliente"
    cursor.execute(sql)
    
    resultados = cursor.fetchall()
    
    lista_cadastros = []
    for cadastro in resultados:
        cadastros = {
            "id_cliente" : cadastro[0],
            "nome_cliente" : cadastro[1],
            "email" : cadastro[2],
            "senha" : cadastro[3],
            "numero" : cadastro[4],
            "data_nascimento" : cadastro[5]
        }
        lista_cadastros.append(cadastro)
        
    cursor.close()  
    connection.close()  
        
    return jsonify(lista_cadastros)

@app.route("/usuarios", methods=["POST"])
def inserir_cadastro():
    
    cadastro = request.json
    nome = cadastro.get("nome_completo") #erro pode ser que não está com o mesmo nome
    email = cadastro.get("email")
    senha = cadastro.get("senha")
    numero = cadastro.get("numero")
    data = cadastro.get("data_nascimento")
    
    connection = get_connection()  
    cursor = connection.cursor()   

    sql = "INSERT INTO chacadastrocliente(nome_completo, email, senha, numero_telefone, data_nascimento) VALUES (:nome_completo, :email, :senha, :numero_telefone, :data_nascimento)"
    cursor.execute(sql, {"nome_cliente" : nome, "email" : email, "senha" : senha, "numero_telefone" : numero, "data_nascimento" : data})
    connection.commit()  

    cursor.close()  
    connection.close()  
    
    return jsonify(cadastro)

@app.route("/usuarios/<int:id>", methods=["PUT"])
def update_cadastro(id):
    
    cadastro = request.json
    nome = cadastro.get("nome_completo") #erro pode ser que não está com o mesmo nome
    email = cadastro.get("email")
    senha = cadastro.get("senha")
    numero = cadastro.get("numero")
    data = cadastro.get("data_nascimento")
    
    connection = get_connection()  
    cursor = connection.cursor()   

    sql = "UPDATE chacadastrocliente SET nome_completo = ?, email = ?, senha = ?, numero_telefone = ?, data_nascimento = ? WHERE id_cliente = :id_cliente"
    cursor(sql, {"nome_cliente" : nome, "email" : email, "senha" : senha, "numero_telefone" : numero, "data_nascimento" : data, "id_cliente" : id})
    
    connection = get_connection()  
    cursor = connection.cursor()  
    
    return jsonify(cadastro)

@app.route("/usuarios/<int:id>", methods=["DELETE"])
def delete_cadastro(id):
    
    connection = get_connection()  
    cursor = connection.cursor() 
    
    sql = "DELETE FROM chacadastrocliente  WHERE id_cliente = :id_cliente"
    cursor.execute(sql, {"id_cliente" : id})
    
    return jsonify({"message" : "Carro deletado com sucesso"})
    
    

#Principal    

app.run(debug='True')   
