from __future__ import annotations

from pathlib import Path

from agent_env.openenv import build_app


BUNDLE = Path(__file__).resolve().parents[1] / "vendor" / "${bundle}"

app = build_app(BUNDLE)


def main():
    import argparse

    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
