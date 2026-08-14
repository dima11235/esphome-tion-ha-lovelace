import unittest
from pathlib import Path

YAML = Path(__file__).resolve().parents[1] / "esphome" / "tion_auto_mode.yaml"


class ModeChangeLogTest(unittest.TestCase):
    """Журнал причин переключения режимов.

    Причина каждого решения прошивки должна доезжать до Home Assistant: сам по
    себе logger.log живёт только в потоке логов ESPHome и теряется при ребуте,
    а device-report от Tion приходит в HA без контекста, и по истории HA нельзя
    отличить команду HA от команды мимо HA.
    """

    def setUp(self):
        self.text = YAML.read_text(encoding="utf-8")

    def test_log_sink_and_helper_exist(self):
        self.assertIn('id: mode_change_log', self.text)
        self.assertIn('id: log_mode_change', self.text)
        self.assertIn('id(mode_change_log).publish_state(message);', self.text)

    def test_every_publication_is_unique(self):
        # HA не пишет в recorder повторно то же самое состояние текстового
        # сенсора, поэтому два одинаковых события подряд слились бы в одну
        # запись истории. Счётчик в начале строки делает их различимыми.
        self.assertIn('id: mode_log_seq', self.text)
        self.assertIn('id(mode_log_seq)++;', self.text)
        self.assertIn('"#%u %s"', self.text)

    def test_reasons_invisible_to_home_assistant_are_logged(self):
        for reason in (
            'reason: "power off: remote"',
            'reason: "power on: remote"',
            'reason: "heat on: hw report"',
            'reason: "heat off: hw report"',
            'reason: "heat on: pending apply"',
            'reason: "heat off: pending apply"',
            'reason: "heat on: pending confirmed"',
            'reason: "heat off: pending confirmed"',
            'reason: "heat on: ha, apply pending"',
            'reason: "heat off: ha, apply pending"',
            'reason: "boot: reapply power on"',
        ):
            self.assertIn(reason, self.text, f"не логируется: {reason}")

    def test_remote_power_off_is_logged_before_the_switch_is_touched(self):
        # Запись должна попасть в журнал до switch.turn_off: иначе при сбое
        # ниже по цепочке причина потерялась бы ровно в том случае, ради
        # которого журнал и заводился.
        branch = self.text.index("turn power_mode off (remote)")
        log_call = self.text.index('reason: "power off: remote"', branch)
        turn_off = self.text.index("switch.turn_off: power_mode", branch)
        self.assertLess(log_call, turn_off)

    def test_routine_pid_steps_are_not_logged(self):
        # Логируется только переход через ноль. Иначе журнал утонул бы в шагах
        # PID: их несколько раз в час на каждом бризере.
        self.assertIn("return (fan_speed == 0) != (current == 0);", self.text)


if __name__ == "__main__":
    unittest.main()
