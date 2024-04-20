import importlib.util
import os
import sys


class ScriptLoader:
    def __init__(self):
        self.script_dir = "./scripts/"
        self.scripts = {}
        for script in os.listdir("./scripts/"):
            if script.endswith('.py'):
                script_name = os.path.splitext(script)[0]
                self.scripts[script_name] = os.path.join("./scripts/", script)

    def run_script(self, script_name, function_name, *args, **kwargs):
        # Get the path of the script from the scripts dictionary
        script_path = self.scripts.get(script_name)
        # If the script is not found, raise a ValueError
        if script_path is None:
            raise ValueError(f"No script named {script_name}")
    
        # Create a module specification from the script path
        spec = importlib.util.spec_from_file_location(script_name, script_path)
        # Create a module from the specification
        module = importlib.util.module_from_spec(spec)
        # Add the module to sys.modules so it can be imported
        sys.modules[script_name] = module 
        # Execute the module
        spec.loader.exec_module(module)
    
        # Get the function from the module
        function = getattr(module, function_name, None)
        # If the function is not found, raise a ValueError
        if function is None:
            raise ValueError(f"No function named {function_name} in {script_name}")
    
        # Call the function with any passed arguments and return its result
        return function(*args, **kwargs)