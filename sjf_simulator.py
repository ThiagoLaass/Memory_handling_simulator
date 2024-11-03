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
        self.tempo_inicio = None
        self.tempo_fim = None
        self.tempo_espera = 0
        self.tempo_fila = 0

def sjf_preemptivo(processos, display_func):
    clear_logs()
    tempo_corrente = 0
    while any(p.tempo_restante > 0 for p in processos):
        processos_disponiveis = [p for p in processos if p.chegada <= tempo_corrente and p.tempo_restante > 0]
        if processos_disponiveis:
            processo_atual = min(processos_disponiveis, key=lambda p: p.tempo_restante)
            if processo_atual.tempo_inicio is None:
                processo_atual.tempo_inicio = tempo_corrente
            processo_atual.tempo_restante -= 1
            display_func(f"Tempo: {tempo_corrente}, Executando {processo_atual.nome}, Tempo Restante: {processo_atual.tempo_restante}", status="executing")
            if processo_atual.tempo_restante == 0:
                processo_atual.finalizado = True
                processo_atual.tempo_fim = tempo_corrente + 1
                processo_atual.tempo_espera = (processo_atual.tempo_fim - processo_atual.chegada) - processo_atual.tempo_execucao
                display_func(f"{processo_atual.nome} finalizado no tempo {tempo_corrente + 1}", status="finished")
        else:
            display_func(f"Tempo: {tempo_corrente}, Nenhum processo disponível", status="idle")
        time.sleep(1)
        tempo_corrente += 1
    calcular_tempo_espera_medio(processos)

def clear_logs():
    status_texto.delete('1.0', tk.END)
    log_texto_espera.delete('1.0', tk.END)

def calcular_tempo_espera_medio(processos):
    total_espera = sum(p.tempo_espera for p in processos)
    media_espera = total_espera / len(processos)
    for processo in processos:
        log_espera(f"{processo.nome} - Tempo de Espera: {processo.tempo_espera}")
    log_espera(f"Tempo médio de espera: {media_espera:.2f}")

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

def atualizar_status(mensagem, status="idle"):
    colors = {
        "executing": "#3DA5F4",
        "finished": "#2ECC71",
        "idle": "#E74C3C"
    }
    log_message = f"{mensagem}\n"
    status_texto.tag_configure("executing", foreground=colors["executing"])
    status_texto.tag_configure("finished", foreground=colors["finished"])
    status_texto.tag_configure("idle", foreground=colors["idle"])
    status_texto.insert(tk.END, log_message, status)
    status_texto.see(tk.END)

def log_espera(mensagem):
    log_texto_espera.insert(tk.END, mensagem + "\n")
    log_texto_espera.see(tk.END)

def gerar_campos_processos():
    try:
        num_processos = int(entry_num_processos.get())
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número inteiro válido.")
        return
    for widget in frame_processos.winfo_children():
        widget.destroy()

    titulo_label = tk.Label(frame_processos, text="Entrada de Processos", font=("Arial", 14, "bold"), bg="#ffffff", fg="#2C3E50")
    titulo_label.grid(row=0, column=0, columnspan=5, pady=(0, 5), sticky="w")

    global entradas
    entradas = []
    for i in range(num_processos):
        tempo_label = tk.Label(frame_processos, text=f"Processo {i + 1} - Tempo Execução:", bg="#ffffff", fg="#2C3E50", font=("Arial", 12))
        tempo_label.grid(row=i+1, column=0, padx=5, pady=5, sticky="e")
        tempo_entry = tk.Entry(frame_processos, width=7, font=("Arial", 12))
        tempo_entry.grid(row=i+1, column=1, padx=5, pady=5)
        chegada_label = tk.Label(frame_processos, text="Tempo Chegada:", bg="#ffffff", fg="#2C3E50", font=("Arial", 12))
        chegada_label.grid(row=i+1, column=2, padx=5, pady=5, sticky="e")
        chegada_entry = tk.Entry(frame_processos, width=7, font=("Arial", 12))
        chegada_entry.grid(row=i+1, column=3, padx=5, pady=5)
        entradas.append((tempo_entry, chegada_entry))

def calcular_tempo_espera_medio(processos):
    total_espera = sum(p.tempo_espera for p in processos)
    media_espera = total_espera / len(processos)
    for processo in processos:
        log_espera(f"{processo.nome} - Tempo de Espera: {processo.tempo_espera}")
    log_espera(f"Tempo médio de espera: {media_espera:.2f}")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def add_scrollbar_to_window():
    global canvas
    global frame_content

    canvas = tk.Canvas(janela, bg="#f0f0f0")
    canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar = tk.Scrollbar(janela, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    frame_content = tk.Frame(canvas, bg="#f0f0f0")

    canvas.create_window((0, 0), window=frame_content, anchor="nw")

    frame_content.bind("<Configure>", on_frame_configure)

janela = tk.Tk()
janela.title("Simulação SJF Preemptivo")
janela.configure(bg="#f0f0f0")

add_scrollbar_to_window()

frame_num_processos = tk.Frame(frame_content, bg="#f0f0f0", padx=10, pady=10)
frame_num_processos.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

label_num_processos = tk.Label(frame_num_processos, text="Número de processos:", font=("Arial", 12), bg="#f0f0f0", fg="#333333")
label_num_processos.grid(row=0, column=0, padx=5, pady=5, sticky="w")

entry_num_processos = tk.Entry(frame_num_processos, width=5)
entry_num_processos.grid(row=0, column=1, padx=5, pady=5)

botao_gerar = tk.Button(frame_num_processos, text="Gerar Campos", command=gerar_campos_processos, bg="#007BFF", fg="white", font=("Arial", 11, "bold"))
botao_gerar.grid(row=0, column=2, padx=5, pady=5)

frame_processos = tk.Frame(frame_content, bg="#ffffff", padx=10, pady=10)
frame_processos.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

botao_iniciar = tk.Button(frame_content, text="Iniciar Simulação", command=iniciar_simulacao, bg="#007BFF", fg="white", font=("Arial", 12, "bold"))
botao_iniciar.grid(row=2, column=0, pady=10, sticky="nsew")

frame_status = tk.Frame(frame_content, bg="#ffffff", padx=10, pady=10)
frame_status.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

status_label = tk.Label(frame_status, text="Status da Simulação", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#333333")
status_label.pack(pady=(0, 10))

scrollbar_status = tk.Scrollbar(frame_status)
scrollbar_status.pack(side=tk.RIGHT, fill=tk.Y)

status_texto = tk.Text(frame_status, height=10, width=70, bg="#ECF0F1", fg="#333333", font=("Arial", 11), yscrollcommand=scrollbar_status.set)
status_texto.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar_status.config(command=status_texto.yview)

frame_espera = tk.Frame(frame_content, bg="#ffffff", padx=10, pady=10)
frame_espera.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

log_label_espera = tk.Label(frame_espera, text="Tempo de Espera Médio", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#333333")
log_label_espera.pack(pady=(0, 10))

scrollbar_espera = tk.Scrollbar(frame_espera)
scrollbar_espera.pack(side=tk.RIGHT, fill=tk.Y)

log_texto_espera = tk.Text(frame_espera, height=6, width=70, bg="#ECF0F1", fg="#333333", font=("Arial", 11), yscrollcommand=scrollbar_espera.set)
log_texto_espera.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar_espera.config(command=log_texto_espera.yview)

janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(0, weight=1)

janela.mainloop()