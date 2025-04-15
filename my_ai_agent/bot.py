from dataclasses import dataclass
from typing import Self, cast, Any, override

from agents import (
    ModelProvider,
    Tool,
    Agent,
    RunConfig,
    Runner,
    TResponseInputItem,
    RunHooks,
    RunContextWrapper,
    TContext,
)

from .log import log


class BotHooks(RunHooks[TContext]):
    @override
    async def on_agent_start(
        self,
        context: RunContextWrapper[TContext],
        agent: Agent[TContext],
    ) -> None:
        log().debug("agent: start %s", agent.name)

    @override
    async def on_agent_end(
        self,
        context: RunContextWrapper[TContext],
        agent: Agent[TContext],
        output: Any,
    ) -> None:
        log().debug("agent: end %s, output=%s", agent.name, output)

    @override
    async def on_tool_start(
        self,
        context: RunContextWrapper[TContext],
        agent: Agent[TContext],
        tool: Tool,
    ) -> None:
        log().debug("tool: start %s", tool.name)

    @override
    async def on_tool_end(
        self,
        context: RunContextWrapper[TContext],
        agent: Agent[TContext],
        tool: Tool,
        result: str,
    ) -> None:
        log().debug("tool: end %s, result=%s", tool.name, result)


@dataclass
class Message:
    role: str
    content: str

    @classmethod
    def user(cls, content: str) -> Self:
        return cls(role="user", content=content)

    @classmethod
    def assistant(cls, content: str) -> Self:
        return cls(role="assistant", content=content)

    @property
    def input_item(self) -> TResponseInputItem:
        return cast(TResponseInputItem, {"role": self.role, "content": self.content})


@dataclass
class BotRequest:
    messages: list[Message]


@dataclass
class BotResponse:
    reply: Message


@dataclass
class Bot:
    model: str
    model_provider: ModelProvider
    instructions: str | None = None

    async def reply(self, req: BotRequest) -> BotResponse:
        agent = Agent(name="assistant", instructions=self.instructions)
        input_items = [x.input_item for x in req.messages]
        result = await Runner.run(
            starting_agent=agent,
            run_config=RunConfig(model_provider=self.model_provider),
            input=input_items,
            hooks=BotHooks(),
        )
        return BotResponse(reply=Message.assistant(result.final_output))
