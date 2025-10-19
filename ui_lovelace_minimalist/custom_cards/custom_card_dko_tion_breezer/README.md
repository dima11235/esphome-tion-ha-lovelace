# custom_card_dko_tion_breezer

Minimalist UI card for Tion breezer devices. The template expects a `climate` entity created by the ESPHome packages in this repository and automatically derives helper entity IDs (`switch`, `number`, `sensor`, etc.) by stripping the `climate.` prefix.

## Installation
1. Copy this folder (`custom_card_dko_tion_breezer/`) into the directory that UI Lovelace Minimalist scans for custom cards (typically `<config>/ui_lovelace_minimalist/custom_cards/`).
2. Reload UI Lovelace Minimalist (or restart Home Assistant) so the new template is discovered.

## Usage
```yaml
- type: "custom:button-card"
  template: "card_dko_tion_breezer"
  entity: climate.tion_bedroom
  variables:
    ulm_card_breezer_enable_controls: true
    ulm_card_breezer_enable_popup: true
```

If you use a different entity naming scheme, override the variables explicitly (see the top of `custom_card_dko_tion_breezer.yaml` for the full list).

## Dependencies
- UI Lovelace Minimalist (core templates + translation engine).
- `custom:button-card`
- `browser_mod` (needed when `ulm_card_breezer_enable_popup: true`).
- `custom:apexcharts-card` for the historical chart in the popup.

## Translations
Localization files live in `languages/`. Create additional `<LANG>.yaml` files following the same structure when you add new languages.
