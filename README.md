# ESPHome-пакеты для бризеров Tion

Готовые ESPHome-пакеты для управления бризером [Tion](https://tion.ru/) через Home Assistant.  
Пакеты создают сущности (`switch`, `number`, `sensor`), с которыми работает **[tion-breezer-tile-card](https://github.com/dima11235/tion-breezer-tile-card)**.

---

## Как это работает

```
dentra/esphome-tion          → climate.brizer_bedroom
esphome-tion-ha-lovelace     → switch/number/sensor.*_power_mode, *_heater_mode, …
tion-breezer-tile-card       → читает все эти сущности и управляет ими
```

[dentra/esphome-tion](https://github.com/dentra/esphome-tion) создаёт климатическую сущность (`climate.<имя>`).  
Пакеты из этого репозитория добавляют вспомогательные сущности поверх неё — автоматику по CO₂, переключатели режимов, числовые настройки.  
Карточка [tion-breezer-tile-card](https://github.com/dima11235/tion-breezer-tile-card) автоматически выводит идентификаторы всех сущностей из имени `climate.<имя>` и предоставляет готовый интерфейс управления.

---

## Требования

- [dentra/esphome-tion](https://github.com/dentra/esphome-tion) — ESPHome-компонент для бризеров Tion.
- [tion-breezer-tile-card](https://github.com/dima11235/tion-breezer-tile-card) — кастомная карточка для Lovelace (устанавливается через HACS).
- Внешний сенсор CO₂ в Home Assistant (если используется `tion_auto_mode.yaml`).

---

## Быстрый старт

### 1. ESPHome-конфигурация

```yaml
esphome:
  name: brizer_bedroom   # имя устройства → префикс всех сущностей

substitutions:
  auto_mode_co2_sensor: sensor.living_room_co2  # ваш сенсор CO₂ в HA

packages:
  tion_auto_mode:
    url: https://github.com/dima11235/esphome-tion-ha-lovelace
    ref: main
    refresh: 0s
    files:
      - esphome/tion_auto_mode.yaml

# Климат настраивается через dentra/esphome-tion:
climate:
  - platform: tion
    id: tion_climate
    name: None
    enable_heat_cool: true
    enable_fan_auto: false
```

После прошивки в HA появятся сущности вида `switch.brizer_bedroom_power_mode`, `sensor.brizer_bedroom_fan_speed` и т. д.

### 2. Карточка в Lovelace

Установите [tion-breezer-tile-card](https://github.com/dima11235/tion-breezer-tile-card) через HACS, затем добавьте карточку:

```yaml
type: custom:tion-breezer-tile-card
entity: climate.brizer_bedroom
```

Карточка автоматически найдёт все вспомогательные сущности по префиксу `brizer_bedroom`.

---

## Схема именования сущностей

Имя устройства ESPHome (`esphome: name:`) становится префиксом всех сущностей.  
Карточка выводит их автоматически из `climate.<prefix>`:

| Сущность в HA | Что делает |
|---|---|
| `climate.<prefix>` | Климат бризера (от dentra/esphome-tion) |
| `switch.<prefix>_power_mode` | Включение / выключение |
| `switch.<prefix>_heater_mode` | Режим нагрева |
| `switch.<prefix>_silent_mode` | Тихий режим (фиксирует скорость 1) |
| `number.<prefix>_heater_temperature` | Целевая температура нагрева, °C |
| `number.<prefix>_target_co2` | Целевой уровень CO₂, ppm |
| `number.<prefix>_min_fan_speed` | Нижняя граница скорости (0–6) |
| `number.<prefix>_max_fan_speed` | Верхняя граница скорости (0–6) |
| `sensor.<prefix>_fan_speed` | Текущая скорость вентилятора |
| `sensor.<prefix>_current_co2` | Текущий CO₂ (зеркало внешнего сенсора) |

---

## Пакеты

### `tion_auto_mode.yaml` — основной

Реализует PID-регулятор скорости по CO₂ и создаёт все сущности из таблицы выше.  
Требует `substitutions.auto_mode_co2_sensor` — entity_id сенсора CO₂ в HA.

### `tion_set_fan_speed.yaml` — сервис для автоматизаций *(опционально)*

Добавляет сервис `esphome.<имя>_set_fan_speed` для управления диапазоном скоростей из автоматизаций Home Assistant:

- первый вызов — запоминает скорость;
- второй вызов в течение ~3 с — задаёт диапазон `[min, max]`;
- если второй вызов не поступил — скорость остаётся фиксированной.

> **Карточке tion-breezer-tile-card этот сервис не нужен** — она устанавливает `min_fan_speed` и `max_fan_speed` напрямую через `number.set_value`.

### `tion_others.yaml` — диагностика *(опционально)*

Добавляет сенсоры Wi-Fi RSSI и BSSID.

---

## Лицензия

MIT.
