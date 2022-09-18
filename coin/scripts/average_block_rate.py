from blockchain.blockchain import Blockchain
from config import SECONDS

import time

blockchain = Blockchain ()
times = []

for i in range (1000):
    start_time = time.time_ns ()
    blockchain.add_block (i)
    end_time = time.time_ns ()

    time_to_mine = (end_time - start_time) / SECONDS
    times.append (time_to_mine)

    average_time = sum (times) / len (times)
    print (f"New block difficulty: {blockchain.chain [-1].difficulty}")
    print (f"Time to mine: {time_to_mine}s")
    print (f"Average time: {average_time}s\n")
