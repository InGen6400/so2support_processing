import datetime
import inspect
import os


def file_log_e(msg):
    frame = inspect.currentframe().f_back
    with open(os.path.join('save', 'log.txt'), 'a') as f:
        print('Error--: ' + str(datetime.datetime.today()) + ' ' +
              os.path.basename(frame.f_code.co_filename) + ':' +
              frame.f_lineno +
              '\n\t'+msg, file=f)


def file_log_f(msg):
    with open(os.path.join('save', 'log.txt'), 'a') as f:
        print('Failed-: ' + str(datetime.datetime.today())+'\n\t'+msg, file=f)


def file_log_s(msg):
    with open(os.path.join('save', 'log.txt'), 'a') as f:
        print('Success: ' + str(datetime.datetime.today())+'\n\t'+msg, file=f)
