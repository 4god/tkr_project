from pyglet.gl import *
from cocos.menu import *
from cocos.layer import *
from cocos.sprite import Sprite


class BGLayer(Layer):
	def __init__(self):
		super(BGLayer, self).__init__()

		bg = Sprite('images/menu/background.png')
		bg.position = (400, 300)
		self.add(bg)


class WaitLayer(Layer):
	def __init__(self, game_controller):
		bg = Sprite('images/menu/wait_screen.png')
		bg.position = (400, 300)



class MainMenu(Menu):
	def __init__(self, game_controller):
		super(MainMenu, self).__init__()
		pyglet.font.add_directory('.')

		self.font_title['font_size'] = 50
		self.font_item['font_size'] = 30
		self.font_item_selected['font_size'] = 30

		self.menu_valign = CENTER
		self.menu_halign = CENTER

		items = []
		items.append(MenuItem('Новая игра'))
		items.append(MenuItem('Управление'))
		items.append(MenuItem('Настройки'))
		items.append(MenuItem('Выход')))

		self.create_menu()


class OptionMenu(Menu):
	def __init__(self):
		super(OptionMenu, self).__init__("Stardust crusader")

		self.font_title['font_size'] = 40

		self.menu_valign = BOTTOM
		self.menu_halign = RIGHT

		items = []
		items.append(MenuItem('Fullscreen))
		items.append(ToggleMenuItem('Show FPS: '))
		items.append(MenuItem('OK'))
		self.create_menu()
