# my-ai-agent

``` shell
❯ python -m my_ai_agent.cli -h
usage: cli.py [-h] [-m MODEL] [-u BASE_URL] [--debug] [--quiet] [-i INSTRUCTIONS] [-r ROLE_SEPARATOR] [-s MESSAGE_SEPARATOR]
              [--tool_timeout TOOL_TIMEOUT] [-t [TOOL ...]] [-p MCP]

My AI agent.

options:
  -h, --help            show this help message and exit
  -m, --model MODEL     AI model, default: gpt-4o-mini
  -u, --base_url BASE_URL
                        base url of API
  --debug               enable debug log
  --quiet               quiet log
  -i, --instructions INSTRUCTIONS
                        instructions, system messages for the agent, @FILENAME is available
  -r, --role_separator ROLE_SEPARATOR
                        role separator string, default: '>'
  -s, --message_separator MESSAGE_SEPARATOR
                        message separator string, default: '\n---\n'
  --tool_timeout TOOL_TIMEOUT
                        tool timeout seconds, default: 30
  -t, --tool [TOOL ...]
                        external tool executables
  -p, --mcp MCP         MCP server settings like {"name"{"command":"COMMAND","args":["ARG"]}}, @FILENAME is available

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
python -m my_ai_agent.cli -u "ENDPOINT_TO_CHAT_COMPLETIONS_API like http://127.0.0.1:11434/v1"\
  -m "MODEL" < input.txt
## external tool
python -m my_ai_agent.cli -t "EXECUTABLE" < input.txt
### Example of EXECUTABLE

#!/usr/bin/env python
import json
import sys
from datetime import datetime
# tool name
name = "current_time"
# tool description
desc = '''\
Display the current local time.
Args:
    timezone: optional
Returns:
    time: string like '2024-01-02 12:13:14''''
# input schema as https://json-schema.org/
schema = {
    "title": "Args",
    "type": "object",
    "properties": {
        "timezone": {
            "title": "timezone",
            "type": "string",
         },
    },
    "required": ["timezone"],
    "additionalProperties": False,
}
help = {
    "name": name,
    "description": desc,
    "schema": schema,
}
input = sys.stdin.read()
try:
    # input should be json
    obj = json.loads(input)
except Exception as e:
    # otherwise, print help and exit with 2
    print(json.dumps(help))
    sys.exit(2)
# simplified impl for demo
if obj.get("timezone"):
    now = datetime.utcnow()
else:
    now = datetime.now()
# output should be json
print(json.dumps({"time": now.strftime("%Y-%m-%d %H:%M:%S")}))
```
