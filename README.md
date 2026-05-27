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
      - esphome/tion_intake_3s.yaml   # для Tion 3S — или tion_intake_4s.yaml для 4S (опционально)
      - esphome/tion_others.yaml      # Wi-Fi диагностика (опционально)

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

## Управляющие элементы в Home Assistant

Имя устройства ESPHome (`esphome: name:`) становится префиксом всех сущностей.

### Основные — `tion_auto_mode.yaml`

| Сущность | Тип | Что делает |
|---|---|---|
| `switch.<prefix>_power_mode` | switch | Включение / выключение бризера |
| `switch.<prefix>_heater_mode` | switch | Режим нагрева воздуха |
| `switch.<prefix>_silent_mode` | switch | Тихий режим — фиксирует скорость 1 |
| `number.<prefix>_heater_temperature` | number | Целевая температура нагрева, °C (0–30) |
| `number.<prefix>_target_co2` | number | Целевой уровень CO₂, ppm (400–1200) |
| `number.<prefix>_min_fan_speed` | number | Нижняя граница скорости вентилятора (0–6) |
| `number.<prefix>_max_fan_speed` | number | Верхняя граница скорости вентилятора (0–6) |
| `sensor.<prefix>_fan_speed` | sensor | Текущая скорость вентилятора |
| `sensor.<prefix>_current_co2` | sensor | Текущий CO₂ (зеркало внешнего сенсора) |
| `sensor.<prefix>_target_co2_sensor` | sensor | Целевой CO₂ (для отображения на графиках) |

### Управление заслонкой — `tion_intake_3s.yaml` / `tion_intake_4s.yaml` *(опционально)*

| Сущность | Тип | Что делает |
|---|---|---|
| `switch.<prefix>_air_intake_target` | switch | Целевое положение заслонки: вкл = открыто (улица), выкл = закрыто (рециркуляция) |

Переключатель отображает **целевое** положение заслонки. Если бризер самопроизвольно сменил положение — пакет автоматически его возвращает. На скорости 0 заслонка закрывается устройством автоматически — это норма, коррекция не срабатывает.

### Диагностика — `tion_others.yaml` *(опционально)*

| Сущность | Тип | Что делает |
|---|---|---|
| `sensor.<prefix>_wi_fi_rssi` | sensor | Уровень сигнала Wi-Fi, dBm |
| `text_sensor.<prefix>_wi_fi_bssid` | text_sensor | BSSID текущей точки доступа |

---

## Пакеты

### `tion_auto_mode.yaml` — основной

Реализует PID-регулятор скорости по CO₂ и создаёт все основные сущности.  
Требует `substitutions.auto_mode_co2_sensor` — entity_id сенсора CO₂ в HA.

### `tion_intake_3s.yaml` — управление заслонкой Tion 3S *(опционально)*

Добавляет переключатель `air_intake_target` для управления положением воздушной заслонки на **Tion 3S** (select с тремя положениями: outdoor / indoor / mixed).

- Определяет `tion_air_intake` с `internal: true` — в HA не виден, только внутренняя логика.
- Целевое состояние сохраняется между перезагрузками.
- Автокоррекция: если заслонка самопроизвольно сменила положение при работающем вентиляторе — возвращает назад (реактивно + раз в 10 секунд).
- При скорости 0 заслонка закрывается устройством автоматически — коррекция не срабатывает.

> В конфигурации бризера можно убрать или оставить `select: platform: tion, type: air_intake` — этот пакет не зависит от его наличия.

### `tion_intake_4s.yaml` — управление заслонкой Tion 4S *(опционально)*

Добавляет переключатель `air_intake_target` для управления воздушной заслонкой на **Tion 4S** (switch рециркуляции: ON = закрыто / OFF = открыто).

- Определяет `tion_recirculation` с `internal: true` — в HA не виден, только внутренняя логика.
- Целевое состояние сохраняется между перезагрузками.
- Автокоррекция: если рециркуляция самопроизвольно включилась/выключилась при работающем вентиляторе — возвращает назад (реактивно + раз в 10 секунд).
- При скорости 0 заслонка закрывается устройством автоматически — коррекция не срабатывает.

> В конфигурации бризера можно убрать или оставить `switch: platform: tion, type: recirculation` — этот пакет не зависит от его наличия.

### `tion_set_fan_speed.yaml` — сервис для автоматизаций *(опционально)*

Добавляет сервис `esphome.<имя>_set_fan_speed` для управления диапазоном скоростей из автоматизаций Home Assistant:

- первый вызов — запоминает скорость;
- второй вызов в течение ~3 с — задаёт диапазон `[min, max]`;
- если второй вызов не поступил — скорость остаётся фиксированной.

> **Карточке tion-breezer-tile-card этот сервис не нужен** — она устанавливает `min_fan_speed` и `max_fan_speed` напрямую через `number.set_value`.

### `tion_others.yaml` — диагностика *(опционально)*

Добавляет сенсоры Wi-Fi RSSI и BSSID.
