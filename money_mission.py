#!/usr/bin/env python3
# money_mission.py
# Requires: pip install rumps
# Run: python3 money_mission.py

import rumps
import json
import os
from datetime import datetime, date

# ── CUSTOMIZE THESE ───────────────────────────────────────────────────────────
GOAL = 25000                          # Your goal amount in dollars
GOAL_DATE = date(2026, 12, 31)        # The date you want to hit your goal
START_DATE = date(2026, 1, 1)         # The date you started tracking
# ─────────────────────────────────────────────────────────────────────────────

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "money_mission_data.json")


# ── Data helpers ──────────────────────────────────────────────────────────────
def load_data():
    if not os.path.exists(DATA_FILE):
        save_data([])
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(entries):
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, indent=2)

def summer_total(entries):
    return sum(e["amount"] for e in entries)

def today_total(entries):
    today = date.today().isoformat()
    return sum(e["amount"] for e in entries if e["timestamp"].startswith(today))

def days_left():
    return max((GOAL_DATE - date.today()).days, 0)

def days_elapsed():
    elapsed = (date.today() - START_DATE).days
    return max(elapsed, 1)

def current_pace(total):
    return total / days_elapsed()

def projected_finish(total):
    return current_pace(total) * days_left()

def progress_bar(total):
    pct = min(total / GOAL, 1.0)
    filled = round(pct * 20)
    return "█" * filled + "░" * (20 - filled)

def pct_label(total):
    return f"{int((total / GOAL) * 100)}%"


# ── App ───────────────────────────────────────────────────────────────────────
class MoneyMission(rumps.App):
    def __init__(self):
        super().__init__("💰", quit_button=None)
        self.entries = load_data()
        self._build_menu()
        self._update_title()

    def _update_title(self):
        total = summer_total(self.entries)
        self.title = f"💰 {pct_label(total)}"

    def _build_menu(self):
        self.menu.clear()
        entries = self.entries
        total = summer_total(entries)
        today = today_total(entries)
        remaining = max(GOAL - total, 0)
        pace = current_pace(total)
        projected = projected_finish(total)
        bar = progress_bar(total)
        pct = pct_label(total)
        dl = days_left()
        elapsed = days_elapsed()

        items = [
            rumps.MenuItem("💰 Money Mission"),
            None,
            rumps.MenuItem(f"📈 Today:  ${today:,.2f}"),
            rumps.MenuItem(f"🌞 Total:  ${total:,.2f}"),
            rumps.MenuItem(f"🎯 Goal:  ${GOAL:,}"),
            None,
            rumps.MenuItem(f"Progress:  {bar} {pct}"),
            None,
            rumps.MenuItem(f"💸 Remaining:  ${remaining:,.2f}"),
            rumps.MenuItem(f"📅 Days Left:  {dl}"),
            rumps.MenuItem(f"📉 Current Pace:  ${pace:,.2f}/day  ({elapsed} days)"),
            rumps.MenuItem(f"🔮 Projected Finish:  ${projected:,.0f}"),
            None,
            rumps.MenuItem("➕ Add Revenue", callback=self.add_revenue),
            None,
            rumps.MenuItem("Quit", callback=self.quit_app),
        ]

        for item in items:
            if item is None:
                self.menu.add(rumps.separator)
            else:
                self.menu.add(item)

    def add_revenue(self, _):
        amount_resp = rumps.Window(
            message="How much did you make?",
            title="➕ Add Revenue",
            default_text="",
            ok="Next",
            cancel="Cancel",
            dimensions=(200, 24),
        ).run()

        if not amount_resp.clicked or not amount_resp.text.strip():
            return

        try:
            amount = float(amount_resp.text.strip().replace("$", "").replace(",", ""))
        except ValueError:
            rumps.alert(title="Invalid amount", message="Enter a number like 150 or 1500.50")
            return

        desc_resp = rumps.Window(
            message="What was it for?",
            title="➕ Add Revenue",
            default_text="",
            ok="Save",
            cancel="Cancel",
            dimensions=(200, 24),
        ).run()

        if not desc_resp.clicked:
            return

        entry = {
            "amount": amount,
            "description": desc_resp.text.strip() or "No description",
            "timestamp": datetime.now().isoformat()
        }

        self.entries.append(entry)
        save_data(self.entries)
        self._update_title()
        self._build_menu()

        total = summer_total(self.entries)
        rumps.notification(
            title=f"💰 +${amount:,.2f} added!",
            subtitle=desc_resp.text.strip() or "No description",
            message=f"Total: ${total:,.2f}  •  {pct_label(total)} to goal",
            sound=False,
        )

    def quit_app(self, _):
        rumps.quit_application()


if __name__ == "__main__":
    MoneyMission().run()
