# SchedulerSim

**A dashboard for simulating how various scheduling policies work.**



### Design Comments

* For now, the OS is treated as the single source of truth regarding process states for simplicity.

    When I am finished with the initial simulation structure, I will refactor for performance by having each scheduler store a suitable data structure for its operations (e.g. min-heap for PSJF) 