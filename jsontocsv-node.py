# coding : utf-8
import json,codecs,re
file = codecs.open('scraped_data_utf8.json','r',encoding='utf-8')
node = codecs.open('node.csv','w',encoding='utf-8')
f = file.read()
i=0
node.write('id,name,nums,\n')
gpid = re.findall(r'"groupid": "([^\"]+)",?',f)
gpname = re.findall(r'"groupname": "([^\"]+)",?',f)
gpnum = re.findall(r'"membersnum": (\d+),?',f)

print len(gpid),len(gpname),len(gpnum)
if len(gpid)==len(gpname)==len(gpnum):
    while i<len(gpid):
        if int(gpnum[i])>10000:
            node.write('%s,"%s",%s,\n' % (gpid[i],gpname[i],gpnum[i]))
        i+=1
file.close()
node.close()