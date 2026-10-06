"""命令行入口。"""

import argparse
import json

from . import core, samples


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _save(path, state):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=1)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="plot")
    ap.add_argument("--sample", choices=["deed", "priority", "guild", "replay", "work"])
    sub = ap.add_subparsers(dest="cmd")
    assign_parser = sub.add_parser("assign")
    assign_parser.add_argument("--state", required=True)
    assign_parser.add_argument("--req-id", required=True)
    status_parser = sub.add_parser("status")
    status_parser.add_argument("--state", required=True)
    args = ap.parse_args(argv)

    if args.sample:
        return samples.run(args.sample)
    if args.cmd is None:
        ap.print_help()
        return 2

    state = _load(args.state)
    if args.cmd == "status":
        print(json.dumps(core.status(state), ensure_ascii=False))
        return 0
    out = core.assign(state, args.req_id, core.Counter())
    _save(args.state, state)
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
