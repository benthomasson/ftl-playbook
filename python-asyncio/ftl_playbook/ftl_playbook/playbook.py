from faster_than_light import run_module
import yaml


def load_playbook(playbook_path):
    with open(playbook_path) as f:
        return yaml.safe_load(f.read())


def get_module_name(task):
    keywords = []
    for key, value in task.items():
        if key not in keywords:
            return key


async def playbook_interpreter(playbook, inventory, module_dirs):
    for play in playbook:
        print(play)
        tasks = play.get('tasks', [])
        hosts = play.get('hosts', [])
        name = play.get('name', '')
        for task in tasks:
            output = await run_module(inventory, module_dirs, get_module_name(task))
            print(output)
