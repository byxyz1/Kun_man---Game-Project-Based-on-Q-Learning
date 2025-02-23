import os
import sys
import pygame
import Levels
import numpy as np
import pickle

# Define colors and file paths
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
SKYBLUE = (0, 191, 255)
BGMPATH = os.path.join(os.getcwd(), 'resources/sounds/bgm.mp3')
ICONPATH = os.path.join(os.getcwd(), 'resources/images/ikun.png')
FONTPATH = os.path.join(os.getcwd(), 'resources/font/ALGER.TTF')
HEROPATH = os.path.join(os.getcwd(), 'resources/images/ball.png')
BlinkyPATH = os.path.join(os.getcwd(), 'resources/images/Blinky.png')
ClydePATH = os.path.join(os.getcwd(), 'resources/images/Clyde.png')
InkyPATH = os.path.join(os.getcwd(), 'resources/images/Inky.png')
PinkyPATH = os.path.join(os.getcwd(), 'resources/images/Pinky.png')

# Define actions
ACTIONS = ['left', 'right', 'up', 'down']

# Q - learning parameters
ALPHA = 0.1  # Learning rate
GAMMA = 0.9  # Discount factor
INITIAL_EPSILON = 0.9  # Initial exploration rate
EPSILON_DECAY = 0.05  # Exploration rate decay value
MIN_EPSILON = 0.1  # Minimum exploration rate
DECAY_INTERVAL = 10  # Exploration rate decay interval (decay once every DECAY_INTERVAL training sessions)

# Extra bonus for clearing the level
WIN_BONUS = 2000
# Maximum number of steps without eating a bean
NO_BEAN_STEPS_LIMIT = 10
# Penalty score for not eating a bean
NO_BEAN_PENALTY = 10
# Maximum number of steps limit
MAX_STEPS = 10000

def get_state(hero_sprites, ghost_sprites, food_sprites):
    """
    Generate the current game state based on the positions of the hero, ghosts, and food.
    :param hero_sprites: Sprite group of the hero
    :param ghost_sprites: Sprite group of the ghosts
    :param food_sprites: Sprite group of the food
    :return: A tuple representing the current game state
    """
    hero_positions = [[hero.rect.x, hero.rect.y] for hero in hero_sprites]
    hero_pos = hero_positions[0]
    ghost_pos = [[ghost.rect.x, ghost.rect.y] for ghost in ghost_sprites]
    food_count = len(food_sprites)
    state = (tuple(hero_pos), tuple(map(tuple, ghost_pos)), food_count)
    return state

def choose_action(state, q_table, epsilon):
    """
    Choose an action based on the current state, Q-table, and exploration rate.
    :param state: The current game state
    :param q_table: The Q-table
    :param epsilon: The exploration rate
    :return: The chosen action
    """
    if np.random.uniform(0, 1) < epsilon:
        # Exploration: randomly choose an action
        action = np.random.choice(ACTIONS)
    else:
        # Exploitation: choose the action with the maximum Q-value
        if state not in q_table:
            q_table[state] = {action: 0 for action in ACTIONS}
        action_values = q_table[state]
        action = max(action_values, key=action_values.get)
    return action

def get_reward(food_eaten, hero_ghost_collision, is_clearance=False, no_bean_penalty=False, steps_exceeded=False):
    if hero_ghost_collision:
        return -100  # Collide with a ghost, give a negative reward
    elif food_eaten:
        return 10  # Eat food, give a positive reward
    elif is_clearance:
        return WIN_BONUS  # Extra bonus for clearing the level
    elif no_bean_penalty:
        return -NO_BEAN_PENALTY  # Penalty for not eating a bean
    elif steps_exceeded:
        return -100  # Exceed the maximum number of steps, give a negative reward
    else:
        return -1  # Other situations, give a small negative reward

def update_q_table(q_table, state, action, reward, next_state):
    """
    Update the Q-table based on the current state, action, reward, and next state.
    :param q_table: The Q-table
    :param state: The current game state
    :param action: The chosen action
    :param reward: The calculated reward
    :param next_state: The next game state
    """
    if state not in q_table:
        q_table[state] = {action: 0 for action in ACTIONS}
    if next_state not in q_table:
        q_table[next_state] = {action: 0 for action in ACTIONS}
    max_q_next = max(q_table[next_state].values())
    q_table[state][action] += ALPHA * (reward + GAMMA * max_q_next - q_table[state][action])

def startLevelGame(level, screen, font, q_table, epsilon):
    """
    Start a level of the game.
    :param level: The current level object
    :param screen: The game screen
    :param font: The font object
    :param q_table: The Q-table
    :param epsilon: The exploration rate
    :return: Whether the level has been cleared and the updated Q-table
    """
    clock = pygame.time.Clock()
    SCORE = 0
    wall_sprites = level.setupWalls(SKYBLUE)
    gate_sprites = level.setupGate(WHITE)
    hero_sprites, ghost_sprites = level.setupPlayers(HEROPATH, [BlinkyPATH, ClydePATH, InkyPATH, PinkyPATH])
    food_sprites = level.setupFood(YELLOW, WHITE)
    is_clearance = False
    no_bean_steps = 0  # Number of consecutive steps without eating a bean
    steps = 0  # Step counter

    while True:
        steps += 1
        if steps > MAX_STEPS:
            is_clearance = False
            break

        state = get_state(hero_sprites, ghost_sprites, food_sprites)
        action = choose_action(state, q_table, epsilon)

        # Update the player's speed based on the action
        if action == 'left':
            for hero in hero_sprites:
                hero.changeSpeed([-1, 0])
                hero.is_move = True
        elif action == 'right':
            for hero in hero_sprites:
                hero.changeSpeed([1, 0])
                hero.is_move = True
        elif action == 'up':
            for hero in hero_sprites:
                hero.changeSpeed([0, -1])
                hero.is_move = True
        elif action == 'down':
            for hero in hero_sprites:
                hero.changeSpeed([0, 1])
                hero.is_move = True

        screen.fill(BLACK)
        for hero in hero_sprites:
            hero.update(wall_sprites, gate_sprites)
        hero_sprites.draw(screen)

        food_eaten = []
        for hero in hero_sprites:
            food_eaten.extend(pygame.sprite.spritecollide(hero, food_sprites, True))
        if food_eaten:
            no_bean_steps = 0  # Reset the step counter if a bean is eaten
            SCORE += len(food_eaten) * 10
        else:
            no_bean_steps += 1  # Increment the step counter if no bean is eaten

        if no_bean_steps >= NO_BEAN_STEPS_LIMIT:
            SCORE -= NO_BEAN_PENALTY
            no_bean_steps = 0  # Reset the step counter

        wall_sprites.draw(screen)
        gate_sprites.draw(screen)
        food_sprites.draw(screen)

        for ghost in ghost_sprites:
            if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
                ghost.tracks_loc[1] += 1
            else:
                if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
                    ghost.tracks_loc[0] += 1
                elif ghost.role_name == 'Clyde':
                    ghost.tracks_loc[0] = 2
                else:
                    ghost.tracks_loc[0] = 0
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
                ghost.tracks_loc[1] = 0
            ghost.update(wall_sprites, None)
        ghost_sprites.draw(screen)

        score_text = font.render("Score: %s" % SCORE, True, RED)
        screen.blit(score_text, [10, 10])

        hero_ghost_collision = pygame.sprite.groupcollide(hero_sprites, ghost_sprites, False, False)
        next_state = get_state(hero_sprites, ghost_sprites, food_sprites)

        if len(food_sprites) == 0:
            is_clearance = True
            SCORE += WIN_BONUS  # Update the score display
            score_text = font.render("Score: %s" % SCORE, True, RED)
            screen.blit(score_text, [10, 10])
            pygame.display.flip()

        no_bean_penalty = no_bean_steps >= NO_BEAN_STEPS_LIMIT
        steps_exceeded = steps > MAX_STEPS
        reward = get_reward(food_eaten, hero_ghost_collision, is_clearance, no_bean_penalty, steps_exceeded)
        update_q_table(q_table, state, action, reward, next_state)

        if len(food_sprites) == 0:
            is_clearance = True
            break
        if hero_ghost_collision:
            is_clearance = False
            break

        pygame.display.flip()
        clock.tick(10)

    return is_clearance, q_table

def showText(screen, font, is_clearance, flag=False, auto_restart=False):
    """
    Show text messages when the game is over.
    :param screen: The game screen
    :param font: The font object
    :param is_clearance: Whether the level has been cleared
    :param flag: A flag indicating a certain condition
    :param auto_restart: Whether to automatically restart the game
    :return: A boolean indicating whether to restart the game
    """
    clock = pygame.time.Clock()
    msg = 'Game Over!' if not is_clearance else 'Congratulations, you won!'
    positions = [[235, 233], [65, 303], [170, 333]] if not is_clearance else [[145, 233], [65, 303], [170, 333]]
    surface = pygame.Surface((400, 200))
    surface.set_alpha(10)
    surface.fill((128, 128, 128))
    screen.blit(surface, (100, 200))
    texts = [font.render(msg, True, WHITE),
             font.render('Press ENTER to continue or play again.', True, WHITE),
             font.render('Press ESCAPE to quit.', True, WHITE)]
    if auto_restart:
        # Simulate pressing the Enter key
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        pygame.event.post(event)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if is_clearance:
                        if not flag:
                            return
                        else:
                            return True
                    else:
                        return True
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
                    pygame.quit()
        for idx, (text, position) in enumerate(zip(texts, positions)):
            screen.blit(text, position)
        pygame.display.flip()
        clock.tick(10)

def initialize():
    """
    Initialize the Pygame environment and set up the game window.
    :return: The game screen object
    """
    pygame.init()
    icon_image = pygame.image.load(ICONPATH)
    pygame.display.set_icon(icon_image)
    screen = pygame.display.set_mode([606, 606])
    pygame.display.set_caption('kun_man')
    return screen

def save_q_table(q_table, episode):
    """
    Save the Q-table to a file.
    :param q_table: The Q-table
    :param episode: The current episode number
    """
    results_dir = os.path.join(os.getcwd(), 'results')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    filename = os.path.join(results_dir, f'{episode}.pkl')
    with open(filename, 'wb') as f:
        pickle.dump(q_table, f)
    print(f"Q-table saved to {filename}")

def test(screen, num_episodes=500):
    """
    Conduct multiple episodes of game training.
    :param screen: The game screen
    :param num_episodes: The number of episodes to train
    """
    pygame.mixer.init()
    pygame.mixer.music.load(BGMPATH)
    pygame.mixer.music.play(-1, 0.0)
    pygame.font.init()
    font_small = pygame.font.Font(FONTPATH, 18)
    font_big = pygame.font.Font(FONTPATH, 24)
    q_table = {}
    epsilon = INITIAL_EPSILON

    for episode in range(num_episodes):
        level = Levels.Level1()
        is_clearance, q_table = startLevelGame(level, screen, font_small, q_table, epsilon)

        if (episode + 1) % 50 == 0:
            save_q_table(q_table, episode + 1)

        # 每 DECAY_INTERVAL 次训练更新一次探索率
        if (episode + 1) % DECAY_INTERVAL == 0 and epsilon > MIN_EPSILON:
            epsilon = max(epsilon - EPSILON_DECAY, MIN_EPSILON)

        if episode < num_episodes - 1:
            # 除了最后一轮，其他轮次自动重启
            restart = showText(screen, font_big, is_clearance, True, auto_restart=True)
        else:
            restart = showText(screen, font_big, is_clearance, True)
        if not restart:
            break

if __name__ == '__main__':
    screen = initialize()
    test(screen, num_episodes=500)