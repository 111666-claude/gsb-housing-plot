"""地块分配核心。"""

GUILD_CAP = 2


class Counter:
    """记录本轮检查过的分配记录条数。"""

    def __init__(self):
        self.scanned = 0


def sort_plots(plots):
    return sorted(plots, key=lambda p: (-p["size"], p["id"]))


def order_applicants(applicants):
    return sorted(applicants,
                  key=lambda a: (not a["deed"], -a["priority"], -a["tickets"]))


def assign(state, req_id, counter):
    if req_id in state["ledger"]:
        return {
            "req_id": req_id,
            "status": "duplicate",
            "assigned": [],
            "waiting": [],
            "scanned": counter.scanned,
        }
    plots = sort_plots(state["plots"])
    assigned = []
    waiting = []
    taken = set()
    guild_counts = {}
    plot_index = 0
    for app in order_applicants(state["applicants"]):
        player = app["player"]
        counter.scanned += 1
        if player in taken:
            continue
        if plot_index >= len(plots):
            waiting.append(player)
            continue
        guild = app["guild"]
        if guild_counts.get(guild, 0) >= GUILD_CAP:
            waiting.append(player)
            continue
        taken.add(player)
        guild_counts[guild] = guild_counts.get(guild, 0) + 1
        assigned.append([plots[plot_index]["id"], player])
        plot_index += 1
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
