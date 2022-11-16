from faster_than_light import run_module, run_ftl_module
import yaml
import os
from pprint import pformat
from collections import defaultdict


def load_playbook(playbook_path):
    with open(playbook_path) as f:
        return yaml.safe_load(f.read())


def get_module_name(task):
    keywords = []
    for key, value in task.items():
        if key not in keywords:
            return key


def get_module_args(task, module_name):
    return task[module_name]


def get_hosts_from_pattern(inventory, hosts):
    return hosts.split(",")


async def playbook_interpreter(playbook, inventory, module_dirs):
    try:
        term_width = os.get_terminal_size()[0]
    except Exception:
        term_width = 80
    gate_cache = {}
    results = defaultdict(lambda :dict(ok=0, failed=0, changed=0, unreachable=0))
    for play in playbook:
        print(play)
        tasks = play.get("tasks", [])
        hosts = get_hosts_from_pattern(inventory, play.get("hosts", ""))
        name = play.get("name", "")
        print()
        print(f"PLAY [{name}] ".ljust(term_width, "*"))
        for task in tasks:
            module_name = get_module_name(task)
            print()
            print(f"TASK [{module_name}] ".ljust(term_width, "*"))
            output = await run_ftl_module(
                inventory,
                module_dirs,
                module_name,
                gate_cache=gate_cache,
                modules=[get_module_name(task)],
                module_args=get_module_args(task, module_name),
            )
            for host, result in output.items():
                print(f"ok: [{host}] => {pformat(result)}")
                results[host]['ok'] += 1

    print(f"\nPLAY RECAP".ljust(term_width, "*"))
    for host in hosts:
        print(f"{host}".ljust(26),
              f": ok={results[host]['ok']}   ",
              f"changed={results[host]['changed']}   ",
              f"failed={results[host]['failed']}   ",
              f"unreachable={results[host]['unreachable']}")
