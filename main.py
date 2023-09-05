"""
Executable file where the command-line program starts
"""
from pick import pick
from src.forge.forge_manager import ForgeManager
from src.vanilla.vanilla_manager import VanillaManager
from src.spigot.spigot_manager import SpigotManager

OPTIONS = {VanillaManager.get_name(): VanillaManager,
           ForgeManager.get_name(): ForgeManager,
           SpigotManager.get_name(): SpigotManager}


def main():
    """
    Main function
    """
    title = 'Choose Minecraft framework:'
    options = list(OPTIONS.keys())
    option = pick(options=options, title=title)[0]

    manager = OPTIONS[option]()
    title = 'Choose version:'
    options = list(manager.get_versions())
    option = pick(options=options, title=title)[0]
    print(manager.get_version_of(option))

if __name__ == '__main__':
    main()
