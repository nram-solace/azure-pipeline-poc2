# provison-queue.py 
# provision list of queues on Solace brokers
# if queue already exists, update their properties instead
#
# To trigger this from Azure devops pipeline, add this to pipeline yaml:
#   - stage: provisionQueue
#     jobs:
#     - job: provisionQueue
#       steps:
#       - task: PythonScript@0
#         inputs:
#           scriptSource: 'filePath' # Options: filePath, inline
#           scriptPath: scripts/provision-queue.py
#           arguments: --host $(HOST) --user $(SEMPUSER) --pass $(SEMPPASS)
# and have the variables HOST, SEMPUSER, SEMPPASS defined in the pipeline / variable group
#
# Requires:
#  input/queues.yaml
#     See input/sample-queues.yaml 
#  templates/queues.json 
#
# Jun 21, 2021 - Ramesh Natarajan (nram), Solace PSG

import sys
import argparse
import yaml
import json
import requests

input_yaml_file="input/queues.yaml"
template_json_file="template/queues.json"
config_url='SEMP/v2/config'

def main(argv):
    print ('provision-queue.py : starting ')

    p = argparse.ArgumentParser()
    p.add_argument('--host', dest="host", required=True, help='solace broker url') 
    p.add_argument('--user', dest="user", required=True, help='solace cli username') 
    p.add_argument('--pass', dest="passwd", required=True, help='solace cli password') 
    r = p.parse_args()

    # read template json
    with open(template_json_file, "r") as fp:
        template_data = json.load(fp)
    print ('Template JSON :', type(template_data), template_data)

    # read input yaml file
    with open(input_yaml_file, 'r') as f:
        queues = yaml.load(f)
    print ('Queues YAML :', type(queues), queues)

    # add template defaults to input yaml
    for k,v in queues['defaults'].items():
        template_data[k] = v

    vpn = queues['defaults']['msgVpnName']
    url = f'{r.host}/{config_url}/msgVpns/{vpn}/queues'

    for queue in queues['queues']:
        q_url = f'{url}/{queue}'
        status = get_queue(q_url, r.user, r.passwd)
        print (f'Get queue {queue} returned {status}')
        data = template_data.copy()
        data['queueName'] = queue
        if status == 200:
            print (f'Queue {queue} exists. Update settings instead of creating')
            print (f'Shutting down queue {queue} before updates')
            # shutdown queue before making changes
            temp_data = data.copy()
            temp_data['ingressEnabled'] = False
            temp_data['egressEnabled'] = False
            update_queue(q_url, r.user, r.passwd, temp_data)

            # send update properties now
            print (f'Updating queue {queue}')
            update_queue(q_url, r.user, r.passwd, data)
        else:
            print (f'Queue does not exist. Create queue {queue}')
            create_queue(url, r.user, r.passwd, data)

def get_queue(url, user, passwd):
    print (f'get_queue: url = {url}')
    status = getattr(requests, 'get')(url, 
        headers={"content-type": "application/json"},
        auth=(user, passwd),
        data=(None))
    #print('response :\n---\n', status.text)
    return status.status_code    

def create_queue(url, user, passwd, json_data):
    print (f'create_queue: url = {url}')
    #print ('request json:\n---\n', json.dumps(json_data, indent=4))
    status = getattr(requests, 'post')(url, 
        headers={"content-type": "application/json"},
        auth=(user, passwd),
        data=(json.dumps(json_data)))
    #print('response :\n---\n', status.text)
    assert status.status_code == 200, status.text
    return status.status_code  

def update_queue(url, user, passwd, json_data):
    print (f'update_queue: url = {url}')
    #print ('request json:\n---\n', json.dumps(json_data, indent=4))
    status = getattr(requests, 'patch')(url, 
        headers={"content-type": "application/json"},
        auth=(user, passwd),
        data=(json.dumps(json_data)))
    #print('response :\n---\n', status.text)
    assert status.status_code == 200, status.text
    return status.status_code

if __name__ == "__main__":
    main(sys.argv[1:])