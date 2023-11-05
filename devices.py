import sys
from tabulate import tabulate
from models import Device
from db import DatabaseConnection
from choiches import BrandType, DeviceType, get_type_by_name
from settings import tabluate_kwargs


class DeviceScript(DatabaseConnection):
    """
        This class contains all the commands for managing devices.
    """
    def __init__(self):
        self.commands = {
            "list": self.list_devices,
            "add": self.add_device,
            "update": self.update_device,
            "delete": self.delete_device,
        }
        self.session = None
        self.joined_brand_choices = ", ".join([brand.value[0] for brand in BrandType])
        self.joined_device_choices = ", ".join([device.value[0] for device in DeviceType])

    def is_code_unique(self, code_to_check):
        """Checks if the entered code is unique."""
        return self.session.query(Device).filter(Device.code == code_to_check).first() is None

    def list_devices(self):
        """List all devices."""
        devices = self.session.query(Device).all()

        if not devices:
            print("No devices found.")
            return

        data = []
        for device in devices:
            data.append({
                "id": str(device.id),
                "description": device.description,
                "brand": device.brand.value[1],
                "type": device.type.value[1],
                "code": device.code
            })
        print(tabulate(data, **tabluate_kwargs))

    def add_device(self):
        """Add a new device."""
        description = input("Enter description: ").strip()
        check_brand, check_device = True, True
        brand, device, code = None, None, None

        while True:
            if check_brand:
                input_brand = input(f"Enter the selected device brand names ({self.joined_brand_choices}): ").strip().lower()
                brand = get_type_by_name(name=input_brand, enum_class=BrandType)
                if not brand:
                    print("Invalid brand. Please enter one of the following: " + self.joined_brand_choices)
                    continue
                check_brand = False

            if check_device:
                input_device = input(f"Enter device type ({self.joined_device_choices}): ").strip().lower()
                device = get_type_by_name(name=input_device, enum_class=DeviceType)
                if not device:
                    print("Invalid brand. Please enter one of the following: " + self.joined_device_choices)
                    continue
                check_device = False

            code = input("Enter code: ").strip()
            if not self.is_code_unique(code_to_check=code):
                print("This code is already in use. Please try a different one.")
                continue
            break

        new_device = Device(description=description, brand=brand, type=device, code=code)
        self.session.add(new_device)
        self.session.commit()
        print(f"Device with code {code} added.")

    def update_device(self):
        """Update an existing device."""
        device_code = input("Enter the device code to update: ")

        if not device_code:
            print("Invalid input.")
            return

        device_inst = self.session.query(Device).filter(Device.code == device_code).first()
        if not device_inst:
            print("Device not found!")
            return

        device_inst.description = input(f"Enter new description: ") or device_inst.description
        check_brand, check_device = True, True

        while True:
            if check_brand:
                input_brand = input(f"Enter new brand ({self.joined_brand_choices}): ").strip().lower()
                brand = get_type_by_name(name=input_brand, enum_class=BrandType)
                if brand:
                    device_inst.brand = brand
                else:
                    print("Invalid brand. Please enter one of the following: " + self.joined_brand_choices)
                    continue
                check_brand = False

            if check_device:
                input_device = input(f"Enter new device type ({self.joined_device_choices}): ").strip().lower()
                device = get_type_by_name(name=input_device, enum_class=DeviceType)
                if device:
                    device_inst.type = device
                else:
                    print("Invalid brand. Please enter one of the following: " + self.joined_device_choices)
                    continue
                check_device = False

            code = input("Enter new code: ").strip()
            if code and not self.is_code_unique(code_to_check=code):
                print("This code is already in use. Please try a different one.")
                continue
            elif code:
                device_inst.code = code
            break

        self.session.commit()
        print(f"Device with code {device_code} updated.")

    def delete_device(self):
        """Delete an existing device."""
        device_code = input("Enter the device code to delete: ")
        device = self.session.query(Device).filter(Device.code == device_code).first()

        if not device:
            print("Device not found!")
            return

        confirm = input("Are you sure you want to delete this device? (yes/no): ").lower()
        if confirm == 'yes':
            self.session.delete(device)
            self.session.commit()
            print(f"Device with code {device_code} deleted.")
        else:
            print("Deletion cancelled.")


def main():
    """This function runs the script."""

    slash = 100
    print("-" * slash + "\n")

    if len(sys.argv) < 2:
        print("Usage: python devices.py list | add | update | delete")
        return

    command = sys.argv[1].lower()
    with DeviceScript() as es:
        if command not in es.commands:
            print(f"Invalid command: {command}")
            return

        es.commands[command]()

        print(("\n" + "-" * slash).strip())


if __name__ == "__main__":
    main()
