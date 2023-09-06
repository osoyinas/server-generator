"""
Executable file where the command-line program starts
"""
import os
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
    picked_version = manager.get_version_of(option)
    options = list(picked_version.keys())
    options.pop(0)
    title = 'Choose download:'
    jar_file = os.path.join('server', '')
    choosed_download = pick(options=options, title=title)[0]
    manager.download_jar(path=jar_file, url=picked_version[choosed_download], name=f"{manager.get_name()}-{picked_version['version']}.jar")


if __name__ == '__main__':
    main()
