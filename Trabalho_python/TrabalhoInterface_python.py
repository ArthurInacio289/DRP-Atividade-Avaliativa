import tkinter as tk
from tkinter import messagebox
import psycopg2

def conectar():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="SCN",
            user="postgres",
            password="postgres"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

def cadastrar_aluno():
    def salvar_aluno():
        nome = entry_nome.get()
        if nome:
            conn = conectar()
            if conn is None:
                return
            try:
                with conn.cursor() as cursor:
                    cursor.execute('INSERT INTO "alunos" ("nome") VALUES (%s) RETURNING "id"', (nome,))
                    conn.commit()
                    aluno_id = cursor.fetchone()[0]
                    messagebox.showinfo("Sucesso", f"Aluno {nome} cadastrado com sucesso! ID: {aluno_id}")
                    entry_nome.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar aluno: {e}")
            finally:
                conn.close()
        else:
            messagebox.showwarning("Atenção", "Digite o nome do aluno.")

    janela_aluno = tk.Toplevel()
    janela_aluno.title("Cadastro de Alunos")
    janela_aluno.geometry("400x250")
    janela_aluno.configure(bg="#e9f5ff")

    frame = tk.Frame(janela_aluno, bg="#ffffff", padx=20, pady=20)
    frame.pack(expand=True)

    tk.Label(frame, text="Nome do Aluno:", bg="#ffffff", font=("Arial", 12)).pack(pady=10)
    entry_nome = tk.Entry(frame, font=("Arial", 12), width=30)
    entry_nome.pack(pady=5)
    tk.Button(frame, text="Cadastrar", command=salvar_aluno, bg="#007bff", fg="white", font=("Arial", 12)).pack(pady=10)

def cadastrar_nota():
    def salvar_nota():
        nome_aluno = entry_nome_aluno.get()
        nota = entry_nota.get()
        
        if nome_aluno and nota:
            try:
                nota_float = float(nota)
                if 0 <= nota_float <= 10:
                    conn = conectar()
                    if conn is None:
                        return
                    
                    with conn.cursor() as cursor:
                        cursor.execute('SELECT "id" FROM "alunos" WHERE "nome" = %s LIMIT 1', (nome_aluno,))
                        aluno = cursor.fetchone()
                        
                        if aluno:
                            id_aluno = aluno[0]
                            cursor.execute('INSERT INTO "notas" ("idaluno", "nota") VALUES (%s, %s)', (id_aluno, nota_float))
                            conn.commit()
                            messagebox.showinfo("Sucesso", f"Nota {nota_float} cadastrada com sucesso para o aluno {nome_aluno}!")
                            entry_nome_aluno.delete(0, tk.END)
                            entry_nota.delete(0, tk.END)
                        else:
                            messagebox.showwarning("Atenção", "Aluno não encontrado. Verifique o nome e tente novamente.")
            
            except ValueError:
                messagebox.showwarning("Atenção", "Digite uma nota válida.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar nota: {e}")
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    janela_nota = tk.Toplevel()
    janela_nota.title("Cadastro de Notas")
    janela_nota.geometry("400x300")
    janela_nota.configure(bg="#e9f5ff")

    frame = tk.Frame(janela_nota, bg="#ffffff", padx=20, pady=20)
    frame.pack(expand=True)

    tk.Label(frame, text="Nome do Aluno:", bg="#ffffff", font=("Arial", 12)).pack(pady=10)
    entry_nome_aluno = tk.Entry(frame, font=("Arial", 12), width=30)
    entry_nome_aluno.pack(pady=5)

    tk.Label(frame, text="Nota:", bg="#ffffff", font=("Arial", 12)).pack(pady=10)
    entry_nota = tk.Entry(frame, font=("Arial", 12), width=30)
    entry_nota.pack(pady=5)

    tk.Button(frame, text="Cadastrar Nota", command=salvar_nota, bg="#007bff", fg="white", font=("Arial", 12)).pack(pady=10)

def consultar_notas():
    def buscar_notas():
        pesquisa = entry_pesquisa.get()
        if pesquisa:
            conn = conectar()
            if conn is None:
                return
            try:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT "id", "nome" FROM "alunos" WHERE "nome" ILIKE %s', (f'%{pesquisa}%',))
                    alunos = cursor.fetchall()
                    if alunos:
                        resultado = ""
                        for aluno in alunos:
                            cursor.execute('SELECT "nota" FROM "notas" WHERE "idaluno" = %s', (aluno[0],))
                            notas = cursor.fetchall()
                            notas_str = ', '.join([str(n[0]) for n in notas]) if notas else "Sem notas"
                            resultado += f"{aluno[1]} (ID: {aluno[0]}): {notas_str}\n"
                        messagebox.showinfo("Notas", resultado)
                    else:
                        messagebox.showwarning("Atenção", "Nenhum aluno encontrado com esse nome.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao consultar notas: {e}")
            finally:
                conn.close()
        else:
            messagebox.showwarning("Atenção", "Digite o nome do aluno.")

    janela_consulta = tk.Toplevel()
    janela_consulta.title("Consulta de Notas")
    janela_consulta.geometry("400x250")
    janela_consulta.configure(bg="#e9f5ff")

    frame = tk.Frame(janela_consulta, bg="#ffffff", padx=20, pady=20)
    frame.pack(expand=True)

    tk.Label(frame, text="Nome do Aluno:", bg="#ffffff", font=("Arial", 12)).pack(pady=10)
    entry_pesquisa = tk.Entry(frame, font=("Arial", 12), width=30)
    entry_pesquisa.pack(pady=5)
    tk.Button(frame, text="Consultar", command=buscar_notas, bg="#007bff", fg="white", font=("Arial", 12)).pack(pady=10)

janela = tk.Tk()
janela.title("Sistema de Cadastro de Notas")
janela.geometry("400x350")
janela.configure(bg="#e9f5ff")

frame_principal = tk.Frame(janela, bg="#ffffff", padx=20, pady=20)
frame_principal.pack(expand=True)

tk.Label(frame_principal, text="Sistema de Cadastro de Notas", font=("Arial", 18, "bold"), bg="#ffffff").pack(pady=10)
tk.Label(frame_principal, text="Gerencie alunos e suas notas", font=("Arial", 12), bg="#ffffff").pack(pady=5)

tk.Button(frame_principal, text="1. Cadastrar Aluno", command=cadastrar_aluno, bg="#007bff", fg="white", font=("Arial", 12)).pack(pady=10)
tk.Button(frame_principal, text="2. Cadastrar Nota", command=cadastrar_nota, bg="#007bff", fg="white", font=("Arial", 12)).pack(pady=10)
tk.Button(frame_principal, text="3. Consultar Notas", command=consultar_notas, bg="#007bff", fg="white", font=("Arial", 12)).pack(pady=10)

janela.mainloop()
