from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Employee, Device, Usage
from choiches import BrandType, DeviceType


DATABASE_URI = "sqlite:///database.db"
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DatabaseConnection:
    def __enter__(self):
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()


def init_db():
    Base.metadata.create_all(bind=engine)


def add_default_devices():

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


if __name__ == "__main__":
    init_db()
    add_default_devices()
