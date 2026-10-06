import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plot import core


def app(player, guild, tickets, priority=0, deed=False):
    return {"player": player, "guild": guild, "tickets": tickets,
            "priority": priority, "deed": deed}


class PlotTest(unittest.TestCase):
    def test_each_applicant_gets_one_plot(self):
        state = core.new_state()
        state["plots"] = [{"id": "p1", "size": 10}, {"id": "p2", "size": 10}]
        state["applicants"] = [app("a", "G1", 9), app("b", "G2", 5)]
        out = core.assign(state, "r1", core.Counter())
        self.assertEqual(len(out["assigned"]), 2)

    def test_bigger_plot_comes_first(self):
        plots = [{"id": "small", "size": 5}, {"id": "big", "size": 20}]
        self.assertEqual(core.sort_plots(plots)[0]["id"], "big")

    def test_no_applicants(self):
        state = core.new_state()
        state["plots"] = [{"id": "p1", "size": 10}]
        out = core.assign(state, "r1", core.Counter())
        self.assertEqual(out["assigned"], [])
        self.assertEqual(out["waiting"], [])

    def test_more_plots_than_applicants(self):
        state = core.new_state()
        state["plots"] = [{"id": "p1", "size": 10}, {"id": "p2", "size": 9}]
        state["applicants"] = [app("a", "G1", 1)]
        out = core.assign(state, "r1", core.Counter())
        self.assertEqual(out["waiting"], [])

    def test_status_counts(self):
        state = core.new_state()
        state["plots"] = [{"id": "p1", "size": 10}]
        state["applicants"] = [app("a", "G1", 1), app("b", "G2", 1)]
        out = core.status(state)
        self.assertEqual(out["plots"], 1)
        self.assertEqual(out["applicants"], 2)


if __name__ == "__main__":
    unittest.main()
