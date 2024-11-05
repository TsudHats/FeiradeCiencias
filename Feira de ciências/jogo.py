# Importa as bibliotecas utilizadas
import pygame  # Biblioteca para criação de jogos 2D em python
import sys  # Biblioteca para manipular a saída do sistema
import random  # Biblioteca para randomizar números
import json  # Biblioteca para utilizar arquivos JSON
import os

# Inicializa o Pygame
pygame.init()

# Define o caminho para os arquivos
if getattr(sys, 'frozen', False):
    # Quando o script está sendo executado como um executável
    base_path = sys._MEIPASS
else:
    # Quando o script está sendo executado como um arquivo Python
    base_path = os.path.dirname(os.path.abspath(__file__))

# Define os caminhos dos arquivos
perguntas_file = os.path.join(base_path, 'perguntas.json')  # Caminho correto
tabuleiro_image = os.path.join(base_path, 'tabuleiro.jpeg')  # Caminho correto

# Carregando arquivos
try:
    with open(perguntas_file) as f:
        perguntas = json.load(f)  # Carrega o JSON corretamente
except FileNotFoundError:
    print(f"Arquivo não encontrado: {perguntas_file}")

try:
    tabuleiro_img = pygame.image.load(tabuleiro_image)  # Usando o caminho dinâmico
except FileNotFoundError:
    print(f"Arquivo não encontrado: {tabuleiro_image}")

# Aqui você pode adicionar o restante do seu código para o jogo
largura, altura = 1920, 1080  # Define a dimensão da tela
tela = pygame.display.set_mode((largura, altura))  # Cria a tela com as dimensiões anteriores
pygame.display.set_caption("Jogo da Tabuleiro - Perguntas e Respostas - Biomas Marítimos")  # Define o título do jogo
clock = pygame.time.Clock()  # Cria um objeto Clock para limitar a quantidade de quadros
clock.tick(120)  # Define a taxa de atualização de tela para 120 FPS

# Carrega perguntas do arquivo perguntas.json e notifica se houver erro
try:
    with open('Feira de ciências\\perguntas.json', 'r', encoding='utf-8') as file:  # Abre o arquivo .JSON e carrega os dados
        data = json.load(file)  # Carrega os arquivos JSON
        questions = data['questions']  # Extrai as perguntas do arquivo
except json.JSONDecodeError as e:  # Captura erro de codificação do JSON
    print(f"Erro ao decodificar JSON: {e}")
    questions = []  # Define perguntas como uma lista vazia em caso de erro
except FileNotFoundError as e:
    print(f"Arquivo não encontrado: {e}")
    questions = []  # Define perguntas como uma lista vazia em caso de erro
except Exception as e:
    print(f"Erro inesperado: {e}")
    questions = []  # Define perguntas como uma lista vazia em caso de erro
    

# Carrega a imagem do tabuleiro
try:
    tabuleiro_img = pygame.image.load('Feira de ciências\\tabuleiro.jpeg')
    tabuleiro_img = pygame.transform.scale(tabuleiro_img, (largura, altura))  # Redimensiona para o tamanho da tela
except pygame.error as e:
    print(f"Erro ao carregar a imagem: {e}")
    pygame.quit()
    sys.exit()

path = [
    (900, 69), (955, 69), (1005, 69), (1050, 69), (1090, 69),
    (1130, 69), (1160, 69), (1200, 69), (1240, 69), (1254, 69),
    (1310, 69), (1370, 69), (1425, 69), (1475, 69), (1530, 69),
    (1585, 69), (1635, 69), (1680, 69), (1730, 69), (1780, 69),
    (1830, 69), (1830, 110), (1830, 155), (1830, 195), (1830, 240),
    (1830, 280), (1830, 322), (1830, 362), (1830, 405), (1830, 445),
    (1830, 490), (1830, 532), (1830, 567), (1830, 600), (1830, 627),
    (1830, 674), (1830, 717), (1830, 760), (1830, 800), (1830, 840),
    (1830, 880), (1830, 917), (1830, 955), (1830, 1000), (1780, 1000),
    (1730, 1000), (1680, 1000), (1635, 1000), (1580, 1000), (1520, 1000),
    (1475, 1000), (1435, 1000), (1390, 1000), (1340, 1000), (1280, 1000),
    (1220, 1000), (1170, 1000), (1130, 1000), (1085, 1000), (1045, 1000),
    (1005, 1000), (955, 1000), (900, 1000), (900, 955), (900, 917),
    (900, 880), (900, 835), (900, 800),(900, 760), (900, 717),
    (900, 674), (900, 630), (900, 585),(900, 540), (900, 495),
    (900, 452), (900, 410), (900, 365),(900, 322), (900, 280),
    (900, 238), (900, 195), (900, 155),(900, 110), (900, 69)
]  # Define as posições do tabuleiro

class Player:  # Define a classe Player para gerenciar os jogadores
    def __init__(self, nome, color, posição=(0, 0)):
        # Inicializa os atributos do jogador
        self.nome = nome  # Nome do jogador
        self.color = color  # Cor do jogador
        self.posição = posição  # Posição do jogador
        self.index = 0  # Local do Tabuleiro do Jogador

    def move(self, passos, path):  # Define a função de movimento
        self.index += passos  # Atualiza o índice com os passos rolados
        if self.index >= len(path):
            self.index = len(path) - 1  # Limita o índice à última posição do caminho
        self.posição = path[self.index]  # Atualiza a posição do jogador

def rola_dado():  # Define o método para rolar o dado
    return random.randint(1, 6)  # Retorna um número aleatório entre 1 e 6

def desenhar_player(player):  # Define o método para desenhar o player no tabuleiro
    pygame.draw.circle(tela, player.color, player.posição, 20)

def desenhar_texto(texto, x, y, tamanho=30, cor=(255,255,255)):
    fonte = pygame.font.Font(None, tamanho)
    texto_renderizado = fonte.render(texto, True, cor)
    tela.blit(texto_renderizado, (x, y))

# Define os players
player1 = Player('Jogador 1', (0, 0, 0), path[0])  # Cria o jogador 1
player2 = Player('Jogador 2', (160, 32, 240), path[0])  # Cria o jogador 2
player3 = Player('Jogador 3', (0, 255, 0), path[0])  # Cria o jogador 3
player4 = Player('Jogador 4', (255, 255, 0), path[0])  # Cria o jogador 4

players = [player1, player2, player3, player4]
current_player_index = 0  # Índice do jogador atual

game_over = False  # Controla se o jogo terminou
resposta_dada = False  # Controla se a resposta foi dada
dado_rolado = False  # Controla se o dado foi rolado
dado_resultado = 0  # Armazena o resultado do dado
pergunta = None  # Armazena a pergunta atual
seleção_escolhida = None  # Armazena a seleção feita pelo jogador
mensagem_erro = ""  # Mensagem de erro a ser exibida

font = pygame.font.SysFont(None, 48)  # Define a fonte do jogo


def desenhar_opcoes(opcoes, x, y, tamanho_fonte=40, largura_max=700, cor=(0, 0, 0)):
    """
    Desenha as opções de resposta com quebra de linha, ajustando o espaçamento entre linhas e opções.
    
    :param opcoes: Lista de opções a serem desenhadas.
    :param x: Posição X para começar a desenhar.
    :param y: Posição Y inicial para desenhar.
    :param tamanho_fonte: Tamanho da fonte das opções.
    :param largura_max: Largura máxima permitida para cada linha.
    :param cor: Cor do texto.
    """
    fonte = pygame.font.Font(None, tamanho_fonte)
    opcoes_quebradas = quebra_texto_opcoes(opcoes, fonte, largura_max)
    
    espaco_entre_opcoes = tamanho_fonte + 35  # Espaço extra entre cada opção
    espaco_entre_linhas = tamanho_fonte + -15   # Espaço entre as linhas de cada opção
    
    for i, linhas in enumerate(opcoes_quebradas):
        y_opcao = y + i * espaco_entre_opcoes  # Calcula a posição inicial Y para cada opção
        for j, linha in enumerate(linhas):
            superficie_texto = fonte.render(linha, True, cor)
            tela.blit(superficie_texto, (x, y_opcao + j * espaco_entre_linhas))  # Ajusta o espaçamento entre linhas dentro da opção


cor_verde = (0,255,0)
cor_vermelho = (255,0,0)



def quebra_texto(texto, fonte, largura_max): # Limite da largura para os textos na tela
    palavras = texto.split()
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        if fonte.size(linha_atual + palavra)[0] <= largura_max:
            linha_atual += palavra + " "
        else:
            linhas.append(linha_atual.strip())
            linha_atual = palavra + " "
    
    linhas.append(linha_atual.strip())
    return linhas

def desenhar_texto_multilinha(texto, x, y, tamanho_fonte, largura_max, cor=(0, 0, 0)):
    fonte = pygame.font.Font(None, tamanho_fonte)
    linhas = quebra_texto(texto, fonte, largura_max)
    for i, linha in enumerate(linhas):
        superficie_texto = fonte.render(linha, True, cor)
        tela.blit(superficie_texto, (x, y + i * (tamanho_fonte + 5)))  # Ajusta o espaçamento entre linhas
        
        
def quebra_texto_opcoes(opcoes, fonte, largura_max):
    """
    Divide as opções em múltiplas linhas, se necessário, com base na largura máxima.
    
    :param opcoes: Lista de opções (strings) a serem quebradas.
    :param fonte: Fonte a ser utilizada para renderizar o texto.
    :param largura_max: Largura máxima permitida para cada linha.
    :return: Lista de listas, onde cada sublista contém as linhas para uma opção.
    """
    opcoes_quebradas = []
    
    for opcao in opcoes:
        palavras = opcao.split()
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            if fonte.size(linha_atual + palavra)[0] <= largura_max:
                linha_atual += palavra + " "
            else:
                linhas.append(linha_atual.strip())
                linha_atual = palavra + " "
        
        linhas.append(linha_atual.strip())
        opcoes_quebradas.append(linhas)

    return opcoes_quebradas

fim = len(path) - 1
        
# Loop principal do jogo
while True:
    for event in pygame.event.get():  # Captura eventos do Pygame
        if event.type == pygame.QUIT:  # Verifica se o evento é de saída
            pygame.quit()
            sys.exit()  # Sai do jogo
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            if not resposta_dada:
                if event.key == pygame.K_1:
                    seleção_escolhida = "A"
                elif event.key == pygame.K_2:
                    seleção_escolhida = "B"
                elif event.key == pygame.K_3:
                    seleção_escolhida = "C"
                elif event.key == pygame.K_4:
                    seleção_escolhida = "D"
            
                if seleção_escolhida:
                    if seleção_escolhida == pergunta["correct_option"]:
                        resposta_dada = True
                        dado_rolado = False
                        mensagem_erro = "Resposta correta! Pressione Espaço para rolar o dado"
                    else:
                        resposta_dada = True
                        mensagem_erro = f"Resposta errada! {players[current_player_index].nome} mudando para o próximo jogador"
                        current_player_index = (current_player_index + 1) % len(players)
                        pergunta = random.choice(questions)
                        mensagem_erro = ""
                        resposta_dada = False
                        
            
            elif resposta_dada and not dado_rolado and event.key == pygame.K_SPACE:
                if mensagem_erro == "Resposta correta! Pressione Espaço para rolar o dado":
                    current_player_index = (current_player_index + 1) % len(players)
                    players[current_player_index].move(dado_resultado, path)
                    dado_resultado = rola_dado()
                    dado_rolado = True
                    mensagem_erro = ""
                
        if event.type == pygame.MOUSEBUTTONDOWN and dado_rolado:
            players[current_player_index].move(dado_resultado, path)
            resposta_dada = False
            dado_rolado = False
            mensagem_erro = ""  # Limpa a mensagem de erro para o próximo turno
            pergunta = random.choice(questions)  # Escolhe uma nova pergunta
            current_player_index = (current_player_index + 1) % len(players)
            


    # (restante do loop permanece igual)


    for player in players:
        desenhar_player(player)

    # Limpa a tela
    tela.fill((255, 255, 255))  # Define a cor de fundo da tela
    tela.blit(tabuleiro_img, (0, 0))  # Desenha a imagem do tabuleiro

    # Desenha os jogadores
    for player in players:
        desenhar_player(player)

    # Exibe a pergunta e as opções, se existir
    if not resposta_dada:
        pergunta = random.choice(questions) if pergunta is None else pergunta
        seleção_escolhida = None
        
    if pergunta:
        desenhar_texto_multilinha(pergunta["question"], 130, 220, 40, 700)  # Define a largura máxima para 700 pixels
        desenhar_opcoes(pergunta["options"], 115, 500, 40)

        if dado_rolado:
            desenhar_texto(f"Dado parou em: {dado_resultado}, Clique do mouse para mover", 150, 450, 40, (0,0,0))


        desenhar_texto(f"{players[current_player_index].nome} é o jogador atual", 250, 1000, 50, (0,0,0))

        if mensagem_erro:
            if mensagem_erro == "Resposta correta! Pressione Espaço para rolar o dado":
                desenhar_texto(mensagem_erro, 150, 450, 40, (0,0,0))
            elif mensagem_erro == f"Resposta errada! {players[current_player_index].nome} mudando para o próximo jogador":
                desenhar_texto(mensagem_erro, 50, 450, 40, (0,0,0))

    for player in players:
        desenhar_player(player)

    pygame.display.flip()

