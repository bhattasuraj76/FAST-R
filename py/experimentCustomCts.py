import sys
import logging
from timeit import default_timer as timer
from datetime import timedelta
from experimentBudgetCore import main

usage = """USAGE: python3 py/experimentCustom.py <prog> 
  """

logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.DEBUG,
)


if __name__ == "__main__":
    script, setting, algorithm = sys.argv

    prog = "cts"
    algos = ["FAST++", "FAST-all", "FAST-CS", "FAST-pw"]
    if algorithm in algos:
        start = timer()
        main(prog, setting, enforce_algorithm=True, enforced_algorithm=algorithm)
        end = timer()
        logging.info(
            prog + " " + setting + " took " + str(timedelta(seconds=end - start))
        )
    else:
        logging.error("Algorithm not found. Please check typos.")
