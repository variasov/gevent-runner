# Gevent Runner

**Gevent Runner** — это инструмент для управления задачами на основе гринлетов (greenlets) в Python с использованием библиотеки gevent.

## Возможности

- ✅ Запуск нескольких конкурентных задач одновременно
- ✅ Динамическое добавление и удаление задач в процессе работы
- ✅ Корректная обработка сигналов завершения (SIGTERM, SIGINT)
- ✅ Потокобезопасное управление задачами

## Установка

### Из исходников

```bash
pip install -e .
```

### Для разработки

```bash
pip install -e ".[dev]"
```

## Требования

- Python >= 3.10
- gevent == 24.11.1

## Быстрый старт

### Базовый пример

Создайте несколько задач и запустите их одновременно:

```python
import time
import gevent
from classic.gevent_runner.runner import GreenletRunner


def print_numbers():
    count = 0
    while True:
        count += 1
        print(f"[Numbers Task] Count: {count}")
        gevent.sleep(2)


def print_timestamp():
    while True:
        current_time = time.strftime("%H:%M:%S")
        print(f"[Timestamp Task] Current time: {current_time}")
        gevent.sleep(3)


def print_heartbeat():
    while True:
        print(f"[Heartbeat Task] System is alive!")
        gevent.sleep(5)


def main():
    print("Starting GreenletRunner with 3 concurrent tasks...")
    print("Press Ctrl+C to stop all tasks\n")
    
    # Создаём экземпляр runner
    runner = GreenletRunner()
    
    # Добавляем задачи в runner
    runner.add(print_numbers, print_timestamp, print_heartbeat)
    
    # Запускаем главный цикл (блокирует выполнение до получения SIGTERM или SIGINT)
    runner.run()
    
    print("\nAll tasks stopped gracefully.")


if __name__ == "__main__":
    main()
```

**Вывод:**
```
Starting GreenletRunner with 3 concurrent tasks...
Press Ctrl+C to stop all tasks

[Numbers Task] Count: 1
[Timestamp Task] Current time: 12:34:56
[Numbers Task] Count: 2
[Heartbeat Task] System is alive!
[Timestamp Task] Current time: 12:34:59
...
```

Нажмите `Ctrl+C` для корректной остановки всех задач.

## Использование

### Создание runner

```python
from classic.gevent_runner.runner import GreenletRunner

runner = GreenletRunner()
```

### Добавление задач

Вы можете добавить одну или несколько задач одновременно:

```python
# Добавление одной задачи
runner.add(my_task)

# Добавление нескольких задач
runner.add(task1, task2, task3)

# Добавление задачи с демоном
runner.add(task1, is_daemon=True)
```

**Важно:** Задача должна быть вызываемой функцией (callable). Каждая задача может быть добавлена только один раз.

### Удаление задач

Остановка и удаление задач с опциональным таймаутом:

```python
# Удаление одной задачи
runner.remove(my_task)

# Удаление нескольких задач с таймаутом
runner.remove(task1, task2, timeout=2.0)
```

При удалении задачи, гринлет будет корректно завершён.

### Запуск runner

```python
# Запуск основного цикла (блокирующий вызов)
runner.run()
```

Метод `run()` блокирует выполнение до получения сигнала `SIGTERM` или `SIGINT` (Ctrl+C).
