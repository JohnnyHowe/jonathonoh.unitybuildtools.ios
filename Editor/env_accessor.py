import os
from pretty_print import *


# region Vars 
APP_STORE_CONNECT_API_KEY_ISSUER_ID=None


# region Loading
_ALL_VARIABLES = {
    "APP_STORE_CONNECT_API_KEY_ISSUER_ID": {"required": True},
    "APP_STORE_CONNECT_API_KEY_KEY_ID": {"required": True},
    "APP_STORE_CONNECT_API_KEY_CONTENT": {"required": True},
    "TEST_GROUPS": {"required": False},
}

_NO_DOTENV_ERROR_MESSAGE="""Missing dependency: python-dotenv.
This can be ignored if you're not using a .env file.
If you are using .env, install dotenv with `pip install python-dotenv` (maybe python3 - check your system)"""


def _load():
    # Load as much without dotenv
    not_found = _try_load_env()
    not_found_and_required = list(filter(lambda var_name: _ALL_VARIABLES[var_name].get("required", True), not_found))

    # quit early if we have everything we need
    if len(not_found_and_required) == 0:
        pretty_print("Found all required environent variables without python-dotenv", color=SUCCESS)
        return

    not_found_variables_display = "\n".join(map(lambda s: "  - " + s, not_found_and_required))
    pretty_print(f"Could not find the following environment variables without python-dotenv\n{not_found_variables_display}", color=WARNING)

    # import dotenv
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError as error:
        pretty_print(_NO_DOTENV_ERROR_MESSAGE, color=ERROR)
        raise error

    # load vars from dotenv
    not_found = _try_load_env()
    not_found_and_required = list(filter(lambda var_name: _ALL_VARIABLES[var_name].get("required", True), not_found))

    # quit early if we have everything we need
    if len(not_found_and_required) == 0:
        pretty_print("Found all required environent variables with python-dotenv", color=SUCCESS)
        return

    not_found_variables_display = "\n".join(map(lambda s: "  - " + s, not_found_and_required))
    error_message = f"Could not find the following environment variables!\n{not_found_variables_display}"
    pretty_print(error_message, color=ERROR)
    raise ValueError(error_message)


def _try_load_env() -> list:
    """ Returns names of variables that could not be set. """
    not_found = []
    for var_name, options in _ALL_VARIABLES.items():
        if var_name in os.environ:
            globals()[var_name] = os.environ[var_name]
        else:
            not_found.append(var_name)
    return not_found


_load()