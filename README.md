
# Simulação do Algoritmo SJF Preemptivo
Este projeto implementa uma simulação do algoritmo Shortest Job First (SJF) Preemptivo em Python, utilizando a biblioteca Tkinter para criar uma interface gráfica amigável para a entrada e visualização dos processos.

## Requisitos
- Python 3.x
- Tkinter (já incluído na maioria das distribuições do Python)
- Baixe o arquivo sjs_simulator.py e o execute 

## Interface gráfica:
### Explicação da Interface
A interface permite que o usuário insira até 6 processos, cada um com seu tempo de execução e tempo de chegada.
Após clicar em "Iniciar Simulação", o status da execução é exibido na área de texto da interface. A cada unidade de tempo, o processo com o menor tempo de execução restante é selecionado e executado.
A simulação considera a chegada dos processos, executando apenas os que estão disponíveis no momento, e é atualizada em tempo real na interface.

### A interface foi desenvolvida com um esquema de cores amigável e simples:

- Fundo geral: Um tom suave de amarelo claro (#f0f4c3).
- Elementos principais (botões e seções): Verde escuro (#388e3c).
- Campos de entrada e rótulos: Tons suaves de verde (#a5d6a7, #c8e6c9, #e8f5e9).
- Essas cores proporcionam uma experiência visual confortável e agradável ao usuário.

## Funcionalidades
- Simulação do SJF Preemptivo: O algoritmo simula a execução de processos, considerando o tempo de chegada e preempção com base no tempo de execução restante.
- Atualização em tempo real: A execução é mostrada em tempo real, com atualizações na interface para cada unidade de tempo.
- Interface amigável: A interface gráfica foi projetada para ser simples e eficiente, permitindo que qualquer usuário possa facilmente interagir com a aplicação.
### Exemplo de Uso

Entrada de Processos:
- Processo 1: Tempo de execução: 5, Tempo de chegada: 0
- Processo 2: Tempo de execução: 3, Tempo de chegada: 1
- Processo 3: Tempo de execução: 8, Tempo de chegada: 2
