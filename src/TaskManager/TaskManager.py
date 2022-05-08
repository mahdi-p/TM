"""
The class is used for Task Manager creation.
"""

from collections import deque
from .task import Task
from .priority import Priority
from .libs import mlogger, MaxTaskSizeError, DuplicateTaskError, EmptyTaskManagerError, InactiveTaskError


class TaskManager:
    """
    A class to create a task manager with fixed size at run time.
         ...

    Attributes
    ----------
        max_queue_size : int
            Determines size of task manager at run time.
        run_mode : str
            Determines what to do when container is filled and we add a new task at run time.
            Acceptable values:
            "default" that raise an error when we add a new task to filled container.
            "fifo" that removes oldest task and adds a new task.
            "priority" that is priority based. When the max size is reached, should result into an evaluation:
                - if the new process passed in the add() call has a higher priority compared to any of the existing
                  one, we remove the lowest priority that is the oldest, otherwise we skip it.
        verbose : bool
            If to print/log from module. Default True.

    Methods
    -------
         add()
             To add a new task to task manager.
         kill_all_tasks()
            To kill all the tasks and clear task manager.
        kill_task()
            Kills task by task id (pid)
        kill_by_group()
            Kills task based on a group variable.
            At the moment group variables  are tasks' priority and pid.
            In case of priority: Every task with given priority will be killed and removed.
            In case of pid: We only look at matching sting in the beginning of tasks pid, using str.startswith()
            Could be further extended to contain RegEx on pid, if necessary.

        list_running_tasks()
            Lists running tasks based on: Creation time, pid or priority ("ctime", "pid", "priority")

    Raises
    ------
        MaxTaskSizeError
        DuplicateTaskError
        EmptyTaskManagerError
        InactiveTaskError

         """

    def __init__(self, max_queue_size: int = 5, run_mode: str = "default", verbose: bool = True,  duplicates_allowed: bool = False):

        """
               Constructs all the necessary attributes for the TaskManager object.

               Parameters
               ----------
                   max_queue_size : int
                       Determines size of task manager at run time.
                   run_mode : str
                       Determines what to do when adding new task to filled container. Default is to raise an error.
                   verbose : bool
                       If to print/log from module. Default True.
                   duplicates_allowed : bool
                        Determines if duplicate task can go into task manager

                       """

        if max_queue_size == 0:
            raise EmptyTaskManagerError("Empty task manager container is not permitted.")
        if run_mode not in ("default", "fifo", "priority"):
            raise Exception("'method' can only be in ('default', 'fifo', 'priority')")
        if not type(max_queue_size) is int:
            raise TypeError("Only integers are allowed")

        self.__max_queue_size = max_queue_size
        self.tasks_queue = deque([], self.__max_queue_size)
        self.__run_mode = run_mode
        self.verbose = verbose
        self.duplicates_allowed = duplicates_allowed

    def _check_if_task_not_exists(self, task: Task):

        if self.duplicates_allowed:
            return self.duplicates_allowed
        if task.get_pid in [elem.get_pid for elem in self.tasks_queue]:
            raise DuplicateTaskError("A job with given pid is already in queue.")
            # if self.verbose:
            #    mlogger("This task is already added.")
            # return False
        return True

    def print_max_queue_size(self) -> None:
        """Prints size of container
        """
        print(f"Container has size of {self.__max_queue_size}")

    def set_max_queue_size(self, max_queue_size):
        """sets new value to max_queue_size."""
        self.__max_queue_size = max_queue_size

    @property
    def get_max_queue_size(self) -> int:
        "Returns size of container."
        return self.__max_queue_size

    def print_method(self) -> None:
        """Prints run method"""
        print(f"Run method is {self.__run_mode}")

    def set_run_method(self, new_run_mode):
        """sets new value to run_mode."""
        self.__run_mode = new_run_mode

    @property
    def get_run_method(self) -> str:
        return self.__run_mode

    @property
    def filled_size(self) -> int:
        return len(self.tasks_queue)

    @property
    def get_empty_slots(self):
        return self.__max_queue_size - len(self.tasks_queue)

    def add(self, task: Task) -> None:
        """
        Adds a task to the tasks queue. If the queue is full, an error message will be printed
        :param task: an instance of task class
        """
        if not task.is_active:
            raise InactiveTaskError("Inactive jobs can not be added to task manager.")

        if self.filled_size >= self.__max_queue_size:
            if self.__run_mode == "default":
                error_message = "Task manager does not have free job slot."
                raise MaxTaskSizeError(error_message)
                # mlogger(error_message)
                # return
            elif self.__run_mode == 'fifo':
                self._add_fifo(task)
            elif self.__run_mode == 'priority':
                self._add_priority_based(task)
        else:
            self._add(task)

    def _add_fifo(self, task: Task):
        """
       Adds a task to the tasks queue. If the queue is full, the oldest task will be removed

       Parameters
       -----------
            task : Task
                An instance of Task class
       """
        if self._check_if_task_not_exists(task):
            _ = self.tasks_queue.popleft()
            self.tasks_queue.append(task)

    def _add(self, task: Task):
        """
       Adds a task to the tasks queue. Adds a task to the tasks queue. If the task is not in queue.

       Parameters
       -----------
            task : Task
                An instance of Task class
       """
        if self._check_if_task_not_exists(task):
            self.tasks_queue.append(task)

    def _add_priority_based(self, new_task: Task):
        """
        Adds a task to the tasks queue. If the queue is full, for new insertion, the oldest task
        with lower priority will be removed.
        if none of the existing tasks have lower priority than the new one, then we skip it.

        Parameters
        ----------
            new_task: Task
                New task to be added to container.
        """

        # Set index_to_remove to -1 and update it in the following loop. If it gets updated and its value changes,
        # Then we have found a task with lower priority which was oldest.
        index_to_remove = -1
        current_index = 0
        previous_low_priority = -1

        # If new task has smallest priority. Return.
        if new_task.get_priority.value == min(Priority).value:
            mlogger("Task has smallest possible priority and can not be replaced with existing tasks in task manager.")
            return

        try:
            self._check_if_task_not_exists(new_task)
        except DuplicateTaskError:
            mlogger("Task is already in task manager.")
            return

        for task in self.tasks_queue:
            if new_task.get_priority > task.get_priority:
                if index_to_remove == -1:
                    # register occurence of first low priority
                    index_to_remove = current_index
                    previous_low_priority = task.get_priority

                    # Place holder for future development in case of more than 3 prio level
                elif index_to_remove != -1 and task.get_priority < previous_low_priority:
                    index_to_remove = current_index
                    current_low_priority = task.get_priority

                if task.get_priority.value == min(Priority).value:
                    # first occurence of lowest priority. Update the index and exit the search
                    index_to_remove = current_index
                    break

            current_index = current_index + 1

        if index_to_remove == -1:
            # We skip it and do not raise Exception.
            if self.verbose:
                message = f"Queue is full and there is no task with lower " \
                          f"priority than new task's priority, '{new_task.get_priority.name}', to be removed."
                mlogger(message)
            return

        del self.tasks_queue[index_to_remove]
        self.tasks_queue.append(new_task)


    def kill_all_tasks(self) -> None:
        """Kills all the tasks in task manager."""
        if self.verbose:
            mlogger("Killing all of the tasks queue.")

        for task in self.tasks_queue:
            task.kill()
        self._clear_tasks_queue(verbose=False)

    def kill_task(self, pid: str) -> None:
        """Kills task by task's pid identifier."""
        self.tasks_queue = [elem for elem in self.tasks_queue if elem.get_pid != pid]

    def kill_by_group(self, group: str = None, match: str = None) -> None:
        """
        Kills tasks by task's group identifier. Group identifier are: task priority and pid.

        Parameters
        ----------
            group : str acceptable values: "pid" or "priority"
                If "priority": Value of 'match' will be used to kill processes.
                If "pid": Using str method startswith(), it will look for 'match' value in the begining of pid.
                "To be extended to contain RegEx on pid"
            match : str
                Used to match pid or priority to kill tasks.

        """

        if group not in ('priority', 'pid'):
            raise ValueError("'group can only be in ('priority' , 'pid')'")

        if group == 'priority':
            self.tasks_queue = [elem for elem in self.tasks_queue if elem.get_priority.name != match]
        else:
            self.tasks_queue = [elem for elem in self.tasks_queue if not elem.get_pid.startswith(match)]

    def _clear_tasks_queue(self, verbose=None):
        """Clears tasks queue"""
        if verbose is None:
            verbose = self.verbose
        if verbose:
            mlogger("Clearing the tasks queue.")
        self.tasks_queue.clear()

    def list_running_tasks(self, by: str = "ctime", reverse: bool = False):
        """
        Prints ordered list of running tasks.

        parameters:
        ----------
        by : str
            Defaulted to ctime that stands for creation time.
            Accepted values are: ("ctime", "pid", "priority")
        reverse : bool
            Default False that means do nor reverse the sort direction.
        """
        if by not in ("ctime", "pid", "priority"):
            mlogger("'by' parameter is not well defined. Acceptable values are: ('ctime', 'pid', 'priority')")
            return
        if self.verbose:
            if self.verbose:
                mlogger(f"Printing list of running tasks by '{by}'.")
        if self.filled_size == 0:
            mlogger("Tasks queue is empty")
            return
        if by == "ctime":
            return list(self.tasks_queue) if not reverse else list(self.tasks_queue)[::-1]
        else:
            return sorted(self.tasks_queue, key=lambda t: t.get_priority, reverse=reverse) if by == "priority" \
                else sorted(self.tasks_queue, key=lambda t: t.get_pid, reverse=reverse)