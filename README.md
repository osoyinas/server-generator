# Minecraft Server Generator

## Description

The Minecraft Server Generator is a Python command-line program that allows you to easily create Minecraft servers with various options and versions. You can choose from Forge, Vanilla, Spigot, Magma, and select the desired Minecraft version. The program automates the process of downloading the necessary server.jar files and setting up the server configuration.

## Installation

To install and use the Minecraft Server Generator, follow these steps:

1. Clone this repository to your local machine:

```bash
git clone https://github.com/osoyinas/server-generator.git
```

2. Navigate to the project directory:

```bash
cd server-generator
```

3. Make a virtual env

```bash
virtualenv venv
source venv/bin/active
```

4. Install the required Python packages:

```bash
pip install -r requirements.txt
```

5. Run the program:

```bash
python main.py
```

## Usage

Once you've launched the program, you can follow these steps to generate a Minecraft server:

1. Select the server type (Forge, Vanilla, Spigot, Magma).
2. Choose the Minecraft version.
3. Configure server settings, such as memory allocation and additional options.
4. The program will automatically download the necessary server.jar files and set up the server.
5. Start your Minecraft server using the generated `run.sh` (Linux/Mac) or `run.bat` (Windows) script.

## Options

Here are some of the available options and features of the Minecraft Server Generator:

- Server Type: Choose from Forge, Vanilla, Spigot, or Magma.
- Minecraft Version: Select the desired version.
- Memory Allocation: Customize the amount of RAM allocated to the server.
- Additional Options: Set various server properties and parameters.
- Automatic Updates: Keep your server files up to date.

## Contact

For any questions or issues, feel free to contact us at osoyinas@gmail.com.
