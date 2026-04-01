# 🦆 Silly Duck
Bem-vindo ao Silly Duck! Um patinho digital amigável e um pouco bobo que passeia pela sua área de trabalho, trazendo um pouco de diversão e caos para o seu dia.

![Silly Duck](https://img.itch.zone/aW1hZ2UvMjA2MjMyMy8xMjEyNjQ3OC5naWY=/original/O7D%2BBO.gif)

## Descrição
Silly Duck é um "desktop pet" (mascote de área de trabalho) desenvolvido em Python. Ele é um pato animado que anda de um lado para o outro na tela, persegue o cursor do mouse, reage a cliques e até tenta arrastar o seu mouse com o bico. É um projeto simples e divertido, perfeito para quem quer um companheiro virtual enquanto estuda ou trabalha.

## Funcionalidades Principais
Animação de caminhada: O pato passeia pela sua tela de forma autônoma, mudando de direção aleatoriamente.
Perseguição do mouse: Fique de olho no seu cursor! O pato pode decidir segui-lo pela tela.
Arrasta o mouse com o bico: Quando alcança o cursor, o pato pode tentar puxá-lo pela tela.
Pato Assustado: Experimente clicar no pato e veja ele sair correndo!
Comportamentos aleatórios: O pato tem momentos de descanso e ações inesperadas para tornar a experiência mais dinâmica.
Animações por estado: Sprites diferentes para caminhar, descansar, puxar e fugir.
Leve e fácil de executar: Não consome recursos relevantes do sistema.

## Tecnologias Utilizadas
Este projeto foi construído utilizando Python e as seguintes bibliotecas principais:
* **Pillow:** Para manipulação e processamento de imagens dos sprites.
* **PyAutoGUI:** Para controlar o mouse e obter informações da tela, permitindo a interação do pato com o ambiente de trabalho.

## Estrutura do Projeto
```bash
Silly-duck/
├── main.py              # Ponto de entrada — inicia o cérebro e a janela
├── requirements.txt
├── .gitignore
├── components/
│   ├── state.py         # Estado central do pato (posição, velocidade, flags)
│   ├── sprites.py       # Carregamento e seleção de sprites por estado
│   ├── movement.py      # Lógica de movimentação (walk, follow, flee, pull)
│   ├── actions.py       # Interações com o mouse do sistema
│   ├── audio.py         # Som de quack
│   └── window.py        # Janela Tkinter e loop de animação
└── assets/
    ├── images/          # Sprites do pato (walk, idle, pull, bounce)
    └── sounds/          # quack.wav
 ```

## Como Executar o Projeto
Para ter o patinho andando na sua tela, siga os passos abaixo.

**Pré-requisitos:**
* Ter o [Python 3](https://www.python.org/downloads/) instalado.
* Ter o [Git](https://git-scm.com/downloads) instalado para clonar o repositório.

**Passos:**
1.  **Clone este repositório:**
    ```bash
    git clone https://github.com/Marcio-A-Barrocal/Silly-duck.git
    cd Silly-duck
    ```
2.  **(Recomendado) Crie e ative um ambiente virtual:**
    Isso isola as dependências do projeto e evita conflitos.
    ```bash
    # No Windows
    python -m venv venv
    .\venv\Scripts\activate
    # No macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    O arquivo `requirements.txt` já contém todas as bibliotecas necessárias. Execute o comando abaixo:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute o Silly Duck!**
    ```bash
    python main.py
    ```

    > **E pronto!** O patinho deve aparecer na sua tela. Tente clicar nele! 🦆
    
## Notas
* Funciona apenas no Windows (usa winsound para o áudio e transparentcolor do Tkinter).
* O pato fica sempre no topo de outras janelas.
* Não consome recursos relevantes — roda tranquilo em segundo plano.
