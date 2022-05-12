import sys, requests, json, time
import urllib.parse
from tqdm import tqdm
from datetime import date

from configuration import *

PAGE_SIZE = 200
sys.tracebacklimit = 0
    
if len(periods) == 0:
    print("ALMOST 1 PERIOD PLS")
    exit()
    
print(API_TOKEN)

allManagemementZones = None
# GET ALL MZs
try:
    response = requests.get(
        BASE_URL + "config/v1/managementZones",
        headers={"Authorization": "Api-Token " + API_TOKEN},
    )
    response.raise_for_status()
    
    allManagemementZones = json.loads(response.content)["values"]
except requests.exceptions.RequestException as e:
    print(e)
    exit()
except:
    print("GENERIC ERROR")
    exit()

allEntityTypes = None
# GET ALL ENTITIES
try:
    response = requests.get(
        BASE_URL + "v2/entityTypes", headers={"Authorization": "Api-Token " + API_TOKEN}
    )
    response.raise_for_status()
    
    allEntityTypes = json.loads(response.content)["types"]
except requests.exceptions.RequestException as e:
    print(e)
    exit()
except:
    print("GENERIC ERROR")
    exit()


#check if there are entities in other pages
try:
    nextPage = json.loads(response.content)["nextPageKey"]
except:
    nextPage = None
    
while nextPage != None:
    response = requests.get(
        BASE_URL + "v2/entityTypes?nextPageKey=" + nextPage,
        headers={"Authorization": "Api-Token " + API_TOKEN},
    )
    response.raise_for_status()
    nextPage = (json.loads(response.content)).get("nextPageKey", None)
    allEntityTypes.extend(json.loads(response.content)["types"])
 
entitiesName = [] 
for entityTypeIndex, entityType in enumerate(allEntityTypes):
    entitiesName.append(allEntityTypes[entityTypeIndex]["type"])
    
#check if there are only one periods
only_one_period = False

if len(periods) == 1:
    only_one_period = True

print("FIRST PHASE - FIND WHICH ENTITIES")

for key, value in ddu_metrics.items(): 

    if value['enable'] == True:
        print("Find entities for:", key)
    else:
        continue
    
    METRIC_NAME = value['metric']
    
    if len(entities[key]) != 0:
        print("There are already a definition list in config, check it")
        continue
    
    
    for entity_temp in tqdm(entitiesName):
        
        if entity_temp in not_good_entity:
            continue
        try:
            #take the first and last period as reference
            FROM = periods[0][0] #first
            TO = periods[-1][1] #last
            
            response = requests.get(
                "{}v2/metrics/query?metricSelector={}:splitBy()&resolution=1d&entitySelector=type({})&from={}&to={}".format(
                    BASE_URL,
                    METRIC_NAME,
                    entity_temp,
                    FROM.replace("+", "%2B", 1),
                    TO.replace("+", "%2B", 1),
                    
                ),
                headers={"Authorization": "Api-Token " + API_TOKEN},
            )
            
            response.raise_for_status()

            time.sleep(60 / MAX_REQUESTS_PER_MINUTE)
            dduConsumptionOfMZandETDict = json.loads(response.content)["result"][0]["data"]
                
            
            dduConsumptionOfMZandET = 0
            if dduConsumptionOfMZandETDict:
                # Filter out every empty usage values and create the sum of ddu usage
                dduConsumptionOfMZandET = sum(
                    filter(None, dduConsumptionOfMZandETDict[0]["values"])
                )
                
            if dduConsumptionOfMZandET > 0:
                entities[key].append(entity_temp)
            
        except requests.exceptions.RequestException as e:
            print("ERRORE", e)
            continue
            
    print(entities[key])
    print()
    

if not only_one_period:
    print("SECOND PHASE - FIND WHICH MZ")
else:
    print("SECOND and THIRD PHASE - FIND DDU CONS. for MZs")
    
for key, value in ddu_metrics.items(): 
    
    temp_list_MZ = []
    
    if value['enable'] == True:
        if only_one_period:
            print("Find MZ DDU Consumption for:", key)
        else:
            print("Find MZ for:", key)
    else:
        continue
    
    METRIC_NAME = value['metric']
    MZ_to_check = []
    
    
    if len(MZs[key]) != 0 and not only_one_period:
        print("There are already a definition list in config, check it")
        continue
    if len(MZs[key]) != 0 and only_one_period:
        print("Skip finding MZ, we have already a list")
        MZ_to_check = MZs[key]
    else:
        for managementZoneIndex, managementZone in enumerate(allManagemementZones):
            MZ_to_check.append(managementZone['name'])
        
    
    for managementZone_name in tqdm(MZ_to_check):
        dduConsumptionOfManagementZone = 0
        FROM = periods[0][0] #str(sys.argv[1])
        TO = periods[-1][1]#str(sys.argv[2])
        
        d0 = date(int(FROM[:4]), int(FROM[5:7]), int(FROM[8:10]))
        d1 = date(int(TO[:4]), int(TO[5:7]), int(TO[8:10]))
        delta = d1 - d0
        delta = int(delta.days)
        
        if delta <= 7:
            resolution = '1h'
        elif delta <= 31:
            resolution = '1d'
        elif delta <= 365:
            resolution = '1w'
        else:
            resolution = '1M'
        
        FILTER_ENTITY = []
        for entityType in entities[key]:
            if entityType in not_good_entity:
                continue
            else:
                temp_string = 'in("dt.entity.monitored_entity",entitySelector("type({}),mzName(~"{}~")"))'.format(entityType, managementZone_name)
                FILTER_ENTITY.append(temp_string)
        
        FILTER_ENTITY = ','.join(FILTER_ENTITY)
        
        base = '{}v2/metrics/query?metricSelector={}:splitBy("dt.entity.monitored_entity"):filter(or({})):splitBy():fold(sum)&resolution={}&from={}&to={}'.format(
            BASE_URL,
            METRIC_NAME,
            FILTER_ENTITY,
            resolution,
            FROM,
            TO
        )
        
        base_encoded = urllib.parse.quote(base, safe=':/?=()&,')
        
        try:  
            response = requests.get(base_encoded, headers={"Authorization": "Api-Token " + API_TOKEN},)
                
            response.raise_for_status()
            time.sleep(60 / MAX_REQUESTS_PER_MINUTE)
            dduConsumptionOfMZandETDict = json.loads(response.content)["result"][0]["data"]


            if dduConsumptionOfMZandETDict:
                dduConsumptionOfMZandET = 0
                dduConsumptionOfMZandET = sum(
                    filter(None, dduConsumptionOfMZandETDict[0]["values"])
                )
                
                dduConsumptionOfManagementZone = dduConsumptionOfMZandET
                
        
        
        except requests.exceptions.RequestException as e:
            print("ERRORE", entityType, e)
            continue
        
        if dduConsumptionOfManagementZone > 0:
            MZs[key].append(managementZone_name)
            if only_one_period:
                temp_list_MZ.append(" ".join([managementZone_name, "|", str(round(dduConsumptionOfManagementZone, 2)), "|", FROM, "|", TO]))
    
    if not only_one_period:
        print(MZs[key])
    else:
        print("\n".join(temp_list_MZ))
    
    print()

if not only_one_period:
    print("THIRD PHASE - FIND DDU CONS. FOR MZ")
else:
    exit() #already done


for key, value in ddu_metrics.items(): 

    if value['enable'] == True:
        if only_one_period:
            print("Find MZ DDU Consumption for:", key)
        else:
            print("Find MZ for:", key)
    else:
        continue
    
    METRIC_NAME = value['metric']

    for managementZone in MZs[key]:
        
        for period in periods:
            
            dduConsumptionOfManagementZone = 0
            FROM = period[0]
            TO = period[1]
           
            
            d0 = date(int(FROM[:4]), int(FROM[5:7]), int(FROM[8:10]))
            d1 = date(int(TO[:4]), int(TO[5:7]), int(TO[8:10]))
            delta = d1 - d0
            delta = int(delta.days)
            
            if delta <= 7:
                resolution = '1h'
            elif delta <= 31:
                resolution = '1d'
            elif delta <= 365:
                resolution = '1w'
            else:
                resolution = '1M'
            
            
            FILTER_ENTITY = []
            for entityType in entities[key]:
                if entityType in not_good_entity:
                    continue
                else:
                    temp_string = 'in("dt.entity.monitored_entity",entitySelector("type({}),mzName(~"{}~")"))'.format(entityType, managementZone)
                    FILTER_ENTITY.append(temp_string)
            
            FILTER_ENTITY = ','.join(FILTER_ENTITY)
            
            base = '{}v2/metrics/query?metricSelector={}:splitBy("dt.entity.monitored_entity"):filter(or({})):splitBy():fold(sum)&resolution={}&from={}&to={}'.format(
                    BASE_URL,
                    METRIC_NAME,
                    FILTER_ENTITY,
                    resolution,
                    FROM,
                    TO
                )
                
            base_encoded = urllib.parse.quote(base, safe=':/?=()&,')
          
            try:  
                response = requests.get(base_encoded, headers={"Authorization": "Api-Token " + API_TOKEN},)
                    
                response.raise_for_status()


                time.sleep(60 / MAX_REQUESTS_PER_MINUTE)
                dduConsumptionOfMZandETDict = json.loads(response.content)["result"][0]["data"]

                if dduConsumptionOfMZandETDict:
                    dduConsumptionOfMZandET = 0
                    dduConsumptionOfMZandET = sum(
                        filter(None, dduConsumptionOfMZandETDict[0]["values"])
                    )
                    
                    dduConsumptionOfManagementZone = dduConsumptionOfMZandET
                    
            except requests.exceptions.RequestException as e:
                print("!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!", entityType, e)
                continue
            
            
            print(managementZone, "|", str(round(dduConsumptionOfManagementZone, 2)), "|", FROM, "|", TO)
             
    print()


