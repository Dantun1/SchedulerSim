from definitions import ProcessState, ProcessAction
from random import random, randint

class Process:
    def __init__(self,pid, start_time: int = 0, duration: int = 20, prob_io_request: float = 0):
        self.pid = pid
        self.start_time = start_time
        self.duration = duration
        self.time_executed= 0
        self._prob_io_request = prob_io_request

    def execute_tick(self):

        if self._should_request_io():
            return ProcessAction.ISSUE_IO

        return ProcessAction.RUN


    def _should_request_io(self) -> bool:
        return random() < self._prob_io_request

    def __str__(self):
        return f"Process {self.pid}, start_time {self.start_time},duration {self.duration}, time executed {self.time_executed}"


class Scheduler:
    is_preemptive = False
    def schedule(self, ready_processes: list[Process]):
        ...

class PSJFScheduler(Scheduler):
    """
    Preemptive shortest job first scheduler.
    # TODO: implement as heap
    """
    is_preemptive = True
    def schedule(self, ready_processes: list[Process], running_process: Process):
        available_processes = ready_processes + [running_process] if running_process else ready_processes
        return min(available_processes, key=lambda p: p.duration-p.time_executed)

class FIFOScheduler(Scheduler):
    def schedule(self, ready_processes: list[Process]):
        return ready_processes[0]


class OperatingSystem:
    def __init__(self, scheduler: Scheduler = PSJFScheduler()):
        self.scheduling_policy: Scheduler = scheduler
        self.processes: dict[ProcessState, list[Process]] = {
            ProcessState.RUNNING: [],
            ProcessState.READY: [],
            ProcessState.BLOCKED: [],
            ProcessState.NEW: [],
            ProcessState.TERMINATED: []
        }
    @property
    def running_process(self):
        try :
            process = self.processes[ProcessState.RUNNING][0]
        except IndexError:
            process = None
        return process

    def add_new_processes(self, processes: list[Process]):
        for process in processes:
            self.processes[ProcessState.NEW].append(process)

    def check_for_new_processes(self):
        for process in self.processes[ProcessState.NEW][:]:
            self.processes[ProcessState.NEW].remove(process)
            self.processes[ProcessState.READY].append(process)

    def check_for_io_completion(self):
        # 1/5 chance of io being completed each tick
        for process in self.processes[ProcessState.BLOCKED][:]:
            if random() < 0.2:
                self.processes[ProcessState.BLOCKED].remove(process)
                self.processes[ProcessState.READY].append(process)

    def schedule_next(self):
        # Do nothing if no processes to schedule
        if not self.processes[ProcessState.READY] and not self.processes[ProcessState.RUNNING]:
            return

        # Handle non-preemptive schedulers
        if not self.scheduling_policy.is_preemptive:
            if self.running_process:
                return
            else:
                process_to_run = self.scheduling_policy.schedule(self.processes[ProcessState.READY])
        # Handle preemptive schedulers
        elif self.scheduling_policy.is_preemptive:
            process_to_run = self.scheduling_policy.schedule(self.processes[ProcessState.READY], self.running_process)



        if self.running_process is None:
            self.processes[ProcessState.RUNNING].append(process_to_run)
            self.processes[ProcessState.READY].remove(process_to_run)


        if process_to_run != self.running_process:
            self._context_switch(process_to_run)


    def handle_action(self, action: ProcessAction):
        if action == ProcessAction.ISSUE_IO:
            process_to_be_blocked = self.processes[ProcessState.RUNNING].pop()
            self.processes[ProcessState.BLOCKED].append(process_to_be_blocked)

    def terminate_process(self, process: Process):
        self.processes[ProcessState.RUNNING].pop()
        self.processes[ProcessState.TERMINATED].append(process)


    def _context_switch(self, process: Process):
        previously_running_process = self.processes[ProcessState.RUNNING].pop()
        self.processes[ProcessState.READY].append(previously_running_process)
        self.processes[ProcessState.RUNNING].append(process)
        self.processes[ProcessState.READY].remove(process)


