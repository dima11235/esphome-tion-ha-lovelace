# ESPHome-пакеты для бризеров Tion

Готовые ESPHome-пакеты для управления бризером [Tion](https://tion.ru/) через Home Assistant.  
Пакеты создают набор сущностей (`switch`, `number`, `sensor`), которые обеспечивают автоматическое управление скоростью по CO₂ и совместимы с [tion-breezer-tile-card](https://github.com/dima11235/tion-breezer-tile-card).

---

## Карточка для Lovelace

Для отображения бризера в дашборде используйте **[tion-breezer-tile-card](https://github.com/dima11235/tion-breezer-tile-card)** — отдельная кастомная карточка, устанавливается через HACS, не требует UI Lovelace Minimalist.

---

## Что внутри

- `esphome/tion_auto_mode.yaml` — основной пакет: автоуправление скоростью по CO₂, все сущности для карточки.
- `esphome/tion_set_fan_speed.yaml` — дополнительный пакет: сервис `esphome.<имя>_set_fan_speed` для задания диапазона скоростей из автоматизаций HA.
- `esphome/tion_others.yaml` — опциональный пакет: диагностические сенсоры (Wi-Fi RSSI, BSSID).

---

## Требования

- Home Assistant.
- ESPHome-интеграция для бризеров Tion — [dentra/esphome-tion](https://github.com/dentra/esphome-tion).

---

## Установка

### Минимальный вариант

Если у вас уже есть `climate`, `switch`, `number` и `sensor`-сущности от [dentra/esphome-tion](https://github.com/dentra/esphome-tion), подключите только пакет `tion_auto_mode.yaml`:

```yaml
substitutions:
  auto_mode_co2_sensor: sensor.living_room_co2  # ваш сенсор CO₂

packages:
  tion_auto_mode:
    url: https://github.com/dima11235/esphome-tion-ha-lovelace
    ref: main
    refresh: 0s
    files:
      - esphome/tion_auto_mode.yaml

climate:
  - platform: tion
    id: tion_climate
    name: None
    enable_heat_cool: true
    enable_fan_auto: false
```

### Полный вариант

```yaml
substitutions:
  auto_mode_co2_sensor: sensor.living_room_co2

packages:
  tion_auto_mode:
    url: https://github.com/dima11235/esphome-tion-ha-lovelace
    ref: main
    refresh: 0s
    files:
      - esphome/tion_auto_mode.yaml      # Авторегулировка скорости по CO₂
      - esphome/tion_set_fan_speed.yaml  # Сервис для автоматизаций HA (опционально)
      - esphome/tion_others.yaml         # Wi-Fi диагностика (опционально)

climate:
  - platform: tion
    id: tion_climate
    name: None
    enable_heat_cool: true
    enable_fan_auto: false
```

---

## Сущности, которые создаёт `tion_auto_mode.yaml`

Все сущности именуются по схеме `<domain>.<device_name>_<suffix>`, где `<device_name>` — имя устройства ESPHome.

| Сущность | Описание |
|---|---|
| `switch.<имя>_power_mode` | Питание бризера |
| `switch.<имя>_heater_mode` | Режим нагрева |
| `switch.<имя>_silent_mode` | Тихий режим (фиксирует скорость 1) |
| `number.<имя>_heater_temperature` | Целевая температура нагрева |
| `number.<имя>_target_co2` | Целевой уровень CO₂ |
| `number.<имя>_min_fan_speed` | Минимальная скорость диапазона |
| `number.<имя>_max_fan_speed` | Максимальная скорость диапазона |
| `sensor.<имя>_fan_speed` | Текущая скорость вентилятора |
| `sensor.<имя>_current_co2` | Текущий уровень CO₂ |

---

## Сервис `tion_set_fan_speed.yaml`

Пакет добавляет сервис `esphome.<имя>_set_fan_speed`. Используется для задания диапазона скоростей из автоматизаций Home Assistant:

- Первый вызов — фиксирует начальную скорость.
- Второй вызов в течение ~3 с — задаёт диапазон `[min, max]`.
- Если второй вызов не поступил — скорость остаётся фиксированной.

> **Карточке [tion-breezer-tile-card](https://github.com/dima11235/tion-breezer-tile-card) этот сервис не нужен** — она устанавливает `min_fan_speed` и `max_fan_speed` напрямую через `number.set_value`.

---

## Лицензия

MIT — см. [`LICENSE`](LICENSE).
