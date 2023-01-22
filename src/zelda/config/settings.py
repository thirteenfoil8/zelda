WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FRAMERATE = 120
TILESIZE = 64

# weapons
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': 'src/zelda/assets/graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30, 'graphic': 'src/zelda/assets/graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': 'src/zelda/assets/graphics/weapons/axe/full.png'},
    'rapier': {'cooldown': 50, 'damage': 8, 'graphic': 'src/zelda/assets/graphics/weapons/rapier/full.png'},
    'sai': {'cooldown': 80, 'damage': 10, 'graphic': 'src/zelda/assets/graphics/weapons/sai/full.png'}}

# magic
magic_data = {
    'flame': {'strength': 5, 'cost': 20, 'graphic': 'src/zelda/assets/graphics/particles/flame/fire.png'},
    'heal': {'strength': 20, 'cost': 10, 'graphic': 'src/zelda/assets/graphics/particles/heal/heal.png'}}

# Interface
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'src/zelda/assets/graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'
