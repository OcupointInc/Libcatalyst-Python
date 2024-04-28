from abc import ABCMeta, ABC, abstractmethod
import json
import functools

def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

class LogABCMeta(ABCMeta):
    """A metaclass that both logs function calls and supports abstract classes."""
    def __new__(cls, name, bases, namespace):
        new_namespace = {}
        for name, value in namespace.items():
            if callable(value) and not name.startswith('__'):
                value = log_function_call(value)
            new_namespace[name] = value
        return super().__new__(cls, name, bases, new_namespace)

class DriverInterface(ABC):
    @abstractmethod
    def write_spi(self, cs, data, num_bits):
        pass

    @abstractmethod
    def read_spi(self, cs, num_bits):
        pass

    def exchange_spi(self, cs, data, num_bits):
        pass

    @abstractmethod
    def set_gpio_direction(self, pin, value):
        pass

    @abstractmethod
    def read_gpio_pin(self, pin):
        pass

    @abstractmethod
    def write_gpio_pin(self, pin_name, value):
        pass