import pygame

class Jogador:
    def __init__(self, nome="Estudante", genero="neutro"):
        self.nome = nome
        self.genero = genero
        #coordenadaa
        self.player_x = 200
        self.player_y = 300
        self.player_speed = 3
        self.x_direction = 0
        self.y_direction = 0

    def draw_player(self, screen):
        image = animations[direction][current_frame]
        #mostra na tela
        screen.blit(image, (player_x, player_y))

    def movimento(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                x_direction = 1
                direction = 'right'

            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                x_direction = -1
                direction = 'left'

            #as coordenadas 0 comecam no canto esquerdo superior da tela
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                y_direction = -1
                direction = 'up'

            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                y_direction = 1
                direction = 'down'

        if event.type == pygame.KEYUP:
            #qnd nn estiver precionando a tecla
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                x_direction = 0
            
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                x_direction = 0   
            
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                y_direction = 0
            
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                y_direction = 0

    def velocidade(self):
        self.player_x += self.player_speed * self.x_direction
        self.player_y += self.player_speed * self.y_direction
