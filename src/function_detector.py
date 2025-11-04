import os
import re

function_pattern = r'\b(?:[A-Za-z_]\w*\.)*[A-Za-z_]\w*\s*\([^)]*\)'

with open(os.path.join("tmp", "gameOfLife.gl", "src", "main.cpp")) as file:
    contents = file.read()
    functions = re.findall(function_pattern, contents)
    for func in functions:
        print(func)