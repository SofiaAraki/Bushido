import os
import sys
import pygame
from lutador import Lutador

# Função para localizar recursos com segurança no executável
def resource_path(relative_path):
    """Obter o caminho absoluto de um recurso, considerando a execução no PyInstaller."""
    try:
        # Caminho usado pelo PyInstaller
        base_path = sys._MEIPASS
    except AttributeError:
        # Caminho usado durante o desenvolvimento
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Configurações principais
LARGURA = 1200
ALTURA = 800
FPS = 30
pygame.display.set_caption('Bushido')

# Inicialização do Pygame
pygame.mixer.init()
pygame.init()

# Criar a tela e o relógio
tela = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 50)

# Função para carregar os sons
def carregar_sons():
    sons = {
        "musica_selecao": resource_path("audio/music_flauta.mp3"),
        "musica_luta": resource_path("audio/music_banjo.mp3"),
        "selecao": pygame.mixer.Sound(resource_path("audio/selection.mp3")),
        "ataque": pygame.mixer.Sound(resource_path("audio/sword.wav")),
    }
    sons["ataque"].set_volume(0.05)
    return sons

# Carregar sons
sons = carregar_sons()

# Carregar o fundo do jogo
fundo = pygame.image.load(resource_path("imagens/fundo/background.jpg"))

# Função para carregar animações dos personagens
def carregar_imagens(dic, lista):
    for x, tipo in enumerate(dic):
        img_l = lista[x].get_width()
        img_a = lista[x].get_height()
        for i in range(int(img_l / img_a)):
            img = lista[x].subsurface(i * img_a, 0, img_a, img_a)
            dic[tipo].append(pygame.transform.scale(img, (img_a * 4, img_a * 4)))
    return dic

# Definir os personagens
personagens = [
    {"nome": "Samurai Azul", "imagens": resource_path("imagens/samurai_azul/"), "animacoes": None},
    {"nome": "Samurai Vermelho", "imagens": resource_path("imagens/samurai_vermelho/"), "animacoes": None},
    {"nome": "Samurai Branco", "imagens": resource_path("imagens/samurai_branco/"), "animacoes": None},
    {"nome": "Samurai Cinza", "imagens": resource_path("imagens/samurai_cinza/"), "animacoes": None},
]

# Carregar animações para cada personagem
for personagem in personagens:
    lista = [
        pygame.image.load(personagem["imagens"] + "idle.png"),
        pygame.image.load(personagem["imagens"] + "jump.png"),
        pygame.image.load(personagem["imagens"] + "run.png"),
        pygame.image.load(personagem["imagens"] + "attack.png"),
    ]
    dic = {"idle": [], "jump": [], "run": [], "attack": []}
    personagem["animacoes"] = carregar_imagens(dic, lista)

# Função para desenhar o fundo na tela
def desenhar_fundo():
    fundo_ajustado = pygame.transform.scale(fundo, (LARGURA, ALTURA))
    tela.blit(fundo_ajustado, (0, 0))

# Função para desenhar a barra de saúde
def desenhar_saude(saude, x, y):
    taxa = saude / 100
    texto = fonte.render(str(saude), True, (255, 255, 255))
    tela.blit(texto, (x, y + 30))
    pygame.draw.rect(tela, (255, 255, 255), (x - 3, y - 3, 406, 36))
    pygame.draw.rect(tela, (255, 0, 0), (x, y, 400, 30))
    pygame.draw.rect(tela, (0, 255, 0), (x, y, 400 * taxa, 30))

# Função para selecionar os personagens
def selecionar_personagem():
    fundo_selecao = pygame.image.load(resource_path("imagens/fundo/home.jpg"))
    fundo_selecao = pygame.transform.scale(fundo_selecao, (LARGURA, ALTURA))

    opcoes = [
        pygame.transform.scale(pygame.image.load(p["imagens"] + "menu.png"), (200, 200))
        for p in personagens
    ]

    posicoes = [(300, 200), (700, 200), (300, 550), (700, 550)]

    lutador_selecionado = [None, None]
    jogador_atual = 0
    destaque_index = -1

    pygame.mixer.music.load(sons["musica_selecao"])
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    while jogador_atual < 2:
        tela.blit(fundo_selecao, (0, 0))
        texto = fonte.render(
            f"Jogador {jogador_atual + 1}, selecione seu personagem",
            True,
            (255, 255, 255),
        )
        tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 50))

        for i, pos in enumerate(posicoes):
            x, y = pos
            if i == destaque_index:
                pygame.draw.rect(tela, (0, 255, 0), (x - 5, y - 5, 210, 210), 5)
            tela.blit(opcoes[i], pos)

        mouse_pos = pygame.mouse.get_pos()
        destaque_index = -1
        for i, pos in enumerate(posicoes):
            x, y = pos
            if x <= mouse_pos[0] <= x + 200 and y <= mouse_pos[1] <= y + 200:
                destaque_index = i

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and destaque_index != -1:
                sons["selecao"].play()
                lutador_selecionado[jogador_atual] = {
                    "lutador": Lutador(100 if jogador_atual == 0 else 800, 0),
                    "animacoes": personagens[destaque_index]["animacoes"],
                }
                jogador_atual += 1

        pygame.display.update()

    pygame.mixer.music.load(sons["musica_luta"])
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    return lutador_selecionado

# Função para desenhar a tela de vitória com botões de restart ou sair
def tela_vitoria(vencedor):
    fundo_selecao = pygame.image.load(resource_path("imagens/fundo/win.jpg"))
    fundo_selecao = pygame.transform.scale(fundo_selecao, (LARGURA, ALTURA))

    # Desenhar o fundo da tela de vitória
    tela.blit(fundo_selecao, (0, 0))

    # Texto de vitória
    texto_vitoria = fonte.render(f"Vencedor: Jogador {vencedor}", True, (255, 255, 255))
    tela.blit(texto_vitoria, (LARGURA // 2 - texto_vitoria.get_width() // 2, ALTURA // 8 - texto_vitoria.get_height() // 2))

    # Botão de Restart
    botao_restart = pygame.Rect(LARGURA // 2 - 150, ALTURA // 2 + 210, 300, 50)
    pygame.draw.rect(tela, (0, 255, 0), botao_restart)
    texto_restart = fonte.render("Reiniciar", True, (255, 255, 255))
    tela.blit(texto_restart, (LARGURA // 2 - texto_restart.get_width() // 2, ALTURA // 2 + 205))

    # Botão de Sair
    botao_sair = pygame.Rect(LARGURA // 2 - 150, ALTURA // 2 + 270, 300, 50)
    pygame.draw.rect(tela, (255, 0, 0), botao_sair)
    texto_sair = fonte.render("Sair", True, (255, 255, 255))
    tela.blit(texto_sair, (LARGURA // 2 - texto_sair.get_width() // 2, ALTURA // 2 + 265))

    pygame.display.update()

    # Aguardar interação do jogador
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar clique no botão de restart
                if botao_restart.collidepoint(event.pos):
                    return "restart"
                # Verificar clique no botão de sair
                elif botao_sair.collidepoint(event.pos):
                    return "sair"


# Loop principal
def loop_jogo(lutador_1, lutador_2, animacoes_1, animacoes_2):
    jogando = True
    while jogando:
        clock.tick(FPS)
        desenhar_fundo()

        desenhar_saude(lutador_1.saude, 20, 20)
        desenhar_saude(lutador_2.saude, 780, 20)

        lutador_1.desenhar(tela, 1, lutador_2, animacoes_1, sons["ataque"])
        lutador_2.desenhar(tela, 2, lutador_1, animacoes_2, sons["ataque"])

        if lutador_1.saude <= 0:
            resultado = tela_vitoria(2)  # Jogador 2 venceu
            if resultado == "restart":
                return loop_jogo(*selecionar_personagem())  # Reiniciar o jogo
            else:
                return  # Sair do jogo
        elif lutador_2.saude <= 0:
            resultado = tela_vitoria(1)  # Jogador 1 venceu
            if resultado == "restart":
                return loop_jogo(*selecionar_personagem())  # Reiniciar o jogo
            else:
                return  # Sair do jogo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogando = False

        pygame.display.update()

# Iniciar o jogo
lutador_1, lutador_2 = selecionar_personagem()
loop_jogo(lutador_1["lutador"], lutador_2["lutador"], lutador_1["animacoes"], lutador_2["animacoes"])

pygame.quit()
