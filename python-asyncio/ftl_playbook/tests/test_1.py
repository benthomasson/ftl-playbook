import os
import pytest
import yaml

from faster_than_light import load_inventory, run_module

HERE = os.path.dirname(os.path.abspath(__file__))


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



@pytest.mark.asyncio
async def test_load_inventory():
    os.chdir(HERE)
    inventory = load_inventory('inventory.yml')
    assert inventory


@pytest.mark.asyncio
async def test_load_playbook():
    os.chdir(HERE)
    playbook = load_playbook('playbook.yml')
    assert playbook


@pytest.mark.asyncio
async def test_playbook_interpreter():
    os.chdir(HERE)
    playbook = load_playbook('playbook.yml')
    inventory = load_inventory('inventory.yml')
    await playbook_interpreter(playbook, inventory, ['modules'])


@pytest.mark.asyncio
async def test_playbook_interpreter10():
    os.chdir(HERE)
    playbook = load_playbook('playbook10.yml')
    inventory = load_inventory('inventory.yml')
    await playbook_interpreter(playbook, inventory, ['modules'])

