import signal
import threading
from types import FrameType
from typing import Callable

import gevent


class GreenletRunner:

    def __init__(self):
        self._tasks: dict[Callable, gevent.Greenlet] = {}
        self._lock = threading.RLock()
        self._is_stoped = threading.Event()

    def add(self, *callables) -> None:
        """Запускает задачи."""
        if self._is_stoped.is_set():
            raise RuntimeError('GreenletRunner stopped')

        with self._lock:
            for func in callables:
                if func in self._tasks:
                    raise ValueError(f'Task {func} already added')
                self._tasks[func] = gevent.spawn(func)

    def remove(self, *callables, timeout: float | None = None) -> None:
        """Останавливает и удаляет задачи.

        Может произойти переключение гринлетов.
        """
        with self._lock:
            for func in callables:
                greenlet = self._tasks.get(func)
                if greenlet is None:
                    continue

                if not greenlet.dead:
                    greenlet.kill(timeout=timeout)

                del self._tasks[func]

    def _shutdown(self, signum: int, frame: FrameType | None) -> None:
        """Корректно завершает работу всех управляемых задач"""
        self._is_stoped.set()
        for greenlet in self._tasks.values():
            greenlet.kill(block=False)

    def run(self) -> None:
        signal.signal(signal.SIGTERM, self._shutdown)
        signal.signal(signal.SIGINT, self._shutdown)

        while not self._is_stoped.is_set():
            gevent.joinall(list(self._tasks.values()))
