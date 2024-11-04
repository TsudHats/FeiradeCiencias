# Importa as bibliotecas utilizadas
import pygame  # Biblioteca para criação de jogos 2D em python
import sys  # Biblioteca para manipular a saída do sistema
import random  # Biblioteca para randomizar números
import json  # Biblioteca para utilizar arquivos JSON
import textwrap

# Inicializa o Pygame
pygame.init()

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

def quebra_texto(texto, font, largura_max):
    """Divide o texto em várias linhas com base na largura máxima."""
    palavras = texto.split(' ')
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        # Adiciona a palavra atual à linha
        teste_linha = linha_atual + palavra + ' '
        largura_linha, _ = font.size(teste_linha)
        
        # Se a linha atual for muito longa, adiciona a linha atual à lista de linhas e começa uma nova
        if largura_linha > largura_max:
            linhas.append(linha_atual.strip())
            linha_atual = palavra + ' '  # Começa uma nova linha
        else:
            linha_atual = teste_linha  # Continua na mesma linha

    # Adiciona a última linha, se existir
    if linha_atual:
        linhas.append(linha_atual.strip())

    return linhas

def desenhar_texto(texto, x, y, tamanho=30, cor=(255,255,255)):
    fonte = pygame.font.Font(None, tamanho)
    texto_renderizado = fonte.render(texto, True, cor)
    tela.blit(texto_renderizado, (x, y))

# Define os players
player1 = Player('Jogador 1', (0, 0, 0), path[0])  # Cria o jogador 1
player2 = Player('Jogador 2', (255, 0, 0), path[0])  # Cria o jogador 2
player3 = Player('Jogador 3', (0, 255, 0), path[0])  # Cria o jogador 3
player4 = Player('Jogador 4', (0, 0, 255), path[0])  # Cria o jogador 4

players = [player1, player2, player3, player4]
current_player_index = 0  # Índice do jogador atual

game_over = False  # Controla se o jogo terminou
resposta_dada = False  # Controla se a resposta foi dada
dado_rolado = False  # Controla se o dado foi rolado
dado_resultado = 0  # Armazena o resultado do dado
pergunta = None  # Armazena a pergunta atual
seleção_escolhida = None  # Armazena a seleção feita pelo jogador
mensagem_erro = ""  # Mensagem de erro a ser exibida
pergunta_atual = None
opçoes_atual = []

# Casas que irão ter uma pergunta
casas_perguntas = {1, 4, 5, 9, 11, 12, 16, 17, 20, 22, 28, 30, 32, 34, 37, 44,
                   47, 48, 50, 51, 52, 53, 54, 55, 56, 59, 60, 61, 63,
                   68, 70, 72, 75, 77, 79, 80, 82, 85}
random.shuffle(questions)

indice_pergunta_atual = 0


def escolher_nova_pergunta():
    global pergunta_atual
    pergunta_atual = random.choice(questions)
    
def verificar_resposta(resposta_usuario):
    global pergunta_atual
    if resposta_usuario == pergunta_atual['correta']:
        print("Correto!")
    else:
        print("Incorreto!")
    # Escolhe uma nova pergunta independente do resultado
    escolher_nova_pergunta()

def verificar_pergunta(casa_do_jogador):
    global indice_pergunta_atual
    if casa_do_jogador in casas_perguntas and indice_pergunta_atual < len(questions):
        # Retorna a pergunta atual e incrementa o índice para a próxima pergunta
        pergunta = questions[indice_pergunta_atual]
        indice_pergunta_atual += 1
        return pergunta
    else:
        return ''

def verificar_resposta(pergunta, resposta_selecionada):
    """
    Verifica se a resposta selecionada está correta.
    
    :param pergunta: Dicionário contendo a pergunta e as respostas.
    :param resposta_selecionada: Resposta escolhida pelo jogador.
    :return: True se a resposta estiver correta, False caso contrário.
    """
    return resposta_selecionada == pergunta['correct_option']

font = pygame.font.SysFont(None, 48)  # Define a fonte do jogo
casa_do_jogador = 1


def mover_jogador(dados_rolados):
    global casa_do_jogador, pergunta_atual, opcoes_atual
    casa_do_jogador += dados_rolados  # Atualiza a posição com base no resultado do dado
    if casa_do_jogador >= len(path):  # Garante que o jogador não ultrapasse o caminho
        casa_do_jogador = len(path) - 1  # Ajusta para a última casa se exceder
    pergunta_atual = verificar_pergunta(casa_do_jogador)  # Verifica se há pergunta na casa
    if pergunta_atual:  # Se há pergunta, pega as opções
        opcoes_atual = pergunta_atual['options']



mover_jogador(dado_rolado)

def desenhar_opcoes(options, x, y, color):  # Desenha as opções das perguntas
    for i, option in enumerate(options):
        desenhar_texto(option, x, y + i * 40, tamanho=40, cor=color)

def selecionar_resposta(pergunta, selecao):
    if 'correct_option' in pergunta:
        return pergunta['correct_option'] == selecao
    else:
        print("A pergunta não contém a chave 'correct_answer'.")
        return False  # ou outra lógica que você desejar


cor_verde = (0,255,0)
cor_vermelho = (255,0,0)


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
            if event.key == pygame.K_RETURN:  # Verifica se a tecla Enter foi pressionada
                if resposta_dada:  # Se a resposta já foi dada, avança para o próximo jogador
                    current_player_index = (current_player_index + 1) % len(players)
                    dado_rolado = False
                    resposta_dada = False
                    pergunta_atual = None  # Reseta a pergunta
                    opcoes_atual = []  # Reseta as opções
                    casa_do_jogador = players[current_player_index].index  # Mantenha a casa atual
                elif not dado_rolado:  # Se o dado não foi rolado
                    dado_resultado = rola_dado()  # Rola o dado
                    dado_rolado = True  # Marca que o dado foi rolado
                    players[current_player_index].move(dado_resultado, path)  # Move o jogador
                    mover_jogador(dado_resultado)  # Atualiza a casa e a pergunta após o movimento
                    if players[current_player_index].index in casas_perguntas:
                        pergunta_atual = verificar_pergunta(players[current_player_index].index)  # Verifica pergunta para a casa atual
                        if pergunta_atual:  # Se houver uma pergunta, define as opções
                            opcoes_atual = pergunta_atual['options']
                        
                        
            if not resposta_dada:  # Se a resposta ainda não foi dada
                # Verifica qual tecla foi pressionada para selecionar a resposta
                if event.key == pygame.K_1:
                    seleção_escolhida = "A"
                elif event.key == pygame.K_2:
                    seleção_escolhida = "B"
                elif event.key == pygame.K_3:
                    seleção_escolhida = "C"
                elif event.key == pygame.K_4:
                    seleção_escolhida = "D"
                elif event.key == pygame.K_5:
                    seleção_escolhida = "E"

                # Verifica se a seleção escolhida está correta
                if seleção_escolhida:
                    if seleção_escolhida == pergunta_atual['correct_option']:  # Verifica se a resposta é a correta
                        resposta_dada = True  # A resposta foi dada corretamente
                        mensagem_erro = "Resposta Correta!"
                        cor_mensagem = cor_verde
                    else:
                        resposta_dada = False  # Mantém a pergunta para o próximo jogador
                        mensagem_erro = f"Resposta Incorreta! {players[current_player_index].nome} mudando para o próximo jogador..."
                        current_player_index = (current_player_index + 1) % len(players)  # Passa para o próximo jogador
                        cor_mensagem = cor_vermelho
            
            elif resposta_dada and not dado_rolado and event.key == pygame.K_SPACE:
                dado_resultado = rola_dado()  # Rola o dado
                dado_rolado = True  # Define que o dado foi rolado
                
        if event.type == pygame.MOUSEBUTTONDOWN and dado_rolado:  # Se o mouse for clicado e o dado foi rolado
            players[current_player_index].move(dado_resultado, path)  # Move o jogador atual
            resposta_dada = False  # Reseta a resposta dada
            dado_rolado = False  # Reseta o estado do dado
            current_player_index = (current_player_index + 1) % len(players)  # Muda para o próximo jogador


    for player in players:
        desenhar_player(player)

    # Limpa a tela
    tela.fill((255, 255, 255))  # Define a cor de fundo da tela
    tela.blit(tabuleiro_img, (0, 0))  # Desenha a imagem do tabuleiro

    # Desenha os jogadores
    for player in players:
        desenhar_player(player)

    if pergunta_atual:
        desenhar_texto(pergunta_atual['question'], 150, 250, 40, (255, 255, 255))
        desenhar_opcoes(opcoes_atual, 150, 500, 40)

    # Exibe a pergunta e as opções, se existir
    if resposta_dada and seleção_escolhida:
        resposta_correta = verificar_resposta(pergunta_atual, seleção_escolhida)
        if resposta_correta:
            mensagem_erro = "Resposta Correta!"
        else:
            mensagem_erro = "Resposta Errada!"  

        if dado_rolado:
            desenhar_texto(f"Dado parou em: {dado_resultado}", 150, 370, 40, (0,0,0)) # Exibe a mensagem de erro
            desenhar_texto("Clique para mover.", 150, 400, 40, (0,0,0))

        # Mostrar jogador atual
        desenhar_texto(f"{players[current_player_index].nome} é o jogador atual", 200, 1000) # Exibe mensagem de erro

        # Mostrar mensagem de erro, se houver
        if mensagem_erro:
            desenhar_texto(mensagem_erro, 150, 450, 40, cor_mensagem)

    # Desenhar todos os jogadores na tela
    for player in players:
        desenhar_player(player) # Desenha cada jogador no tabuleiro

    pygame.display.flip()

pygame.quit()