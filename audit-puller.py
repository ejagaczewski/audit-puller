import requests, json, time, os, boto3
import pandas as pd

#Get Access keys from environment variables PC_ACCESS_KEY and PC_SECRET_KEY

accessKey = os.environ.get("PC_ACCESS_KEY")
secretKey = os.environ.get("PC_SECRET_KEY")

#Hard-code Prisma Cloud Access Keys *NOT RECOMMENDED*
accessKey = ""
secretKey = ""

#Bucket for optional S3 upload
#bucketName = ""

#Specify correct API address
apiUrl = "https://api3.prismacloud.io/audit/redlock"

#Time unit for audit logs https://api.docs.prismacloud.io/reference#rl-audit-logs
timeUnit = "day"
#Amount of time unit
timeAmount = "120"

#Enter URL for tenant
loginUrl = "https://api3.prismacloud.io/login"

loginPayload = '{"username" : "' + accessKey + '", "password" : "' + secretKey + '"}'

headers = {
    'accept': "application/json; charset=UTF-8",
    'content-type': "application/json; charset=UTF-8"
    }

#Get JWT Token for login
loginResponse = requests.request("POST", loginUrl, data=loginPayload, headers=headers, verify=False)
jsonResponse = loginResponse.json()
print(loginResponse.text)
#Extract token from json
token = jsonResponse['token']

#Pull audit logs

querystring = {"timeType":"relative","timeAmount": timeAmount,"timeUnit": timeUnit}

headers = {'accept': "application/json; charset=UTF-8",'x-redlock-auth': token}

auditLogs = requests.request("GET", apiUrl, headers=headers, params=querystring, verify=False)

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

#print("Writing files to S3...")
#Copy CSV to S3 bucket
#s3 = boto3.client('s3')
#s3.upload_file('logs/' + timestr +".csv", bucketName, timestr +".csv")
