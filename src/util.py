import datetime
import os


def file_log_e(msg):
    with open(os.path.join('save', 'log.txt'), 'a') as f:
        print('Error--: ' + str(datetime.datetime.today())+'\n\t'+msg, file=f)


def file_log_f(msg):
    with open(os.path.join('save', 'log.txt'), 'a') as f:
        print('Failed-: ' + str(datetime.datetime.today())+'\n\t'+msg, file=f)


def file_log_s(msg):
    with open(os.path.join('save', 'log.txt'), 'a') as f:
        print('Success: ' + str(datetime.datetime.today())+'\n\t'+msg, file=f)