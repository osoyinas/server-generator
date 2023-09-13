import os
import psutil


def generate_sh(server_path, min_ram, max_ram, start_file_name):
    """
    generates run.sh
    """
    file = os.path.join(server_path, 'run.sh')
    file_content = f"""#!/bin/bash
    java -Xms{min_ram}G -Xmx{max_ram}G -XX:+UseG1GC {start_file_name} nogui"""
    with open(file, 'w', encoding='utf-8') as file:
        file.write(file_content)
    return file


def generate_bat(server_path, min_ram, max_ram, start_file_name):
    """Generates run.bat
    """
    file = os.path.join(server_path, 'run.bat')
    file_content = f"""java -Xms{min_ram}G -Xmx{max_ram}G -XX:+UseG1GC {start_file_name} nogui"""
    with open(file, 'w', encoding='utf-8') as file:
        file.write(file_content)
    return file


def generate_eula(server_path):
    """generates eula.txt with eula=true
    """
    eula_file = os.path.join(server_path, 'eula.txt')

    eula_content = """eula=true"""

    with open(eula_file, 'w', encoding='utf-8') as file:
        file.write(eula_content)
    return file


def get_ram_gb():
    """Get the available ram in the system

    Returns:
        int: GB ram
    """
    virtual_memory = psutil.virtual_memory()
    # Convertir bytes a gigabytes
    ram_gb = virtual_memory.total / (1024 ** 3)
    return ram_gb
