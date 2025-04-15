# my-ai-agent

``` shell
❯ python -m my_ai_agent.cli -h
usage: cli.py [-h] [-m MODEL] [-u BASE_URL] [--debug] [--quiet] [-i INSTRUCTIONS] [-r ROLE_SEPARATOR]
              [-s MESSAGE_SEPARATOR]

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
```
