# 🥋 Jogo de Luta 2D com Pygame - Bushido

Este é um projeto de jogo de luta 2D desenvolvido com **Python e Pygame**, onde dois lutadores se enfrentam em uma arena simples com animações, ataques, detecção de colisão e controle de vida. O objetivo é oferecer uma base para estudos em desenvolvimento de jogos com foco em lógica de movimento, física básica, e interação entre personagens.

## 🎮 Funcionalidades

- ✅ Dois lutadores controlados via teclado (WASD e setas).
- ✅ Sistema de animações: idle, corrida, pulo e ataque.
- ✅ Detecção de colisão entre ataques e oponente.
- ✅ Controle de saúde dos personagens.
- ✅ Sistema de gravidade e pulo com física simples.
- ✅ Espelhamento automático do personagem (flip horizontal).
- ✅ Sons de ataque (via mixer do Pygame).

## 🧠 Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [Pygame](https://www.pygame.org/)

## 🗂️ Estrutura do Projeto

- `lutador.py`: classe principal do personagem com movimentação, ataque, animações e física.
- `main.py`: arquivo de inicialização do jogo, carregamento de recursos e loop principal.
- `assets/`: sprites, sons e outros recursos visuais.

## 🚀 Como Executar

1. Instale o Pygame:
   ```bash
   pip install pygame
   ```

2. Execute o jogo:
   ```bash
   python main.py
   ```

## 💡 Melhorias Futuras

- Implementação de barra de vida visual.
- Tela de vitória/derrota.
- IA para um dos lutadores (modo solo).
- Menu inicial e pausa.
- Efeitos visuais e de partículas.

---

> Projeto criado com fins educacionais, ideal para quem está iniciando no desenvolvimento de jogos com Python.
