import display
import game
from sys import exit
from time import time, sleep

if __name__ == "__main__":
    frame_duration = 1/60
    game_instance = game.Game()
    window_instance = display.Window(game_instance, size_multiplier=2, show_targets=True)
    while 1:
        start_time = time()
        window_instance.refresh()
        game_instance.set_input(window_instance.key_pressed)
        game_instance.advance()
        if game_instance.game_has_ended or game_instance.player_died:   exit(0)
        sleep(max(0, frame_duration - (time() - start_time)))

