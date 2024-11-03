# Simulação do Algoritmo SJF Preemptivo com Paginação de Memória (Web)

Este projeto implementa uma simulação do algoritmo Shortest Job First (SJF) Preemptivo utilizando HTML, CSS e JavaScript. A aplicação simula a execução de processos, a movimentação entre a memória principal e a memória virtual, e a visualização de processos divididos em páginas. **Os Processos e páginas são criados automaticamente, visto que novos processos chegam na memória em tempo de execução**

## Requisitos
- Um navegador moderno (Chrome, Firefox, Edge, etc.)

## Descrição

![image](https://github.com/user-attachments/assets/50ad5005-1859-470a-926c-20735facb868)

#### Páginas:
Como visto na imagem, os processos estão sendo dividios em páginas, onde o primeiro "P" representa o processo, o segundo a página e o (T<tamanho>), o tamanho da página.

#### CPU:
A CPU pode estar executando uma página, ou ociosa, como mostra a imagem abaixo:

![image](https://github.com/user-attachments/assets/f83dd207-4c76-4f7d-b488-6ae13f2eeea9)


## Como executar
1. Apenas abra o link enviado via canvas, ou clicando em deployments no repositorio e clique em iniciar simulação. Após todos os processos forem executados, o programa continua esperando processos, para rodar novamente, apenas clique em iniciar simulação novamente.

## Funcionalidades
- **Simulação do Algoritmo SJF Preemptivo**: O algoritmo simula a execução de processos, selecionando o processo com o menor tempo de execução restante para ser executado a cada unidade de tempo.
- **Criação Automática de Processos**: Os processos são gerados automaticamente, permitindo que novos processos sejam criados durante a execução da simulação para simular a chegada dinâmica de processos.
- **Gerenciamento de Memória Virtual**: A memória é visualmente dividida em **Memória Principal** e **Memória Virtual**. Quando a memória principal está cheia, as páginas são automaticamente movidas para a memória virtual.
- **Visualização em Paginação**: Cada processo é representado como uma página que pode ser visualmente alocada na memória principal ou movida para a memória virtual, facilitando a compreensão do conceito de paginação.
- **Atualizações em Tempo Real**: O status da execução e a utilização da memória são atualizados em tempo real, permitindo que os usuários acompanhem o progresso da simulação.

### Exemplo de Uso
- Ao abrir a aplicação, os processos serão gerados automaticamente e alocados na memória principal.
- Durante a execução, se a memória principal estiver cheia, os processos serão movidos para a memória virtual.
- A cada unidade de tempo, o processo com o menor tempo restante será executado, e a visualização mostrará as mudanças na alocação de memória.

## Integrantes do Grupo
- Thiago Laass
- Lucas Valente
- Luisa Clara de Paula
