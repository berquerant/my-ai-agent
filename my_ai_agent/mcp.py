import json
import typing
from contextlib import asynccontextmanager
from dataclasses import dataclass, field

from agents.mcp import MCPServer, MCPServerStdio

from .log import log
from .shx import expand


class MCPException(Exception):
    pass


@dataclass
class Setting:
    command: str
    args: list[str] = field(default_factory=list)

    def server(self, name: str) -> MCPServer:
        return MCPServerStdio(
            name=name,
            params={
                "command": expand(self.command),
                "args": [expand(x) for x in self.args],
            },
        )

    @classmethod
    def from_dict(cls, d: dict[str, typing.Any]) -> typing.Self:
        command = d.get("command")
        if not command or not isinstance(command, str):
            raise Exception("command is required")
        args = d.get("args", [])
        if not isinstance(args, list) or not all(isinstance(x, str) for x in args):
            raise Exception("args is required as list[str]")
        return cls(command=command, args=args)


@dataclass
class Settings:
    settings: dict[str, Setting] = field(default_factory=dict)

    @classmethod
    def load_from_dict(cls, d: dict[str, typing.Any]) -> typing.Self:
        if not d:
            return cls(settings={})
        if not all(isinstance(x, dict) for x in d.values()):
            raise Exception("settings are required")
        return cls(settings={k: Setting.from_dict(v) for k, v in d.items()})

    @classmethod
    def loads(cls, v: str) -> typing.Self:
        if not v:
            return cls(settings={})
        try:
            return cls.load_from_dict(json.loads(v))
        except Exception as e:
            raise MCPException from e

    @asynccontextmanager
    async def mcp_servers(self) -> typing.AsyncGenerator[list[MCPServer], None]:
        xs: list[MCPServer] = []
        try:
            for name, s in self.settings.items():
                x: MCPServer = s.server(name)
                xs.append(x)
                log().debug("mcp: connect to %s", x.name)
                await x.connect()  # type: ignore[no-untyped-call]
            yield xs
        finally:
            for x in reversed(xs):
                log().debug("mcp: cleanup %s", x.name)
                await x.cleanup()  # type: ignore[no-untyped-call]
