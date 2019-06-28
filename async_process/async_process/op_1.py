import logging
import os
import time
from functools import lru_cache
from os import getpid
from random import randint

model_weight = None


@lru_cache(None)
def get_model():
    log = logging.getLogger(f"In-Memory Loading of Model")
    model = os.getpid()
    log.info(f"Started for [{model}]")
    time.sleep(model_weight * 3)
    log.info(f"Done for [{model}]")
    return model


def operation(context, data):
    log = logging.getLogger(f"Operation {data}")
    model = get_model()
    log.info(f"Predict Using Model[{model}]")
    time.sleep(data % 3)
    log.info(f"Result --> {data}")
    return data


def init_operation():
    global model_weight
    pid = os.getpid()
    model_weight = (pid % 3) + 1
    log = logging.getLogger(f"Init Operation Worker [{pid}]")
    log.info("Started")
    get_model()
    log.info("Ready")
