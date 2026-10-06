"""地块分配核心。"""

GUILD_CAP = 2


class Counter:
    """记录本轮检查过的分配记录条数。"""

    def __init__(self):
        self.scanned = 0


def sort_plots(plots):
    return sorted(plots, key=lambda p: (-p["size"], p["id"]))


def order_applicants(applicants):
    return sorted(applicants, key=lambda a: -a["tickets"])


def assign(state, req_id, counter):
    plots = sort_plots(state["plots"])
    assigned = []
    waiting = []
    for plot, app in zip(plots, order_applicants(state["applicants"])):
        dup = False
        for row in assigned:
            counter.scanned += 1
            if row[1] == app["player"]:
                dup = True
                break
        if dup:
            continue
        assigned.append([plot["id"], app["player"]])
    for app in order_applicants(state["applicants"])[len(plots):]:
        waiting.append(app["player"])
    state["assigned"].extend(assigned)
    state["ledger"].append(req_id)
    return {
        "req_id": req_id,
        "status": "ok",
        "assigned": assigned,
        "waiting": waiting,
        "scanned": counter.scanned,
    }


def status(state):
    return {
        "plots": len(state["plots"]),
        "applicants": len(state["applicants"]),
        "assigned": len(state["assigned"]),
        "requests": len(state["ledger"]),
    }


def new_state():
    return {"plots": [], "applicants": [], "assigned": [], "ledger": []}
