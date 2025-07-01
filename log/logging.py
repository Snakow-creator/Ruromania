import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

console = logging.StreamHandler()
file_handler = logging.FileHandler("logs.log")


async def start_logging():
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(name)-4s: %(levelname)-8s %(message)s")
    console.setFormatter(formatter)

    file_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter(
      "[%(asctime)s]\t Filename: %(module)s(%(lineno)d line) - %(levelname)s - %(message)s",
      datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)

    log.addHandler(console)
    log.addHandler(file_handler)

    log.info("Start Ruromaina")
