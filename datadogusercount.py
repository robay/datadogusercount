#!/usr/bin/env python

# Rob Ayres 2019

# get a list of users from DataDog and then send the numbers back into 
# DataDog as metrics. You can then create some nice dashboards showing your
# pending and active users. api and app keys are read from an external file

from datadog import initialize, api
import time

# get DataDog api keys

credsfile = "ddapilogin"
credsfp = open(credsfile, "r")
credslist = credsfp.readlines()
datadog_api_key = credslist[0].rstrip()
datadog_app_key = credslist[1].rstrip()

live = 0
pending = 0

# connect to DD

options = {'api_key': datadog_api_key, 'app_key': datadog_app_key}
initialize(**options)

userlist = api.User.get_all()

epochts = int(time.time())

for user in userlist['users']:

  if user['verified']:
    live = live + 1
  else:
    pending = pending + 1

ddret = api.Metric.send([
 {"metric": "datadog.users", "points": [epochts, live], "tags": ["datadogusers:live"]},
 {"metric": "datadog.users", "points": [epochts, pending], "tags": ["datadogusers:pending"]}])

print ddret
print("live: %s pending: %s total: %s") % (live, pending, len(userlist['users']))
