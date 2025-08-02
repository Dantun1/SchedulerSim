from engine import SimEngine
from opsys import Process

processes = [Process(f"p{i}",start_time=0, duration=5 * (10-i), prob_io_request=0.3) for i in range(10)]

my_sim = SimEngine(processes)

my_sim.run(100)