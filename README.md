# esphome-tion-ha-lovelace
Example of HA lovelace configuration for brizer Tion

Внимание!
К моему большому сожалению, данный набор конфигураций совсем не приспособлен для какого-либо простого распространения и использования.
И, более того, я не представляю, как его приспособить.
Поэтому для того, чтобы его интегрировать в собственную конфигурацию нужно будет приложить много усилий.
И если этот процесс вас не увлекает, бросьте и не занимайтесь.

Кроме того, конфигурации только что переписаны на новую платформу https://github.com/dentra/esphome-tion.
В эксплуатации практически не были. Поэтому, наверняка, содержат много недочетов и ошибок.
Если найдете - буду крайне признателен, если проанализируете и посоветуете как и что поправить.

Весь огород затеян только для того, чтобы получить карточку бризера Тион следующего вида


Используются следующие дополнения к Home Assistant.
Нужно добавить их через HACS и в configuration.yaml.
decluttering-card
card_mod
bar-card
slider-entity-row
multiple-entity-row
mini-graph-card


Описание файлов:
esphome/esphome_config.yaml - файл с добавлениями к конфигурации https://github.com/dentra/esphome-tion
packages/brizer_bedroom.yaml - пакет с дополнительными сущностями и автоматизациями для HA
ui-lovelace/decluttering_card_brizer_template.yaml - шаблон карточки бризера для decluttering_card
ui-lovelace/brizer_bedroom_card.yaml - пример карточки бризера для lovelace

