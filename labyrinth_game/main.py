#!/usr/bin/env python3

from labyrinth_game import player_actions, utils

game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната 'entrance',
    'game_over': False,  # Значения окончания игры
    'steps_taken': 0  # Количество шагов
}

def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    utils.describe_current_room(game_state)
    while not game_state['game_over']:
        user_input = input('Введите команду:').strip().lower()
        if user_input == 'quit':
            print('Вы вышли из игры')
            break
        process_command(game_state, user_input)

if __name__ == "__main__":
    main()

def process_command(game_state, command):
    command = command.lower().split()
    if command[0] in ('north', 'east', 'west', 'south'):
        player_actions.move_player(game_state, command[0])
    else:
        match command[0]:
            case 'look':
                utils.describe_current_room(game_state)
            case 'use':
                player_actions.use_item(game_state, command[1])
            case 'go':
                player_actions.move_player(game_state, command[1])
            case 'take':
                player_actions.take_item(game_state, command[1])
            case 'inventory':
                player_actions.show_inventory(game_state)
            case 'solve':
                if game_state['current_room'] == 'treasure_room':
                    utils.attempt_open_treasure(game_state)
                else:
                    utils.solve_puzzle(game_state)
            case 'help':
                utils.show_help()
            case 'quit':
                return
            case _:
                print('Неизвестная команда')

