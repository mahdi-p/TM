# Introduction

Task Manager, TM, is designed for handling multiple processes inside an operating system. 
Each process is identified by 2 fields, a unique immutablele identifier (PID), and a priority 
which could have one of predefined values in (low, medium, high).

The process is immutable, it is generated with a priority and will die with this priority – each process has a **kill()** method that will destroy it.

The idea is that the Task Manager exposes the following functionality:

- Add a process
- List running processes
- Kill/KillGroup/KillAll 

In the following we will first set up our working environment and install necessary 
libraries. And then we will demonstrate how to run the application.

We will also try to explain why certain decisions were made.

One of the main requirements to run the codes is to make sure that our Python version is at least
3.6. That is because we have made use of `f-strings`.

The reason to use them was that f-strings are a great new way to format strings. 
They are more readable, concise, and less prone to error as well as faster than other
ways of formatting!

## Installation

Utilize git in order to clone the project with



### Clone the project

```bash
git clone  https://github.com/mahdi-p/TM.git
```

### Create a virtual environment

After the project is cloned simply navigate to it with


```bash
cd TM
```

The first thing we need to do when developing our own 
Python application
or library, is to create a virtual environment. The virtual environment 
for our project will create an isolated environment for all its 
dependencies.

Python3 comes with **venv** to create a virtual environment. 

We will continue with following command on command line:

```bash
python3 -m venv my_venv
```

The above command, will create a virtual environment called `my_venv` 
which is placed under the current directory.

 

### Activate a virtual environment
Now that we have created a virtual environment, we need to instruct 
our operating system to make use of it by first activating. 
To do so, we need to call the activate script which is located under 
the `bin/` sub-directory in the created tree structure of our virtual 
environment.

 

```bash
source my_venv/bin/activate
```

The following command will show the newly installed location and version 
of Python interpreter, if it is properly activated.

```bash
which python3 && python3 --version
```

Once the virtual environment is activated, everything we install or 
uninstall will only have effect within that specific environment and 
nowhere else. Now let us run the following command to get all necessary
libraries installed.

```bash
pip install -r requirements.txt
```

Before we run our application, let us have a look at some implementations.

# Technical Implementation
Let us have a look at two main components of our application, namely 
```Task``` and ``TaskManager``.

## Task class
As mentioned in **Introduction** the Task class
is identified at least by 2 attributes and one method.

- `pid` which is immutable and unique
- `priority` that can carry only 3 distinct values, namely
- `kill()` method.

Note that the processes are immutable and basically after they are 
created their priority as well as pid can not change. 
But in some real world cases, this scenario can be 
slightly different. Every Unix process has a feature called "Nice", 
on very high level, a process with higher nice number may be 
completed before a process with the lowest nice number. It 
helps in execution of a process with modified scheduling priority. 
If a process has a higher priority, then Kernel will allocate more CPU 
time to that process. In other words, it  affects the way the processor
does the context switch.

In order to implement the class, we first utilize Python's builtin `enum` 
module to create our own new data types (class). An enumeration is a set of members that have associated 
unique constant values, in other words, we can have pairs of ``name-value`` attached to eachother. 

Python provides us with the enum module that contains the Enum type for defining 
new enumerations. We define a new enumeration type by subclassing the Enum class or inherit from `enum`. An 
implementation of such a helper class would look like something:

```python
from enum import auto, Enum

class Priority(Enum):
    low    = auto()  # 1
    medium = auto()  # 2
    high   = auto()  # 3

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
```

An implementation of Python's ```magic methods``` also enable us to easily 
compare priorities of two objects of class later in our codes. We can either 
assign the values explicitly or by help of ``auto`` function in `enum`.

To implement the ``Task`` class, one easy way would be to utilize 
`dataclasses` module in `Python`. The `dataclasses` class makes the 
development easier by automatically implementing some methods in 
background. The module is only available in Python 3.7 and newer versions  
as part of Python's standard library, but it can also be installed 
in 3.6 version via package managers.

In this case, our implementation would look like:

```python
from dataclasses import dataclass
from uuid import UUID

@dataclass
class Task:
    pid: UUID.hex
    priority: Priority
    is_alive: bool = True

    def kill(self):
        self.is_alive = False
```

Here we also make use of ``uuid`` module in Python. In the following I will 
explain why this is a good idea. 

According to documentation of the module, it provides immutable UUID objects (the UUID class) and 
the functions uuid1(), uuid3(), uuid4(), uuid5() for generating UUIDs. The uuid4() method creates a
random Universally Unique Ids, UUID.
 
As seen, this implementation is easy, clean and readable. But, the class created in this way has 
attributes that are mutable. One way to resolve it is to use ``@dataclass(frozen= True)`` decorator. 
However, the problem with this approach is that it makes all of the class attributes and methods immutable, 
and we will not be able to use ``kill`` method easily. There seems to be some hacky ways to get around 
this, but those approaches go beyond the whole philosophy of ``dataclasses'`` implementation.

With this in mind and in order to have more flexible class that can also be further extended in future, I twisted 
to a new implementation, utilizing ```class``` ecosystem in Python. The new implementation is:

```python

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
     is_active : int
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
            is_active : bool
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
    def get_priority(self):
        """Helper to return priority of task"""
        return self.__priority

    # def set_pid(self, value) -> None:
    #     """Helper to set pid of task"""
    #     self.__pid = value

    def set_priority(self, value) -> None:
        """Helper to set priority of task."""
        self.__priority = value

    def __eq__(self, other) -> bool:
        return True if self.__pid == other.__pid else False

    def __repr__(self) -> str:
        return f"Task(pid='{self.__pid}', priority= <{self.__priority.name}:{self.__priority.value}>, is_active={self.is_active}) "

    def __str__(self) -> str:
        return f"pid='{self.__pid}', priority= <{self.__priority.name}:{self.__priority.value}>, is_active={self.is_active}"

```
#### Class Attributes
As seen we make use of some advanced techniques, such as, `encapsulation`
as well as `property decorators`.  These decorators are used instead of builtin `property()` function.

Utilizing decorators will allow us to use these class methods like class attributes. It makes 
the development smoother and the code cleaner and easier to read.

We do know that `pid` and `priority` will not change and a process will die with the same 
pid and priority it was created, that is why we implemented these attributes as ``private`` 
member, but letting an advanced user to be able to manipulate at least the `priority` attribute, 
by means of a ```set_priority``` function.

I believe it is a good practice to do so, and in this way we make sure that other programs 
and processes can not unexpectedly modify values of `pid` and `priority`, unless setter functions 
are explicitly invoked. Let say, if we want to tune the resources with respect to tasks' priority and 
we want specific tasks to get more resources.

At the end of day, the concept of ``private`` and ```public``` members are indeed extremely
fragile in Python.

We have also implemented the magic method ``__eq__``. All tasks must have unique pids (ids), 
otherwise they can not be distinguished and may give rise to undesired results without causing 
any error or warning. This is to great extend supported by implementation of `uuid` class.

However, to even more secure our task manager and jobs going into it, we require jobs to 
have different pid in our `TaskManager` class implementation . This will ensure that user 
does not mistakenly add a given active task multiple times. Of course such a test will increase 
time complexity of the code.

We have also made pid to be of type ``UUID.hex``. This approach has some advantages over usual 
`str` type! With this implementation user has more control on pid number definition at the time 
of creating objects from class. For example, user can enter numeric values, 
and these numeric values will be automatically converted to string without raising exceptions and causing any error. 
Of course, numeric values will be required to criteria. This will in particular useful if later 
we apply some sorting on pids! Also user defined defined strings will be accepted. Also user can concatenate other 
strings to pid to group similar tasks together. Indeed we will utilize this concept in implementation of our 
second class methods.

Improper user defined values for pid, may give raise to an ``AttributeError`` or `SyntaxError` at 
the time of creating class objects.  

#### Class methods
The most important method of the class is `kill()`. When called on an object of the class, will change 
the value of ``is_active`` from initially assigned value of `True` to `False` as an indication that the task
is no longer active and available for our task manager. Note that we did not make ``is_active`` private and we 
let user and other programs change its value in the course of execution. 

### TaskManager class
Our the Task Manager should expose the following functionality:

- Add a process
- List running processes
- Kill/KillGroup/KillAll 

The definition and requirements of our task manager makes it a perfect use case to 
utilize ``collections.deque`` from Python's standard library which is First In, First out, 
**FIFO**, data structure. ``collections.deque`` are ordered structure and we do not need to take 
care of the time a given task was added. 

Let us first demonestrate the code and look at what happens in the code. For simplicity, I have skipped some imports.

our initializer reads:

```python
"""
The class is used for Task Manager creation.
"""

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

```

````python
__init__(self, max_queue_size: int = 5, run_mode: str = "default", verbose: bool = True,  duplicates_allowed: bool = False)
````
#### Class Attributes

Where `max_queue_size` will determine our container size at run time. Once it is defined, it 
can not be modified. It will impose the number of tasks that can be added to task manager.

We have made it private to signal to user that after it is defined, it should not be modified. 
At the same time we enable users to get, set and print its value, by means of helper functions
in the class definition.

In a real word scenario its value can come from a command line or another 
application or some config files built into application. We have given a default value 
for this parameter where it can be tuned. The given default value will be used in our `unit test`.


We have also implemented en extremely simple module level logging, that can be controlled by 
``verbose`` attribute. The default value of `True` tells that we will get some light reporting (logging).
A user can silence it by assigning boolean ``False`` to this. The module level logging can be further extended!

What is ``duplicates_allowed``? The default behaviour of our task manager is to only accepts the jobs that are not
in the task manager container. If it is not desired, then user can allow duplicate tasks with setting this parameter 
to ```True```. But it is hugely discouraged to accept duplicate tasks and in the following all my explanations are 
under the assumption that we do not let in duplicate tasks. Letting duplicate tasks will drop time complexity to 
constant value or almost `O(1)`.

The ``run_mode`` argument is by far the most important attribute of our class. 
It will indeed control and cover all 3 senarions in our 
"**Business Requirements**". It will also be defined at run time 
when a class object is initialized. We make it a ```private``` member of the class, 
to signal that its value should not change once it is initialized. We also protect it 
from unexpected modifications, but we provide helper methods for an advanced user to 
caousiously interact with it.

At the moment it will only accept 3 values:

- "default" which is also provided as the default value. 
  - This will tackle the first business requirement, 
    where when the task manager is filled, addition of 
    new tasks will not take effect, unless user explicitly removes a task from task manager.
    
- "fifo" which will satisfy second requirement.
    - If run_mode = "fifo" and if the task manager is alreay filled, adding new task will remove the oldest one in queue
    
- "priority" which will cover the third question.
   - If run_mode = "priority", when the max size is reached, an evaluation will take place. 
     If the new process passed has a higher priority compared to any of the existing one, 
     we will remove the lowest priority that is the oldest, otherwise we skip it.
     
All of these 3 scenarios will be handeled via `add()` method of the class.

In our initializer (`__init__`) function we also check for some input quality and if expected values are 
not supplied we raise proper exceptions, so that user can already fix them. Some of these exceptions are 
defined as helper functions.

After user provides proper values and initializes object of the class, a task manager container 
will be created utilizing ``collections.deque``.

````python
self.tasks_queue = deque([], self.__max_queue_size)
````

#### Class Methods

The class method ``add()`` is designed to add a new task to our task manager. 
This will tackle all 3 business questions by means of ``run_mode``, as discussed above.

When ``add()`` on a given task is called, first we make sure that the task is still active (valid/alive) in 
global namespace. If not, we raise an `InactiveTaskError` exception. Such an exception can be caught and 
proper action could be taken. If the task is active, then we examine if there is an open slot in our 
task manager. Here we are kind of branching and we can have 2 cases:

##### Case 1: The task manager still has some capacity.
If there is an open slot, then a helper function `_add()` will be invoked. The function will 
make sure that the task is not already in the task manager. If a task with identical pid number is 
not in the task manager, then the task will be safely added to task manager.

If a task with identical pid number is 
already in the task manager a ``DuplicateTaskError`` exception will be raised. It will ensure that 
we do not run duplicate active jobs. One may consider, to gently skip raising exceptions and simply 
echoing a warning. But I think raising exceptions have a few advantages in production environment:

- This will minimize/prevent human error. If a user by mistake has added the same job twice, 
  then extra care will be taken and we will make sure that we do not confuse the task insertion. 
  We may need to 
   implement some code to catch and remedy such a scenarios when we implement the calls 
  to add() method in our applications.
- If error comes from uuid, meaning that it has created the same pid to two different tasks, 
  even though it is almost impossible, then breaking pipeline early on would be better that 
  skipping the task addition by simply printing some 
  warnings. There might be some dependencies to this task downstream and if we skip this task we may break 
  other pipelines. Even though uuid almost guarantees there will be no two pid created!
  
- If we continue and add the duplicate task, and we do not skip it, the task could be CPU expensive and blocks 
other processes without any need to run it twice. Imagine we have a Spark job that is extremly resource intensive.
  
The reason we check for duplication of task in `_add()` and not in `add()` is that if the container 
is already filled, then there is no need to check its existence in task manager when we are in "default" 
run mode.

- **In this case time complexity of function is O(n), since we search for existence of duplicate tasks in task list.**

##### Case 2: The task manager has no capacity.

In this case, we will deal with 3 subcases.

A)

when ```run_mode="default```, then a `MaxTaskSizeError` will be raised. 
**Please note that the first question states: When there is no capacity in task manager, we won’t accept any new process.**

I know that raising Exceptions could be expensive and slow down the speed of program, 
but I believe that it is more resistence to error in production environment.
Not to give a wrong and random data product is very crucial in business. Wrong results, would harm the business.
In this subcase, we almost have no time complexity. 

B)

But if ``run_mode="fifo"``, another helper function will be invoked, namely ``_add_fifo()``. Here we will first 
make sure the task is not already in the task manager, if it is not, then we will kill the oldest task and add 
the new task to task manager. If the new task was already in task manager, before we kill the oldest task,
we will raise ``DuplicateTaskError`` exception.

 **Since, we will look at existence of task in the task manager, the time complexity will be  is `O(n)`**. 

C) 

If ``run_mode="priority"``, another helper function will be invoked, namely ``_add_priority_based``. 

Now first we make sure that the task we are trying to add does not have the lowest possible priority. We 
also make sure that the task is not already in task manager. In both these cases we print some message and return.

We will first define two indicator variable and initilize them to -1:

- index_to_remove = -1
- previous_low_priority = -1

We will also create another indicator variable to record position of oldest and smalllest task: `current_index =0`

Now we will compare the priority of our new task with existing ones. As soon as we find a task with lowr priority, 
then we will update "index_to_remove" with the position of the task in task manager. If the task which is found is 
the lowest of all available priorities, then we have found the task of interest (task with the smallest priority that is oldest) 
and we stop iteration. If it is not 
of the smallest available priorities we keep searching and exhaust the loop, but only update 
the "index_to_remove" if we find smaller than what 
we have found so far.

At the end, if value of "index_to_remove" has not changed and "index_to_remove= -1", then we report there is no task 
with smaller priority. But if value of "index_to_remove" has changed, then we kill the job in the position of 
"index_to_remove" and add the new task.

 In this case he time complexity could be of ``O(n*n)``.

##### Kill group methods
We have implemented 3 methods here:

- kill_task to kill task by pid
- kill_all_tasks to kill all the tasks and clear the task manager.
- kill_by_group to kill task by a group identifier. 
  - Main grop identifier is ```priority```.
  - Pid can only be used as group identifier! It is a minimum functionality we have provided so far.
  
When we kill task by group we will need to provide a ```match``` string, such as "low" or "medium" when group is 
"priority". If we select to use the ```pid``` as group identifier, the ```match``` string will only match the 
beginning of the pid. This is in particular useful when we create our tasks and attach some names to them. 
For instance all our Pyspark's tasks have "pyspark" attached to the begining of the pid. Then we can kill 
any task having to do with Pyspark jobs.

This is bare minimum implementation and can be further extended/discussed/discarded.

The implementation of `kill_all_tasks` might look a bit overkilling, since we use "Task" class method
first and then we clear the container. we can simplify it like

```python
def kill_all_tasks(self) -> None:
        """Kills all the tasks in task manager."""
        if self.verbose:
            mlogger("Killing all of the tasks queue.")
        self.tasks_queue.clear()
    
```

The final method implemented in class is `list_running_tasks`. This will be used to list running task inside the 
task manager. The default behaviour will be listing the tasks with respect to creation time. 

The method enables us to list the tasks ordered by pid or priority in ascending or desending order.
 

 

### A word on Complexity Analysis of Queues

Queue structure is First In, First out, **FIFO**, data structure. Whatever is pushed first in the buffer, 
will be consumed first. In Python we can use list class or collections.deque class to easily implement the 
queue structure, as we did above.

The following table represents the time complexity of Queue objects with respect to different operations. 
The complexity is the number of Access and Search operations being performed, is proportional to the number of 
elements or **n**. We call this **O(n)** or linear complexity.

We notice that insertion and deletion of data is quite fast, of the order of constant  1  or  **O(1)**.

 

|      |         | Access  | Search    | Insertion| Deletion|
|---   | ---     | ---     |----      |---        |---  |
|Queue | Average |  O(n)   |  O(n)    |  O(1)     |O(1) |
|Queue | Worst   |  O(n)   | O(n)     |  O(1)     |O(1) |

 

The worst space complexity of Queue objects is O(n). Usually when we are talking about complexity analysis, 
we consider the worst case. For instance, when we search for an element in queue we traverse from the beginning 
of the queue until we reach the element. The element may be located at the end of container and we will need to
traverse **n** times, where "n" is the number of elements in the container.

**Bounded queues, used in our solution, has similar complexity pattern.**

## Test run of the app and logging

Now we are ready to run an example of our `Task Manager`, where we will 
create a number of processes or jobs and a task manager. Then we will 
add these tasks to the task manager and log their execution to screen, 
and a log file.

We can run our code with some default values for class arguments to initialize our task manager. 
These value can either be injected via commandline or via a ```yaml``` file. 

Every argument that is introduced via commandline, will overwrite the values coming from config file. 
We assume our working environment is "dev" that refers to "development". In other words, if it is not explicitly 
provided via commandline, then "dev" will ve considered.

```bash
python3 main.py
python3 main.py --env prod --task_number 2

```

The ```yaml``` file looks like:

````yaml
run_mode :
  dev :
    task_number : 4
    method: "fifo"
    verbose: True
    allow_duplicates: False
  uat :
    task_number : 50
    erbose: True,
    method: "fifo"
    verbose: False
    allow_duplicates: False
  prod :
    task_number : 3
    method: "fifo"
    verbose: True
    allow_duplicates: False
````


## Unit testing with Pytest
Unit tests are small isolated tests to make sure our code is performing as expected. 
We can easily run these tests whenever we make changes to our code to make sure we haven’t broken anything, 
and we can continue to add tests to make sure the new changes we make to our code don't break old scenarios.

When we have a code or package that will be used in production, unit tests can save lots of time and frustration.
For this end, we have implemented a number of tests including:

- Testing Exceptions
- Addition of killed tasks to task manager
- Addition of duplicate tasks
- Default values
- Priority based additions
- Killing tasks by pid
- Killing all task


These test are implemented on both of our classes and can be further extended to include 
many other corner and general cases.

In order to run the tests in the root directory of the project and in command line execute the following command:

```python
python3 -m pytest tests/ -v
```

As we further develope our application, we have to make sure to update tests as appropriate.

### Trouble Shooting

- Please make sure that your Python installation supports f-strings.
- If pytest did not work after it is installed, you may need to deactivate your virtual environment and reactivate it.
- Make sure that ```.here``` file is in root directory. It is a hidden empty file that van be created in root 
directory of the project with:
  
```bash
touch .here
```

### Deactivate a virtual environment

In order to deactivate a virtual environment, we can do so by running deactivate in the command line.

```bash
deactivate
```

## License

[MIT](https://choosealicense.com/licenses/mit/)