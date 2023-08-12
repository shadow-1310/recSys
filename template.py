import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format = '[%(asctime)s]: %(message)s:')

project_name = 'recSys'

list_of_files = [
        ".github.workflows/.gitkeep",
        f"src/{project_name}/__init__.py",
        f"src/{project_name}/components/__init__.py",
        f"src/{project_name}/utils/__init__.py",
        f"src/{project_name}/utils/common.py",
        f"src/{project_name}/config/configuration.py",
        f"src/{project_name}/config/__init__.py",
        f"src/{project_name}/pipeline/__init__.py",
        f"src/{project_name}/entity/config_entity.py",
        f"src/{project_name}/entity/__init__.py",
        f"src/{project_name}/constants/__init__.py",
        "config/config.yaml",
        "params.yaml",
        "schema.yaml",
        "main.py",
        "app.py",
        "Dockerfile",
        "requirements.txt",
        "setup.py",
        "research/test.ipynb",
        "templates/index.html",
        "test.py",
        "README.md",
        ]


for filepath in list_of_files:
    #uncomment the following line in case of Windows OS
    # filepath = Path(filepath)

    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Directory created: {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass

        logging.info(f"Empty file created: {filepath}")

    else:
        logging.info(f"{filename} already exists")

