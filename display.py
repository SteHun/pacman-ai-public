import sys, pygame
import game
from os import path
from time import time, sleep

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#MAKE SURE TO MULTIPLY POSITIONS BY SIZE_MULTIPLIER WHEN FINALIZING
class Window:
    def __init__(self, game_object, size_multiplier=2, show_targets=False):
        pygame.init()
        self.game_object = game_object
        self.size_multiplier = size_multiplier
        self.show_targets = show_targets

        self.font = pygame.font.Font("pacfont.ttf", 20)
        self.previous_score = self.game_object.player.score
        self.score_text = self.font.render(str(self.previous_score), True, (255, 255, 255))
        self.score_text_rect = self.score_text.get_rect()
        self.key_pressed = game.directions.left
        self.tile_width_height = 8 * self.size_multiplier
        self.sprite_width_height = 16 * self.size_multiplier
        self.width = 224
        self.height = 288
        self.fill_color = (0, 0, 0)
        self.fruit_position = self.get_fruit_position((self.game_object.tile_to_left_of_fruit[0] + 0.5, self.game_object.tile_to_left_of_fruit[1]))
        number_of_fruits = 8
        number_of_sprites_per_enemy_type = 4
        scared_blue_enemy_sprite_position = (0, 4)
        scared_white_enemy_sprite_position = (1, 4)

        self.dot_map = [[item == game.maze.dot or item == game.maze.power for item in row] for row in self.game_object.maze]

        self.size = self.width, self.height = self.width*self.size_multiplier, self.height*self.size_multiplier

        self.screen = pygame.display.set_mode(self.size)

        #lambdas
        enlarge_image = lambda image, factor : pygame.transform.scale(image, (image.get_width()*factor, image.get_height()*factor))
        get_rect = lambda x_cord, y_cord : (self.sprite_width_height*x_cord, self.sprite_width_height*y_cord, self.sprite_width_height, self.sprite_width_height)
        self.scale_position = lambda x_pos, y_pos : tuple([(i * self.size_multiplier) - self.sprite_width_height / 2 for i in (x_pos, y_pos)])

        #load background
        self.bg = pygame.image.load(path.join("images", "maze.png"))
        self.bg = enlarge_image(self.bg, self.size_multiplier).convert()


        #load player
        player_right = enlarge_image(pygame.image.load(path.join("images", "pacman.png")), self.size_multiplier)
        player_up = pygame.transform.rotate(player_right, 90)
        player_left = pygame.transform.flip(player_right, True, False)
        player_down = pygame.transform.flip(player_up, False, True)
        self.player_sprites = (player_up, player_down, player_left, player_right)

        #load enemies
        self.enemy_sheet = enlarge_image(pygame.image.load(path.join("images", "enemies.png")), self.size_multiplier)

        self.blinky_rects = tuple([get_rect(i, 0) for i in range(number_of_sprites_per_enemy_type)])
        self.pinky_rects = tuple([get_rect(i, 1) for i in range(number_of_sprites_per_enemy_type)])
        self.inky_rects = tuple([get_rect(i, 2) for i in range(number_of_sprites_per_enemy_type)])
        self.clyde_rects = tuple([get_rect(i, 3) for i in range(number_of_sprites_per_enemy_type)])

        self.scared_blue_rect = get_rect(*scared_blue_enemy_sprite_position)
        self.scared_white_rect = get_rect(*scared_white_enemy_sprite_position)

        #load fruits
        self.fruit_sheet = enlarge_image(pygame.image.load(path.join("images", "fruit.png")), self.size_multiplier)
        self.fruit_rects = tuple([get_rect(i, 0) for i in range(number_of_fruits + 1)])

    def refresh(self):
        if self.previous_score != self.game_object.player.score:
            self.previous_score = self.game_object.player.score
            self.score_text = self.font.render(str(self.previous_score), True, (255, 255, 255))
            self.score_text_rect = self.score_text.get_rect()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.key_pressed = game.directions.up
                elif event.key == pygame.K_DOWN:
                    self.key_pressed = game.directions.down
                elif event.key == pygame.K_LEFT:
                    self.key_pressed = game.directions.left
                elif event.key == pygame.K_RIGHT:
                    self.key_pressed = game.directions.right
        
        
        for row_index, row in enumerate(self.game_object.maze):
            for item_index, item in enumerate(row):
                if item != game.maze.empty or self.dot_map[row_index][item_index] == False: continue
                self.dot_map[row_index][item_index] = False
                pygame.draw.rect(self.bg, self.fill_color, (self.tile_width_height * item_index, self.tile_width_height * row_index, self.tile_width_height, self.tile_width_height))

        self.screen.blit(self.bg, (0, 0))

        self.screen.blit(self.score_text, self.score_text_rect)


        self.screen.blit(self.player_sprites[self.game_object.player.direction], self.scale_position(self.game_object.player.x_pos, self.game_object.player.y_pos))

        if self.game_object.active_fruit != game.fruits.none:
            self.screen.blit(self.fruit_sheet, self.fruit_position, area=self.fruit_rects[self.game_object.active_fruit])
        for enemy in self.game_object.enemies:
            if enemy.is_eaten:
                self.screen.blit(self.enemy_sheet, self.scale_position(enemy.x_pos, enemy.y_pos), area=self.scared_white_rect)
            elif enemy.is_scared:
                self.screen.blit(self.enemy_sheet, self.scale_position(enemy.x_pos, enemy.y_pos), area=self.scared_blue_rect)
            elif type(enemy) == game.Blinky:
                self.screen.blit(self.enemy_sheet, self.scale_position(enemy.x_pos, enemy.y_pos), area=self.blinky_rects[enemy.direction])
            elif type(enemy) == game.Pinky:
                self.screen.blit(self.enemy_sheet, self.scale_position(enemy.x_pos, enemy.y_pos), area=self.pinky_rects[enemy.direction])
            elif type(enemy) == game.Inky:
                self.screen.blit(self.enemy_sheet, self.scale_position(enemy.x_pos, enemy.y_pos), area=self.inky_rects[enemy.direction])
            elif type(enemy) == game.Clyde:
                self.screen.blit(self.enemy_sheet, self.scale_position(enemy.x_pos, enemy.y_pos), area=self.clyde_rects[enemy.direction])

        if self.show_targets:
            twh = self.game_object.tile_width_height
            for enemy in self.game_object.enemies:
                if type(enemy) == game.Blinky:  color = (255, 0, 0)
                elif type(enemy) == game.Pinky: color = (255, 105, 180)
                elif type(enemy) == game.Inky:    color = (0, 255, 255)
                elif type(enemy) == game.Clyde: color = (255, 156, 0)
                
                pygame.draw.rect(self.screen, color, pygame.Rect(
                    enemy.target_x*twh*self.size_multiplier, enemy.target_y*twh*self.size_multiplier, twh*self.size_multiplier, twh*self.size_multiplier
                ))

        pygame.display.flip()

    def get_fruit_position(self, position):
        center = tuple([i * self.tile_width_height + self.tile_width_height / 2 for i in position])
        return tuple([i - self.sprite_width_height / 2 for i in center])

    def close_window(self):
        pygame.display.quit()
        pygame.quit()