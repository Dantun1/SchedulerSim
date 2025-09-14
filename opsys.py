from random import random
from collections.abc import Sequence

from definitions import ProcessState, ProcessAction



class Process:
    """ Process class to store process information during simulation.

    Attributes:
        pid: Process ID
        start_time: Process start time (in ticks)
        duration: Process duration / ticks to complete
        time_executed: Number of ticks during which a process has been executed
    """

    def __init__(self, pid: str, start_time: int = 0, duration: int = 20, prob_io_request: float = 0) -> None:
        """ Initialize Process object.

        Args:
            pid: Process ID
            start_time: Process start time (in ticks)
            duration: Process duration / ticks to complete
            prob_io_request: Probability of the process requesting IO on each tick
        """
        self.pid = pid
        self.start_time = start_time
        self.duration = abs(duration)
        self.time_executed= 0
        self._prob_io_request = prob_io_request

    def execute_tick(self) -> ProcessAction:
        """ Return the action that the process should take on a given tick.
        """
        if self._should_request_io():
            return ProcessAction.ISSUE_IO

        return ProcessAction.RUN

    def _should_request_io(self) -> bool:
        """ Determine whether the process should request IO.
        """
        return random() < self._prob_io_request

    def __str__(self):
        return (f"Process {self.pid},"
                f" start_time {self.start_time},"
                f"duration {self.duration},"
                f" time executed {self.time_executed}")


class Scheduler:
    """ Represents a generic base class for a scheduler.

    Designed to be extended by specific schedulers that implement specific scheduling policies.
    """

    def schedule(self, ready_processes: Sequence[Process], running_process: Process | None) -> Process | None:
        """ Get the next process to run from the ready/running processes.

        Args:
            ready_processes: Currently ready processes.
            running_process: Currently running process if any.

        Returns:
            The process to run next or None if no runnable processes are available.
        """
        raise NotImplementedError("scheduler must implement schedule method")


class PSJFScheduler(Scheduler):
    """Preemptive shortest job first scheduler."""

    def schedule(self, ready_processes: Sequence[Process], running_process: Process | None) -> Process | None:
        available_processes = list(ready_processes)

        if running_process is not None:
            available_processes.append(running_process)

        if not available_processes:
            return None

        return min(available_processes, key=lambda p: p.duration - p.time_executed)


class FIFOScheduler(Scheduler):
    """Non-preemptive FIFO scheduler."""

    def schedule(self, ready_processes: Sequence[Process], running_process: Process | None) -> Process | None:
        if running_process:
            return running_process

        if not ready_processes:
            return None

        return min(ready_processes, key=lambda p: p.start_time)


class OperatingSystem:
    """Operating System class to store and manage processes during simulation.

    Attributes:
        scheduling_policy: Scheduler used to schedule a process on each tick.
        processes: Dictionary of processes and their states.
    """

    def __init__(self, scheduler: Scheduler = PSJFScheduler()) -> None:
        """ Initialize OperatingSystem object.

        Args:
            scheduler: Scheduler object used to schedule a process on each tick.
        """
        self.scheduling_policy: Scheduler = scheduler
        self.processes: dict[ProcessState, list[Process]] = {
            ProcessState.RUNNING: [],
            ProcessState.READY: [],
            ProcessState.BLOCKED: [],
            ProcessState.NEW: [],
            ProcessState.TERMINATED: []
        }

    @property
    def running_process(self) -> Process | None:
        try:
            process = self.processes[ProcessState.RUNNING][0]
        except IndexError:
            process = None
        return process

    def add_new_processes(self, processes: Sequence[Process]) -> None:
        """ Add new processes to the new queue. """
        for process in processes:
            self.processes[ProcessState.NEW].append(process)

    def check_for_new_processes(self, current_time) -> None:
        """ Add new processes to the ready queue if they are scheduled to begin at the current tick."""
        for process in self.processes[ProcessState.NEW][:]:
            if process.start_time == current_time:
                self.processes[ProcessState.NEW].remove(process)
                self.processes[ProcessState.READY].append(process)

    def check_for_io_completion(self):
        """ Check if any processes completed IO. Swap from Blocked to Ready accordingly."""
        for process in self.processes[ProcessState.BLOCKED][:]:
            if random() < 0.2:
                self.processes[ProcessState.BLOCKED].remove(process)
                self.processes[ProcessState.READY].append(process)

    def schedule_next(self) -> None:
        """ Schedule the next process to run based on the scheduler's scheduling strategy. """

        # No processes to schedule so do nothing
        if not self.processes[ProcessState.READY] and not self.processes[ProcessState.RUNNING]:
            return

        # Schedule next process using scheduling policy
        next_process = self.scheduling_policy.schedule(self.processes[ProcessState.READY], self.running_process)

        # No context switch if the scheduler wants to continue current
        if next_process is self.running_process:
            return

        self._context_switch(next_process)


    def handle_action(self, action: ProcessAction) -> None:
        """Handle the actions/sys calls taken by the process on a tick."""
        if action == ProcessAction.ISSUE_IO:
            process_to_be_blocked = self.processes[ProcessState.RUNNING].pop()
            self.processes[ProcessState.BLOCKED].append(process_to_be_blocked)

    def terminate_process(self, process: Process) -> None:
        """Terminate the running process."""
        self.processes[ProcessState.RUNNING].pop()
        self.processes[ProcessState.TERMINATED].append(process)


    def _context_switch(self, next_process: Process) -> None:
        """Switch the previously running process with the next scheduled process in the ready queue."""
        running_list = self.processes[ProcessState.RUNNING]
        prev_running = running_list.pop() if running_list else None

        if prev_running is not None and prev_running is not next_process:
            self.processes[ProcessState.READY].append(prev_running)

        self.processes[ProcessState.READY].remove(next_process)
        running_list.append(next_process)




