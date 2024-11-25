# lutador.py
import pygame

class Lutador:
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 120, 96))  # Dimensões ajustadas
        self.saude = 100
        self.img_index = 0
        self.atc_index = 0
        self.velocidade = 10
        self.gravidade = 2  # Gravidade mais natural
        self.vel_y = 0  # Velocidade vertical
        self.no_ar = False
        self.chao = 320  # Define o limite do chão

    def desenhar(self, tela, lutador, oponente, animacoes, som):
        # Animação padrão (idle)
        lutador_img = animacoes['idle'][self.img_index]
        self.img_index += 1
        if self.img_index >= len(animacoes['idle']):
            self.img_index = 0

        # Controles de movimento
        key = pygame.key.get_pressed()

        # Esquerda
        if (key[pygame.K_a] and lutador == 1) or (key[pygame.K_LEFT] and lutador == 2):
            lutador_img = animacoes['run'][self.img_index % len(animacoes['run'])]
            self.rect.x -= self.velocidade
            self.rect.x = max(self.rect.x, 0)  # Limita à borda esquerda

        # Direita
        if (key[pygame.K_d] and lutador == 1) or (key[pygame.K_RIGHT] and lutador == 2):
            lutador_img = animacoes['run'][self.img_index % len(animacoes['run'])]
            self.rect.x += self.velocidade
            self.rect.x = min(self.rect.x, tela.get_width() - self.rect.width)  # Limita à borda direita

        # Gravidade e queda
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y

        # Colisão com o chão
        if self.rect.y >= self.chao:
            self.rect.y = self.chao
            self.vel_y = 0
            self.no_ar = False
        else:
            self.no_ar = True

        # Pular
        if ((key[pygame.K_w] and lutador == 1) or (key[pygame.K_UP] and lutador == 2)) and not self.no_ar:
            lutador_img = animacoes['jump'][0]
            self.vel_y = -40  # Velocidade inicial do salto
            self.no_ar = True

        # Ataque
        if self.atc_index > 0:
            if self.atc_index < len(animacoes['attack']):
                lutador_img = animacoes['attack'][self.atc_index]
                self.atc_index += 1
            else:
                self.atc_index = 0

        if ((key[pygame.K_s] and lutador == 1) or (key[pygame.K_DOWN] and lutador == 2)) and self.atc_index == 0:
            som.play()
            self.atc_index = 1
            if self.rect.centerx < oponente.rect.centerx:
                ataque = pygame.Rect(self.rect.right, self.rect.y, 80, 96)
            else:
                ataque = pygame.Rect(self.rect.left - 80, self.rect.y, 80, 96)

            if ataque.colliderect(oponente.rect) and oponente.atc_index == 0:
                oponente.saude -= 10

        # Inverter imagem se necessário
        if self.rect.centerx > oponente.rect.centerx:
            lutador_img = pygame.transform.flip(lutador_img, True, False)

        # Desenhar o lutador
        tela.blit(lutador_img, (self.rect.x - 60, self.rect.y - 64))
