# 002: Does my agent actually verify before saying "done"?

- **Date:** 2026-11-02
- **Hypothesis:** My instructions already say "proof before done": after writing to an external tool, read it back before reporting success. If the written rule were enough, most turns that write to an external tool would read the result back before the turn ends.
- **Change:** Turned the rule into a hook that can block.
  - [`hooks/proof_before_done.py`](../plugins/proof-before-done/hooks/proof_before_done.py), wired in [`hooks/hooks.json`](../plugins/proof-before-done/hooks/hooks.json). After an external write it reminds the agent to read it back. At the end of a turn that wrote externally, never read back after the last write, and claims completion, it blocks the stop once and asks for the read-back or an explicit "not verified".
  - [`scripts/backtest.py`](../plugins/proof-before-done/scripts/backtest.py) replays that same end-of-turn check over past transcripts.
  - The first version of the hook shipped with 10 regression tests. The packaged plugin now has 23: 15 for the hook and 8 for the backtest, in [`tests/`](../plugins/proof-before-done/tests/).
- **Measure:** A backtest over my own past session transcripts. For every turn (one user prompt up to the next), it counts:
  - **write turns:** turns that called a tool which writes to an external surface (a doc, a chat message, an email draft, a spreadsheet);
  - **read back:** write turns that called a tool from the hook's read-back list after the last write;
  - **would block:** write turns with no read-back whose final message claims completion ("done", "sent", "published" and similar) without saying "not verified".

  Re-run it on your own transcripts:

  ```
  python3 plugins/proof-before-done/scripts/backtest.py PATH/TO/TRANSCRIPTS --json
  ```

  `PATH/TO/TRANSCRIPTS` is a folder of Claude Code session `.jsonl` files, searched recursively. The output is counts only.

- **Result:** measured 2026-11-02, before the hook was on.

  | Count | Number |
  |---|---|
  | Turns scanned | 3,731 |
  | Turns that wrote to an external tool | 538 |
  | Of those, read it back after the last write | 45 (8%) |
  | Claimed completion with no read-back | 425 |

  Source: the backtest above, run 2026-11-02 with the pre-packaging version of the script, which uses the same counting rule. Its tool lists may differ slightly from the packaged version. The rule was written down the whole time. It was followed in 8% of the turns it applied to.

  Caveat: "claims completion" is a word match, so `would block` is an estimate of the check, not a verdict on any single turn.

- **Decision:** Keep the rule, and enforce it with the hook rather than with more wording.
- **Next:** Re-measure in 2 weeks with the hook on, using the same script, and report both data sets side by side. Result pending.
