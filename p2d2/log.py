import logging

getLogger = logging.getLogger

# set up logging to file - see previous section for more details
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename="mylog.log",
    filemode="w",
)
# define a Handler which writes INFO messages or higher to the sys.stderr
formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")

# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)

debuglog = logging.FileHandler("debug.log")
debuglog.setLevel(logging.DEBUG)
logging.getLogger("").addHandler(debuglog)

infolog = logging.FileHandler("info.log")
infolog.setLevel(logging.INFO)
logging.getLogger("").addHandler(infolog)
