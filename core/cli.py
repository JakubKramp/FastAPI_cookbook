import os
from typing import Annotated

import typer
from rich import print

from config import settings
from core.constants import (
    DIRECTORIES_TO_CREATE,
    FILE_CONTENTS,
    FILES_TO_CREATE,
    ROUTER_IMPORT_LINE,
    TEST_FILES_TO_CREATE,
)

app = typer.Typer()

def create_file(filename:str, app_name:str) -> None:
    """
    Create a file with content defined in constants.
    """
    with open(filename,'a') as f:
        if file_content := FILE_CONTENTS.get(filename, ''):
            f.write(file_content(app_name))

def modify_app_file(app_name:str) -> None:
    """
    When crating a new app new router is created.
    This updates the main app file to use this router.
    After updating the file we run ruff to organise imports.
    """
    if settings.APP_LOCATION:
        with open(settings.APP_LOCATION,'r') as f:
            content = f.read()
            content = ROUTER_IMPORT_LINE(app_name) + content

            # add to routers list
            content = content.replace(
                "routers = [",
                f"routers = [{app_name}_router, "
            )

            with open(settings.APP_LOCATION, "w") as f:
                f.write(content)

            import subprocess
            subprocess.run(["ruff", "check", "--fix", settings.APP_LOCATION], capture_output=True)
            subprocess.run(["ruff", "format", settings.APP_LOCATION], capture_output=True)

        print("[bold red]Please note that your main app file has changed.[/bold red]")

    else:
        raise AttributeError('Please set APP_LOCATION setting')


def update_pyproject(app_name:str) -> None:
    """
    Updates pyproject.toml file to include new app in coverage report.
    """
    filename ='pyproject.toml'
    if not filename in os.listdir():
        print(f"[bold red]{filename} not found in your project directory.[/bold red]")
        return
    else:
        with open(filename, 'r') as f:
            content = f.read()

            content = content.replace(
                "source = [",
                f'source = ["{app_name}", '
            )

            with open(filename, "w") as f:
                f.write(content)

@app.command()
def startapp(app_name: str,
             modify: Annotated[
                 bool, typer.Option(prompt="Do you want to update your main app file?")
    ],) -> None:
    """
    Creates new app with appropriate files and test files.
    Optionally you can update the main app file.
    """
    os.mkdir(app_name)
    os.chdir(app_name)
    for filename in FILES_TO_CREATE:
        create_file(filename, app_name)
    for directory in DIRECTORIES_TO_CREATE:
        os.mkdir(directory)
    os.chdir('tests')
    for test_file in TEST_FILES_TO_CREATE:
        create_file(test_file, app_name)
    os.chdir('..')
    os.chdir('..')
    if modify:
        modify_app_file(app_name)
    update_pyproject(app_name)

@app.command()
def test():
    pass

if __name__ == "__main__":
    app()