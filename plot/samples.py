"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def _app(player, guild="G", tickets=5, priority=0, deed=False):
    return {"player": player, "guild": guild, "tickets": tickets,
            "priority": priority, "deed": deed}


def _plot(pid, size=10):
    return {"id": pid, "size": size}


def run(name):
    if name == "deed":
        state = core.new_state()
        state["plots"] = [_plot("p1")]
        state["applicants"] = [_app("a", tickets=5), _app("b", "H", tickets=1, deed=True)]
        out = core.assign(state, "d-1", core.Counter())
        _line({"assigned": out["assigned"]})
        return 0
    if name == "priority":
        state = core.new_state()
        state["plots"] = [_plot("p1")]
        state["applicants"] = [_app("a", tickets=9), _app("b", "H", tickets=2, priority=5)]
        out = core.assign(state, "p-1", core.Counter())
        _line({"assigned": out["assigned"]})
        return 0
    if name == "guild":
        state = core.new_state()
        state["plots"] = [_plot("p1"), _plot("p2"), _plot("p3")]
        state["applicants"] = [_app("g1", tickets=9), _app("g2", tickets=8),
                               _app("g3", tickets=7), _app("h1", "H", tickets=1)]
        out = core.assign(state, "g-1", core.Counter())
        _line({"assigned": out["assigned"]})
        return 0
    if name == "replay":
        state = core.new_state()
        state["plots"] = [_plot("p1")]
        state["applicants"] = [_app("a")]
        core.assign(state, "r-1", core.Counter())
        core.assign(state, "r-1", core.Counter())
        _line({"assigned": len(state["assigned"])})
        return 0
    if name == "work":
        state = core.new_state()
        for i in range(2000):
            state["plots"].append(_plot("p%04d" % i))
            state["applicants"].append(_app("a%04d" % i, "G%04d" % i, tickets=i))
        out = core.assign(state, "w-1", core.Counter())
        _line({"applicants": 2000, "scanned": out["scanned"]})
        return 0
    raise SystemExit("未知场景：" + name)
