import pygame

def play_background_music():
    pygame.mixer.init()
    pygame.mixer.music.load("../piano2.wav")
    pygame.mixer.music.play(loops=-1)
    while pygame.mixer.music.get_busy() == True:
        continue
