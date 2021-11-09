"""VSCode

Open VSCode Workspaces defined in config.json"""


from collections import namedtuple
from unicodedata import name
import albert

import os
import json

__title__ = "VSCode"
__version__ = "0.4.0"
__triggers__ = "vsc "
__authors__ = "@justanotherariel"
__exec_deps__ = ["code-insiders"]


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
Workspace = namedtuple("Workspace", ["name", "path"])


def getWorkspaces():
    f = open(os.path.join(__location__, "config.json"))
    data = json.load(f)

    for workspace in data:
        # print(workspace)
        # albert.info([workspace["name"], workspace["path"]])
        yield Workspace(workspace["name"], workspace["path"])

    f.close()


def buildItem(ws):
    text = f"Open {ws.name}"
    commandline = ["code-insiders", ws.path]

    iconPath = os.path.join(__location__, "icons/workspace.png")

    return albert.Item(
        id=f"vscode-{ws.name}",
        text=ws.name,
        subtext=text,
        icon=iconPath,
        completion=ws.name,
        actions=[albert.ProcAction(text=text, commandline=commandline)],
    )


def handleQuery(query):
    if not query.isTriggered and query.string == "":
        return []

    if query.isValid:
        workspaces = getWorkspaces()

        return [
            buildItem(ws)
            for ws in workspaces
            if query.string.lower() in ws.name.lower()
        ]

    return []
