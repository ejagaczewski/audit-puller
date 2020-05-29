import requests, json, csv, time, os
import pandas as pd


#Prisma Cloud Access Keys
accessKey = ""
secretKey = ""

#Specify correct API address
apiUrl = "https://api3.prismacloud.io/audit/redlock"

#Time unit for audit logs https://api.docs.prismacloud.io/reference#rl-audit-logs
timeUnit = "day"
#Amount of time unit
timeAmount = "120"

#Enter correct URL for tenant
loginUrl = "https://api3.prismacloud.io/login"

loginPayload = '{"username" : "' + accessKey + '", "password" : "' + secretKey + '"}'

headers = {
    'accept': "application/json; charset=UTF-8",
    'content-type': "application/json; charset=UTF-8"
    }

#Get JWT Token for login
loginResponse = requests.request("POST", loginUrl, data=loginPayload, headers=headers)
jsonResponse = loginResponse.json()

#Extract token from json
token = jsonResponse['token']

#Pull audit logs


querystring = {"timeType":"relative","timeAmount": timeAmount,"timeUnit": timeUnit}

headers = {'accept': "application/json; charset=UTF-8",'x-redlock-auth': token}

auditLogs = requests.request("GET", apiUrl, headers=headers, params=querystring)

timestr = time.strftime("%Y%m%d-%H%M%S")
print(timestr)

#Output to file
f = open(timestr + '.txt', "w")
f.write(auditLogs.text)
#Convert to CSV
df = pd.read_json (timestr + '.txt')
df.to_csv ('logs/' + timestr + '.csv', index = None)
#Cleanup
os.remove(timestr + '.txt')
print("Pulled audit logs sucessfully and wrote them to " + timestr +".csv")
