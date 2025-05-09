"""Entry point of CLI."""

import argparse
import logging
import os
import sys
import textwrap

from .bot import Bot, BotRequest
from .io import read_file_or
from .log import log, init as init_log
from .provider import Setting
from .serde import Converter


async def main() -> int:
    """Entry point of CLI."""
    parser = argparse.ArgumentParser(
        description="My AI agent.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
            # Examples
            ## minimal
            python -m my_ai_agent.cli < input.txt
            ## continue chat
            python -m my_ai_agent.cli < input.txt > output.txt
            // edit output.txt to append user reply
            python -m my_ai_agent.cli < output.txt
            ## with instructions
            python -m my_ai_agent.cli -i @instructions.txt < input.txt
            ## change API endpoint
            python -m my_ai_agent.cli -u "ENDPOINT_TO_CHAT_COMPLETIONS_API like http://127.0.0.1:11434/v1"\\
              -m "MODEL" < input.txt
        """
        ),
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        action="store",
        default="gpt-4o-mini",
        help="AI model, default: gpt-4o-mini",
    )
    parser.add_argument(
        "-u",
        "--base_url",
        type=str,
        action="store",
        help="base url of API",
    )
    parser.add_argument("--debug", action="store_true", help="enable debug log")
    parser.add_argument("--quiet", action="store_true", help="quiet log")
    parser.add_argument(
        "-i",
        "--instructions",
        action="store",
        type=str,
        help="instructions, system messages for the agent, @FILENAME is available",
    )
    parser.add_argument(
        "-r", "--role_separator", type=str, action="store", default=">\n", help="role separator string, default: '>'"
    )
    parser.add_argument(
        "-s",
        "--message_separator",
        type=str,
        action="store",
        default="\n---\n",
        help="message separator string, default: '\\n---\\n'",
    )
    args = parser.parse_args()

    log_level = logging.INFO
    if args.debug:
        log_level = logging.DEBUG
    if args.quiet:
        log_level = logging.CRITICAL
    init_log(log_level)

    log().debug("start my-ai-agent")

    provider_setting = Setting(model_name=args.model, base_url=args.base_url, api_key=os.getenv("OPENAI_API_KEY") or "")
    instructions = read_file_or(args.instructions)
    converter = Converter(role_separator=args.role_separator, message_separator=args.message_separator)

    bot = Bot(
        model=args.model,
        model_provider=provider_setting.provider,
        instructions=instructions,
    )
    input_items = converter.from_str(sys.stdin.read())
    request = BotRequest(messages=input_items)
    response = await bot.reply(request)

    input_items.append(response.reply)
    result_text = converter.into_str(input_items)
    print(result_text)

    log().debug("end my-ai-agent successfully")
    return 0


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
