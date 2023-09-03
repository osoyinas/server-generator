import os
import sys
import subprocess

if len(sys.argv) != 2:
    sys.exit(1)

# Obtiene la ruta proporcionada como argumento
server_executable = os.path.abspath(sys.argv[1])
min_ram = input('Enter the min RAM: ')
max_ram = input('Enter the max RAM:')
java_command = ['java' ,f'-Xms{min_ram}G',f'-Xmx{max_ram}G','-XX:+UseG1GC','-jar', server_executable, 'nogui']
