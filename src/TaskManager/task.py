"""
A class to create a task with unique identifier and priority level.
"""

from .priority import Priority
from uuid import UUID


class Task:
    """
     A class to create a task with unique identifier and priority level

     ...

     Attributes
     ----------
     pid : UUID.hex
         Represents pid (id) of task
     priority: : Priority
         Represents priority of ask
     is_active : bool
         Shows status of task

     Methods
     -------
     kill():
         Makes a given task inactive.

    set_priority()
        Used to update task property


    property attributes
   --------------------
   get_pid
   get_priority
     """

    def __init__(self, pid: UUID.hex, priority: Priority, is_active: bool = True):
        """
        Constructs all the necessary attributes for the task object.

        Parameters
        ----------
            pid : UUID.hex
                Represents pid (id) of task
            priority:  Priority
                Represents priority of ask
            is_active : int
                Shows status of task
                """

        self.__pid = pid
        self.__priority = priority
        self.is_active = is_active

    def kill(self) -> None:
        """
        Kills the job.
        This method changes the status of the job to False.

        Returns
        -------
        None
        """
        self.is_active = False

    @property
    def get_pid(self):
        """Helper to return pid of task"""
        return self.__pid

    @property
    def get_priority(self) -> Priority:
        """Helper to return priority of task"""
        return self.__priority

    # def set_pid(self, value) -> None:
    #     """Helper to set pid of task"""
    #     self.__pid = value

    def set_priority(self, value) -> None:
        """Helper to set priority of task."""
        if isinstance(value, Priority):
            self.__priority = value
        else:
            print(f"{value} is not of type 'Priority'. Please provide a valid value!")

    def __eq__(self, other) -> bool:
        return True if self.__pid == other.__pid else False

    def __repr__(self) -> str:
        return f"Task(pid='{self.__pid}', priority= <{self.__priority.name}:{self.__priority.value}>, is_active={self.is_active}) "

    def __str__(self) -> str:
        return f"pid='{self.__pid}', priority= <{self.__priority.name}:{self.__priority.value}>, is_active={self.is_active}"
