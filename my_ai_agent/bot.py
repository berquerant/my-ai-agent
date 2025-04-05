from dataclasses import dataclass, field
from typing import Self, cast

from agents import ModelProvider, Tool, Agent, RunConfig, Runner, TResponseInputItem

from .log import log


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
    tools: list[Tool] = field(default_factory=list)

    async def reply(self, req: BotRequest) -> BotResponse:
        log().info("bot: begin reply")
        for t in self.tools:
            log().debug("bot: enabled tool=%s", t.name)
        agent = Agent(name="assistant", instructions=self.instructions, tools=self.tools)
        input_items = [x.input_item for x in req.messages]
        result = await Runner.run(
            starting_agent=agent, run_config=RunConfig(model_provider=self.model_provider), input=input_items
        )
        log().info("bot: end reply")
        return BotResponse(reply=Message.assistant(result.final_output))
