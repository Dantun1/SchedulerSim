from engine import SimEngine
from opsys import Process, OperatingSystem, FIFOScheduler, PSJFScheduler

processes = [Process(f"p{i}",start_time= i, duration=5 * (10-i), prob_io_request=0.3) for i in range(10)]

my_os = OperatingSystem()
my_sim = SimEngine(my_os,processes)

my_sim.run(1000)