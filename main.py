from engine import SimEngine
from opsys import Process

processes = [Process(f"p{i}", 10 * i, 5 * (10-i)) for i in range(10)]

my_sim = SimEngine(processes)

my_sim.run(100)