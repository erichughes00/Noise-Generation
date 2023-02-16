import perlin_noise as perlin
import sys
import pygame
import pygame.gfxdraw
import noise_data as nd
import color as c
import game_control as g

def main():
    # creates the game controller and initializes everything
    controller = g.game_control(256, 256, 1)
    main_loop(controller)

def main_loop(controller:g.game_control):

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Keyboard events:
            elif event.type == pygame.KEYDOWN:
                controller.input.on_keyboard_press()

        controller.on_user_update()
        controller.draw_event()

if __name__ == "__main__":
    main()