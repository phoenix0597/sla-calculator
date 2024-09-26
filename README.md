## SLA-калькулятор
Взято отсюда: https://github.com/tric-itpc/task-python

### Дано:
Есть несколько рабочих сервисов, у каждого сервиса есть состояние работает/не работает/работает нестабильно.

### Требуется написать API который:

* Получает и сохраняет данные: имя, состояние, описание
* Выводит список сервисов с актуальным состоянием
* По имени сервиса выдает историю изменения состояния и все данные по каждому состоянию

### Дополнительно

По указанному интервалу выдается информация о том сколько не работал сервис и считать SLA в процентах до 3-й запятой
Вывод всех данных должен быть в формате JSON**