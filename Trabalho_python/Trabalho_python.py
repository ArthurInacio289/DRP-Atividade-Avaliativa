# coding=windows-1252
import psycopg2

def conectar():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="TrabalhoPython",
            user="postgres",
            password="postgres"
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def cadastrar_aluno(nome):
    conn = conectar()
    if conn is None:
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO "alunos" ("nome") VALUES (%s) RETURNING "id"', (nome,))
            conn.commit()
            aluno_id = cursor.fetchone()[0]
            print(f"Aluno {nome} cadastrado com sucesso! ID: {aluno_id}")
    except Exception as e:
        print(f"Erro ao cadastrar aluno: {e}")
    finally:
        conn.close()

def cadastrar_nota(id_aluno, nota):
    conn = conectar()
    if conn is None:
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO "notas" ("idaluno", "nota") VALUES (%s, %s)', (id_aluno, nota))
            conn.commit()
            print(f"Nota {nota} cadastrada com sucesso para o aluno de ID {id_aluno}!")
    except Exception as e:
        print(f"Erro ao cadastrar nota: {e}")
    finally:
        conn.close()
def consultar_notas(id_aluno):
    conn = conectar()
    if conn is None:
        return 

    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT "nota" FROM "notas" WHERE "idaluno" = %s', (id_aluno,))
            notas = cursor.fetchall()
            cursor.execute('SELECT "nome" FROM "alunos" WHERE "id" = %s',(id_aluno,))
            nome_aluno = cursor.fetchone()[0]
            if not notas or not nome_aluno:                
                print(f"Nenhuma nota encontrada para o aluno {id_aluno} ou o aluno não foi cadastrado.")
            else:                
                print(f"Notas do aluno {nome_aluno}: {', '.join([str(n[0]) for n in notas])}")
                
    except Exception as e:
        print(f"Erro ao consultar notas: {e}")
    finally:
        conn.close()

def listar_alunos():
    conn = conectar()
    if conn is None:
        return []

    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT "id", "nome" FROM "alunos"')
            alunos = cursor.fetchall()
            return alunos
    except Exception as e:
        print(f"Erro ao listar alunos: {e}")
        return []
    finally:
        conn.close()

def menu():
    while True:
        print("\n---- Sistema de Cadastro de Notas ----")
        print("1. Cadastrar Aluno")
        print("2. Cadastrar Nota para Aluno")
        print("3. Consultar Notas de Aluno")
        print("4. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Digite o nome do aluno: ")
            cadastrar_aluno(nome)

        elif opcao == "2":
            alunos = listar_alunos()
            if not alunos:
                print("Nenhum aluno cadastrado.")
            else:
                print("\nAlunos cadastrados:")
                for aluno in alunos:
                    print(f"{aluno[0]} - {aluno[1]}")
                id_aluno = input("Digite o ID do aluno para inserir a nota: ")
                nota = float(input("Digite a nota: "))
                if nota > 10 or nota < 0:
                    print ("A nota precisa ser menor ou igual a 10 e maior ou igual a 0!")
                else:
                    cadastrar_nota(id_aluno, nota)

        elif opcao == "3":
            alunos = listar_alunos()
            if not alunos:
                print("Nenhum aluno cadastrado.")
            else:
                print("\nAlunos cadastrados:")
                for aluno in alunos:
                    print(f"{aluno[0]} - {aluno[1]}")
                id_aluno = input("Digite o ID do aluno para consultar as notas: ")
                consultar_notas(id_aluno)

        elif opcao == "4":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()