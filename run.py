import training
import pickle
import neat
import os

if __name__ == "__main__":
    with open("winner.neat", "rb") as file:
        winner = pickle.loads(file.read())
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    training.play_game(winner, config, show_visuals=True)