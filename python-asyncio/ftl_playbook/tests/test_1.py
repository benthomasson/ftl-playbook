import os
import pytest
import yaml

from faster_than_light import load_inventory

HERE = os.path.dirname(os.path.abspath(__file__))


def load_playbook(playbook_path):
    with open(playbook_path) as f:
        return yaml.load(f.read())


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
