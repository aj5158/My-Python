""" 
Requirement - dnspython toolkit
git clone git://github.com/rthalley/dnspython.git
cd dnspython
python setup.py install --user
"""

ACL = []
from dns import resolver

res = resolver.Resolver()
res.nameservers = ['8.8.8.8']

#Can return multiple values per URL
#Some URLS dont resolve, doesnt handle this yet
#Strips newline and spaces

with open ('VIC-GOV-URLs.txt') as f:
    for url in f:
        IP = []
        url = url.strip()
        answers = res.query(url)
        for rdata in answers:
            IP.append(rdata.address)
        for elem in IP:
            ACL.append(elem)

#sort and uniq
ACL = sorted(set(ACL))

#Print our ACL
f = open('VIC-GOV-UNMETER-LIST.csv','w')
f.write('ip access-list extended VIC-GOV-UNMETER-LIST\n')
f.write(' remark --- Must unmeter the WLC ---\n')
f.write(' deny   ip any host 100.79.0.2\n')
f.write(' remark --- Host IPs to unmeter ---\n')
for elem in ACL:
    f.write(' deny   ip host ' +  str(elem) + ' any\n')
f.write(' permit ip any any')
f.close()
