import pygame
from map import *
from settings import *
from timer import Timer
from time import time
from copy import deepcopy

class TableGame:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_maps = [map1, map2, map3, map4, map5, map6, map7]
        self.name_maps = ['Tradicional', 'Losango', 'Piramide', 'Flecha', 'Banquinho', 'Mais', 'Cruz']
        self.id_map = 0
        self.set_map()
        self.selected_piece = [] #j/i
        self.selected = False
        self.start = False
        # timer
        self.start_time = 0
        self.atual_time = 0
        # font
        self.font = pygame.font.Font('font/Pixeltype.ttf', 25)
        # surfaces
        self.surf = pygame.Surface((tile_size, tile_size))
        self.surf.fill('gray')
        self.v_line = pygame.Surface((2, tile_size))
        self.h_line = pygame.Surface((tile_size, 2))
        self.v_line.fill('red')
        self.h_line.fill('red')
        # images
        ball = pygame.image.load('img/ball.png').convert_alpha()
        self.ball = pygame.transform.scale(ball, (tile_size, tile_size))
        empty_ball = pygame.image.load('img/eball.png').convert_alpha()
        self.empty_ball = pygame.transform.scale(empty_ball, (tile_size, tile_size))
        select_ball = pygame.image.load('img/selball.png').convert_alpha()
        self.select_ball = pygame.transform.scale(select_ball, (tile_size, tile_size))
        # collisions
        self.start_retry_surf = pygame.Surface((tile_size * 1.5, tile_size - 16))
        self.start_retry_rect = self.start_retry_surf.get_rect(topleft= (10, screen_height - (tile_size - 8)))
        self.sel_map_surf = pygame.Surface(((tile_size * 4), tile_size - 16))
        self.sel_map_rect = self.sel_map_surf.get_rect(topleft= ((tile_size * 2.5) + 5, screen_height - (tile_size - 8)))
        # mouse
        self.mouse_surf = pygame.Surface((5, 5))
        self.mouse_rect = self.mouse_surf.get_rect(center= (0, 0))
        self.mouse_timer = Timer(0.2)

    def set_map(self):
        self.map = deepcopy(self.all_maps[self.id_map])
    
    def unselect(self):
        self.selected_piece = [] #j/i
        self.selected = False

    def start_timer(self):
        self.start_time = time()
        self.atual_time = self.start_time

    def blit_text(self, text, pos, color='black', center=False):
        text_surf = self.font.render(text, False, color)
        if not center:
            text_rect = text_surf.get_rect(topright= (pos))
        else:
            text_rect = text_surf.get_rect(center= (pos))
        self.display_surface.blit(text_surf, text_rect)

    def blit_shadow_text(self, text, pos, color, back_color='black', center=False):
        self.blit_text(text, [pos[0] + 1, pos[1] + 1], back_color, center)
        self.blit_text(text, [pos[0] - 1, pos[1] - 1], back_color, center)
        self.blit_text(text, pos, color, center)

    def retry(self):
        self.set_map()
        self.start_time = self.atual_time
        self.unselect()
        self.start = False

    def check_moves(self, index):
        # verifica se há como mover a peça selecionada
        num = self.map[index[1]][index[0]]
        moves = [False, False, False, False]
        if num == 1:
            # verifica se há alguma bola por perto e se há espaço livre nele
            if self.map[index[1]][index[0] - 1] == 1 and self.map[index[1]][index[0] - 2] == 0: # up
                moves[0] = True
            elif self.map[index[1]][index[0] + 1] == 1 and self.map[index[1]][index[0] + 2] == 0: # down
                moves[1] = True
            elif self.map[index[1] + 1][index[0]] == 1 and self.map[index[1] + 2][index[0]] == 0: # right
                moves[2] = True
            elif self.map[index[1] - 1][index[0]] == 1 and self.map[index[1] - 2][index[0]] == 0: # left
                moves[3] = True
            if moves[0] or moves[1] or moves[2] or moves[3]:
                return True
        return False

    def check_end(self):
        # verifica todas as peças se há como mover pelo menos uma
        for j, col in enumerate(self.map):
            for i, num in enumerate(col):
               if num == 1:
                   if self.check_moves([i, j]):
                       return False
        return True

    def move(self, mouse_pos):
        # movimenta a peça selecionada no local desejado
        if (mouse_pos[0] + 2) == self.selected_piece[0]: #left
            self.map[mouse_pos[1]][mouse_pos[0]+1] = 0
        elif (mouse_pos[0] - 2) == self.selected_piece[0]: #right
            self.map[mouse_pos[1]][mouse_pos[0]-1] = 0
        elif (mouse_pos[1] + 2) == self.selected_piece[1]: #up
            self.map[mouse_pos[1]+1][mouse_pos[0]] = 0
        elif (mouse_pos[1] - 2) == self.selected_piece[1]: #down
            self.map[mouse_pos[1]-1][mouse_pos[0]] = 0

        self.map[self.selected_piece[1]][self.selected_piece[0]] = 0
        self.map[mouse_pos[1]][mouse_pos[0]] = 1
        self.selected_piece = []
        self.selected = False        
    
    def input(self):
        if not self.mouse_timer.run:
            if pygame.mouse.get_pressed()[0]:
                self.mouse_rect.center = pygame.mouse.get_pos()
                if self.mouse_rect.colliderect(self.start_retry_rect):
                    if self.start:
                        self.retry()
                    else:
                        self.set_map()
                        self.start = True
                        self.start_timer()
                elif self.mouse_rect.colliderect(self.sel_map_rect):
                    if not self.start:
                        self.id_map = self.id_map + 1 if self.id_map < len(self.all_maps)-1 else 0
                        self.set_map()

                if self.start:
                    mouse_pos = [int(pygame.mouse.get_pos()[0]/tile_size) + 1, int(pygame.mouse.get_pos()[1]/tile_size) + 1]
                    if self.selected:
                        if self.map[mouse_pos[1]][mouse_pos[0]] == 0 and (mouse_pos[0] + 2 == self.selected_piece[0] or mouse_pos[0] - 2 == self.selected_piece[0] or mouse_pos[1] + 2 == self.selected_piece[1] or mouse_pos[1] - 2 == self.selected_piece[1]):
                            self.move(mouse_pos)
                            if self.check_end():
                                self.start = False
                        else:
                            self.unselect()
                    else:
                        if self.check_moves(mouse_pos):
                            self.selected_piece = mouse_pos[:]
                            self.selected = True
                        else:
                            self.unselect()
            
                self.mouse_timer.active()

    def update(self):
        if self.mouse_timer.run:
            self.mouse_timer.update()
        if self.start:
            self.atual_time = time()
        self.blit_text(f'Time: {round(self.atual_time - self.start_time)}', (screen_width - 10, 10))
        self.input()

    def draw_map(self):
        for j, col in enumerate(self.map):
            for i, num in enumerate(col):
                if i == 0 or i == len(self.map[0])-1 or j == 0 or j == len(self.map)-1:
                    continue

                x = (i-1) * tile_size
                y = (j-1) * tile_size

                if num == 0:
                    self.display_surface.blit(self.empty_ball, (x, y))
                    if self.selected:
                        if j == self.selected_piece[1] and i == self.selected_piece[0] + 2:
                            if self.map[self.selected_piece[1]][self.selected_piece[0]+1] == 1:
                                self.display_surface.blit(self.select_ball, (x, y))
                        elif j == self.selected_piece[1] and i == self.selected_piece[0] - 2:
                            if self.map[self.selected_piece[1]][self.selected_piece[0]-1] == 1:
                                self.display_surface.blit(self.select_ball, (x, y))
                        elif j == self.selected_piece[1] + 2 and i == self.selected_piece[0]:
                            if self.map[self.selected_piece[1]+1][self.selected_piece[0]] == 1:
                                self.display_surface.blit(self.select_ball, (x, y))
                        elif j == self.selected_piece[1] - 2 and i == self.selected_piece[0]:
                            if self.map[self.selected_piece[1]-1][self.selected_piece[0]] == 1:
                                self.display_surface.blit(self.select_ball, (x, y))
                elif num == 1:
                    self.display_surface.blit(self.ball, (x, y))
                elif num == -1:
                    self.display_surface.blit(self.surf, (x, y))
                
                self.display_surface.blit(self.v_line, (x, y))
                self.display_surface.blit(self.h_line, (x, y))
                self.display_surface.blit(self.v_line, (x + tile_size, y))
                self.display_surface.blit(self.h_line, (x, y + tile_size))

    def draw_bottom(self):
        pygame.draw.rect(self.display_surface, 'gray', [0, screen_height - tile_size, screen_width, tile_size]) 
        pygame.draw.rect(self.display_surface, 'red', [0, screen_height - tile_size, screen_width, tile_size], 3)
        pygame.draw.rect(self.display_surface, 'black', [2, screen_height - (tile_size - 2), screen_width - 4, tile_size - 4], 3) 

        self.display_surface.blit(self.start_retry_surf, self.start_retry_rect)
        self.display_surface.blit(self.sel_map_surf, self.sel_map_rect)
        pygame.draw.rect(self.display_surface, 'red', [self.start_retry_rect.topleft[0], self.start_retry_rect.topleft[1], self.start_retry_rect.width, self.start_retry_rect.height], 3) 
        pygame.draw.rect(self.display_surface, 'red' if not self.start else 'white', [self.sel_map_rect.topleft[0], self.sel_map_rect.topleft[1], self.sel_map_rect.width, self.sel_map_rect.height], 3) 


        self.blit_shadow_text('Start' if not self.start else 'Retry', self.start_retry_rect.center, 'white', back_color= 'red', center= True)
        self.blit_shadow_text(f'{self.name_maps[self.id_map]}', self.sel_map_rect.center, 'white', back_color= 'red', center= True)
    
    def draw(self):
        self.draw_bottom()
        self.draw_map()

    