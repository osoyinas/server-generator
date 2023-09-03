import os

def generate_sh(server_path, min_ram, max_ram, start_file_name):
    file = os.path.join(server_path, 'run.sh')
    file_content = f"""#!/bin/bash
    java -Xms{min_ram}G -Xmx{max_ram}G -XX:+UseG1GC {start_file_name} nogui"""
    with open(file, 'w',) as file:
        file.write(file_content)
    return file

def generate_bat(server_path, min_ram, max_ram, start_file_name):
    file = os.path.join(server_path, 'run.bat')
    file_content = f"""java -Xms{min_ram}G -Xmx{max_ram}G -XX:+UseG1GC {start_file_name} nogui"""
    with open(file, 'w',) as file:
        file.write(file_content)
    return file


def generate_eula(server_path):
    eula_file = os.path.join(server_path,'eula.txt')

    eula_content = """eula=true"""

    with open(eula_file, 'w',) as file:
        file.write(eula_content)
    return file

