import argparse
import os
import sys
import time
from flask import Flask
from requests import request

def createApp(exp_start, probes, periods, exp_end, rounds):
    app = Flask(__name__)
    app.config['exp_start'] = exp_start
    app.config['probes'] = probes
    app.config['periods'] = periods
    app.config['exp_end'] = exp_end
    app.config['rounds'] = rounds
    app.config['probe_total'] = 0

    print('ExpStart: ' + time.strftime('%H:%M:%S', time.localtime(exp_start)) + ' (' + str(exp_start) + ')')
    print('Probes: ' + str(probes))
    print('Probe times: ' + str(periods))
    print('ExpEnd: ' + time.strftime('%H:%M:%S', time.localtime(exp_end)) + ' (' + str(exp_end) + ')')

    @app.route('/signalTermination', methods=['POST'])
    def signal_termination():
        global client_count
        client_count -= 1
        print("client_count: " + str(client_count))
        if client_count == 0:
            os.system("touch terminator")
        return "terminated"

    @app.route('/client', methods=['POST'])
    def clientTime():
        return str(app.config['exp_start'])+' '+str(app.config['exp_end'])

    @app.route('/probe', methods=['POST'])
    def probeTime():
        app.config['probe_total'] += 1
        probe_total = app.config['probe_total']
        probes = app.config['probes']
        for i in range(len(probes)):
            if probe_total > probes[i]: continue
            else:
                times = app.config['periods'][i:]
                times[-1] *= i+1
                output = str(app.config['exp_start'] + (times[-1]-interval) * 60)+'_'+str(app.config['exp_end'])+'_'+str(times)+'_'+str(app.config['rounds'])
                print(output)
                return output
        return "probed"
    
    @app.route('/client_terminate', methods=['POST'])
    def clientTerm():
        print('Client terminated')
        return "terminated"
    
    @app.route('/probe_terminate', methods=['POST'])
    def probeTerm():
        app.config['probe_total'] -= 1
        print('Probe terminated. Probes left: %s' % str(app.config['probe_total']))
        return "terminated"
    
    return app

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('-s', type=float, default=1.0, help='Time, in minutes, before the experiment starts or ends (default: %(default)s)')
    argparser.add_argument('-i', type=float, default=4.0, help='Interval, in minutes, between probings (default: %(default)s)')
    argparser.add_argument('-p', nargs='+', type=int, default=[1, 2, 5, 10], help='Probes per probing session (default: %(default)s)')
    argparser.add_argument('-r', type=int, default=50, help='Number of rounds of probing for each probe number indicated in -p (default: %(default)s)')

    args = argparser.parse_args()
    time_buffer = args.s
    interval = args.i
    probes = args.p
    rounds = args.r

    exp_start = time.mktime(time.gmtime()) + time_buffer*60 #Exp start 1min after the coord
    exp_end = exp_start + len(probes) * interval * 60 * rounds
    periods = []
    for i in range(len(probes)):
        periods.append(interval)

    probe_total = 0

    original = sys.stdout
    with open('./experiment_times.txt','w') as f:
        sys.stdout = f

        print('ExpStart: ' + time.strftime('%H:%M:%S', time.localtime(exp_start)) + ' (' + str(exp_start) + ')')
        print('Probes: ' + str(probes))
        print('Probe periods: ' + str(periods))
        print('Rounds: ' + str(rounds))
        print('ExpEnd: ' + time.strftime('%H:%M:%S', time.localtime(exp_end)) + ' (' + str(exp_end) + ')')

        sys.stdout = original
        f.close()

    app = createApp(exp_start, probes, periods, exp_end, rounds)
    app.run(debug=False, host='0.0.0.0', port=5005)
    