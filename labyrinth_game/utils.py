#from cleo.io.inputs.input import Input
import math

#import main

RANDOM_STATE_1 = 12.9898
RANDOM_STATE_2 = 43758.5453
MAX_DAMAGE = 9
HERO_HP = 3
RANDOM_EVENT = 10
EVENT_COUNT = 2

try:
    from labyrinth_game.constant import ROOMS
except:
    from constant import ROOMS

def describe_current_room(game_state):
    """
    Выводит характеристику комнаты в которой находится игрок
    Параметры:
        game_state (dict): состояние игрока.
    Возвращает:
        str: текстовое описание комнаты.
    """
    curr_room = game_state['current_room']
    print(f"== {curr_room} ==")
    print('Описание комнаты: \n', ROOMS[curr_room]['description'])
    print('Выходы:')
    for exit in ROOMS[curr_room]['exits'].keys():
        print(f'- {exit}')
    print('Заметные предметы:')
    for item in ROOMS[curr_room]['items']:
        print(f'- {item}')
    if ROOMS[curr_room]['puzzle'] is not None:
        print('Кажется, здесь есть загадка (используйте команду solve).')
    else:
        print('Загадок нет')

def solve_puzzle(game_state):
    if ROOMS[game_state['current_room']]['puzzle'] is None:
        print('Загадок нет')
        return
    else:
        puzzle = ROOMS[game_state['current_room']]['puzzle'][0]
        puzzle_answer = ROOMS[game_state['current_room']]['puzzle'][1]
        print(puzzle)
        user_answer = input('Ваш ответ:').strip().lower()
        if user_answer == puzzle_answer:
            ROOMS[game_state['current_room']]['puzzle'] = None
            print('Вы верно ответили за загадку! В ваш инвентарь добавлена ачивка!')
            game_state['player_inventory'].append('achievement')
        else:
            print('Неверно. Попробуйте снова.')

def attempt_open_treasure(game_state):
    if game_state['current_room'] == 'treasure_room':
        if 'rusty_key' in game_state['player_inventory']:
            print('Вы применяете ключ, и замок щёлкает. Сундук открыт!')
            ROOMS[game_state['current_room']]['items'].remove('treasure_chest')
            ROOMS[game_state['current_room']]['puzzle'] = None
            game_state['game_over'] = True
        else:
            user_answer = input('Сундук заперт. ... Ввести код? (да/нет)').strip().lower()
            if user_answer == 'да':
                puzzle = ROOMS[game_state['current_room']]['puzzle'][0]
                puzzle_answer = ROOMS[game_state['current_room']]['puzzle'][1]
                print(puzzle)
                user_answer = input('Введите код:').strip().lower()
                if user_answer == puzzle_answer:
                    print('Вы верно ввели код, и замок щёлкает. Сундук открыт!')
                    ROOMS[game_state['current_room']]['items'].remove('treasure_chest')
                    ROOMS[game_state['current_room']]['puzzle'] = None
                    game_state['game_over'] = True
                else:
                    print('Ошибка в введенном коде')
            else:
                print('Вы отступаете от сундука.')
    else:
        print('Команду можно использовать только в treasure_room')

def pseudo_random(seed, modulo):
    """
    Функция для псевдо рандома
    Параметры:
        seed (integer): число шагов игрока.
    Возвращает:
        str: текстовое описание комнаты.
    """
    x = math.sin(seed * RANDOM_STATE_1) * RANDOM_STATE_2
    x = (x - math.floor(x)) * modulo
    x = math.floor(x)
    return(x)

def trigger_trap(game_state):
    """
    Функция имитирует срабатывание ловушки
    """
    print("Ловушка активирована! Пол стал дрожать...")
    if game_state['player_inventory'] != []:
        drop_item_number = pseudo_random(game_state['steps_taken'], len(game_state['player_inventory']))
        print(game_state['player_inventory'])
        print(f'Вы потеряли {game_state['player_inventory'][drop_item_number]}')
        game_state['player_inventory'].pop(drop_item_number)
        print(game_state['player_inventory'])
    else:
        take_damage = pseudo_random(game_state['steps_taken'], MAX_DAMAGE)
        if take_damage >= HERO_HP:
            print(f'Вы получаете урон в {take_damage}, вы погибли')
            game_state['game_over'] = True
        else:
            print(f'Вы получаете урон в {take_damage}, но вы выжили')

def random_event(game_state):
    print('шанс рандома = ', pseudo_random(game_state['steps_taken'],RANDOM_EVENT))

    if pseudo_random(game_state['steps_taken'],RANDOM_EVENT) == 0:
        event = pseudo_random(game_state['steps_taken'],EVENT_COUNT)
        print('ранжом = ', event)
        match event:
            case 0:
                print('Игрок находит на полу монетку')
                #ROOMS[game_state['current_room']]['items'].append('coin')]
            case 1:
                print('Игрок слышит шорох')
                if 'sword' in game_state['player_inventory']:
                    print('Игрок отпугнул существо')
            case 2:
                if game_state['current_room'] == 'trap_room' and 'torch' not in game_state['player_inventory']:
                    print('Опасность!')
                    trigger_trap(game_state)
                else:
                    print('Вы успешно заметили и обошли ловушки')


def show_help():
    print("\nДоступные команды:")
    print("go <direction> - перейти в направлении (north/south/east/west)")
    print("look - осмотреть текущую комнату")
    print("take <item> - поднять предмет")
    print("use <item> - использовать предмет из инвентаря")
    print("inventory - показать инвентарь")
    print("solve - попытаться решить загадку в комнате")
    print("quit - выйти из игры")
    print("help - показать это сообщение")


