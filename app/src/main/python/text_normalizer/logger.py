import logging
from logstash_async.handler import AsynchronousLogstashHandler
from logstash_async.formatter import LogstashFormatter


def init_logger(config):
    logger = logging.getLogger(config["name"])
    logger.setLevel(logging.INFO)
    logstash_formatter = LogstashFormatter(message_type=f"text_normalizer-{config['name']}")
    logstash_handler = AsynchronousLogstashHandler(config["host"], config["port"], None)
    logstash_handler.setFormatter(logstash_formatter)
    logger.addHandler(logstash_handler)
    logger.info(f"Started {config['name']}", extra={"log_event": "system started"})
    return logger

