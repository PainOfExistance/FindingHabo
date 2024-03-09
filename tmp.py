from game_manager import GameManager as GM
from script_loader import ScriptLoader

loader = ScriptLoader()
print(GM.line_time)
result = loader.run_script("neke", "meow", meow="Hello, World!")
print(GM.line_time)