"""Manifest and wiring consistency (stdlib unittest).

- marketplace.json entries agree with each plugin.json (name, version, description).
- templates/settings.example.json hand-copies the plugins' hooks.json: the PostToolUse matcher
  must be identical and every script path must exist in the repo.
"""
import json
import os
import re
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def load(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return json.load(f)


class MarketplaceAgreesWithPlugins(unittest.TestCase):
    def test_name_version_description_agree(self):
        market = load(".claude-plugin", "marketplace.json")
        self.assertTrue(market["plugins"])
        for entry in market["plugins"]:
            src = entry["source"]
            plugin = load(src, ".claude-plugin", "plugin.json")
            for key in ("name", "version", "description"):
                self.assertEqual(entry.get(key), plugin.get(key),
                                 f"{entry['name']}: marketplace.json and plugin.json disagree on {key}")

    def test_every_plugin_dir_is_listed(self):
        market = load(".claude-plugin", "marketplace.json")
        listed = {os.path.normpath(e["source"]) for e in market["plugins"]}
        on_disk = {os.path.join("plugins", d) for d in os.listdir(os.path.join(ROOT, "plugins"))
                   if os.path.isdir(os.path.join(ROOT, "plugins", d))}
        self.assertEqual(listed, on_disk)


class SettingsExampleMatchesHooks(unittest.TestCase):
    def setUp(self):
        self.settings = load("templates", "settings.example.json")["hooks"]
        self.pbd = load("plugins", "proof-before-done", "hooks", "hooks.json")["hooks"]

    def test_post_tool_use_matcher_equal(self):
        mine = self.settings["PostToolUse"][0]["matcher"]
        theirs = self.pbd["PostToolUse"][0]["matcher"]
        self.assertEqual(mine, theirs)

    def test_script_paths_exist_in_repo(self):
        commands = []
        for groups in self.settings.values():
            for group in groups:
                for h in group["hooks"]:
                    commands.append(h["command"])
        self.assertTrue(commands)
        for cmd in commands:
            m = re.search(r"~/path/to/ai-pm-os/(\S+\.py)", cmd)
            self.assertIsNotNone(m, f"no ai-pm-os script path in: {cmd}")
            self.assertTrue(os.path.isfile(os.path.join(ROOT, m.group(1))),
                            f"settings.example.json points at a missing script: {m.group(1)}")

    def test_stop_and_post_modes_match_plugin(self):
        # the plugin wires the same script with the same mode argument
        for event, mode in (("PostToolUse", "post"), ("Stop", "stop")):
            self.assertTrue(self.settings[event][0]["hooks"][0]["command"].endswith(" " + mode))
            self.assertTrue(self.pbd[event][0]["hooks"][0]["command"].endswith(" " + mode))


if __name__ == "__main__":
    unittest.main()
