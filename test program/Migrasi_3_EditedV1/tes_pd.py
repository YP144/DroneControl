from Drone import PID
import time
kp, td = 0.144, 1.429
pd = PID(Kp=kp, Td=td, control_type='pd')

for i in range(1, 10, 1):
    waktu = time.perf_counter()
    result = pd.run(i, waktu)
    print(f'{result}, {i}, {pd.dt}')
