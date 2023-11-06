import sys
import re
from tabulate import tabulate
from models import Employee, Usage
from db import DatabaseConnectionMixin
from choices import UsageCheck
from settings import tabluate_kwargs


class EmployeeScript(DatabaseConnectionMixin):
    """
    This class contains all the commands for managing employees table.
    """

    def __init__(self):
        self.commands = {
            "list": self.list_employees,
            "add": self.add_employee,
            "update": self.update_employee,
            "delete": self.delete_employee,
        }
        self.session = None

    @staticmethod
    def validate_name(name):
        """
        Checks if the entered name is valid.

        Args:
            name (tuple): index: 0 - (First name or Second name), 1 - (input name).

        Returns:
            bool: Returns True if the name is valid, otherwise False.
        """

        key = name[0]
        value = name[1].strip()

        if len(value) < 3:
            print(f"{key} must be longer than 2 characters.")
            return False

        if any(char.isdigit() for char in value):
            print(f"{key} cannot contain numbers.")
            return False

        if re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            print(f"{key} cannot contain special characters.")
            return False

        return True

    def validate_code(self, code, employee=None):
        """
            Checks if the entered code is not used by another Enployee.

            Args:
                code (str): The code to validate.
                employee (object | none): The instance of Enployee model.

            Returns:
                bool: Returns True if the code is valid, otherwise False.
        """

        if not code:
            print("Invalid code.")
            return False

        existing_code = self.session.query(Employee).filter(Employee.code == code).first()
        if not existing_code:
            return True

        if employee and code == employee.code:
            return True

        print("This code is already in use. Please try a different one.")
        return False

    def validate_email(self, email, employee=None):
        """
            Verifies that the entered email address is valid and not used by another employee.

            Args:
                email (str): The email address to validate.
                employee (object | none): The instance of Enployee model.

            Returns:
                bool: Returns True if the email is valid, otherwise False.
        """

        pattern = r"(^[a-z0-9_.+-]+@[a-z0-9-]+\.[a-z]+$)"
        if not re.match(pattern, email):
            print("This is not a valid email format. Please try again.")
            return False

        existing_email = self.session.query(Employee).filter(Employee.email == email).first()
        if not existing_email:
            return True

        if employee and email == employee.email:
            return True

        print("This email is already used by another employee. Please enter a different email.")
        return False

    def list_employees(self):
        """Print list of all employees.(Prints a table with all employees using tabulate)."""

        employees = self.session.query(Employee).all()
        if not employees:
            print("No employees found.")
            return

        data = []
        for employee in employees:
            data.append({
                "id": employee.id,
                "first name": employee.first_name,
                "last name": employee.last_name,
                "email": employee.email,
                "code": employee.code
            })
        print("Employees list:")
        print(tabulate(data, **tabluate_kwargs))

    def add_employee(self):
        """Add a new employee."""
        while True:
            first_name, last_name = input("Enter first and last name: ").title().split()
            if not self.validate_name(("First name", first_name)) or not self.validate_name(("Last name", last_name)):
                continue
            break

        email, code = None, None

        while True:
            if not email:
                email = input("Enter email: ").strip()
                if not self.validate_email(email=email):
                    email = None
                    continue

            if not code:
                code = input("Enter code: ").strip()
                if not self.validate_code(code=code):
                    code = None
                    continue
            break

        self.session.add(
            Employee(first_name=first_name, last_name=last_name, email=email, code=code)
        )
        self.session.commit()
        print(f'Employee {code} added.')

    def update_employee(self):
        """Update an existing employee."""
        employee_code = input("Enter the employee code to update: ")

        if not employee_code:
            print("Invalid input.")
            return

        employee = self.session.query(Employee).filter(Employee.code == employee_code).first()
        if not employee:
            print("Employee not found!")
            return

        first_name = True

        while True:
            if first_name:
                first_name = input("Enter first name if want to update, to skip press Enter: ").title()
                if not first_name:
                    first_name = False
                    continue

                if self.validate_name(("First name", first_name)):
                    employee.first_name = first_name
                else:
                    continue

                first_name = False
                continue

            last_name = input("Enter last name if want to update, to skip press Enter: ").title()

            if last_name and self.validate_name(("Last name", last_name)):
                employee.last_name = last_name
                break

            if not last_name:
                break

            continue

        chek_email = True

        while True:
            if chek_email:
                new_email = input(f"Enter your new email address if you want to update, to skip press Enter: ").strip()
                if new_email and not self.validate_email(new_email, employee=employee):
                    continue
                elif new_email:
                    employee.email = new_email

                chek_email = False

            new_code = input(f"Enter your new employee code if you want to update, to skip press Enter: ").strip()
            if new_code and not self.validate_code(new_code, employee=employee):
                continue
            elif new_code:
                employee.code = new_code
            break

        self.session.commit()
        print(f'Employee {employee_code} updated.')

    def delete_employee(self):
        """Delete an existing employee."""
        employee_code = input("Enter the employee code to delete: ")
        employee = self.session.query(Employee).filter(Employee.code == employee_code).first()

        if not employee:
            print("Employee not found!")
            return

        confirm = input("Are you sure you want to delete this employee? (yes/no): ").lower()
        if confirm in ['yes', 'y']:
            self.check_out_usages(employee)
            self.session.delete(employee)
            self.session.commit()
            print(f"Employee {employee_code} deleted.")
        else:
            print("Deletion cancelled.")

    def check_out_usages(self, employee):
        """Check out usages for employee."""
        usages = self.session.query(Usage).filter(
            Usage.employee_id == employee.id, Usage.type == UsageCheck.CHECK_IN).all()
        if not usages:
            return

        for usage in usages:
            usage.type = UsageCheck.CHECK_OUT


def main():
    """This function runs the script."""

    slash = 100
    print("-" * slash + "\n")

    if len(sys.argv) < 2:
        print("Usage: python employees.py\nlist | add | update | delete")
        return

    command = sys.argv[1].lower()
    with EmployeeScript() as es:
        if command not in es.commands:
            print(f"Invalid command: {command}. Valid commands:\nlist | add | update | delete")
            return

        es.commands[command]()

        print("\n" + "-" * slash)


if __name__ == "__main__":
    main()
