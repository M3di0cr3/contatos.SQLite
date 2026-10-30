import sqlite3

def conexao_banco():
    conexao = sqlite3.connect("contatos.db")

    cursor = conexao.cursor()

    sql = """
    CREATE TABLE IF NOT EXISTS contatos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT NOT NULL,
        email TEXT NOT NULL
    )"""

    conexao.execute(sql)
    return conexao
    

def adicionar_contato(nome, telefone, email):
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = '''
    INSERT INTO contatos (nome, telefone, email)
    VALUES (?, ?, ?)'''
    cursor.execute(sql, (nome, telefone, email))
    conexao.commit()
    conexao.close()
def listar_contatos():
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = """
    SELECT * FROM contatos
    """
    cursor.execute(sql)
    contatos = cursor.fetchall()
    conexao.close()

    if len(contatos) == 0:
        print("Nenhum contato encontrado.")
    else:
        print("### LISTA DE CONTATOS ###")
        print("ID | Nome | Telefone | Email")
        for contato in contatos:
            print(f"{contato[0]:<50}| {contato[1]:<20} | {contato[2]:<15} | {contato[3]:<30}")
def buscar_contato():
    conexao = conexao_banco()
    cursor = conexao.cursor()
    contato_name = input("Digite o nome do contato que deseja buscar: ")
    sql = """
    SELECT * FROM contatos WHERE nome LIKE ?
    """
    cursor.execute(sql, ('%' + contato_name + '%',))
    contatos = cursor.fetchall()
    print("### RESULTADO DA BUSCA ###")
    if len(contatos) == 0:
        print("Nenhum contato encontrado.")
    else:
        print("ID | Nome | Telefone | Email")
        for contato in contatos:
            print(f"{contato[0]:<50}| {contato[1]:<20} | {contato[2]:<15} | {contato[3]:<30}")
    conexao.close()
def atualizar_contato():    
    conexao = conexao_banco()
    cursor = conexao.cursor()
    contato_name = input("Digite o nome do contato que deseja atualizar: ")
    sql = """
    SELECT * FROM contatos WHERE nome LIKE ?
    """
    cursor.execute(sql, ('%' + contato_name + '%',))
    contato = cursor.fetchone()
    if len(contato) == 0:
        print("Contato não encontrado.")
        return
    else:
        print("Contato encontrado:")
        print(f"ID: {contato[0]}")
        print(f"Nome: {contato[1]}")
        print(f"Telefone: {contato[2]}")
        print(f"Email: {contato[3]}")
        novo_nome = input("Digite o novo nome do contato (ou pressione Enter para manter o mesmo): ")
        novo_telefone = input("Digite o novo telefone do contato (ou pressione Enter para manter o mesmo): ")
        novo_email = input("Digite o novo email do contato (ou pressione Enter para manter o mesmo): ")
        if novo_nome == "":
            novo_nome = contato[1]
        if novo_telefone == "":
            novo_telefone = contato[2]
        if novo_email == "":
            novo_email = contato[3]
        sql = """
        UPDATE contatos SET nome = ?, telefone = ?, email = ? WHERE id = ?
        """
        cursor.execute(sql, (novo_nome, novo_telefone, novo_email, contato[0]))
        conexao.commit()
        print("Contato atualizado com sucesso!")
        conexao.close()
def remover_contato():
    conexao = conexao_banco()
    cursor = conexao.cursor()
    contato_name = input("Digite o nome do contato que deseja remover: ")
    sql = """
    SELECT * FROM contatos WHERE nome LIKE ?
    """
    cursor.execute(sql, ('%' + contato_name + '%',))
    contato = cursor.fetchone()
    if contato is None:
        print("Contato não encontrado.")
        return
    else:
        print("Contato encontrado:")
        print(f"ID: {contato[0]}")
        print(f"Nome: {contato[1]}")
        print(f"Telefone: {contato[2]}")
        print(f"Email: {contato[3]}")
        confirmacao = input("Tem certeza que deseja remover este contato? (s/n): ")
        if confirmacao.lower() == "s":
            sql = """
            DELETE FROM contatos WHERE id = ?
            """
            cursor.execute(sql, (contato[0],))
            conexao.commit()
            print("Contato removido com sucesso!")
            conexao.close()
        else:
            print("Remoção cancelada.")
            conexao.close()


    print("Função para atualizar contato ainda não implementada.")

def menu():

    while True:

        print ("### CONTATOS ###")
        print ("1. Adicionar contato")
        print ("2. Listar contatos")
        print ("3. Buscar contato")
        print ("4. Atualizar contato")
        print ("5. Remover contato")
        print ("0. Sair")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            nome = input("Digite o nome do contato: ")
            telefone = input("Digite o telefone do contato: ")
            email = input("Digite o email do contato: ")
            adicionar_contato(nome, telefone, email)
            print("Contato adicionado com sucesso!")
        elif opcao == "2":
            listar_contatos()
        elif opcao == "3":
            buscar_contato()
        elif opcao == "4":
            atualizar_contato()
        elif opcao == "5":
            remover_contato()
        elif opcao == "0":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()
