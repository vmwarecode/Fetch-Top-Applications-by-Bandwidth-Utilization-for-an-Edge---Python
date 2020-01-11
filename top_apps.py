#!/usr/bin/env python3
#
# Fetch top applications by bandwidth utilization
# 
# Usage: VC_USERNAME='user@velocloud.net' VC_PASSWORD=s3cret python top_apps.py
#

import os
from datetime import datetime, timedelta
from client import *

# EDIT THESE
VCO_HOSTNAME = 'vcoX.velocloud.net'
ENTERPRISE_ID = 1
EDGE_ID = 1
INTERVAL_START = datetime.now() - timedelta(hours=12)
LIMIT = 10
IS_OPERATOR = False

def datetime_to_epoch_ms(dtm):
    return int(dtm.timestamp()) * 1000

def main():

    client = VcoRequestManager(VCO_HOSTNAME)
    client.authenticate(os.environ['VC_USERNAME'], os.environ['VC_PASSWORD'], is_operator=os.environ.get('VC_OPERATOR', IS_OPERATOR))

    result = client.call_api('configuration/getIdentifiableApplications', {
        # As always, note that an enterpriseId is only required when acting as a Partner or Operator user
        # i.e. not a Customer Admin
        "enterpriseId": ENTERPRISE_ID
    })
    applications_by_id = { app['id']: app for app in result['applications'] }

    top_apps_bytes_rx = client.call_api('metrics/getEdgeAppMetrics', {
        "enterpriseId": ENTERPRISE_ID,
        "edgeId": EDGE_ID,
        "interval": {
            "start": datetime_to_epoch_ms(INTERVAL_START)
        },
        "sort": "bytesRx",
        "limit": LIMIT
    })

    print("Top Applications by bytesRx")
    print("===========================")
    for item in top_apps_bytes_rx:
        if item['name'] == 'other':
            display_name = 'Other'
            value = item['metrics']['bytesRx']
        else:
            display_name = applications_by_id[item['name']]['displayName']
            value = item['bytesRx']
        print("%s:\t%d" % (display_name, value))

    top_apps_bytes_tx = client.call_api('metrics/getEdgeAppMetrics', {
        "enterpriseId": ENTERPRISE_ID,
        "edgeId": EDGE_ID,
        "interval": {
            "start": datetime_to_epoch_ms(INTERVAL_START)
        },
        "sort": "bytesTx",
        "limit": LIMIT
    })

    print("Top Applications by bytesTx")
    print("===========================")
    for item in top_apps_bytes_tx:
        if item['name'] == 'other':
            display_name = 'Other'
            value = item['metrics']['bytesTx']
        else:
            display_name = applications_by_id[item['name']]['displayName']
            value = item['bytesTx']
        print("%s:\t%d" % (display_name, value))


if __name__ == '__main__':
    main()
