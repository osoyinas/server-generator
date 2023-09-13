"""
Executable file where the command-line program starts
"""
from pick import pick
from src.forge.forge_manager import ForgeManager
from src.vanilla.vanilla_manager import VanillaManager
from src.spigot.spigot_manager import SpigotManager
from src.manager import Manager

OPTIONS = {VanillaManager.get_name(): VanillaManager,
           ForgeManager.get_name(): ForgeManager,
           SpigotManager.get_name(): SpigotManager}


def get_manager(option: str) -> Manager:
    """returns manager object

    Args:
        option (str): _description_

    Returns:
        Manager: _description_
    """
    return OPTIONS[option]()


def main():
    """
    Main function
    """
    title = 'Choose Minecraft framework:'
    options = list(OPTIONS.keys())
    option = pick(options=options, title=title)[0]

    manager = get_manager(option)
    title = 'Choose version:'
    version_options = list(manager.get_versions())
    print(version_options)
    picked_version = pick(options=version_options, title=title)[0]
    manager.set_picked_version(picked_version)
    available_downloads = manager.get_picked_version_downloads()
    download_picked = 'download'
    if len(available_downloads) > 1:
        title = 'Choose download:'
        download_picked = pick(options=available_downloads, title=title)[0]
    manager.init_server(download_picked)



if __name__ == '__main__':
    main()
