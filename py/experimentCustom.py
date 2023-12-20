import sys
import logging
from timeit import default_timer as timer
from datetime import timedelta
from experimentBudgetModified import main

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
    script, prog, setting = sys.argv
    start = timer()
    main(prog, setting)
    end = timer()
    logging.info(prog + " " + setting + " took " + str(timedelta(seconds=end - start)))
    logging.error("help")
