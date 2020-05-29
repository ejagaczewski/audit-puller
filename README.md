# audit-puller
Pulls Audit Logs from Prisma Cloud and outputs them to CSV

<b>Requirements and Dependencies</b>

Python 3.X

Requires Pandas

<code> sudo pip install pandas </code>

Requires Requests

<code> sudo pip install requests </code>

<b>Config</b>

<p>Create folder called logs in the directory that you run the script</p>
<p>Fill in the variable for accessKey/secretKey and make sure that both the logon url and API url are the same as your tenant</p>
<p>Set environment variables for PC_SECRET_KEY and PC_ACCESS_KEY
