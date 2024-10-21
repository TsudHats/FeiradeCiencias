# Importa as bibliotecas utilizadas
import pygame # Biblioteca para criação de jogos 2D em python
import sys # Biblioteca para manipular a saída do sistema
import random # Biblioteca para randomizar números
import json # Biblioteca para utilizar arquivos JSON

# Inicializa o Pygame
pygame.init()


largura, altura = 1920, 1080 # Define a dimensão da tela
tela = pygame.display.set_mode((largura, altura)) # Cria a tela com as dimensiões anteriores
pygame.display.set_caption("Jogo da Tabuleiro - Perguntas e Respostas - Biomas Marítimos") # Define o título do jogo
clock = pygame.time.Clock() # Cria um objeto Clock para limitar a quantidade de quadros
clock.tick(120) # Define a taxa de atualização de tela para 120 FPS

# Carrega perguntas do arquivo perguntas.json e notifica se houver erro
try:
    with open('Feira de ciências\\perguntas.json', 'r', encoding='utf-8') as file: # Abre o arquivo .JSON e carrega os dados
        data = json.load(file) # Carrega os arquivos JSON
        questions = data['questions'] # Extrai as perguntas do arquivo
except json.JSONDecodeError as e: # Captura erro de codificação do JSON
    print(f"Erro ao decodificar JSON: {e}")
    questions = [] # Define perguntas como uma lista vazia em caso de erro
except FileNotFoundError as e:
    print(f"Arquivo não encontrado: {e}")
    questions = [] # Define perguntas como uma lista vazia em caso de erro
except Exception as e:
    print(f"Erro inesperado: {e}")
    questions = [] # Define perguntas como uma lista vazia em caso de erro

path = [
    (50, 50), (150, 50), (250, 50), (350, 50), (450, 50),
    (450, 150), (450, 250), (350, 250), (250, 250), (150, 250),
    (50, 250), (50, 350), (150, 350), (250, 350), (350, 350)
]  # Define as posições do tabuleiro

class Player:  # Define a classe Player para gerenciar os jogadores
    def __init__(self, nome, color, posição=(0, 0)):
        # Inicializa os atributos do jogador
        self.nome = nome # Nome do jogador
        self.color = color # Cor do jogador
        self.posição = posição # Posição do jogador
        self.index = 0 # Local do Tabuleiro do Jogador

    def move(self, passos, path):  # Define a função de movimento
        self.index += passos # Atualiza o índice com os passos rolados
        if self.index >= len(path):
            self.index = len(path) - 1 # Limita o índice à última posição do caminho
        self.posição = path[self.index] # Atualiza a posição do jogador

def rola_dado():  # Define o método para rolar o dado
    return random.randint(1, 6) # Retorna um número aleatório entre 1 e 6

def desenhar_player(player):  # Define o método para desenhar o player no tabuleiro
    pygame.draw.circle(tela, player.color, player.posição, 20)

def desenhar_texto(texto, font, cor, x, y):  # Desenha os textos na tela
    tela_texto = font.render(texto, True, cor) # Desenha um círculo representando o jogador
    tela.blit(tela_texto, (x, y)) # Desenha o texto na tela na posição especificada

# Define os players
player1 = Player('Jogador 1', (0, 0, 0), path[0]) # Cria o jogador 1
player2 = Player('Jogador 2', (255, 0, 0), path[0]) # Cria o jogador 2
player3 = Player('Jogador 3', (0, 255, 0), path[0]) # Cria o jogador 3
player4 = Player('Jogador 4', (0, 0, 255), path[0]) # Cria o jogador 4

players = [player1, player2, player3, player4]
current_player_index = 0  # Índice do jogador atual

game_over = False # Controla se o jogo terminou
resposta_dada = False # Controla se a resposta foi dada
dado_rolado = False # Controla se o dado foi rolado
dado_resultado = 0 # Armazena o resultado do dado
pergunta = None # Armazena a pergunta atual
seleção_escolhida = None # Armazena a seleção feita pelo jogador
mensagem_erro = ""  # Mensagem de erro a ser exibida

font = pygame.font.SysFont(None, 48)  # Define a fonte do jogo

def desenhar_opcoes(options, font, color, x, y):  # Desenha as opções das perguntas
    for i, option in enumerate(options):
        desenhar_texto(option, font, color, x, y + i * 40) # Desenha cada opção com espaçamento

while not game_over:  # Enquanto o jogo não terminar
    for event in pygame.event.get(): # Verifica eventos na fila de eventos
        if event.type == pygame.QUIT: # Se o evento for de sair
            pygame.quit() # Finaliza o Pygame
            sys.exit()  # Sai do sistema

        if event.type == pygame.KEYDOWN: # Se uma tecla for pressionada
            if event.key == pygame.K_ESCAPE:  # Se a tecla ESC for pressionada
                pygame.quit() # Finaliza o Pygame
                sys.exit() # Sai do sistema

            if not resposta_dada: # Se a resposta ainda não foi dada
                 # Verifica qual tecla foi pressionada para selecionar a resposta
                if event.key == pygame.K_1:
                    seleção_escolhida = "A"
                elif event.key == pygame.K_2:
                    seleção_escolhida = "B"
                elif event.key == pygame.K_3:
                    seleção_escolhida = "C"
                elif event.key == pygame.K_4:
                    seleção_escolhida = "D"

                if seleção_escolhida:  # Se uma seleção foi feita
                    # Verifica se a resposta dada está correta
                    if seleção_escolhida == pergunta["correct_option"]:
                        resposta_dada = True  # A resposta foi dada corretamente
                        dado_rolado = False # Reseta o estado do dado
                        mensagem_erro = ""  # Limpa a mensagem de erro
                    else:
                        resposta_dada = False  # Mantém a pergunta para o próximo jogador
                        mensagem_erro = f"Resposta errada! {players[current_player_index].nome} mudando para o próximo jogador..."
                        current_player_index = (current_player_index + 1) % len(players)  # Passa para o próximo jogador

            elif resposta_dada and not dado_rolado and event.key == pygame.K_SPACE:
                dado_resultado = rola_dado()  # Rola o dado
                dado_rolado = True # Define que o dado foi rolado

        if event.type == pygame.MOUSEBUTTONDOWN and dado_rolado: # Se o mouse for clicado e o dado foi rolado
            players[current_player_index].move(dado_resultado, path) # Move o jogador atual
            resposta_dada = False # Reseta a resposta dada
            dado_rolado = False # Reseta o estado do dado
            current_player_index = (current_player_index + 1) % len(players)  # Muda para o próximo jogador

    tela.fill((255, 255, 255)) # Limpa a tela com a cor branca

    if not resposta_dada:  # Se a resposta ainda não foi dada
        pergunta = random.choice(questions) if pergunta is None else pergunta # Seleciona uma pergunta aleatória
        seleção_escolhida = None # Reseta a seleção

    if pergunta:
        desenhar_texto(pergunta["question"], font, (0, 0, 0), 50, 50) # Desenha a pergunta na tela
        desenhar_opcoes(pergunta["options"], font, (0, 0, 0), 50, 150) # Desenha as opções de resposta

        if resposta_dada:
            desenhar_texto("PRESSIONE ESPAÇO PARA ROLAR DADO.", font, (0, 0, 0), 50, 350) # Mostra a seleção

        if dado_rolado:
            desenhar_texto(f"Dado parou em: {dado_resultado}", font, (0, 0, 0), 50, 400) # Exibe a mensagem de erro
            desenhar_texto("Clique para mover.", font, (0, 0, 0), 50, 450)

        # Mostrar jogador atual
        desenhar_texto(f"{players[current_player_index].nome} é o jogador atual", font, (0, 0, 0), 50, 500) # Exibe mensagem de erro

        # Mostrar mensagem de erro, se houver
        if mensagem_erro:
            desenhar_texto(mensagem_erro, font, (255, 0, 0), 50, 550)

    # Desenhar todos os jogadores na tela
    for player in players:
        desenhar_player(player) # Desenha cada jogador no tabuleiro

    pygame.display.flip()

pygame.quit()