import argparse
import os
import time


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('t', type=float, default=None, help='When to kill exp (default: %(default)s)')

    args = argparser.parse_args()
    end = args.t

    wait = 60 * 60 # 1h
    now = time.mktime(time.gmtime())
    while  now < end:
        if end - now < 2 * 60: # 2min
            wait = 1
        elif end - now < 10 * 60: # 10min
            wait = 60
        elif end - now < 60 * 60: # 1h
            wait = 5 * 60
        elif end - now < 2 * 60 * 60: # 2h
            wait = 20 * 60
        
        time.sleep(wait)
    
    os.system('nohup ansible-playbook run_collection.yml --tags \"kill_ecp\" -i inventory_model.cfg > kill_play_log.txt 2>&1 &')