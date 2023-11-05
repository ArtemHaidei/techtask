import sys
import re
from tabulate import tabulate
from models import Employee
from db import DatabaseConnection
from settings import tabluate_kwargs


class EmployeeScript(DatabaseConnection):
    def __init__(self):
        self.commands = {
            "list": self.list_employees,
            "add": self.add_employee,
            "update": self.update_employee,
            "delete": self.delete_employee,
        }
        self.session = None

    def is_valid_code(self, code, employee=None):
        """
            Checks if the entered code is valid.

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

    def is_valid_email(self, email, employee=None):
        """
            Checks if the entered email address is valid and if exist in db.

            Args:
                email (str): The email address to validate.
                employee (object | none): The instance of Enployee model.

            Returns:
                bool: Returns True if the email is valid, otherwise False.
        """
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(pattern, email) is not None:
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
        """List all employees."""
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
        first_name = input("Enter first name: ").strip()
        last_name = input("Enter last name: ").strip()
        email, code = None, None

        while True:
            if not email:
                email = input("Enter email: ").strip()
                if not self.is_valid_email(email=email):
                    email = None
                    continue

            if not code:
                code = input("Enter code: ").strip()
                if not self.is_valid_code(code=code):
                    code = None
                    continue
            break

        self.session.add(
            Employee(first_name=first_name, last_name=last_name, email=email, code=code)
        )
        self.session.commit()
        print(f'Employee with code "{code}" added.')

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

        employee.first_name = input(f"Enter your new first name if you want to update, to skip press Enter: ").strip() or employee.first_name
        employee.last_name = input(f"Enter your new second name if you want to update, to skip press Enter: ").strip() or employee.last_name
        chek_email = True

        while True:
            if chek_email:
                new_email = input(f"Enter your new email address if you want to update, to skip press Enter: ").strip()
                if new_email and not self.is_valid_email(new_email, employee=employee):
                    continue
                elif new_email:
                    employee.email = new_email

                chek_email = False

            new_code = input(f"Enter your new employee code if you want to update, to skip press Enter: ").strip()
            if new_code and not self.is_valid_code(new_code, employee=employee):
                continue
            elif new_code:
                employee.code = new_code
            break

        self.session.commit()
        print(f'Employee with code "{employee_code}" updated.')

    def delete_employee(self):
        """Delete an existing employee."""
        employee_code = input("Enter the employee code to delete: ")
        employee = self.session.query(Employee).filter(Employee.code == employee_code).first()

        if not employee:
            print("Employee not found!")
            return

        confirm = input("Are you sure you want to delete this employee? (yes/no): ").lower()
        if confirm in ['yes', 'y']:
            self.session.delete(employee)
            self.session.commit()
            print(f"Employee with code {employee_code} deleted.")
        else:
            print("Deletion cancelled.")


def main():
    """This function runs the script."""

    slash = 100
    print("-" * slash + "\n")

    if len(sys.argv) < 2:
        print("Usage: python employees.py list | add | update | delete")
        return

    command = sys.argv[1].lower()
    with EmployeeScript() as es:
        if command not in es.commands:
            print(f"Invalid command: {command}")
            return

        es.commands[command]()

        print("\n" + "-" * slash)


if __name__ == "__main__":
    main()
