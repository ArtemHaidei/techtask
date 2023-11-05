import sys
from tabulate import tabulate
from models import Employee, Device, Usage
from db import DatabaseConnection
from choiches import UsageCheck
from settings import tabluate_kwargs


class EmployeeUsageScript(DatabaseConnection):
    def __init__(self):
        self.commands = {
            "list": self.list,
            "all": self.all_usages,
            "in": self.all_check_in,
            "out": self.all_check_out,
            "check_in": self.check_in,
            "check_out": self.check_out,
        }
        self.employee = None
        self.device = None
        self.session = None

    def get_usages_with_device_info(self, search_type=None):
        """Get query usages with device info."""
        query = self.session.query(
            Usage.date,
            Usage.type,
            Device.description,
            Device.brand,
            Device.type.label('device_type'),
            Device.code
        ).join(Device).join(Employee)

        if search_type == 'in':
            return query.filter(Usage.employee_id == self.employee.id, Usage.type == UsageCheck.CHECK_IN).all()
        elif search_type == 'out':
            return query.filter(Usage.employee_id == self.employee.id, Usage.type == UsageCheck.CHECK_OUT).all()
        else:
            return query.filter(Usage.employee_id == self.employee.id).all()

    def load_employee_and_device(self):
        """Loads an employee and device by code and stores it in a class attribute."""
        chek_employee = True
        while True:
            if chek_employee:
                employee_code = input("Enter employee code: ").strip()
                if not employee_code:
                    print("Invalid input.")
                    continue

                if self.load_employee(employee_code):
                    chek_employee = False
                    continue

                print(f"Employee with code: {employee_code} - not found!")
                continue

            device_code = input("Enter device code: ").strip()
            if not device_code:
                print("Invalid input.")
                continue

            device = self.session.query(Device).filter(Device.code == device_code).first()
            if device is None:
                print(f"Device with code: {device_code} - not found!")
                continue
            self.device = device
            break

    def load_employee(self, code):
        """Loads an employee by code and stores it in a class attribute."""
        self.employee = self.session.query(Employee).filter(Employee.code == code).first()
        return self.employee is not None

    @staticmethod
    def print_usages(query, all_colums=False):
        """Print usages."""
        if not query:
            print("No usages found.")
            return

        data = []
        for q in query:
            data_q = [
                ("Date", q.date),
                ("Device description", q.description),
                ("Device brand", q.brand),
                ("Device type", q.device_type),
                ("Device code", q.code)
            ]
            if all_colums:
                data_q.insert(1, ("Usages type", q.type.value[1]))

            data.append(dict(data_q))

        print(tabulate(data, **tabluate_kwargs))

    def all_usages(self):
        """List all usage for an employee."""
        query = self.get_usages_with_device_info()
        if not query:
            print(f"No usages found for employee {self.employee.code}")
            return
        self.print_usages(query, all_colums=True)

    def all_check_in(self):
        """List all check in for an employee."""
        query = self.get_usages_with_device_info(search_type='in')
        if not query:
            print(f"No usages chek in found for employee {self.employee.code}")
            return
        self.print_usages(query)

    def all_check_out(self):
        """List all check out for an employee code."""
        query = self.get_usages_with_device_info(search_type='out')
        if not query:
            print(f"No usages chek out found for employee {self.employee.code}")
            return
        self.print_usages(query)

    def check_in_or_out(self, prefix, usage=None):
        """Check in or out a device."""
        if prefix == "checked in":
            self.session.add(
                Usage(employee_id=self.employee.id, device_id=self.device.id, type=UsageCheck.CHECK_IN)
            )
        elif prefix == "checked out":
            usage.type = UsageCheck.CHECK_OUT

        self.session.commit()
        print(f'Device with code "{self.device.code}" {prefix} for Employee with code "{self.employee.code}".')

    def check_in(self):
        """Check in a device."""
        self.load_employee_and_device()

        if self.session.query(Usage).filter(Usage.device_id == self.device.id,
                                            Usage.type == UsageCheck.CHECK_IN).first():
            print(f"Device with code: {self.device.code} - already checked in!")
            return

        self.check_in_or_out(prefix="checked in")

    def check_out(self):
        """Check out a device."""
        self.load_employee_and_device()
        usage = self.session.query(Usage).filter(Usage.device_id == self.device.id,
                                                 Usage.employee_id == self.employee.id,
                                                 Usage.type == UsageCheck.CHECK_IN).first()
        if usage is None:
            print(f"Device with code: {self.device.code} - was check out!")
            return

        self.check_in_or_out(prefix="checked out", usage=usage)


def run():
    """This function runs the script."""

    slash = 100
    print("-" * slash + "\n")

    if len(sys.argv) < 2:
        print("usage.py comands:"
              "\n all | in | out | check_in [employee_code] | check_out [employee_code]")
        return

    command = sys.argv[1].lower()

    with EmployeeUsageScript() as eus:
        if command not in eus.commands:
            print(f"Invalid command: {command}")
            return

        if len(sys.argv) == 3:
            code = sys.argv[2]
            if not eus.load_employee(code):
                print(f"Employee with code {code} not found!")
                return

        eus.commands[command]()

        print("\n" + "-" * slash)


if __name__ == "__main__":
    run()
