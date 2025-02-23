import os
import sys
import pygame
import Levels
import numpy as np
import pickle
import matplotlib.pyplot as plt
import pyautogui
import time
# cd kun_man
#  python load.py 350
# Define colors and file paths
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
SKYBLUE = (0, 191, 255)
# Path of the background music file
BGMPATH = os.path.join(os.getcwd(), 'resources/sounds/bgm.mp3')
# Path of the game icon file
ICONPATH = os.path.join(os.getcwd(), 'resources/images/ikun.png')
# Path of the font file
FONTPATH = os.path.join(os.getcwd(), 'resources/font/ALGER.TTF')
# Path of the hero image file
HEROPATH = os.path.join(os.getcwd(), 'resources/images/ball.png')
# Path of Blinky's image file
BlinkyPATH = os.path.join(os.getcwd(), 'resources/images/Blinky.png')
# Path of Clyde's image file
ClydePATH = os.path.join(os.getcwd(), 'resources/images/Clyde.png')
# Path of Inky's image file
InkyPATH = os.path.join(os.getcwd(), 'resources/images/Inky.png')
# Path of Pinky's image file
PinkyPATH = os.path.join(os.getcwd(), 'resources/images/Pinky.png')

# Define actions
ACTIONS = ['left', 'right', 'up', 'down']


def get_state(hero_sprites, ghost_sprites, food_sprites):
    """
    Get the current state of the game.

    :param hero_sprites: Sprite group of heroes
    :param ghost_sprites: Sprite group of ghosts
    :param food_sprites: Sprite group of foods
    :return: A tuple representing the state
    """
    hero_positions = [[hero.rect.x, hero.rect.y] for hero in hero_sprites]
    hero_pos = hero_positions[0]
    ghost_pos = [[ghost.rect.x, ghost.rect.y] for ghost in ghost_sprites]
    food_count = len(food_sprites)
    state = (tuple(hero_pos), tuple(map(tuple, ghost_pos)), food_count)
    return state


def choose_action(state, q_table):
    """
    Choose an action based on the current state and Q-table.

    :param state: The current state of the game
    :param q_table: The Q-table
    :return: The chosen action
    """
    if state not in q_table:
        q_table[state] = {action: 0 for action in ACTIONS}
    action_values = q_table[state]
    action = max(action_values, key=action_values.get)
    return action


def startLevelGame(level, screen, font, q_table):
    """
    Start a level game.

    :param level: The game level
    :param screen: The Pygame screen
    :param font: The font for rendering text
    :param q_table: The Q-table
    :return: The score and clearance status
    """
    clock = pygame.time.Clock()
    SCORE = 0
    wall_sprites = level.setupWalls(SKYBLUE)
    gate_sprites = level.setupGate(WHITE)
    hero_sprites, ghost_sprites = level.setupPlayers(HEROPATH, [BlinkyPATH, ClydePATH, InkyPATH, PinkyPATH])
    food_sprites = level.setupFood(YELLOW, WHITE)
    is_clearance = False
    steps = 0
    last_move_time = time.time()

    first_hero = next(iter(hero_sprites))
    last_hero_pos = [first_hero.rect.x, first_hero.rect.y]

    while True:
        state = get_state(hero_sprites, ghost_sprites, food_sprites)
        action = choose_action(state, q_table)

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
        SCORE += len(food_eaten) * 10

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

        first_hero = next(iter(hero_sprites))
        current_hero_pos = [first_hero.rect.x, first_hero.rect.y]

        if current_hero_pos != last_hero_pos:
            last_move_time = time.time()
            last_hero_pos = current_hero_pos
            steps += 1

        if time.time() - last_move_time > 30 or steps > 3500:
            is_clearance = False
            break

        if len(food_sprites) == 0:
            is_clearance = True
            break
        if hero_ghost_collision:
            is_clearance = False
            break

        pygame.display.flip()
        clock.tick(10)

    return SCORE, is_clearance


def showText(screen, font, is_clearance, auto_press_enter=False):
    """
    Show the result text on the screen.

    :param screen: The Pygame screen
    :param font: The font for rendering text
    :param is_clearance: Whether the level is cleared
    :param auto_press_enter: Whether to automatically press Enter
    """
    clock = pygame.time.Clock()
    msg = 'Game Over!' if not is_clearance else 'Congratulations, you won!'
    positions = [[235, 233], [65, 303], [170, 333]] if not is_clearance else [[145, 233], [65, 303], [170, 333]]
    surface = pygame.Surface((400, 200))
    surface.set_alpha(10)
    surface.fill((128, 128, 128))
    screen.blit(surface, (100, 200))
    texts = [font.render(msg, True, WHITE),
             font.render('Press ENTER to quit.', True, WHITE),
             font.render('Press ESCAPE to quit.', True, WHITE)]
    pygame.display.flip()

    if auto_press_enter:
        time.sleep(1)
        pyautogui.press('enter')
    else:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                        sys.exit()
                        pygame.quit()
            for idx, (text, position) in enumerate(zip(texts, positions)):
                screen.blit(text, position)
            pygame.display.flip()
            clock.tick(10)


def initialize():
    """
    Initialize the Pygame environment.

    :return: The Pygame screen
    """
    pygame.init()
    icon_image = pygame.image.load(ICONPATH)
    pygame.display.set_icon(icon_image)
    screen = pygame.display.set_mode([606, 606])
    pygame.display.set_caption('kun_man - View Training Result')
    return screen


def load_q_table(episode):
    """
    Load the Q-table from a pickle file.

    :param episode: The episode number
    :return: The loaded Q-table or None if the file is not found
    """
    results_dir = os.path.join(os.getcwd(), 'results')
    filename = os.path.join(results_dir, f'{episode}.pkl')
    try:
        with open(filename, 'rb') as f:
            q_table = pickle.load(f)
        return q_table
    except FileNotFoundError:
        return None


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python view_training_result.py <episode_number> or <start_episode>-<end_episode>")
        sys.exit(1)

    arg = sys.argv[1]
    if '-' in arg:
        start_episode, end_episode = map(int, arg.split('-'))
        if start_episode % 50 != 0 or end_episode % 50 != 0:
            print("Start and end episodes should be multiples of 50.")
            sys.exit(1)
        episodes = list(range(start_episode, end_episode + 1, 50))

        valid_episodes_score = []
        average_scores = []
        valid_episodes_rate = []
        pass_rates = []

        for episode in episodes:
            q_table = load_q_table(episode)
            if q_table is None:
                print(f"Q-table file for episode {episode} not found.")
                continue

            screen = initialize()
            pygame.mixer.init()
            pygame.mixer.music.load(BGMPATH)
            pygame.mixer.music.play(-1, 0.0)
            pygame.font.init()
            font_small = pygame.font.Font(FONTPATH, 18)
            font_big = pygame.font.Font(FONTPATH, 24)
            level = Levels.Level1()

            score, is_clearance = startLevelGame(level, screen, font_small, q_table)
            valid_episodes_score.append(episode)
            average_scores.append(score)
            print(f"Episode {episode} Score: {score}")

            valid_episodes_rate.append(episode)
            pass_rates.append(1 if is_clearance else 0)
            print(f"Episode {episode} Pass Rate: {1 if is_clearance else 0}")

            if episode < 350:
                showText(screen, font_big, is_clearance, auto_press_enter=True)
            pygame.quit()

        plots_dir = os.path.join(os.getcwd(), 'plots')
        if not os.path.exists(plots_dir):
            os.makedirs(plots_dir)

        if valid_episodes_score:
            plt.figure()
            plt.plot(valid_episodes_score, average_scores)
            plt.xlabel('Training Episodes')
            plt.ylabel('Score')
            plt.title('Performance Evaluation: Score')
            score_path = os.path.join(plots_dir, 'score.png')
            plt.savefig(score_path)
            plt.show()

        if valid_episodes_rate:
            plt.figure()
            plt.plot(valid_episodes_rate, pass_rates)
            plt.xlabel('Training Episodes')
            plt.ylabel('Pass Rate')
            plt.title('Performance Evaluation: Pass Rate')
            pass_rate_path = os.path.join(plots_dir, 'pass_rate.png')
            plt.savefig(pass_rate_path)
            plt.show()

    else:
        episode = int(arg)
        screen = initialize()
        pygame.mixer.init()
        pygame.mixer.music.load(BGMPATH)
        pygame.mixer.music.play(-1, 0.0)
        pygame.font.init()
        font_small = pygame.font.Font(FONTPATH, 18)
        font_big = pygame.font.Font(FONTPATH, 24)

        q_table = load_q_table(episode)
        if q_table is None:
            print(f"Q-table file for episode {episode} not found.")
            sys.exit(1)
        level = Levels.Level1()
        _, is_clearance = startLevelGame(level, screen, font_small, q_table)
        showText(screen, font_big, is_clearance, auto_press_enter=False)
        pygame.quit()