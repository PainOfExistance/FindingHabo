from game_manager import ClassManager as CM
from game_manager import GameManager as GM


def player_dialogue_tubolca(args):
    for x in range(int(args[1])):
        CM.inventory.add_item(GM.items[args[0]])