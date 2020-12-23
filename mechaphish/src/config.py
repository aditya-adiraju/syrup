logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored_console': {
           '()': 'coloredlogs.ColoredFormatter', 
           'format': "%(asctime)s - %(name)-10s - %(levelname)8s - %(message)s", 
           'datefmt': '%H:%M:%S'
        },
        'format_for_file': {
           'format': "%(asctime)s :: %(levelname)s :: %(funcName)s in %(filename)s (l:%(lineno)d) :: %(message)s", 
           'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'colored_console',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console']
        }
    }
}