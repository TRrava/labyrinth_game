from labyrinth_game.constant import ROOMS
from labyrinth_game.utils import random_event

# try:
#     from labyrinth_game.constant import ROOMS
#     from labyrinth_game.utils import random_event
# except:
#     from constant import ROOMS
#     from utils import random_event

def show_inventory(game_state):
    """
    Выводит инвентарь игрока
    Параметры:
        game_state (dict): состояние игрока
    Возвращает:
        str: текстовое описание предметов в интвентаре.
    """
    if not game_state['player_inventory']:
        print('Инвентарь пуст')
    else:
        print('Твой инвентарь')
        for item in game_state['player_inventory']:
            print(f'- {item}')

def get_input(prompt="> "):
    # начало работы
    try:
        print(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state, direction):
    # функция движения,
    """
    Позволяет игроку передвигаться внутри игры и рассчитывает количетсво шагов
    Параметры:
        game_state (dict): состояние игрока.
        direction (str): направление движения.
    Возвращает:
        str: текстовое описание новой комнаты.
    """
    current_room = game_state['current_room']
    if direction in ROOMS[current_room]['exits'].keys():
        if ROOMS[current_room]['exits'][direction] == 'treasure_room':
            if 'rusty_key' in game_state['player_inventory']:
                print('Вы используете ключ, чтобы открыть путь в соквовищницу')
                game_state['current_room'] = ROOMS[current_room]['exits'][direction]
                game_state['steps_taken'] += 1
                print(ROOMS[game_state['current_room']]['description'])
                random_event(game_state)
            else:
                print('Для доступа в комнату вам нужен особый ключ')
                return
        else:
            game_state['current_room'] = ROOMS[current_room]['exits'][direction]
            game_state['steps_taken'] += 1
            print(ROOMS[game_state['current_room']]['description'])
            random_event(game_state)
    else:
        print('Нельзя пойти в этом направлении.')

def take_item(game_state, item_name):
    if  game_state['current_room'] == 'treasure_room' and item_name == 'treasure_chest':
        print('Вы не можете поднять сундук, он слишком тяжелый.')
        return
    current_room = game_state['current_room']
    if item_name in ROOMS[current_room]['items']:
        game_state['player_inventory'].append(item_name)
        print(f'Вы подняли: {item_name}')
        ROOMS[current_room]['items'].remove(item_name)
    else:
        print('Такого предмета здесь нет.')

def use_item(game_state, item_name):
    if item_name not in game_state['player_inventory']:
        print('У вас нет такого предмета.')
    else:
        match item_name:
            case 'torch':
                print('Cтало светлее')
            case 'sword':
                print('Ты стал увереннее')
            case 'bronze_box':
                if 'rusty_key' in game_state['player_inventory']:
                    print('Шкатулка пуста')
                else:
                    print('Шкатулка открыта. В ваш инвентарь добавлен: rusty_key')
                    game_state['player_inventory'].append('rusty_key')
            case 'ghost_key':
                if game_state['current_room'] == 'hiden_treasure_room':
                    game_state['player_inventory'].append('guldan_skull')
                else:
                    print('Ключ ускользает от вашего взора')
            case _:
                print(f'Игрок не знает, как их использовать: {item_name}')

