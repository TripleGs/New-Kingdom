import pygame
import sys
import os
import random
from pygame.locals import *
from ..config.config import SOUND_FILES

sounds = {}  # create empty dictionary of sounds


def initSoundManager():
    pygame.mixer.init()
    # Load sounds using paths from config
    for sound_name, sound_path in SOUND_FILES.items():
        sounds[sound_name] = pygame.mixer.Sound(sound_path)


def playSound(soundName):
    channel = sounds[soundName].play()


def playSoundContinuous(soundName):
    channel = sounds[soundName].play(-1)


def stopSound(soundName):
    channel = sounds[soundName].stop()
