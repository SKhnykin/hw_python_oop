from typing import Dict
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        mess = (f'Тип тренировки: {self.training_type}; Длительность:'
                f' {self.duration:.3f} ч.; Дистанция: '
                f'{self.distance:.3f} км; Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')
        return mess


@dataclass
class Training:
    """Базовый класс тренировки."""
    name: str = 'Training'
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    min_in_hour: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_spead: float = self.get_distance() / self.duration
        return mean_spead

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Переопроедлите метод get_spent_calories в'
                                  f' {type(self).name}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        mess = InfoMessage(type(self).name,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )
        return mess


class Running(Training):
    """Тренировка: бег."""
    name: str = 'Running'
    const_for_calc_colories1: int = 18
    const_for_calc_colories2: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        avg_spd: float = self.get_mean_speed()
        time_in_min: float = self.duration * self.min_in_hour

        calories: float = ((self.const_for_calc_colories1 * avg_spd
                            - self.const_for_calc_colories2)
                           * self.weight / self.M_IN_KM * time_in_min)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    name: str = 'SportsWalking'
    const_for_calc_colories1: float = 0.035
    const_for_calc_colories2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        avg_spd: float = self.get_mean_speed()
        time_in_min: float = self.duration * self.min_in_hour

        calories: float = ((self.const_for_calc_colories1 * self.weight
                            + (avg_spd ** 2 // self.height)
                            * self.const_for_calc_colories2
                            * self.weight) * time_in_min)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    name: str = 'Swimming'
    LEN_STEP: float = 1.38
    const_for_calc_colories1: float = 1.1
    const_for_calc_colories2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_spead: float = (self.length_pool * self.count_pool / self.M_IN_KM
                             / self.duration)
        return mean_spead

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        avg_spd: float = self.get_mean_speed()

        calories: float = ((avg_spd + self.const_for_calc_colories1)
                           * self.const_for_calc_colories2 * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    train_dct: Dict[str, Training] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }

    if train_dct.get(workout_type) is not None:
        # Создаем объект по ключу тренеровки и передаем упакованный набор
        # параметров в конструктор
        train_obj: Training = train_dct[workout_type](*data)
        return train_obj
    else:
        raise Exception('Неверный вид тренеровки')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        try:
            training = read_package(workout_type, data)
            main(training)
        except Exception as e:
            print(e)
