from collections import defaultdict
from faster_than_light import run_module
from faster_than_light.gate import build_ftl_gate, use_gate
import yaml
import os
from pprint import pprint
import jinja2
from functools import partial

dependencies = [
    "ftl_module_utils @ git+https://github.com/benthomasson/ftl_module_utils@main" # noqa
]


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


def print_result(result):

    for host, results in result.items():
        if results.get("changed"):
            print(f"changed: [{host}]")
        if results.get("failed"):
            print(f'failed: [{host}]: {results.get("msg")}')
        if results.get("error"):
            print(f'error: [{host}]: {results.get("message")}')
        else:
            print(f"ok: [{host}]")
            pprint(results)


def lookup(lookup_type, location):
    if lookup_type == "file":
        with open(location) as f:
            return f.read()
    if lookup_type == "ansible.builtin.env" or lookup_type == "env":
        return os.environ.get(location)


def render_module_args(module_args, variables, fns):
    fns_and_variables = {}
    fns_and_variables.update(variables)
    fns_and_variables.update(fns)
    for key, value in module_args.items():
        if "{{" in value and "}}" in value:
            module_args[key] = jinja2.Template(value).render(**fns_and_variables)


async def playbook_interpreter(playbook, inventory, module_dirs):
    try:
        term_width = os.get_terminal_size()[0]
    except OSError:
        term_width = 80
    gate_cache = {}
    results = defaultdict(lambda: dict(ok=0, failed=0, changed=0, unreachable=0))
    modules = []
    for play in playbook:
        tasks = play.get("tasks", [])
        for task in tasks:
            modules.append(get_module_name(task))
    gate = partial(
        use_gate,
        *build_ftl_gate(
            modules=modules,
            module_dirs=module_dirs,
            interpreter="/usr/bin/python3",
            dependencies=dependencies,
        ),
    )
    for play in playbook:
        print(play)
        tasks = play.get("tasks", [])
        hosts = play.get("hosts", [])
        name = play.get("name", "")
        print()
        print(f"PLAY [{name}] ".ljust(term_width, "*"))
        for task in tasks:
            print()
            print(f"TASK [{get_module_name(task)}] ".ljust(term_width, "*"))
            module_args = task.get(get_module_name(task), {})
            print(f"{module_args=}")
            render_module_args(module_args, {}, {"lookup": lookup})
            output = await run_module(
                inventory,
                module_dirs,
                get_module_name(task),
                module_args=task[get_module_name(task)],
                gate_cache=gate_cache,
                modules=[get_module_name(task)],
                dependencies=dependencies,
                use_gate=gate,
            )
            print_result(output)
    print("\nPLAY RECAP".ljust(term_width, "*"))
    for host in hosts:
        print(
            f"{host}".ljust(26),
            f": ok={results[host]['ok']}   ",
            f"changed={results[host]['changed']}   ",
            f"failed={results[host]['failed']}   ",
            f"unreachable={results[host]['unreachable']}",
        )
