import pytest
import uuid

from src.TaskManager import TaskManager, Task, Priority, MaxTaskSizeError, DuplicateTaskError, EmptyTaskManagerError, InactiveTaskError


@pytest.fixture
def default_task_manager():
    """
    Returns a blank TaskManager with the default values.
    Notice that this function returns a class object and this is what fixture is doing.
    """
    return TaskManager()


def test_max_task_size_error_exception():
    """Test exceptions for max container size."""
    task_manager = TaskManager(max_queue_size=2, verbose=False)
    task1 = Task(pid=uuid.uuid4().hex, priority=Priority.medium)
    task2 = Task(pid=uuid.uuid4().hex, priority=Priority.high)
    task3 = Task(pid=uuid.uuid4().hex, priority=Priority.low)

    # Checking for MaxTaskSizeError: If no error is raised, raise an exception.
    # If an error is raised of type MaxTaskSizeError, then silence it, which means test is passed.
    with pytest.raises(MaxTaskSizeError) as exception_info:
        task_manager.add(task=task1)
        task_manager.add(task=task2)
        task_manager.add(task=task3)

   # Further test if error messages are identical
    assert exception_info.match("Task manager does not have free job slot.")


def test_adding_inactive_task():
    """Test insertion of in-active tasks."""
    # Instantiate TM
    task_manager = TaskManager(max_queue_size=5, verbose=False)

    # Create some tasks
    task1 = Task(pid=uuid.uuid4().hex, priority=Priority.medium)
    task2 = Task(pid=uuid.uuid4().hex, priority=Priority.high)
    task3 = Task(pid=uuid.uuid4().hex, priority=Priority.low)

    # If a task is killed or deactivated, it will not be added to TM
    task3.kill()
    with pytest.raises(InactiveTaskError):
        task_manager.add(task=task1)
        task_manager.add(task=task2)
        task_manager.add(task=task3)


def test_default_initial_max_queue_size(default_task_manager):
    """Test for default values in class.__init__"""
    assert default_task_manager.get_max_queue_size == 5


def test_duplicate_tasks():
    """Test excepion for insertion of duplicate task."""
    task_manager = TaskManager(max_queue_size=5, verbose=False)
    task1 = Task(pid=uuid.uuid4().hex, priority=Priority.medium)
    task2 = Task(pid=uuid.uuid4().hex, priority=Priority.high)

    task_manager.add(task=task1)
    task_manager.add(task=task2)

    with pytest.raises(DuplicateTaskError) as exception_info:
        task_manager.add(task=task1)

    # Further test if error messages are identical
    assert exception_info.match("A job with given pid is already in queue.")


def test_empty_task_manager_creation_exception():
    """Test exception for creatino of empty tasks."""
    with pytest.raises(EmptyTaskManagerError):
        TaskManager(0)

def test_priority_based_additions():
    """Test of adding jobs based on priority."""
    task_manager = TaskManager(max_queue_size=3, run_mode="priority" , verbose=False)
    task1 = Task(pid=uuid.uuid4().hex, priority=Priority.high)
    task2 = Task(pid=uuid.uuid4().hex, priority=Priority.high)
    task3 = Task(pid=uuid.uuid4().hex, priority=Priority.high)
    task4 = Task(pid=uuid.uuid4().hex, priority=Priority.low)

    task_manager.add(task=task1)
    task_manager.add(task=task2)
    task_manager.add(task=task3)

    t1 = tuple(sorted([elem.get_pid for elem in task_manager.tasks_queue]))

    task_manager.add(task4)

    t2 = tuple(sorted([elem.get_pid for elem in task_manager.tasks_queue]))
    assert t1 == t2


def test_adding_high_priority_task():
    """
    Test of adding jobs based on priority.
    In paricular, we remove the lowest priority that is the oldes.
    """
    task_manager = TaskManager(8, run_mode="priority")

    task1 = Task(uuid.uuid4().hex, Priority.medium)
    task2 = Task(uuid.uuid4().hex, Priority.medium)
    task3 = Task(uuid.uuid4().hex, Priority.low)
    task4 = Task(uuid.uuid4().hex, Priority.medium)
    task5 = Task(uuid.uuid4().hex, Priority.low)
    task6 = Task(uuid.uuid4().hex, Priority.high)
    task7 = Task(uuid.uuid4().hex, Priority.low)
    task8 = Task(uuid.uuid4().hex, Priority.low)
    task9 = Task(uuid.uuid4().hex, Priority.high)

    task_manager.add(task1)
    task_manager.add(task2)
    task_manager.add(task3)
    task_manager.add(task4)
    task_manager.add(task5)
    task_manager.add(task6)
    task_manager.add(task7)
    task_manager.add(task8)

    pid3 = task3.get_pid
    pid9 = task9.get_pid
    task_manager.add(task9)

    assert pid3 not in [elem.get_pid for elem in task_manager.tasks_queue]
    assert [elem.get_pid for elem in task_manager.tasks_queue][7] == pid9



def test_killing_single_task_by_pid(default_task_manager):
    """Test for killing jobs based on their pid."""
    task1 = Task(pid=uuid.uuid4().hex, priority=Priority.low)
    task2 = Task(pid=uuid.uuid4().hex, priority=Priority.high)

    default_task_manager.add(task1)
    default_task_manager.add(task2)

    task_id = task1.get_pid
    size_i = default_task_manager.filled_size
    default_task_manager.kill_task(task_id)
    size_f = default_task_manager.filled_size
    assert size_i == size_f + 1
    assert not task_id in [elem.get_pid for elem in default_task_manager.tasks_queue]


def test_kill_all_tasks(default_task_manager):
    """Test for clearing all the tasks."""
    for item in range(0, default_task_manager.get_max_queue_size):
        task = Task(pid=uuid.uuid4().hex, priority=Priority.low)
        default_task_manager.add(task)

    filled_size = default_task_manager.filled_size
    # Remove all tasks:
    default_task_manager.kill_all_tasks()
    emptied_size = default_task_manager.filled_size

    assert filled_size == 5
    assert emptied_size == 0

def test_task_class_attributes_exception():
    """This function tests AttributeError fot Task class."""
    with pytest.raises(AttributeError):
        task1 = Task(uuid.uuid4().hex, Priority.HIGH)

def test_fifo_mode_with_first_task_addition():
    """This function tests a very corner case that user may popleft one task in task manager and then add the same task by mistake!.
    Such an implementation is error and should not work and raise an exception.
    """
    with pytest.raises(DuplicateTaskError):
        taskManager = TaskManager(4, run_mode="fifo")
        task1 = Task(uuid.uuid4().hex, Priority.medium)
        task2 = Task(uuid.uuid4().hex, Priority.medium)
        task3 = Task(uuid.uuid4().hex, Priority.low)
        task4 = Task(uuid.uuid4().hex, Priority.medium)

        taskManager.add(task1)
        taskManager.add(task2)
        taskManager.add(task3)
        taskManager.add(task4)

        # Adding first task again!
        taskManager.add(task1)