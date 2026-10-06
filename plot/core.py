"""地块分配核心。"""

GUILD_CAP = 2


class Counter:
    """记录本轮检查过的申请人数。"""

    def __init__(self):
        self.scanned = 0


def sort_plots(plots):
    return sorted(plots, key=lambda p: (-p["size"], p["id"]))


def order_applicants(applicants):
    return sorted(applicants, key=lambda a: (not a["deed"], -a["priority"], -a["tickets"]))


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
    taken_plots = {row[0] for row in state["assigned"]}
    free_plots = [p for p in plots if p["id"] not in taken_plots]
    guild_of = {a["player"]: a["guild"] for a in state["applicants"]}
    assigned_players = set()
    guild_counts = {}
    for row in state["assigned"]:
        assigned_players.add(row[1])
        guild = guild_of.get(row[1])
        if guild is not None:
            guild_counts[guild] = guild_counts.get(guild, 0) + 1
    assigned = []
    waiting = []
    plot_iter = iter(free_plots)
    for app in order_applicants(state["applicants"]):
        counter.scanned += 1
        player = app["player"]
        if player in assigned_players:
            continue
        if guild_counts.get(app["guild"], 0) >= GUILD_CAP:
            waiting.append(player)
            continue
        plot = next(plot_iter, None)
        if plot is None:
            waiting.append(player)
            continue
        assigned.append([plot["id"], player])
        assigned_players.add(player)
        guild_counts[app["guild"]] = guild_counts.get(app["guild"], 0) + 1
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
