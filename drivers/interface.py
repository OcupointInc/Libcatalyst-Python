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

class DriverInterface(ABC, metaclass=LogABCMeta):
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
    def write_gpio_pin(self, pin, value):
        pass

    @abstractmethod
    def get_pin_name(self, pin):
        pass

class MockDriver(DriverInterface):
    def __init__(self, id, config_file):
        # Load the configuration json file
        with open(config_file, 'r') as f:
            self.config = json.load(f)

    def write_spi(self, cs, data, num_bits):
        print(f"SPI Write {cs}: {data:#2x}")

    def read_spi(self, cs, num_bits):
        data = 31
        print(f"SPI Read {cs}: {data:#2x}")
        return data  # Return a mock value

    def exchange_spi(self, cs, data, num_bits):
        print(f"SPI Exchange: {cs} {num_bits} bits: {data}")
        return 0  # Return a mock value

    def set_gpio_direction(self, pin, value):
        #print(f"Mock: Setting GPIO pin {pin} mode to {'output' if value else 'input'}")
        return

    def read_gpio_pin(self, pin):
        print(f"GPIO Read: {pin}")
        return 0  # Return a mock value

    def write_gpio_pin(self, pin, value):
        print(f"GPIO Write: {pin}: {value}")

    def get_pin_name(self, pin):
        return self.config[pin]