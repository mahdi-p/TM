from pyprojroot import here as phere
from pyhere import here
from src.TaskManager import *
import uuid
from datetime import datetime
import argparse

if __name__ == "__main__":

    # initialize parser for command line arguments
    parser = argparse.ArgumentParser(description="Task manager")
    # optional
    # 'env' will help to pick up proper values from config file, depending on running job mode
    parser.add_argument("--env", help="Determine if job runs in dev/uat/prod", type=str, default=None)
    parser.add_argument("--task_numbers", help="Max size of task manager", type=int, default=None)
    parser.add_argument("--run_mode", help="Running method (default, fifo, ...)", type=str, default= None)
    parser.add_argument("--verbose", help="Module level logging. OK?", type=bool, default=None)
    parser.add_argument("--allow_duplicates", help="Determine if duplicate jobs permitted", type=bool, default= None)

    args = parser.parse_args()
    if args.env is None:
        env= "dev"
    else:
        env= args.env

    # Get applications root directory
    project_root = phere()
    mlogger(f"Root directory of project: {project_root}")

    # Create log file
    log_path = f"{project_root}/data/logs/run_log_{datetime.now().strftime('%Y_%m_%d')}.log"
    logger = py_logger(log_path=log_path)

    logger.info(f"Working environment: '{env}'")
    logger.info(f"Logging at '{log_path}'")

    # Read the config file for some decisioning
    logger.info("Get the config file")
    config_params = get_config(str(here("data", "config", "config_file.yaml")))

    logger.info("The content of config file is:")
    logger.info(config_params)

    task1 = Task(pid=uuid.uuid4().hex, priority=Priority.medium)
    task2 = Task(pid=uuid.uuid4().hex, priority=Priority.high)
    task3 = Task(pid=uuid.uuid4().hex, priority=Priority.low)
    task4 = Task(pid=uuid.uuid4().hex, priority=Priority.medium)
    task5 = Task(pid=uuid.uuid4().hex, priority=Priority.medium)
    task6 = Task(pid=uuid.uuid4().hex, priority=Priority.high)
    task7 = Task(pid=uuid.uuid4().hex, priority=Priority.low)

    # Utilize/control values from config file
    max_queue_size = config_params['run_mode'][env]['task_number']
    run_mode = config_params['run_mode'][env]['method']
    verbose = config_params['run_mode'][env]['verbose']
    allow_duplicates = config_params['run_mode'][env]['allow_duplicates']

    if args.task_numbers is None:
        args.task_numbers = max_queue_size
    if args.run_mode is None:
        args.run_mode = run_mode
    if args.verbose is None:
        args.verbose = verbose
    if args.allow_duplicates is None:
        args.allow_duplicates = allow_duplicates


    task_manager = TaskManager(max_queue_size=args.task_numbers, run_mode=args.run_mode, verbose=args.verbose,
                               duplicates_allowed = args.allow_duplicates)
    task_manager.add(task=task1)
    task_manager.add(task=task2)

    try:
        task_manager.add(task=task2)
    except DuplicateTaskError:
        print("Trying to add duplicate dupplicate task. Addition of tasks with identical ids are not allowed.")
    except InactiveTaskError:
        print("The task status is inactive. Please update its status or create a new task.")
    except:
        print("Something else went wrong")
    else:
        print("Addition of task went through.")

    # Add two new tasks
    task_manager.add(task3)

    print(task_manager.get_empty_slots)

    task_manager.add(task6)

    # Print running task by task id
    print(task_manager.list_running_tasks())
    print(task_manager.list_running_tasks(reverse=True))

    logger.info("Log running jobs:")
    logger.info(task_manager.list_running_tasks())

    logger.info("Log running jobs ordered by priority:")
    logger.info(task_manager.list_running_tasks(by="priority"))
    logger.info(f"Max size of task manager container is: {task_manager.get_max_queue_size}")

    task_manager.print_run_mode()
    task_manager.print_max_queue_size()

    logger.info("Shutting down the task manager:")
    task_manager.kill_all_tasks()



