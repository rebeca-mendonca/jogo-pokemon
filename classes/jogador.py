import pygame

class Jogador:
    def __init__(self):
        #coordenadaa
        self.player_x = 200
        self.player_y = 300
        self.player_speed = 3
        self.x_direction = 0
        self.y_direction = 0

    def draw_player(self, screen):
        #inicio do desenvolvimento do formato do personagem
        pygame.draw.rect(screen, 'gray', [self.player_x, self.player_y, 100, 100], 0, 5)

    def movimento(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                x_direction = 1

            elif event.key == pygame.K_LEFT:
                x_direction = -1    

            #as coordenadas 0 comecam no canto esquerdo superior da tela
            elif event.key == pygame.K_UP:
                y_direction = -1

            elif event.key == pygame.K_DOWN:
                y_direction = 1

        if event.type == pygame.KEYUP:
            #qnd nn estiver precionando a tecla
            if event.key == pygame.K_RIGHT:
                x_direction = 0
            
            elif event.key == pygame.K_LEFT:
                x_direction = 0   
            
            elif event.key == pygame.K_UP:
                y_direction = 0
            
            elif event.key == pygame.K_DOWN:
                y_direction = 0

    def velocidade(self):
        self.player_x += self.player_speed * self.x_direction
        self.player_y += self.player_speed * self.y_direction
