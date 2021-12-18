import pygame
from settings import X, Y, image_load, SpriteSheet

CHARACTER_SELECT_MENU = {
    'class_option_rects': {
        "Fighter": [X * 15 / 100, Y * 80 / 100, X * 20 / 100, Y * 5 / 100],
        "Adept": [X * 35 / 100, Y * 80 / 100, X * 20 / 100, Y * 5 / 100],
        "Rogue": [X * 55 / 100, Y * 80 / 100, X * 20 / 100, Y * 5 / 100],
        "Artificer": [X * 75 / 100, Y * 80 / 100, X * 20 / 100, Y * 5 / 100],
    },
    'name_entry_option_rects': {
        "random": [X * 75 / 100, Y * 30 / 100, X * 25 / 100, Y * 10 / 100],
        "select": [X * 75 / 100, Y * 40 / 100, X * 25 / 100, Y * 10 / 100],
        "back": [X * 75 / 100, Y * 50 / 100, X * 25 / 100, Y * 10 / 100],
    },
    'confirm_rects': {
        "confirm": [X * 75 / 100, Y * 40 / 100, X * 25 / 100, Y * 10 / 100],
        "back": [X * 75 / 100, Y * 50 / 100, X * 25 / 100, Y * 10 / 100],
    },
    'name_display_rect': [X * 50 / 100, Y * 70 / 100, X * 80 / 100, Y * 5 / 100],
    'class_display_rect': [X * 50 / 100, Y * 5 / 100, X * 80 / 100, Y * 5 / 100],
    'prompt_rect': [X * 1 / 8, Y * 13 / 16, X * 3 / 4, Y * 1 / 8],
    'fighter pos': (X * 1 / 10, Y * 8 / 100),
    'adept pos': (X * 3 / 10, Y * 8 / 100),
    'rogue pos': (X * 5 / 10, Y * 8 / 100),
    'artificer pos': (X * 7 / 10, Y * 8 / 100),
    'selected pos': (X * 4 / 10, Y * 2 / 8),
    'sprites': {
        "Fighter": {
            'images128': [image_load(
                r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p1.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character "
                    r"Select\Fighter128p2.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p3.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p4.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p5.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p6.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p7.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p8.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p9.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p10.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p11.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter128p12.png"),
            ],
            'images256': [image_load(
                r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p1.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p2.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p3.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p4.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p5.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p6.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p7.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p8.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p9.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p10.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p11.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Fighter256p12.png"),
            ],
            'idle_frames': [0, 1],
            'idle_weights': [5, 1],
            'idle_speed': 2000,
            'flourish_frames': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            'flourish_weights': [10, 1, 1, 1, 1, 1, 1, 1, 1, 5],
            'flourish_speed': 2000
        },
        "Rogue": {
            'images128': [image_load(
                r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p1.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p2.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p3.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p4.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p5.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p6.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p7.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p8.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p9.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p10.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p11.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue128p12.png"),
            ],
            'images256': [image_load(
                r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p1.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p2.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p3.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p4.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p5.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p6.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p7.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p8.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p9.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p10.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p11.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Rogue256p12.png"),
            ],
            'idle_frames': [0, 1],
            'idle_weights': [11, 1],
            'idle_speed': 6000,
            'flourish_frames': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            'flourish_weights': [10, 1, 1, 1, 1, 1, 1, 1, 1, 5],
            'flourish_speed': 2000
        },
        "Adept": {
            'images128': [image_load(
                r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p1.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p2.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p3.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p4.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p5.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p6.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p7.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p8.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p9.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p10.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p11.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p12.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p13.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p14.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p15.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept128p16.png"),
            ],
            'images256': [image_load(
                r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p1.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p2.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p3.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p4.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p5.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p6.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p7.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p8.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p9.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p10.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p11.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p12.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p13.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p14.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p15.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Adept256p16.png"),
            ],
            'idle_frames': range(16),
            'idle_weights': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'idle_speed': 500,
            'flourish_frames': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            'flourish_weights': [10, 1, 1, 1, 1, 1, 1, 1, 1, 5],
            'flourish_speed': 2000
        },
        "Artificer": {
            'images128': [image_load(
                r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p1.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p2.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p3.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p4.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p5.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p6.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p7.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p8.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p9.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p10.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p11.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p12.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p13.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p14.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p15.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p16.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p17.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p18.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p19.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p20.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p21.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p22.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p23.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p24.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p25.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p26.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p27.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p28.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p29.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer128p30.png"),
            ],
            'images256': [image_load(
                r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p1.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p2.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p3.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p4.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p5.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p6.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p7.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p8.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p9.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p10.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p11.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p12.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p13.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p14.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p15.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p16.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p17.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p18.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p19.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p20.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p21.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p22.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p23.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p24.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p25.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p26.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p27.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p28.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p29.png"),
                image_load(
                    r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Character Select\Artificer256p30.png"),
            ],
            'idle_frames': range(30),
            'idle_weights': [500, 100, 50, 50, 50, 50, 50, 50, 50, 50, 50, 100, 100, 100, 50, 50, 200, 50, 30, 30, 30,
                             100, 50, 50, 50, 50, 50, 50, 50, 50],
            'idle_speed': 2290,
            'flourish_frames': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            'flourish_weights': [10, 1, 1, 1, 1, 1, 1, 1, 1, 5],
            'flourish_speed': 2000
        }
    },
}
REGION_CARDS = {
    "Desert": image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Cards\Desert_Card_480p_1.png"),
    "Grasslands": image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Cards\Grasslands_Card_480p_1.png"),
    "Valley": image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Cards\Valley_Card_480p_1.png"),
    "Savannah": image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Cards\Savannah_Card_480p_1.png"),
}
UNEXPLORED_NODE = [
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet1.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet2.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet3.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet4.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet5.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet6.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet7.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet8.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet9.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet10.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet11.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet12.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Sheet13.png")]
REGION_LAYOUTS = {
    # num_nodes=30, knn=4, node_space=100, space_probability=100,
    # node_space_ll=0, node_space_ul=350, min_edge_angle=15
    'Badlands':
        {
            "Badlands_1":
                {
                    'Image': image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\BGs"
                                        r"\Badlands_720_BG_2.png"),
                    'Start': [176, 424, 312, 592],
                    'End': [904, 496, 1024, 528],
                    'Shapes': [[(120, 224), (432, 264), (592, 184), (760, 176), (1048, 280), (1048, 680), (848, 680),
                                (776, 624), (712, 368), (560, 360), (328, 600), (120, 608)]],
                    'Positive': True,
                },
        },
    'Desert':
        {
            "Desert_1":
                {
                    'Image': image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\BGs"
                                        r"\Desert_720_BG_1.png"),
                    'Start': [120, 264, 296, 440],
                    'End': [856, 344, 1032, 488],
                    'Shapes': [[(120, 96), (950, 96), (950, 504), (912, 528), (824, 432), (816, 288), (720, 232),
                                (536, 288), (480, 472), (376, 512), (120, 440)],
                               [(120, 512), (336, 600), (552, 528), (640, 392), (728, 432), (856, 584), (950, 580),
                                (950, 580), (120, 580)],
                               [(552, 424), (560, 344), (696, 280), (776, 320), (768, 350), (704, 300), (616, 300)]],
                    'Positive': True,
                },
            "Desert_2":
                {
                    'Image': image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\BGs"
                                        r"\Desert_720_BG_2.png"),
                    'Start': [124, 94, 266, 418],
                    'End': [956, 244, 1022, 506],
                    'Shapes': [[(122, 92), (966, 90), (680, 369), (650, 588), (602, 606), (420, 476), (124, 428)],
                               [(792, 472), (1026, 164), (1032, 540), (904, 446), (790, 508)]],
                    'Positive': True,
                },
        }
}
EXPLORED_NODE = [
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored1.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored2.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored3.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored4.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored5.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored6.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored7.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored8.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored9.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored10.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored11.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored12.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Node_Explored13.png")]
EXIT_NODE = [
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node1.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node2.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node3.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node4.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node5.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node6.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node7.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node8.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node9.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node10.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node11.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node12.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Exit_Node13.png")]
EVENT_NODE = [
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Event_Node32p1.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Event_Node32p2.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Event_Node32p3.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Event_Node32p4.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Event_Node32p5.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Event_Node32p6.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Event_Node32p7.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Event_Node32p8.png")]
DUNGEON_NODE = [
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Dungeon_Node32p1.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Dungeon_Node32p2.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Dungeon_Node32p3.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Dungeon_Node32p4.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Dungeon_Node32p5.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Dungeon_Node32p6.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Dungeon_Node32p7.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Dungeon_Node32p8.png")]
SHOP_NODE = [
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Shop_Node32p1.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Shop_Node32p2.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Shop_Node32p3.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Shop_Node32p4.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Shop_Node32p5.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Shop_Node32p6.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Shop_Node32p7.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Shop_Node32p8.png")]
ENCOUNTER_NODE = [
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Encounter_Node32p1.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Encounter_Node32p2.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Encounter_Node32p3.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Encounter_Node32p4.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Encounter_Node32p5.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Encounter_Node32p6.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Encounter_Node32p7.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Encounter_Node32p8.png")]
BOSS_NODE = [
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Boss_Node32p1.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Boss_Node32p2.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Boss_Node32p3.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Boss_Node32p4.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Boss_Node32p5.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Boss_Node32p6.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Boss_Node32p7.png"),
    pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Node\Boss_Node32p8.png")]
Party_Marker = [
    [pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Party_Marker1.png"),
     pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Party_Marker2.png"),
     pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Party_Marker3.png"),
     pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Party_Marker4.png"),
     pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Party_Marker5.png"),
     pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Party_Marker6.png"),
     pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Party_Marker7.png"),
     pygame.image.load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Party_Marker8.png")],
    [65, 65, 65, 65, 65, 65, 65, 65]]
REGION_STATIC_SPRITES = {
    'coin icon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Coin Icon.png"),
    'supplies icon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Supplies Icon.png"),
    'elixir icon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Elixir Icon.png"),
    'heart icon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Heart Icon.png"),
    'charge icon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Charge Icon.png"),
    "FighterIcon": image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Fighter Icon 64.png"),
    'AdeptIcon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Fighter Icon 64.png"),
    'ArtificerIcon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Fighter Icon 64.png"),
    'RogueIcon': image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Region\Fighter Icon 64.png")
}
BATTLE_MENU_SPRITES = {
    'action_slot_sprites': [image_load(
        r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p1.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p2.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p3.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p4.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p5.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p6.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p7.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p8.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p9.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p10.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p11.png"),
        image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Action Slot720p12.png")
    ],
    'attack_action': [0],
    'attack_action_weights': [1],
    'ability_action': [1],
    'ability_action_weights': [1],
    'item_action': [2],
    'item_action_weights': [1],
    'defend_action': [3],
    'defend_action_weights': [1],
    'no_action': [4, 5, 6, 7, 8, 9, 10, 11],
    'no_action_weights': [8, 1, 1, 1, 16, 1, 1, 1],
    'animation_speed': 2000,
    'target_reticules': {
        'target': image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Target Rets128p2.png"),
        'source': image_load(
            r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Menus\Target Rets128p1.png"),
    }

}
battle_characters = {
    "Fighter": {'sprites': [image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                       r"\Character\Battle\Fighter\Fighter_Battle128p1.png"),
                            image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                       r"\Character\Battle\Fighter\Fighter_Battle128p2.png"),
                            image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                       r"\Character\Battle\Fighter\Fighter_Battle128p3.png"),
                            image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                       r"\Character\Battle\Fighter\Fighter_Battle128p4.png"),
                            image_load(r"C:\Users\Chase\Dropbox\Pycharm\FinalRogue\venv\resources\sprites"
                                       r"\Character\Battle\Fighter\Fighter_Battle128p5.png")
                            ],
                'idle': [0, 1, 2, 3],  # frames of sprites associated with idle state
                'idle weights': [10, 1, 3, 1],  # time weights for idle frames
                'idle speed': 2000,  # ms to complete idle cycle
                'attack': [4],  # frames of sprites associated with attack state
                'cast': [4],  # frames of sprites associated with cast state
                'hit': [0],  # frames of sprites associated with hit state
                'miss': [2],  # frames of sprites associated with miss state
                },
}
BATTLE_ANIMATIONS = {
    "Slash_1": {
        'sprites': [image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\slash1animation64p1.png"),
                    image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\slash1animation64p2.png"),
                    image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\slash1animation64p3.png"),
                    image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\slash1animation64p4.png"),
                    image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\slash1animation64p5.png"),
                    image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\slash1animation64p6.png"),
                    image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\slash1animation64p7.png"),
                    image_load(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\slash1animation64p8.png"),
                    ],
        'weights': [1, 1, 1, 1, 1, 1, 1, 10],  # time weights for idle frames
        'speed': 500,  # ms to complete idle cycle
        'delay': 100,
        'screen': False,
    },
    "Wide_Blast_1": {
        'sprites': SpriteSheet(r"C:\Users\Chase\Dropbox\Pycharm\NeonKnights\venv\resources\sprites\Battle\Effects"
                               r"\attack_all_enemy_animation_1_720p.png").load_strip([0, 0, 1280, 720], 19),
    },
}