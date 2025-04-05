from dataclasses import dataclass

from .bot import Message


@dataclass
class Converter:
    role_separator: str
    message_separator: str

    def __into_str(self, v: Message) -> str:
        return v.role + self.role_separator + v.content

    def into_str(self, v: list[Message]) -> str:
        return self.message_separator.join(self.__into_str(x) for x in v)

    def __from_str(self, v: str) -> Message:
        if self.role_separator not in v:
            return Message.user(v)

        role, content = v.split(self.role_separator, maxsplit=1)
        return Message(role=role, content=content)

    def from_str(self, v: str) -> list[Message]:
        if v.strip() == "":
            return []
        return [self.__from_str(x.strip()) for x in v.split(self.message_separator)]
