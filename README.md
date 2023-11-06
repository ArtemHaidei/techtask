# Python Device Management System

This project includes a simple set of .py scripts for managing Employees, Devices, and Device Usages within a Docker environment, utilizing SQLAlchemy for database interaction with an SQL database.

## Features

- `Employee`, `Devices`, `Usages` models implemented using SQLAlchemy ORM.
- Command-line interaction with models through simple Python scripts.
- Data persistence in `database.db`.
- Interactive addition, updating, and deletion of records.
- Reporting of device usage per employee.
- Functionality for checking in and checking out devices by employees.

## Requirements

- Docker or for local install Python and the required dependencies on your machine.

# Quick Start

## Docker

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/ArtemHaidei/techtask.git
cd path/to/repository
```

Run the Docker container:

```bash
docker build -t techtask . && docker run -it --name techtask techtask
```

After creating the image and launching the container, the terminal will have access to run scripts in the container and display the result in the terminal. 

## or Environment

- Create venv and install requirements.txt

## Commands

### To test eaiser there are scripts to add employees and devices, by defoult in database.db in repository already exist 5 devices.

Commands to start working with a new database or create dummy employees or devices:

**Create tables**

```bash
python db.py init
```

**Add default devices**

```bash
python db.py dummy_devices
``` 

**Add default employees**
```bash
python db.py dummy_employees
```


### For `Employee`:

**List all employees:**

```bash
python employees.py list
```

**Add an employee (interactively):**

```bash
python employees.py add
```

**Update an employee (interactively):**

```bash
python employees.py update
```

**Delete an employee (interactive with confirmation):**

```bash
python employees.py delete
```



### For `Device`:

**List all devices:**

```bash
python device.py list
```

**Add an devices (interactively):**

```bash
python device.py add
```

**Update an employee (interactively):**

```bash
python device.py update
```

**Delete an devices (interactive with confirmation):**

```bash
python device.py delete
```



### For `Usage`:

**List all usage for an employee code:**

```bash
python usage.py all [employee code]
```

**List all check-ins for an employee code:**

```bash
python usage.py in [employee code]
```

**List all check-outs for an employee code:**

```bash
python usage.py out [employee code]
```

**Check in a device for an employee (interactively):**

```bash
python usage.py check_in
```

**Check out a device for an employee (interactively):**

```bash
python usage.py check_out
```
