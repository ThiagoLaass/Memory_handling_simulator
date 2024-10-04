import tkinter as tk
from tkinter import messagebox
import time
import threading

class Processo:
    def __init__(self, nome, tempo_execucao, chegada):
        self.nome = nome
        self.tempo_execucao = tempo_execucao
        self.tempo_restante = tempo_execucao
        self.chegada = chegada
        self.finalizado = False

def sjf_preemptivo(processos, display_func):
    tempo_corrente = 0
    while any(p.tempo_restante > 0 for p in processos):
        processos_disponiveis = [p for p in processos if p.chegada <= tempo_corrente and p.tempo_restante > 0]

        if processos_disponiveis:
            processo_atual = min(processos_disponiveis, key=lambda p: p.tempo_restante)
            processo_atual.tempo_restante -= 1

            display_func(f"Tempo: {tempo_corrente}, Executando {processo_atual.nome}, Tempo Restante: {processo_atual.tempo_restante}")

            if processo_atual.tempo_restante == 0:
                processo_atual.finalizado = True
                display_func(f"{processo_atual.nome} finalizado no tempo {tempo_corrente + 1}")

        else:
            display_func(f"Tempo: {tempo_corrente}, Nenhum processo disponível")

        time.sleep(1)
        tempo_corrente += 1

def iniciar_simulacao():
    processos = []
    for i, entrada in enumerate(entradas):
        nome_processo = f"Processo {i + 1}" 
        try:
            tempo_execucao = int(entrada[0].get())
            tempo_chegada = int(entrada[1].get())
        except ValueError:
            messagebox.showerror("Erro", "O tempo de execução e de chegada devem ser números inteiros.")
            return

        processos.append(Processo(nome_processo, tempo_execucao, tempo_chegada))

    threading.Thread(target=sjf_preemptivo, args=(processos, atualizar_status)).start()

def atualizar_status(mensagem):
    status_texto.insert(tk.END, mensagem + '\n')
    status_texto.see(tk.END)

janela = tk.Tk()
janela.title("Simulação SJF Preemptivo")
janela.configure(bg="#B0C4DE")

frame_processos = tk.Frame(janela, bg="#778899", padx=10, pady=10)
frame_processos.grid(row=0, column=0, padx=20, pady=10)

titulo_label = tk.Label(frame_processos, text="Entrada de Processos", font=("Arial", 14, "bold"), bg="#778899", fg="white")
titulo_label.grid(row=0, column=0, columnspan=5, pady=(0, 10))

entradas = []
cores = ["#778899"] 
for i in range(6):
    tempo_label = tk.Label(frame_processos, text=f"Processo {i + 1} - Tempo Execução:", bg=cores[0])
    tempo_label.grid(row=i+1, column=0, padx=5, pady=5, sticky="e")
    tempo_entry = tk.Entry(frame_processos)
    tempo_entry.grid(row=i+1, column=1, padx=5, pady=5)

    chegada_label = tk.Label(frame_processos, text="Tempo Chegada:", bg=cores[0])
    chegada_label.grid(row=i+1, column=2, padx=5, pady=5, sticky="e")
    chegada_entry = tk.Entry(frame_processos)
    chegada_entry.grid(row=i+1, column=3, padx=5, pady=5)

    entradas.append((tempo_entry, chegada_entry))

botao_iniciar = tk.Button(janela, text="Iniciar Simulação", command=iniciar_simulacao, bg="#2e7d32", fg="white", font=("Arial", 12, "bold"))
botao_iniciar.grid(row=1, column=0, pady=20)

frame_status = tk.Frame(janela, bg="#DCDCDC", padx=10, pady=10)
frame_status.grid(row=2, column=0, padx=20, pady=10)

status_label = tk.Label(frame_status, text="Status da Simulação", font=("Arial", 14, "bold"), bg="#388e3c", fg="white")
status_label.grid(row=0, column=0, pady=(0, 10))

status_texto = tk.Text(frame_status, height=10, width=60, bg="#f1f8e9", fg="#2e7d32", font=("Arial", 10))
status_texto.grid(row=1, column=0, padx=10, pady=10)

janela.mainloop()