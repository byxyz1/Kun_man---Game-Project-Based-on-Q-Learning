import random
import pygame

# Wall class
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, **kwargs):
        # Initialize the parent class
        pygame.sprite.Sprite.__init__(self)
        # Create a surface with the specified width and height
        self.image = pygame.Surface([width, height])
        # Fill the surface with the specified color
        self.image.fill(color)
        # Get the rectangle object of the surface
        self.rect = self.image.get_rect()
        # Set the left position of the rectangle
        self.rect.left = x
        # Set the top position of the rectangle
        self.rect.top = y

# Food class
class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, bg_color, **kwargs):
        # Initialize the parent class
        pygame.sprite.Sprite.__init__(self)
        # Create a surface with the specified width and height
        self.image = pygame.Surface([width, height])
        # Fill the surface with the background color
        self.image.fill(bg_color)
        # Set the background color as the transparent color
        self.image.set_colorkey(bg_color)
        # Draw an ellipse on the surface with the specified color
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        # Get the rectangle object of the surface
        self.rect = self.image.get_rect()
        # Set the left position of the rectangle
        self.rect.left = x
        # Set the top position of the rectangle
        self.rect.top = y

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, role_image_path):
        # Initialize the parent class
        pygame.sprite.Sprite.__init__(self)
        # Get the role name from the image path
        self.role_name = role_image_path.split('/')[-1].split('.')[0]
        # Load the role image and convert it
        self.base_image = pygame.image.load(role_image_path).convert()
        # Make a copy of the base image
        self.image = self.base_image.copy()
        # Get the rectangle object of the image
        self.rect = self.image.get_rect()
        # Set the left position of the rectangle
        self.rect.left = x
        # Set the top position of the rectangle
        self.rect.top = y
        # Store the previous x position
        self.prev_x = x
        # Store the previous y position
        self.prev_y = y
        # Set the base speed of the player
        self.base_speed = [30, 30]
        # Set the initial speed of the player
        self.speed = [0, 0]
        # Set the initial movement state of the player
        self.is_move = False
        # Initialize the tracks list
        self.tracks = []
        # Initialize the tracks location
        self.tracks_loc = [0, 0]

    # Change the speed direction of the player
    def changeSpeed(self, direction):
        if direction[0] < 0:
            # Flip the base image horizontally
            self.image = pygame.transform.flip(self.base_image, True, False)
        elif direction[0] > 0:
            # Use the base image
            self.image = self.base_image.copy()
        elif direction[1] < 0:
            # Rotate the base image 90 degrees counterclockwise
            self.image = pygame.transform.rotate(self.base_image, 90)
        elif direction[1] > 0:
            # Rotate the base image 90 degrees clockwise
            self.image = pygame.transform.rotate(self.base_image, -90)
        # Calculate the new speed
        self.speed = [direction[0] * self.base_speed[0], direction[1] * self.base_speed[1]]
        return self.speed

    # Update the position of the player
    def update(self, wall_sprites, gate_sprites):
        if not self.is_move:
            return False
        # Store the previous x position
        x_prev = self.rect.left
        # Store the previous y position
        y_prev = self.rect.top
        # Update the x position
        self.rect.left += self.speed[0]
        # Update the y position
        self.rect.top += self.speed[1]
        # Check if the player collides with the walls
        is_collide = pygame.sprite.spritecollide(self, wall_sprites, False)
        if gate_sprites is not None:
            if not is_collide:
                # Check if the player collides with the gates
                is_collide = pygame.sprite.spritecollide(self, gate_sprites, False)
        if is_collide:
            # Restore the previous x position
            self.rect.left = x_prev
            # Restore the previous y position
            self.rect.top = y_prev
            return False
        return True

    # Generate a random direction
    def randomDirection(self):
        return random.choice([[-0.5, 0], [0.5, 0], [0, 0.5], [0, -0.5]])