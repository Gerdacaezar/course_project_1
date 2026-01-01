import logging


def setup_logging() -> None:
    """
        Настраивает корневое логирование для всего проекта.

    Конфигурация включает:
    - корневой логгер с уровнем DEBUG (захват всех сообщений);
    - консольный вывод (StreamHandler) с уровнем INFO и выше;
    - единый формат сообщений с датой, именем логгера, уровнем и текстом;

    Параметры:
        Нет. Функция не принимает аргументов.

    Возвращаемое значение:
        None. Функция выполняет настройку глобально через logging-модуль.
    """

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    # Консольный вывод (всегда включен)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
