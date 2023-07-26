import logging

# to maintain a dict of logger instances
dict_of_loggers_in_use = dict()


def pick_log_format(log_type="json"):
    # import json
    format_dict = {}
    if log_type == "json":
        format_dict["date_fmt"] = "%d/%m/%Y %H:%M:%S"
        # base_dict = {"time": "%(asctime)s", "level": "%(levelname)s",
        # "message": "%(message)s","file":"%(name)s"}
        base_dict = "%(message)s"
        # extra - dynamically add new key,value pairs to json format
        # format_dict["msg_fmt"] = json.dumps({**base_dict, **extra})
        format_dict["msg_fmt"] = base_dict
        # json.dumps({**base_dict})

    if log_type == "text":
        format_dict["date_fmt"] = "%d/%m/%Y %H:%M:%S"
        format_dict["msg_fmt"] = "[%(levelname)s] %(asctime)s - %(name)s:  %(message)s"

    return format_dict


def create_stream_handler(format_dict, loglevel=logging.INFO):
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        logging.Formatter(fmt=format_dict["msg_fmt"], datefmt=format_dict["date_fmt"])
    )
    stream_handler.setLevel(loglevel)
    return stream_handler


def create_file_handler(
    format_dict, trace_file="/var/tmp/quester_trace.log", loglevel=logging.WARNING
):
    file_handler = logging.FileHandler(trace_file)
    file_handler.setFormatter(
        logging.Formatter(fmt=format_dict["msg_fmt"], datefmt=format_dict["date_fmt"])
    )
    file_handler.setLevel(loglevel)
    return file_handler


def get_logger(
    name=__name__, log_type="text", trace_file="/var/tmp/quester_trace.log", extra={}
) -> logging.Logger:
    """a method that returns an instance of logger based on configuaration

    based on log_type, format can be text,json
    add the log handlers
    """

    from config import Settings, get_settings

    settings: Settings = get_settings()

    loglevel = settings.LOG_LEVEL  # read loglevel from config

    global dict_of_loggers_in_use

    # set msg_fmt & date_fmt based on log_type - json or text
    # extra is dict of additonal params to be logged
    format_dict = pick_log_format(log_type)

    # create the logger instance
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)  # log level at root is set to DEBUG
    # if logger.hasHandlers
    # set up the log handlers - stream and file
    logger.addHandler(create_stream_handler(format_dict=format_dict, loglevel=loglevel))
    # loglevel for file_handler is set to ERROR (default is WARNING)
    logger.addHandler(
        create_file_handler(
            format_dict=format_dict, trace_file=trace_file, loglevel=logging.WARNING
        )
    )
    logger.propagate = False

    # to avoid creating duplicate instances of logger
    if dict_of_loggers_in_use.get(name + "_" + log_type, None) == None:
        dict_of_loggers_in_use[name + "_" + log_type] = logger
        # print(len(dict_of_loggers_in_use.keys()), \
        #               dict_of_loggers_in_use[name+'_'+log_type] )

    return dict_of_loggers_in_use[name + "_" + log_type]
