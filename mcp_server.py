"""
MCP Server for Iterative Delta Debugging Minimizer Skill.
"""

import json
import sys
from client import DeltaDebuggingMinimizer

MINIMIZER = DeltaDebuggingMinimizer()


def handle_request(req: dict) -> dict:
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "minimize_failure",
                    "description": "Minimize failing list of tokens or lines using ddmin",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "elements": {"type": "array"},
                            "target_elements": {
                                "type": "array",
                                "description": "Required elements simulating the failing condition"
                            }
                        },
                        "required": ["elements", "target_elements"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "minimize_failure":
            targets = set(args["target_elements"])
            def mock_test(sub):
                return targets.issubset(set(sub))

            res = MINIMIZER.minimize(args["elements"], mock_test)
            return {"content": [{"type": "text", "text": json.dumps(res)}]}

        return {"error": f"Unknown tool: {tool_name}"}

    return {"error": f"Unknown method: {method}"}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            resp["id"] = req.get("id")
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
