from random import random
from typing import Optional

from definitions import ProcessState, ProcessAction
from opsys import OperatingSystem, Process


class SimEngine:
    def __init__(self, opsys: OperatingSystem = OperatingSystem(), initial_processes: Optional[list[Process]] = None):
        if initial_processes is None:
            initial_processes = []
        self.os = opsys
        self.initial_processes: list[Process] = initial_processes
        self.time: int = 0

    def run(self, duration: int):
        self.os.add_new_processes(self.initial_processes)

        while self.time < duration:
            self.os.check_for_new_processes(self.time)
            self.os.check_for_io_completion()
            self.os.schedule_next()
            process = self.os.running_process

            if process:
                action = process.execute_tick()
                self.os.handle_action(action)
                if action == ProcessAction.ISSUE_IO:
                    print(f"Process {process.pid} issued IO at time {self.time}")
                elif action == ProcessAction.RUN:
                    process.time_executed += 1
                    print(f"Process {process.pid} ran at time {self.time}, {process.duration - process.time_executed} left")
                    if process.time_executed >= process.duration:
                        self.os.terminate_process(process)
                        print(f"Process {process.pid} complete!")



            self.time += 1

        self.time= 0



