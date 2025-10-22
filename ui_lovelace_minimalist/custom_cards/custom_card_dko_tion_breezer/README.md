# card_dko_tion_breezer

Карточка UI Lovelace Minimalist для управления бризерами Tion. Шаблон ожидает сущность `climate`, созданную ESPHome-пакетами из этого репозитория, и автоматически подставляет идентификаторы вспомогательных сущностей (`switch`, `number`, `sensor` и т. д.), отбрасывая префикс `climate.`.

## Требования
- UI Lovelace Minimalist;
- `custom:button-card`;
- `browser_mod` (когда используется всплывающее окно);
- `custom:apexcharts-card` для графика в попапе;
- ESPHome-настройка бризера на основе [dentra/esphome-tion](https://github.com/dentra/esphome-tion) с пакетами из каталога `esphome/`.

Карточка совместима со стандартными сущностями, которые создаёт проект `esphome-tion`: `climate`, `switch`, `number`, `sensor` и т. д. Единственное, что требуется дополнительно, — сервис `esphome.<имя>_set_fan_speed` для задания диапазона скоростей. Его можно добавить, подключив облегчённый пакет из этого репозитория:

```yaml
packages:
  tion_auto_mode:
    url: https://github.com/dima11235/esphome-tion-ha-lovelace
    ref: main
    refresh: 0s
    files:
      - esphome/tion_set_fan_speed.yaml
```

Пакет обращается к числовым компонентам с `id: min_fan_speed` и `id: max_fan_speed`. Убедитесь, что в конфигурации `esphome-tion` соответствующие `number`-элементы (минимальная и максимальная скорость) объявлены именно с такими идентификаторами — иначе сервис `esphome.<имя>_set_fan_speed` не сможет корректно задать диапазон.

## Установка
1. Скопируйте папку `custom_card_dko_tion_breezer/` в `<config>/ui_lovelace_minimalist/custom_cards/`. Создайте каталог `custom_cards`, если его ещё нет.
2. Перезагрузите UI Lovelace Minimalist (или перезапустите Home Assistant), чтобы шаблон подхватился.

## Использование
```yaml
- type: "custom:button-card"
  template: "card_dko_tion_breezer"
  entity: climate.tion_breezer
  variables:
    ulm_card_breezer_enable_controls: true
    ulm_card_breezer_enable_popup: true  # требуется browser_mod
```

Если климатическая сущность называется иначе, укажите нужные идентификаторы вручную — их список приведён в верхней части `custom_card_dko_tion_breezer.yaml`. Карточка поддерживает переключатели режимов (`switch.*`), селекторы (`select.*`), числовые входы (`number.*`), сенсоры (`sensor.*`) и сервис `esphome.<имя>_set_fan_speed`, созданные конфигурацией ESPHome.

## Всплывающее окно
Опциональный попап описан в `custom_card_dko_popup_tion_breezer.yaml`. Включите его, передав `ulm_card_breezer_enable_popup: true`. Попап отображает краткий обзор режимов, показатели CO₂ и историю за последние 24 часа (график строится через `custom:apexcharts-card`).

## Локализация
Переводы лежат в каталоге `languages/`. Добавляйте новые файлы `<lang>.yaml`, повторяя структуру существующих переводов.
