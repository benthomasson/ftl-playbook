from faster_than_light import run_module
import yaml
import os


def load_playbook(playbook_path):
    with open(playbook_path) as f:
        return yaml.safe_load(f.read())


def get_module_name(task):
    keywords = []
    for key, value in task.items():
        if key not in keywords:
            return key


async def playbook_interpreter(playbook, inventory, module_dirs):
    term_width = os.get_terminal_size()[0]
    gate_cache = {}
    for play in playbook:
        #print(play)
        tasks = play.get('tasks', [])
        hosts = play.get('hosts', [])
        name = play.get('name', '')
        print()
        print(f'PLAY [{name}] '.ljust(term_width, '*'))
        for task in tasks:
            print ()
            print (f'TASK [{get_module_name(task)}] '.ljust(term_width, '*'))
            output = await run_module(inventory, module_dirs, get_module_name(task), gate_cache=gate_cache, modules=[get_module_name(task)])
            #for i in output:
            #    print("ok:", f'[{i}]')
