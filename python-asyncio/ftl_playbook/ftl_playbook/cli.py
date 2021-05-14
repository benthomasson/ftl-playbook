
"""
Usage:
    ftl-playbook [options] <playbook>

Options:
    -h, --help        Show this page
    --debug            Show debug logging
    --verbose        Show verbose logging
    -i=<i>, --inventory=<i>     Inventory
    -M=<M>, --module-dir=<M>    Module directory
"""
import asyncio
from docopt import docopt
import logging
import sys

from .playbook import playbook_interpreter, load_playbook
from faster_than_light import load_inventory

logger = logging.getLogger('cli')


async def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parsed_args = docopt(__doc__, args)
    if parsed_args['--debug']:
        logging.basicConfig(level=logging.DEBUG)
    elif parsed_args['--verbose']:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    await playbook_interpreter(load_playbook(parsed_args['<playbook>']),
                               load_inventory(parsed_args['--inventory']),
                               [parsed_args['--module-dir']])

    return 0


def entry_point():
    asyncio.run(main(sys.argv[1:]))
