# CLI Task Manager

A command-line task manager built with Python. It allows users to create, view, complete, filter, sort, and delete tasks. Tasks are stored in a JSON file so they can persist between program runs.

## Features

* Add tasks with a title, priority, and due date.
* List saved tasks.
* Mark tasks as completed.
* Filter tasks by completion status or priority.
* Sort tasks by due date or priority.
* Delete tasks.
* Store task data in JSON.
* Support interactive menu and command-line arguments.
* Validate task input and handle common errors.

## Requirements

* Python 3
* pytest (for running the tests)

## Setup

1. Clone this repository:

   ```bash
   git clone <your-repository-url>
   ```

2. Navigate to the project directory:

   ```bash
   cd CLI_TASK_MANAGER
   ```

## Usage

Start the interactive menu:

```bash
python main.py
```

You can also use command-line subcommands. For example:

```bash
python main.py list
```

To see the available commands and arguments, run:

```bash
python main.py --help
```

For help with a particular command, use:

```bash
python main.py add --help
```

Check the command-line arguments supported by your implementation before relying on these examples.

## Running Tests

Run the test suite with:

```bash
python -m pytest
```

## Technologies

* Python
* JSON
* argparse
* pytest

## Project Purpose

This project was built to practise Python programming, file handling, data validation, error handling, command-line interfaces, and automated testing.
