import unittest
from pathlib import Path

YAML = Path(__file__).resolve().parents[1] / "esphome" / "tion_auto_mode.yaml"


class TionAutoModeStructureTest(unittest.TestCase):
    def test_heater_mode_off_while_stopped_is_remembered_and_later_applied(self):
        text = YAML.read_text(encoding="utf-8")

        self.assertIn("desired_heater_mode", text)
        self.assertIn("heater_mode_apply_pending", text)
        self.assertIn("heater mode desired: off; apply pending", text)
        self.assertIn("heater mode pending apply: fan_only", text)

        pending_decl = text.index("id: heater_mode_apply_pending")
        pending_use = text.index("heater mode pending apply: fan_only")
        self.assertLess(pending_decl, pending_use)

        turn_off = text.index("turn_off_action:", text.index("id: heater_mode"))
        pending_set = text.index("id: heater_mode_apply_pending", turn_off)
        self.assertLess(turn_off, pending_set)

    def test_existing_safety_condition_for_live_heater_switch_is_preserved(self):
        text = YAML.read_text(encoding="utf-8")

        self.assertIn("id(tion_climate_current).mode == CLIMATE_MODE_HEAT", text)
        self.assertIn("static_cast<int>(std::lround(speed)) > 0", text)
        self.assertIn('climate.control: { id: tion_climate_current, mode: "FAN_ONLY" }', text)


if __name__ == "__main__":
    unittest.main()
