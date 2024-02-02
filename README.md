<p># esphome-tion-ha-lovelace</p>

<h1>Example of HA lovelace configuration for brizer Tion</h1>

<p>Внимание!</p>
<p>К моему большому сожалению, данный набор конфигураций совсем не приспособлен для какого-либо простого распространения и использования. 
<p>И, более того, я не представляю, как его приспособить.</p>
<p>Поэтому для того, чтобы его интегрировать в собственную конфигурацию нужно будет приложить много усилий.</p>
<p>И если этот процесс вас не увлекает, бросьте и не занимайтесь.</p>

<p>Кроме того, конфигурации только что переписаны на новую платформу https://github.com/dentra/esphome-tion.</p>
<p>В эксплуатации практически не были. Поэтому, наверняка, содержат много недочетов и ошибок.</p>
<p>Если найдете - буду крайне признателен, если проанализируете и посоветуете как и что поправить.</p>

<p>&nbsp;</p>
<p>Весь огород затеян только для того, чтобы получить карточку бризера Тион следующего вида:</p>

<p><img alt="" src="https://github.com/dima11235/esphome-tion-ha-lovelace/blob/main/images/tion-ha-lovelace.jpg" />

<p>Используются следующие дополнения к Home Assistant. Нужно добавить их через HACS и в configuration.yaml.</p>
<ul>
	<li>decluttering-card</li>
	<li>card_mod</li>
	<li>bar-card</li>
	<li>slider-entity-row</li>
	<li>multiple-entity-row</li>
	<li>mini-graph-card</li>
</ul>

<p>Описание файлов:</p>
<ul>
	<li>esphome/esphome_config.yaml - файл с добавлениями к конфигурации https://github.com/dentra/esphome-tion</li>
	<li>packages/brizer_bedroom.yaml - пакет с дополнительными сущностями и автоматизациями для HA</li>
	<li>ui-lovelace/decluttering_card_brizer_template.yaml - шаблон карточки бризера для decluttering_card</li>
	<li>ui-lovelace/brizer_bedroom_card.yaml - пример карточки бризера для lovelace</li>
</ul>

