<p># esphome-tion-ha-lovelace</p>

<h1>Example of Home Assistant lovelace configuration for brizer Tion</h1>

<p>Новости 2024-03-06: создан пакет для ESPHOME и логика работы автоматизаций частично перенесена в него.</p>

<p>Проект затеян для того, чтобы:</p>
<ul>
	<li>реализовать автоматический режим управления скоростью бризера по аналогии с тем, как это сделано в приложении Tion MagicAir</li>
	<li>получить карточку бризера Тион в Home Assistant следующего вида:</li>
</ul>
 <p><img alt="" src="https://github.com/dima11235/esphome-tion-ha-lovelace/blob/main/images/tion-ha-lovelace.jpg" width=50%; />

<ul>
	<li>реализовать возможность управления бризером по расписанию с помощью Home Assistant:</li>
</ul>
<p><img alt="" src="https://github.com/dima11235/esphome-tion-ha-lovelace/blob/main/images/tion-ha-scheduler-card.jpg" width=50%; />

<p>К моему большому сожалению, данный набор конфигураций слабо приспособлен для простого распространения.
Поэтому, если соберетесь их как-то использовать, нужно будет приложить много усилий.</p>

<p>Кроме того, конфигурации только что переписаны на новую платформу https://github.com/dentra/esphome-tion.
Если вы все-таки соберетесь использовать данную конфигурацию и найдете ошибки - буду крайне признателен, 
если проанализируете сбои и посоветуете как и что поправить.</p>

<p>Эта конфигурация не сопровождается и развивается по мере возможности. Все что вы делаете, вы делаете исключительно на свой страх и риск.</p>

<p>В конфигурации используются следующие дополнения к Home Assistant. Нужно добавить их через HACS и в configuration.yaml.</p>
<ul>
	<li>decluttering-card</li>
	<li>card_mod</li>
	<li>bar-card</li>
	<li>slider-entity-row</li>
	<li>multiple-entity-row</li>
	<li>mini-graph-card</li>
	<li>scheduler-card (опционально, если хотите управлять бризером по расписанию)</li>
</ul>

<p>Описание файлов:</p>
<ul>
	<li>esphome/tion_auto_mode.yaml - файл с дополнительным пакетом к конфигурации https://github.com/dentra/esphome-tion</li>
	<li>packages/brizer_bedroom.yaml - пакет с дополнительными сущностями и автоматизациями для HA</li>
	<li>ui-lovelace/decluttering_card_brizer_template.yaml - шаблон карточки бризера для decluttering_card</li>
	<li>ui-lovelace/brizer_bedroom_card.yaml - пример карточки бризера для lovelace</li>
	<li>packages/brizer_bedroom_scheduler.yaml - дополнительный пакет для управления бризером по расписанию с помощью scheduler-card (опционально)</li>
	<li>ui-lovelace/climate_scheduler_card.yaml - пример карточки scheduler-card с управлением расписание работы бризера (опционально)</li>
</ul>

<p>Приблизительная инструкция по применению дана в начале каждого из файлов.<p>
