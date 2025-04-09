import json
import subprocess
import textwrap
from dataclasses import dataclass, asdict
from typing import Any

from agents import FunctionTool, RunContextWrapper, Tool
from pydantic import BaseModel

from .log import log
from .shx import expand_quote


@dataclass
class Output:
    stdout: str
    stderr: str
    returncode: int

    @property
    def ok(self) -> bool:
        return self.returncode == 0


@dataclass
class Help:
    name: str
    description: str
    schema: dict[str, Any]


@dataclass
class Command:
    """
    Execute external tool.

    The tool should:
    - accept JSON input
    - write JSON output
    - display help as JSON and exit with 2, when read not JSON input

    The help JSON is like:
    {
      "name": "name of tool",
      "description": "description of tool",
      "schema": {...}
    }
    """

    executable: str
    timeout_seconds: int
    env: dict[str, str] | None = None

    def as_tool(self) -> Tool:
        h = self.help()

        class Args(BaseModel):
            input: str

        @dataclass
        class Error:
            message: str
            returncode: int
            error: bool = True

            @property
            def json(self) -> str:
                return json.dumps(asdict(self), separators=(",", ":"))

        async def run(ctx: RunContextWrapper[Any], args: str) -> str:
            log().info("call: command(%s) with %s", self.executable, args)
            try:
                json.loads(args)
            except Exception as e:
                log().error("command got invalid json input %s: %s", e, args)
                e.add_note("command got a not json input")
                raise
            r = await self.arun(args)
            if not r.ok:
                log().error("call: command(%s) exit with %d: %s", r.returncode, r.stderr)
                return Error(message=r.stderr, returncode=r.returncode).json
            log().info("call: command(%s) with %s return=%s", self.executable, args, r.stdout)
            return r.stdout

        desc_trailer = textwrap.dedent(
            """\
            This tool only accepts JSON input and produces only JSON output.
            When the tool call fails, the following JSON will be returned:
              error: true
              returncode: exit code of call
              message: error message
            """
        )
        name = h.name
        desc = h.description + "\n\n" + desc_trailer
        log().info("tool: name=%s description=%s schema=%s", name, desc, json.dumps(h.schema, separators=(",", ":")))

        return FunctionTool(
            name=name,
            description=desc,
            params_json_schema=h.schema,
            on_invoke_tool=run,
        )

    @property
    def __executable(self) -> str:
        return expand_quote(self.executable)

    def help(self) -> Help:
        r = self.run("help")
        if r.returncode != 2:
            raise Exception(f"command: {self.executable} failed to display help: {r.stderr}")
        obj = json.loads(r.stdout)
        if "name" not in obj:
            raise Exception(f"command: {self.executable} should have name in help")
        if "description" not in obj:
            raise Exception(f"command: {self.executable} should have description in help")
        if "schema" not in obj:
            raise Exception(f"command: {self.executable} should have schema in help")
        return Help(name=obj["name"], description=obj["description"], schema=obj["schema"])

    async def arun(self, input: str) -> Output:
        return self.run(input)

    def run(self, input: str) -> Output:
        r = subprocess.run(
            self.__executable,
            input=input,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True,
            timeout=self.timeout_seconds,
            env=self.env,
        )
        return Output(
            stdout=r.stdout,
            stderr=r.stderr,
            returncode=r.returncode,
        )
