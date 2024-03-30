from game_manager import ClassManager as CM
from game_manager import GameManager as GM


def player_stats_adjust(args):
    stat, amount= args[0], args[1]
    CM.player.update_stats(stat, amount)