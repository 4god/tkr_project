from cocos.sprite import Sprite
from cocos.tiles import load
from cocos.mapcolliders import RectMapCollider
from cocos.layer import ScrollingManager, ScrollableLayer, ColorLayer, Layer
from cocos.director import director
from cocos.scene import Scene
from cocos.actions import Action, MoveBy, Move, Repeat, Reverse
from pyglet.window import key
import pyglet
from time import time
import cocos.collision_model as cm
import cocos.euclid as eu
import cocos
from cocos.text import Label

from protocol import MyProtocol


keyboard = key.KeyStateHandler()


class Swin(Sprite):
    def __init__(self, enemy_id, position):
        super().__init__("images/swin_right/Fall.png")
        self.position = position
        self.enemy_id = enemy_id
        self.cshape = cm.AARectShape(eu.Vector2(*self.position), self.width / 2, self.height / 2)
        self.alive = True
        self.state = 'passive'
        self.right = True
        self.activity = 'idle'

    def idle_right_animation(self):
        img = pyglet.image.load('images/swin_right/Idle.png')
        img_grid = pyglet.image.ImageGrid(img, 1, 11, item_width=80, item_height=56)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=True)
        self.image = anim

    def idle_left_animation(self):
        img = pyglet.image.load('images/swin_left/Run.png')
        img_grid = pyglet.image.ImageGrid(img, 1, 11, item_width=80, item_height=56)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=True)
        self.image = anim

    def run_right_animation(self):
        img = pyglet.image.load('images/swin_right/Run.png')
        img_grid = pyglet.image.ImageGrid(img, 1, 7, item_width=80, item_height=56)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=True)
        self.image = anim

    def run_left_animation(self):
        img = pyglet.image.load('images/swin_left/Idle.png')
        img_grid = pyglet.image.ImageGrid(img, 1, 7, item_width=80, item_height=56)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=True)
        self.image = anim

    def attack_right_animation(self):
        img = pyglet.image.load('images/swin_right/Attack.png')
        img_grid = pyglet.image.ImageGrid(img, 1, 5, item_width=80, item_height=56)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=False)
        self.image = anim

    def attack_left_animation(self):
        img = pyglet.image.load('images/swin_left/Attack.png')
        img_grid = pyglet.image.ImageGrid(img, 1, 5, item_width=80, item_height=56)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=False)
        self.image = anim

class Door(Sprite):
    def __init__(self):
        super().__init__("images/other_elements/door.png")
        self.position = 800, 400 #coord(x_pos, y_pos, self.width, self.height)
        self.cshape = cm.AARectShape(eu.Vector2(*self.position), self.width / 1, self.height / 1)
        self.closed = True
        self.last_time_opened = 0

    def open(self):
        print('door_open')
        self.last_time_opened = time()
        if self.closed:
            img = pyglet.image.load("images/other_elements/door_anim.png")
            img_grid = pyglet.image.ImageGrid(img, 1, 5, item_width=100, item_height=147)
            anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.15, loop=False)
            self.image = anim
            self.closed = False

    def close(self):
        if not self.closed:
            img = pyglet.image.load("images/other_elements/door_anim.png")
            img_grid = pyglet.image.ImageGrid(img, 1, 5, item_width=100, item_height=147)
            anim = pyglet.image.Animation.from_image_sequence(img_grid[::-1], 0.15, loop=False)
            self.image = anim
            self.closed = True



class OnlinePlayer(Sprite):
    def __init__(self, player_id):
        super().__init__(f"images/king_right/{(player_id - 1) % 2 + 1}/Fall.png")
        self.player_id = player_id
        self.image_id = (self.player_id - 1) % 2 + 1
        self.cshape = cm.AARectShape(eu.Vector2(*self.position), self.width / 2, self.height / 2)

    def idle_right_animation(self):
        img = pyglet.image.load(f"images/king_right/{self.image_id}/Idle.png")
        img_grid = pyglet.image.ImageGrid(img, 1, 11, item_width=186, item_height=116)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.05, loop=True)
        self.image = anim

    def idle_left_animation(self):
        img = pyglet.image.load(f"images/king_left/{self.image_id}/Idle.png")
        img_grid = pyglet.image.ImageGrid(img, 1, 11, item_width=186, item_height=116)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.05, loop=True)
        self.image = anim

    def run_right_animation(self):
        img = pyglet.image.load(f"images/king_right/{self.image_id}/Run.png")
        img_grid = pyglet.image.ImageGrid(img, 1, 8, item_width=186, item_height=116)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.05, loop=True)
        self.image = anim

    def run_left_animation(self):
        img = pyglet.image.load(f"images/king_left/{self.image_id}/Run.png")
        img_grid = pyglet.image.ImageGrid(img, 1, 8, item_width=186, item_height=116)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.05, loop=True)
        self.image = anim

    def attack_right_animation(self):
        img = pyglet.image.load(f"images/king_right/{self.image_id}/Attack.png")
        img_grid = pyglet.image.ImageGrid(img, 1, 3, item_width=186, item_height=116)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=False)
        self.image = anim

    def attack_left_animation(self):
        img = pyglet.image.load(f"images/king_left/{self.image_id}/Attack.png")
        img_grid = pyglet.image.ImageGrid(img, 1, 3, item_width=186, item_height=116)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=False)
        self.image = anim


class Player(Sprite):

    def idle_right_animation(self):
        img = pyglet.image.load(f"images/king_right/{self.image_id}/Idle.png")
        img_grid = pyglet.image.ImageGrid(img, 1, 11, item_width=186, item_height=116)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.05, loop=True)
        self.image = anim
        self.anim_list.append('idle_r')

    def idle_left_animation(self):
        img = pyglet.image.load(f"images/king_left/{self.image_id}/Idle.png")
        img_grid = pyglet.image.ImageGrid(img, 1, 11, item_width=186, item_height=116)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.05, loop=True)
        self.image = anim
        self.anim_list.append('idle_l')

    def run_right_animation(self):
        img = pyglet.image.load(f"images/king_right/{self.image_id}/Run.png")
        img_grid = pyglet.image.ImageGrid(img, 1, 8, item_width=186, item_height=116)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.05, loop=True)
        self.image = anim
        self.anim_list.append('run_r')

    def run_left_animation(self):
        img = pyglet.image.load(f"images/king_left/{self.image_id}/Run.png")
        img_grid = pyglet.image.ImageGrid(img, 1, 8, item_width=186, item_height=116)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.05, loop=True)
        self.image = anim
        self.anim_list.append('run_l')

    def attack_right_animation(self):
        img = pyglet.image.load(f"images/king_right/{self.image_id}/Attack.png")
        img_grid = pyglet.image.ImageGrid(img, 1, 3, item_width=186, item_height=116)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=False)
        self.image = anim
        self.anim_list.append('attack_r')

    def attack_left_animation(self):
        img = pyglet.image.load(f"images/king_left/{self.image_id}/Attack.png")
        img_grid = pyglet.image.ImageGrid(img, 1, 3, item_width=186, item_height=116)
        anim = pyglet.image.Animation.from_image_sequence(img_grid, 0.1, loop=False)
        self.image = anim
        self.anim_list.append('attack_l')


class Level1Scene(Scene):
    def __init__(self, g_c):


        map_layer = load("tiles/map1/map_3.tmx")['base']
        map_h = (map_layer.cells[-1][-1].y // map_layer.tw + 1)
        map_layer_bg_0 = load("tiles/map1/map_3.tmx")['background']
        map_layer_bg_1 = load("tiles/map1/map_3.tmx")['decorations']

        main_layer = MainLayer((500, 500))

        scroller.add(map_layer_bg_0, z=-2)
        scroller.add(map_layer_bg_1, z=-1)
        scroller.add(map_layer, z=0)
        scroller.add(main_layer, z=1)

        self.add(scroller)
        self.schedule_interval(main_layer.update, 1 / 30)  # 30 times per second
