import json
import os
import random
import shutil
import string
import time
from dataclasses import dataclass
from pprint import pprint

from utilities.data import Account

import psutil as psutil


@dataclass
class Colours:
    """Colours for the console."""
    # pylint: disable=invalid-name
    HEADER: str = "\033[95m"
    OKBLUE: str = "\033[94m"
    OKCYAN: str = "\033[96m"
    OKGREEN: str = "\033[92m"
    WARNING: str = "\033[93m"
    FAIL: str = "\033[91m"
    ENDC: str = "\033[0m"


def get_random_string(length):
    """Generate a random string with a given length."""
    lower_letters = string.ascii_lowercase
    upper_letters = string.ascii_uppercase
    numbers = string.digits
    alphabet = lower_letters + upper_letters + numbers

    result_str = "".join(random.choice(alphabet) for _ in range(length))
    return result_str


async def save_credentials(Account: type(Account), AccountEncoder: type(json.JSONEncoder)):
    """Pass credentials into a file."""
    if not os.path.exists("credentials"):
        os.mkdir("credentials")
    with open(f"credentials/{Account.email[:-4]}.json",
              "w",
              encoding="UTF-8") as file:
        del Account.id
        json_file = json.dumps(Account, cls=AccountEncoder, indent=4)
        file.write(json_file)


def clear_tmp():
    """Clears tmp folder."""
    if os.path.exists("tmp"):
        try:
            shutil.rmtree("tmp")
            p_print("Cleared tmp folder successfully!", Colours.OKGREEN)
        except PermissionError:
            p_print(
                "Failed to clear temporary files... killing previous instances.", Colours.FAIL)
            kill_process()
            time.sleep(1)

            clear_tmp()


def kill_process():
    """Kills processes."""
    dirty_procs = []

    for process in psutil.process_iter():
        try:
            if "local-chromium" in process.as_dict()["cmdline"][0]:
                p_print(f"Found process {process.name()}...", Colours.WARNING)
                dirty_procs.append(process)
        except (KeyError, IndexError, TypeError, psutil.AccessDenied):
            pass

    for proc in dirty_procs:
        try:
            proc.kill()
        except (OSError, psutil.NoSuchProcess):
            pass

    p_print("Killed previous instances successfully!", Colours.OKGREEN)


def p_print(
        text,
        colour=None,
):
    """Prints text in colour."""
    if colour is not None:
        print(colour + text + Colours.ENDC)
    else:
        print(text)


def clear_console():
    """Clears console."""
    os.system("cls" if os.name == "nt" else "clear")
