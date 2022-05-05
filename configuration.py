
#PUT YOUR ENVIROMENT HERE
BASE_URL = 'https://yourenviroment.live.dynatrace.com/api/'

#PUT YOUR TOKEN HERE
API_TOKEN = 'PUTYOURTOKEN'

MAX_REQUESTS_PER_MINUTE = 1000


periods = [
    ("2022-04-28T00:00:00+02:00", "2022-05-05T00:00:00+02:00"),
]

ddu_metrics = {
'log' : 
    { "metric" : "builtin:billing.ddu.log.byEntity",
      "enable" : True},
'metrics' : 
    {"metric" : "builtin:billing.ddu.metrics.byEntity",
      "enable" : True},
'events' : 
    {"metric" : "builtin:billing.ddu.events.byEntity",
      "enable" : False},
'traces' : 
    {"metric" : "builtin:billing.ddu.traces.byEntity",
      "enable" : False},
'serveless' : 
    {"metric" : "builtin:billing.ddu.serveless.byEntity",
      "enable" : False},
}

MZs = {
'log' : [],
'metrics' : [],
'events' : [],
'traces' : [],
'serveless' : [],
}

entities = {
'log' : [],
'metrics' : [],
'events' : [],
'traces' : [],
'serveless' : [],
}




################################
not_good_entity = ["APM_SECURITY_GATEWAY", "APPLICATION_METHOD_GROUP", "AZURE_REGION", "BOSH_DEPLOYMENT", "BROWSER", 
"CINDER_VOLUME", "CONTAINER_GROUP", "DCRUM_SERVICE_INSTANCE", "DEVICE_APPLICATION_METHOD_GROUP", 
"DOCKER_CONTAINER_GROUP", "ENVIRONMENT", "GCP_ZONE", "GEOLOCATION", "GEOLOC_SITE", "HYPERVISOR_CLUSTER", 
"NEUTRON_SUBNET", "OPENSTACK_AVAILABILITY_ZONE", "OPENSTACK_COMPUTE_NODE", "OPENSTACK_PROJECT", "OPENSTACK_REGION", 
"OS", "QUEUE_INSTANCE", "RUNTIME_COMPONENT", "SOFTWARE_COMPONENT", "SWIFT_CONTAINER", "SYNTHETIC_LOCATION", "VMWARE_DATACENTER"]
