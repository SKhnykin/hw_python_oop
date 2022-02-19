from typing import Dict, TypeVar


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration,
                 distance,
                 speed,
                 calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        mess = (f'Тип тренировки: {self.training_type}; Длительность:'
                f' {self.duration:.3f} ч.; Дистанция: '
                f'{self.distance:.3f} км; Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')
        return mess


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    name: str = 'Training'

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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        mess = InfoMessage(self.name,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )
        return mess


class Running(Training):
    """Тренировка: бег."""
    name: str = 'Running'

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        const_for_calc1: int = 18
        const_for_calc2: int = 20
        avg_spd: float = self.get_mean_speed()
        time_in_min: float = self.duration * 60

        calories: float = ((const_for_calc1 * avg_spd - const_for_calc2) *
                           self.weight / self.M_IN_KM * time_in_min)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    name: str = 'SportsWalking'

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
        const_for_calc1: float = 0.035
        const_for_calc2: float = 0.029
        avg_spd: float = self.get_mean_speed()
        time_in_min: float = self.duration * 60

        calories: float = ((const_for_calc1 * self.weight +
                            (avg_spd ** 2 // self.height)
                            * const_for_calc2 * self.weight) * time_in_min)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    name: str = 'Swimming'
    LEN_STEP: float = 1.38

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
        const_for_calc1: float = 1.1
        const_for_calc2: int = 2
        avg_spd: float = self.get_mean_speed()

        calories: float = ((avg_spd + const_for_calc1) * const_for_calc2 *
                           self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    train = TypeVar('train', Running, SportsWalking, Swimming)

    train_dct: Dict[str, train] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }

    # Создаем объект по ключу тренеровки и передаем упакованный набор
    # параметров в конструктор
    train_obj: Training = train_dct[workout_type](*data)
    return train_obj


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
        training = read_package(workout_type, data)
        main(training)
