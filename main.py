from src.forge.ForgeManager import ForgeManager
from src.spigot.scrap_spigot import *
from pick import pick


def main():
    title = 'Choose Minecraft framework:'
    options = ['Vanilla', 'Forge', 'Spigot', ]
    option, index = pick(options=options, title=title)
    available_versions = []
    versions_tittle = 'Select the minecraft version:'
    if (option == 'Forge'):
        forge = ForgeManager()
        available_versions = forge.get_forge_versions()
        version_picked, index = pick(
            options=available_versions, title=versions_tittle)
        title = 'Select the download:'
        options = list(forge.get_version(version_picked).keys())
        options.pop(0)
        download_picked, index = pick(options=options, title=title)

    elif option == 'Spigot':
        available_versions = get_spigot_versions()


if __name__ == '__main__':
    main()
