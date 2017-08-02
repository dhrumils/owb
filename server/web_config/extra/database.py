import sys
import json
print(sys.argv)


my_dict = {}
my_dict['filename']=sys.argv[1]
my_dict['major_version']=sys.argv[2]
my_dict['minor_version']=sys.argv[3]
my_dict['commit_number']=sys.argv[4]
my_dict['commit_date']=sys.argv[5]


print my_dict

output_file= sys.argv[6]
with open(output_file,'w') as outfile:
	json.dump(my_dict,outfile)
