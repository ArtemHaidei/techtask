import uuid

from sqlalchemy import Column, String, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from choices import BrandType, DeviceType, UsageCheck
from settings import GUID

Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(128))
    last_name = Column(String(128))
    email = Column(String(128), unique=True)
    code = Column(String, unique=True)
    usages = relationship("Usage", back_populates="employee")

    def __repr__(self):
        return f"Code: {self.code}"

    def __str__(self):
        return f"<{self.code}>"


class Device(Base):
    __tablename__ = 'device'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    description = Column(String)
    brand = Column(Enum(BrandType), nullable=False, default=BrandType.DELL)
    type = Column(Enum(DeviceType), nullable=False, default=DeviceType.COMPUTER)
    code = Column(String(10), unique=True)
    usages = relationship("Usage", back_populates="device")

    def __repr__(self):
        return f"Code: {self.code}"

    def __str__(self):
        return f"<{self.code}>"


class Usage(Base):
    __tablename__ = 'usage'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    date = Column(DateTime, default=func.now())
    employee_id = Column(GUID(), ForeignKey('employee.id'), nullable=True)
    employee = relationship("Employee", back_populates="usages")
    device_id = Column(GUID(), ForeignKey('device.id', ondelete='CASCADE'))
    device = relationship("Device", back_populates="usages")
    type = Column(Enum(UsageCheck), nullable=False, default=UsageCheck.CHECK_IN)

    def __str__(self):
        return (f"Date: {self.date}"
                f"\nType: ({self.type})")

    def __repr__(self):
        return (f"Date: {self.date}"
                f"\nEmployee code: {self.employee.code}"
                f"\nDevice code: {self.device.code}"
                f"\nType: {self.type}")
