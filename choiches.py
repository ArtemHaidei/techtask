from enum import Enum


class BrandType(Enum):
    DELL = 'dell', 'DELL'
    HP = 'hp', 'HP'
    SAMSUNG = 'samsung', 'SAMSUNG'


class DeviceType(Enum):
    COMPUTER = 'computer', 'COMPUTER'
    PHONE = 'phone', 'PHONE'
    PRINTER = 'printer', 'PRINTER'


class UsageCheck(Enum):
    CHECK_IN = 'check in', 'CHECK IN'
    CHECK_OUT = 'check out', 'CHECK OUT'


def get_type_by_name(name, enum_class):
    for device_type in enum_class:
        if name.lower() in (variant.lower() for variant in device_type.value):
            return device_type
    return None
