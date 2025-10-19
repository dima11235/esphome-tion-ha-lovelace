# Tion Breezer Toolkit for Home Assistant

Ready-to-use ESPHome packages and a UI Lovelace Minimalist custom card for controlling Tion breezer devices (including MagicAir based builds) from Home Assistant. The goal of this repository is to give you a single place to grab the firmware logic, Lovelace card, popup, and translation pieces so you can share the same polished user experience with others.

## What's inside?
- `esphome/` - reusable packages that expose CO2-driven auto mode, helper services, and diagnostics for ESPHome-based Tion controllers.
- `ui_lovelace_minimalist/custom_cards/` - the minimalist dashboard card (`custom_card_dko_tion_breezer`) and matching popup for deep control.
- `images/` - drop screenshots here if you want to showcase the card (add your own image before publishing a release).

## Requirements
- Home Assistant 2023.12 or newer.
- ESPHome 2023.12 or newer with a Tion controller flashed (tested with [dentra/esphome-tion](https://github.com/dentra/esphome-tion)).
- UI Lovelace Minimalist 2024.6+.
- Custom cards used by the template: `button-card`, `browser_mod`, and `apexcharts-card`.

## Quick start
1. **Download the project.** Clone the repo or grab the latest archive from GitHub.
2. **Copy the Minimalist card.** Place `ui_lovelace_minimalist/custom_cards/custom_card_dko_tion_breezer/` into the folder that UI Lovelace Minimalist reads for custom cards (typically `<config>/ui_lovelace_minimalist/custom_cards/`). Restart Home Assistant if the new template is not detected immediately.
3. **Import the ESPHome packages.** Reference the packages from your device YAML to enable automatic fan control plus helper services (example below).
4. **(Optional) Enable the popup.** Keep the popup template in the same directory so it can be loaded when `ulm_card_breezer_enable_popup` is set to `true`.

## ESPHome integration
Include the packages from `esphome/` to bring in the CO2-based auto mode, manual speed helpers, and diagnostics. Configure the CO2 sensor that should drive the automation via `substitutions`:

```yaml
substitutions:
  auto_mode_co2_sensor: sensor.living_room_co2

packages:
  tion_auto_mode:
    url: https://github.com/dima11235/esphome-tion-ha-lovelace
    files:
      - esphome/tion_auto_mode.yaml
      - esphome/tion_set_fan_speed.yaml
      - esphome/tion_others.yaml
```

Key entities exposed by these packages (the card expects the same suffixes):
- `number.<name>_target_co2` - CO2 setpoint in ppm.
- `number.<name>_min_fan_speed` / `number.<name>_max_fan_speed` - boundaries for the automatic mode.
- `switch.<name>_power_mode`, `switch.<name>_heater_mode`, `switch.<name>_silent_mode`, `switch.<name>_recirculation`.
- `number.<name>_heater_temperature` - target heater temperature.
- `sensor.<name>_current_co2`, `sensor.<name>_fan_speed`, `sensor.<name>_outdoor_temperature`.
- ESPHome service `esphome.<name>_set_fan_speed` - allows direct speed overrides.

## UI Lovelace Minimalist card
Copy the whole `ui_lovelace_minimalist/custom_cards/custom_card_dko_tion_breezer/` directory into your `ulm_templates/custom_cards/` folder (or reference it via Git). Then extend ULM with the new card in your `user_config.yaml`:

```yaml
custom_cards:
  - "custom_card_dko_tion_breezer"
```

Add the card to a dashboard:

```yaml
- type: "custom:button-card"
  template: "card_dko_tion_breezer"
  entity: climate.tion_breezer
  variables:
    ulm_card_breezer_enable_popup: true   # requires browser_mod
    ulm_card_breezer_enable_controls: true
```

The template derives helper entity IDs from the `climate` entity name (everything after `climate.` is used as a prefix), so keep the ESPHome entity names consistent with the defaults from this repo or override the variables manually for custom setups.

### Popup
The matching popup lives in `custom_card_dko_popup_tion_breezer.yaml`. Include it beside the main card and enable `ulm_card_breezer_enable_popup`. The popup gives you quick access to socket power, heater, CO2 target, speed boundaries, and a 24h ApexCharts history (make sure `custom:apexcharts-card` is installed).

## Preview
![Full card layout](images/big.jpg)
![Compact card layout](images/small.jpg)

### Localization
English and Russian strings are pre-defined in `languages/`. If you need another language just drop an additional `<LANG>.yaml` file in the same folder following the existing structure.

## Development & contributions
- Feel free to open issues or pull requests with enhancements and bug fixes.
- Keep YAML formatted with two spaces, avoid trailing spaces, and prefer ASCII characters unless the target language demands otherwise.
- When contributing new strings remember to update the translation files.

## License
Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.

## Кратко на русском
- Скачайте репозиторий (git clone или архив).
- Подключите пакеты из каталога `esphome/` и пропишите свой датчик CO2 через `substitutions`.
- Скопируйте папку `ui_lovelace_minimalist/custom_cards/custom_card_dko_tion_breezer/` в каталог custom_cards UI Lovelace Minimalist.
- Добавьте карточку и (опционально) всплывающее окно (`custom_card_dko_popup_tion_breezer.yaml`) на дашборд.

Готово — карточкой можно делиться с сообществом, просто дав ссылку на этот репозиторий GitHub.
