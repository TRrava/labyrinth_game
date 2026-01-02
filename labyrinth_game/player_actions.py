try:
    #from labyrinth_game.main import game_state
    from labyrinth_game.constant import ROOMS
except:
    #from main import game_state
    from constant import ROOMS
    from utils import random_event

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
        game_state['current_room'] = ROOMS[current_room]['exits'][direction]
        game_state['steps_taken'] += 1
        print(ROOMS[game_state['current_room']]['description'])
        #random_event(game_state)
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
                print('Шкатулка открыта. В ваш инвентарь добавлен предмет: rusty_key')
                game_state['player_inventory'].append('rusty_key')
            case 'ghost_key':
                if game_state['current_room'] == 'hiden_treasure_room':
                    game_state['player_inventory'].append('guldan_skull')
                    print('ПОБЕДА')
                else:
                    print('Ключ постоянно ускользает от вашего взора, его нужно применить в другом месте')
            case _:
                print(f'Игрок не знает, как их использовать: {item_name}')




