# coding : utf-8
import json,codecs,re
file = codecs.open('scraped_data_utf8.json','r',encoding='utf-8')
edge = codecs.open('edge.csv','w',encoding='utf-8')
f = file.read()
i=0
edge.write('Source,Target,\n')
gpid = re.findall(r'"groupid": "([^\"]+)",?',f)
bgps = re.findall(r'"bdgroupsid": (\[.+\]?), "membersnum":?',f)
gpnum = re.findall(r'"membersnum": (\d+),?',f)
sid = set(gpid)
if len(gpid)==len(bgps):
    while i<len(gpid):
        if int(gpnum[i]) > 10000:
            bgps[i] = re.findall(r'"(.+?)"',bgps[i])
            for target in bgps[i]:
                if target in sid:
                    edge.write('%s,%s,\n' % (gpid[i],target))
        i+=1
file.close()
edge.close()