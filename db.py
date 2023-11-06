import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Employee, Device, Usage
from choices import BrandType, DeviceType


DATABASE_URI = "sqlite:///database.db"
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DatabaseConnectionMixin:
    """This class mixin contains the database connection."""

    def __enter__(self):
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.session.rollback()

        self.session.close()


def init_db():
    """This function creates the database tables."""

    Base.metadata.create_all(bind=engine)
    print("Database initialized.")


def add_dummy_devices():
    """This function adds dummy devices."""

    default_devices = [
        {"description": "XP13 laptop", "brand": BrandType.DELL, "type": DeviceType.COMPUTER, "code": "001"},
        {"description": "Meeting room printer", "brand": BrandType.HP, "type": DeviceType.PRINTER, "code": "002"},
        {"description": "Reception printer", "brand": BrandType.HP, "type": DeviceType.PRINTER, "code": "003"},
        {"description": "QA phone 1", "brand": BrandType.SAMSUNG, "type": DeviceType.PHONE, "code": "004"},
        {"description": "QA phone 2", "brand": BrandType.SAMSUNG, "type": DeviceType.PHONE, "code": "005"},
    ]

    with SessionLocal() as session:
        for device_info in default_devices:
            device = Device(**device_info)
            session.add(device)
        session.commit()
        print("Default devices added.")


def add_dummy_employees():
    """This function adds dummy employees."""

    default_employees = [
        {"first_name": "John", "last_name": "Doe", "email": "john.doe010@example.com", "code": "010"},
        {"first_name": "Jane", "last_name": "Smith", "email": "jane.smith011@example.com", "code": "011"},
        {"first_name": "Emily", "last_name": "Johnson", "email": "emily.johnson012@example.com", "code": "012"},
        {"first_name": "Michael", "last_name": "Brown", "email": "michael.brown013@example.com", "code": "013"},
        {"first_name": "Jessica", "last_name": "Davis", "email": "jessica.davis014@example.com", "code": "014"},
    ]

    with SessionLocal() as session:
        for user_info in default_employees:
            user = Employee(**user_info)
            session.add(user)
        session.commit()
        print("Default employees added.")


def main(scripts_dict):
    """This function runs the script."""

    slash = 100
    print("-" * slash + "\n")

    if len(sys.argv) < 2:
        print("Usage: python db.py\n init | dummy_devices | dummy_employees")
        return

    commands = sys.argv[1:]

    for command in commands:
        if command not in scripts_dict:
            print(f"Invalid command: {command}. Valid commands:\ninit | dummy_devices | dummy_employees")
            return

    for command in commands:
        scripts_dict[command.lower()]()

    print("\n" + "-" * slash)


if __name__ == "__main__":
    scripts = {
        "init": init_db,  # create tables
        "dummy_devices": add_dummy_devices,  # add default devices
        "dummy_employees": add_dummy_employees,  # add default employees
    }
    main(scripts)
