import re
import unittest
from pathlib import Path

YAML = Path(__file__).resolve().parents[1] / "esphome" / "tion_auto_mode.yaml"


class SettleWindowTest(unittest.TestCase):
    """Окно устаканивания должно покрывать все команды, а не только скорость.

    Инцидент 14.08.2026 (бризер Ани, 23:00): слот расписания запустил вентилятор,
    прошивка отправила FAN_ONLY вместе со скоростью и целевой температурой,
    железо через 255 мс подтвердило FAN_ONLY и ещё через 186 мс отдало HEAT.
    Зеркалирование приняло это за действие пультом и переписало желаемый режим —
    нагрев держался двое суток. Ветки смены режима и температуры окно не
    взводили, а зеркалирование его не проверяло.
    """

    def setUp(self):
        self.text = YAML.read_text(encoding="utf-8")

    def test_single_place_arms_the_window(self):
        # Иначе легко добавить команду и забыть про сброс счётчика попыток.
        self.assertIn("id: arm_settle", self.text)
        self.assertIn("id(heater_reassert_count)", self.text)
        direct = re.findall(
            r"globals\.set:\s*\n\s*id: fan_speed_settle_until", self.text
        )
        self.assertEqual(
            len(direct), 1, "окно должно взводиться только внутри script arm_settle"
        )

    def test_every_hardware_command_arms_the_window(self):
        # Каждая climate.control по tion_climate_current — это команда в железо.
        # pid_co2 не считается: это внутренний контроллер, не устройство.
        # Комментарии пропускаем: в шапке пакета climate.control упоминается
        # текстом, командой это не является.
        lines = self.text.splitlines()
        commands = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("#") or "climate.control" not in stripped:
                continue
            if not stripped.startswith("- climate.control"):
                continue
            block = "\n".join(lines[i:i + 8])
            if "tion_climate_current" not in block:
                continue  # pid_co2 — внутренний контроллер
            commands += 1
            # Окно может взводиться и до команды: в set_fan_speed оно
            # намеренно взводится один раз в начале ветки «скорость реально
            # изменилась», а команд там две (пуск и остановка).
            neighbourhood = "\n".join(lines[max(0, i - 35):i + 10])
            self.assertIn(
                "arm_settle",
                neighbourhood,
                f"команда в железо без взведения окна, строка {i + 1}:\n{stripped}",
            )
        self.assertGreaterEqual(commands, 6, "команды в железо не найдены")

    def test_hardware_reports_are_only_trusted_outside_the_window(self):
        guard = "millis() >= id(fan_speed_settle_until)"
        # Зеркалирование HEAT/FAN_ONLY, синхронизация температуры, удалённое
        # включение и выключение питания, смена скорости пультом.
        self.assertGreaterEqual(
            self.text.count(guard),
            6,
            "не все ветки, трактующие отчёт железа как чужое действие, проверяют окно",
        )

    def test_mismatch_inside_window_is_re_asserted_not_mirrored(self):
        self.assertIn("millis() < id(fan_speed_settle_until)", self.text)
        self.assertIn("settle mismatch, re-assert", self.text)
        # Расхождение переводится в pending: додавливанием занимается уже
        # существующий и проверенный механизм отложенного применения.
        idx = self.text.index("settle mismatch, re-assert")
        tail = self.text[idx:idx + 400]
        self.assertIn("heater_mode_apply_pending", tail)
        self.assertIn("value: 'true'", tail)

    def test_re_assert_is_bounded(self):
        # Без предела расхождение, которое железо не умеет исполнить,
        # крутилось бы вечно и никогда не отдало бы управление пульту.
        self.assertIn("id(heater_reassert_count) < 3", self.text)
        self.assertIn("id(heater_reassert_count)++;", self.text)

    def test_existing_guards_are_preserved(self):
        # Условия из issue-002/004/006 удалять нельзя.
        self.assertIn("id(last_set_speed) != 0", self.text)
        self.assertIn("desired_heater_mode", self.text)
        self.assertIn('climate.control: { id: tion_climate_current, mode: "FAN_ONLY" }', self.text)


if __name__ == "__main__":
    unittest.main()
