import sys

import yaml
from yaml.loader import SafeLoader

from executor import Executor
from models.workflow import Flow

import logging

logging.basicConfig(filename='app.log', filemode='w+', format='%(asctime)s;%(message)s', level=logging.DEBUG)
logging.info("Logging started")

if __name__ == "__main__":
    # if len(sys.argv) <= 1:
    #     print("No file to load")
    # filename = sys.argv[0]
    filename = "DataSet\Examples\Milestone1\Milestone1_Example.yaml"

    with open(filename) as f:
        configuration = yaml.load(f, Loader=SafeLoader)
        name = [key for key in configuration.keys()][0]
        flow = Flow(**configuration[name])
        Executor(name, flow).start_execution()
