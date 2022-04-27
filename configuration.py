
#PUT YOUR ENVIROMENT HERE
BASE_URL = 'https://yourenviroment.live.dynatrace.com/api/'

#PUT YOUR TOKEN HERE
API_TOKEN = 'PUTYOURTOKEN'

MAX_REQUESTS_PER_MINUTE = 1000


#PUT YOUR PERIOD HERE IN THIS FORMAT YYYY-MM-DD:HH:MM:SS+hh:mm where the hh:mm indicated the selected timezone (in italy 02:00)
periods = [
    ("2022-04-14T00:00:00+02:00", "2022-04-19T00:00:00+02:00"),
    ("2022-04-19T00:00:00+02:00", "2022-04-23T00:00:00+02:00"),
]

#LIST OF METRICS (i will add serveless in future), you can select if enable it or not
ddu_metrics = {
'log' : 
    { "metric" : "builtin:billing.ddu.log.byEntity",
      "enable" : True},
'metrics' : 
    {"metric" : "builtin:billing.ddu.metrics.byEntity",
      "enable" : True},
'events' : 
    {"metric" : "builtin:billing.ddu.events.byEntity",
      "enable" : True},
}

#IF IT IS EMPTY THE SCRIPT WILL FIND AUTOMATICALLY THE MZs, IF YOU WANT A SPECIF MZ, PUT THE EXACT NAME IN THE LIST LIKE ["TEST1", "TEST2"]
MZs = {
'log' : [],
'metrics' : [],
'events' : [],
}
#SAME AS FOR MZs BUT FOR ENTITIES, INSERT ENTITIES ONLY IF YOU ALREADY KNOW IT (NOT SUGGESTED)
entities = {
'log' : [],
'metrics' : [],
'events' : [],
}

################################
#THIS LIST ARE THE ENTITIES THAT HAVEN?T THE MZs PROPERTIES; SO YOU CAN'T FILTER 
not_good_entity = ["APM_SECURITY_GATEWAY", "APPLICATION_METHOD_GROUP", "AZURE_REGION", "BOSH_DEPLOYMENT", "BROWSER", 
"CINDER_VOLUME", "CONTAINER_GROUP", "DCRUM_SERVICE_INSTANCE", "DEVICE_APPLICATION_METHOD_GROUP", 
"DOCKER_CONTAINER_GROUP", "ENVIRONMENT", "GCP_ZONE", "GEOLOCATION", "GEOLOC_SITE", "HYPERVISOR_CLUSTER", 
"NEUTRON_SUBNET", "OPENSTACK_AVAILABILITY_ZONE", "OPENSTACK_COMPUTE_NODE", "OPENSTACK_PROJECT", "OPENSTACK_REGION", 
"OS", "QUEUE_INSTANCE", "RUNTIME_COMPONENT", "SOFTWARE_COMPONENT", "SWIFT_CONTAINER", "SYNTHETIC_LOCATION", "VMWARE_DATACENTER"]
