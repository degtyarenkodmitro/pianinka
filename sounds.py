from pygame import mixer
mixer.init()

def load_sounds(keys):
    sounds = {}
    for key, filename in keys.items():
        sounds[key] = mixer.Sound("assets/sounds/" + filename)
    return sounds
