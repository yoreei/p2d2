import logging

getLogger = logging.getLogger


def add_console_output(format_str):
    """
    define a Handler which writes INFO messages or higher to the sys.stderr
    """
    formatter = logging.Formatter(format_str)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)


format_str = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
# set up logging to file - see previous section for more details
logging.basicConfig(
    level=logging.DEBUG,
    format=format_str,
    datefmt="%m-%d %H:%M",
    filename="logs/mylog.log",
    filemode="w",
)

# Uncomment to disable console output
add_console_output(format_str)

debuglog = logging.FileHandler("logs/debug.log")
debuglog.setLevel(logging.DEBUG)
logging.getLogger("").addHandler(debuglog)

infolog = logging.FileHandler("logs/info.log")
infolog.setLevel(logging.INFO)
logging.getLogger("").addHandler(infolog)
