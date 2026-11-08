"""Headless CLI:  python main.py "Find report.pdf in Downloads, rename it and move it to Documents"

Prints the live execution log and asks for approval in the terminal when the agent reaches a checkpoint.
Handy for debugging and for recording demo runs without the UI.
"""
import sys
import time

from exora_agent.preflight import check_llm
from exora_agent.runtime import AgentTaskController
from exora_agent.tracking import APPROVAL, TRACKER


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    good, msg = check_llm(force=True)
    print("Preflight:", msg)
    if not good:
        return 1
    ctrl = AgentTaskController()
    ctrl.start(" ".join(sys.argv[1:]))
    seen = 0
    try:
        while ctrl.running or seen < len(TRACKER.snapshot()["entries"]):
            snap = TRACKER.snapshot()
            for e in snap["entries"][seen:]:
                print(f"[{time.strftime('%H:%M:%S', time.localtime(e.ts))}] {e.kind:<11} {e.message}")
            seen = len(snap["entries"])
            if APPROVAL.pending and APPROVAL.decision is None:
                p = APPROVAL.pending
                print("\n=== APPROVAL REQUIRED ===\n" + p["summary"] + "\n  " + "\n  ".join(p["fields"]))
                APPROVAL.decide(input("Approve? [y/N] ").strip().lower() == "y")
            time.sleep(0.5)
    except KeyboardInterrupt:
        ctrl.stop()
        time.sleep(2)
    snap = TRACKER.snapshot()
    print(f"\nFINAL STATUS: {snap['status'].upper()}\n{snap['summary']}")
    for ev in snap["evidence"]:
        print("  evidence:", ev)
    return 0 if snap["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
