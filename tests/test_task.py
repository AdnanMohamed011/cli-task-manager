from main import add_task, list_tasks, complete_task, delete_task, filter_tasks, sort_task
import json

def test_add_task(tmp_path):
    json_file = tmp_path / "test.json"

    with open(json_file, "w") as f:
        json.dump([], f)

    add_task(json_file, "pytest", "high", "2026-09-28")

    with open(json_file, "r") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["title"] == "pytest"
    assert data[0]["priority"] == "high"
    assert data[0]["due_date"] =="2026-09-28"
    assert data[0]["completed"] is False


def test_add_task_invalid_date(tmp_path, capsys, monkeypatch):
    json_file = tmp_path / "test.json"
    
    with open(json_file, "w") as f:
        json.dump([], f)

    add_task(json_file, "pytest", "high", "banana")
    captured = capsys.readouterr()

    assert captured.out == "Invalid date format! Please use YYYY-MM-DD.\n"


def test_add_task_invalid_priority(tmp_path, capsys, monkeypatch):
    json_file = tmp_path / "test.json"
         
    with open(json_file, "w") as f:
        json.dump([], f)

    add_task(json_file, "pytest", "banana", "2026-09-30")
    captured = capsys.readouterr()

    assert captured.out == "You must enter one of these three (low, medium, high)\n"


def test_list_task(tmp_path, capsys):
    json_file = tmp_path / "test.json"

    with open(json_file, "w") as f:
        json.dump([{    
            "id": 3,
            "title": "testing",
            "completed": False,
            "priority": "medium",
            "due_date": "2026-09-28"
        }], f)

    list_tasks(json_file)

    captured = capsys.readouterr()

    with open(json_file, "r") as f:
        data = json.load(f)

    assert data[0]["title"] in captured.out
    assert "Pending" in captured.out


def test_list_task_empty(tmp_path, capsys):
    json_file = tmp_path / "test.json"

    with open(json_file, "w") as f:
        json.dump([], f)

    list_tasks(json_file)

    captured = capsys.readouterr()

    assert captured.out == "List empty.\n"


def test_complete_task(tmp_path, capsys):
    json_file = tmp_path / "test.json"

    with open(json_file, "w") as f:
        json.dump([{    
            "id": 3,
            "title": "testing",
            "completed": False,
            "priority": "medium",
            "due_date": "2026-09-28"
        }], f)

    complete_task(json_file, 3)
    captured = capsys.readouterr()

    with open(json_file, "r") as f:
        data = json.load(f)

    assert data[0]["completed"] is True
    assert captured.out == "testing completed!\n"


def test_complete_task_invalid_id(tmp_path, monkeypatch, capsys):
    json_file = tmp_path / "test.json"

    with open(json_file, "w") as f:
            json.dump([{    
                "id": 3,
                "title": "testing",
                "completed": False,
                "priority": "medium",
                "due_date": "2026-09-28"
            }], f)

    monkeypatch.setattr("builtins.input", lambda _: "banana")
    complete_task(json_file)
    captured = capsys.readouterr()

    assert captured.out == "You entered a non numerical value!\n"


def test_numeric_but_nonexistent_id(tmp_path, capsys):
    json_file = tmp_path / "test.json"
    with open(json_file, "w") as f:
            json.dump([{    
                "id": 3,
                "title": "testing",
                "completed": False,
                "priority": "medium",
                "due_date": "2026-09-28"
            }], f)

    complete_task(json_file, 99)
    captured = capsys.readouterr()

    assert captured.out == "ID not found.\n"


def test_task_already_completed(tmp_path, capsys):
    json_file = tmp_path / "test.json"
    with open(json_file, "w") as f:
            json.dump([{    
                "id": 3,
                "title": "testing",
                "completed": True,
                "priority": "medium",
                "due_date": "2026-09-28"
            }], f)

    complete_task(json_file, 3)
    captured = capsys.readouterr()

    assert captured.out == "This task is already completed.\n"


def test_delete_task(tmp_path):
    json_file = tmp_path / "test.json"
    with open(json_file, "w") as f:
            json.dump([{    
                "id": 3,
                "title": "testing",
                "completed": True,
                "priority": "medium",
                "due_date": "2026-09-28"
            }], f)

    delete_task(json_file, 3)

    with open(json_file, "r") as f:
        data = json.load(f)

    assert len(data) == 0


def test_numeric_nonexistent_id(tmp_path, capsys):
    json_file = tmp_path / "test.json"
    with open(json_file, "w") as f:
            json.dump([{    
                "id": 3,
                "title": "testing",
                "completed": True,
                "priority": "medium",
                "due_date": "2026-09-28"
            }], f)

    delete_task(json_file, 99)
    captured = capsys.readouterr()

    assert captured.out == "ID doesn't exist!\n"


def test_non_numeric_id(tmp_path, monkeypatch, capsys):
    json_file = tmp_path / "test.json"    
    with open(json_file, "w") as f:
            json.dump([{    
                "id": 3,
                "title": "testing",
                "completed": True,
                "priority": "medium",
                "due_date": "2026-09-28"
            }], f)

    monkeypatch.setattr("builtins.input", lambda _: "banana")
    delete_task(json_file)
    captured = capsys.readouterr()

    assert captured.out == "You entered a non numerical value!\n"


def test_filter_completed(tmp_path, capsys):
    json_file = tmp_path / "test.json"
    with open(json_file, "w") as f:
            json.dump([{    
                "id": 3,
                "title": "testing",
                "completed": False,
                "priority": "medium",
                "due_date": "2026-09-29"
                },{
                "id": 9,
                "title": "pytest",
                "completed": True,
                "priority": "high",
                "due_date": "2026-09-28"
                }], f)


    filter_tasks(json_file, "completed")
    captured = capsys.readouterr()

    assert "pytest" in captured.out
    assert "testing" not in captured.out


def test_filter_priority(tmp_path, capsys):
    json_file = tmp_path / "test.json"
    with open(json_file, "w") as f:
            json.dump([{    
                "id": 3,
                "title": "testing",
                "completed": False,
                "priority": "medium",
                "due_date": "2026-09-29"
                },{
                "id": 9,
                "title": "pytest",
                "completed": True,
                "priority": "high",
                "due_date": "2026-09-28"
                }], f)

    filter_tasks(json_file, priority="high")
    captured = capsys.readouterr()

    assert "pytest" in captured.out 
    assert "testing" not in captured.out


def test_sort_task_priority(tmp_path, capsys):
    json_file = tmp_path / "test.json"
    with open(json_file, "w") as f:
            json.dump([{    
                "id": 3,
                "title": "testing",
                "completed": False,
                "priority": "low",
                "due_date": "2026-09-29"
                },{
                "id": 9,
                "title": "pytest",
                "completed": True,
                "priority": "medium",
                "due_date": "2027-01-28"
                },
                {
                "id": 12,
                "title": "numpy",
                "completed": False,
                "priority": "high",
                "due_date": "2027-02-28"
                }], f)

    sort_task(json_file, by="priority")
    captured = capsys.readouterr()

    assert "numpy" in captured.out.splitlines()[0] 
    assert "pytest" in captured.out.splitlines()[1]
    assert "testing" in captured.out.splitlines()[2]


def test_sort_task_due_date(tmp_path, capsys):
    json_file = tmp_path / "test.json"
    with open(json_file, "w") as f:
            json.dump([{    
                "id": 3,
                "title": "testing",
                "completed": False,
                "priority": "low",
                "due_date": "2026-09-29"
                },{
                "id": 9,
                "title": "pytest",
                "completed": True,
                "priority": "medium",
                "due_date": "2027-01-28"
                },
                {
                "id": 12,
                "title": "numpy",
                "completed": False,
                "priority": "high",
                "due_date": "2027-02-28"
                }], f)

    sort_task(json_file, by="due_date")
    captured = capsys.readouterr()

    assert "testing" in captured.out.splitlines()[0]
    assert "pytest" in captured.out.splitlines()[1]
    assert "numpy" in captured.out.splitlines()[2]


def test_filter_tasks_no_matching_tasks(tmp_path, capsys):
    json_file = tmp_path / "test.json"
    with open(json_file, "w") as f:
        json.dump([{
            "id": 9,
            "title": "pytest",
            "completed": True,
            "priority": "medium",
            "due_date": "2027-01-28"
            },
            {
            "id": 12,
            "title": "numpy",
            "completed": False,
            "priority": "high",
            "due_date": "2027-02-28"
            }], f)

    filter_tasks(json_file, priority="low")
    captured = capsys.readouterr()

    assert captured.out == "No matching tasks found.\n"



