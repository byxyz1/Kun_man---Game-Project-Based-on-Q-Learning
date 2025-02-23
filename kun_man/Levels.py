import pygame
from Sprites import *

# Define the number of levels in the game
NUMLEVELS = 1


# LV1
class Level1():
    def __init__(self):
        # Initialize level information
        self.info = 'level1'

    # Create walls
    def setupWalls(self, wall_color):
        # Create a sprite group for walls
        self.wall_sprites = pygame.sprite.Group()
        # Define wall positions
        wall_positions = [[0, 0, 6, 600],
                          [0, 0, 600, 6],
                          [0, 600, 606, 6],
                          [600, 0, 6, 606],
                          [300, 0, 6, 66],
                          [60, 60, 186, 6],
                          [360, 60, 186, 6],
                          [60, 120, 66, 6],
                          [60, 120, 6, 126],
                          [180, 120, 246, 6],
                          [480, 120, 66, 6],
                          [540, 120, 6, 126],
                          [120, 180, 126, 6],
                          [120, 180, 6, 126],
                          [360, 180, 126, 6],
                          [480, 180, 6, 126],
                          [180, 240, 6, 126],
                          [180, 360, 246, 6],
                          [420, 240, 6, 126],
                          [240, 240, 6, 66],
                          [240, 300, 126, 6],
                          [360, 240, 6, 66],
                          [0, 300, 66, 6],
                          [540, 300, 66, 6],
                          [60, 360, 66, 6],
                          [60, 360, 6, 186],
                          [480, 360, 66, 6],
                          [540, 360, 6, 186],
                          [120, 420, 366, 6],
                          [120, 420, 6, 66],
                          [480, 420, 6, 66],
                          [180, 480, 246, 6],
                          [300, 480, 6, 66],
                          [120, 540, 126, 6],
                          [360, 540, 126, 6]]
        # Create wall sprites and add them to the group
        for wall_position in wall_positions:
            wall = Wall(*wall_position, wall_color)
            self.wall_sprites.add(wall)
        return self.wall_sprites

    # Create the gate
    def setupGate(self, gate_color):
        # Create a sprite group for the gate
        self.gate_sprites = pygame.sprite.Group()
        # Add a gate sprite to the group
        self.gate_sprites.add(Wall(240, 240, 126, 2, gate_color))
        return self.gate_sprites

    # Create players
    def setupPlayers(self, hero_image_path, ghost_images_path):
        # Create a sprite group for the hero
        self.hero_sprites = pygame.sprite.Group()
        # Create a sprite group for ghosts
        self.ghost_sprites = pygame.sprite.Group()
        # Add the hero sprite to the group
        self.hero_sprites.add(Player(287, 439, hero_image_path))
        # Create ghost sprites and add them to the group
        for each in ghost_images_path:
            # Get the role name from the image path
            role_name = each.split('/')[-1].split('.')[0]
            if role_name == 'Blinky':
                player = Player(287, 199, each)
                player.is_move = True
                player.tracks = [[0, -0.5, 4], [0.5, 0, 9], [0, 0.5, 11], [0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 11],
                                 [0, 0.5, 3],
                                 [0.5, 0, 15], [0, -0.5, 15], [0.5, 0, 3], [0, -0.5, 11], [-0.5, 0, 3], [0, -0.5, 11],
                                 [-0.5, 0, 3],
                                 [0, -0.5, 3], [-0.5, 0, 7], [0, -0.5, 3], [0.5, 0, 15], [0, 0.5, 15], [-0.5, 0, 3],
                                 [0, 0.5, 3],
                                 [-0.5, 0, 3], [0, -0.5, 7], [-0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 11], [0, -0.5, 7],
                                 [0.5, 0, 5]]
                self.ghost_sprites.add(player)
            elif role_name == 'Clyde':
                player = Player(319, 259, each)
                player.is_move = True
                player.tracks = [[-1, 0, 2], [0, -0.5, 4], [0.5, 0, 5], [0, 0.5, 7], [-0.5, 0, 11], [0, -0.5, 7],
                                 [-0.5, 0, 3], [0, 0.5, 7], [-0.5, 0, 7], [0, 0.5, 15], [0.5, 0, 15], [0, -0.5, 3],
                                 [-0.5, 0, 11], [0, -0.5, 7], [0.5, 0, 3], [0, -0.5, 11], [0.5, 0, 9]]
                self.ghost_sprites.add(player)
            elif role_name == 'Inky':
                player = Player(255, 259, each)
                player.is_move = True
                player.tracks = [[1, 0, 2], [0, -0.5, 4], [0.5, 0, 10], [0, 0.5, 7], [0.5, 0, 3], [0, -0.5, 3],
                                 [0.5, 0, 3], [0, -0.5, 15], [-0.5, 0, 15], [0, 0.5, 3], [0.5, 0, 15], [0, 0.5, 11],
                                 [-0.5, 0, 3], [0, -0.5, 7], [-0.5, 0, 11], [0, 0.5, 3], [-0.5, 0, 11], [0, 0.5, 7],
                                 [-0.5, 0, 3], [0, -0.5, 3], [-0.5, 0, 3], [0, -0.5, 15], [0.5, 0, 15], [0, 0.5, 3],
                                 [-0.5, 0, 15], [0, 0.5, 11], [0.5, 0, 3], [0, -0.5, 11], [0.5, 0, 11], [0, 0.5, 3],
                                 [0.5, 0, 1]]
                self.ghost_sprites.add(player)
            elif role_name == 'Pinky':
                player = Player(287, 259, each)
                player.is_move = True
                player.tracks = [[0, -1, 4], [0.5, 0, 9], [0, 0.5, 11], [-0.5, 0, 23], [0, 0.5, 7], [0.5, 0, 3],
                                 [0, -0.5, 3], [0.5, 0, 19], [0, 0.5, 3], [0.5, 0, 3], [0, 0.5, 3], [0.5, 0, 3],
                                 [0, -0.5, 15], [-0.5, 0, 7], [0, 0.5, 3], [-0.5, 0, 19], [0, -0.5, 11], [0.5, 0, 9]]
                self.ghost_sprites.add(player)
        return self.hero_sprites, self.ghost_sprites

    # Create food
    def setupFood(self, food_color, bg_color):
        # Create a sprite group for food
        self.food_sprites = pygame.sprite.Group()
        # Create food sprites
        for row in range(19):
            for col in range(19):
                if (row == 7 or row == 8) and (col == 8 or col == 9 or col == 10):
                    continue
                else:
                    food = Food(30 * col + 32, 30 * row + 32, 4, 4, food_color, bg_color)
                    # Check if the food sprite collides with walls
                    is_collide = pygame.sprite.spritecollide(food, self.wall_sprites, False)
                    if is_collide:
                        continue
                    # Check if the food sprite collides with the hero
                    is_collide = pygame.sprite.spritecollide(food, self.hero_sprites, False)
                    if is_collide:
                        continue
                    self.food_sprites.add(food)
        return self.food_sprites