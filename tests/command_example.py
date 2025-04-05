#!/usr/bin/env python
import json
import sys


def main():
    input = sys.stdin.read()

    try:
        json.loads(input)
    except Exception:
        d = {
            "name": "example",
            "description": "sample",
            "schema": {
                "title": "Args",
                "type": "object",
            },
        }
        print(json.dumps(d, separators=(",", ":")), end="")
        sys.exit(2)

    print(input, end="")


if __name__ == "__main__":
    main()
