import os
import sys

sys.path.append("../funsearch/implementation")

from funsearch import _extract_function_names, main
from config import Config, ProgramsDatabaseConfig, Sandbox


def score(prog):
    with open("Priority.py", "w") as f:
        f.write(prog)
    os.system("python3 evalFunc.py")
    with open("result", "r") as f:
        res = f.read().rstrip()
        result = float(res)
    return result, True


def prompt_manipulate(prompt):
    with open("prompt_head.txt", "r") as f:
        head = f.read()
    return head + "\n" + prompt


with open("skeleton.py", "r") as f:
    content = f.read()
    sandbox = Sandbox(score)
    databaseConf = ProgramsDatabaseConfig(num_islands=1)
    conf = Config(
        sandbox=sandbox,
        programs_database=databaseConf,
        init_template="init_template/",
        prompt_manipulate=prompt_manipulate,
        num_samplers=1,
        num_evaluators=1,
        samples_per_prompt=1,
        iterations=5,
    )
    inputs = [None]
    main(content, inputs, conf)
