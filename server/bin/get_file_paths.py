import json
import os

out = []

g = os.walk(r'..\course_helper')
for path, dir_list, file_list in g:
    for file_name in file_list:
        t = os.path.abspath(os.path.join(path, file_name))
        if t.find('__pycache') > -1:
            continue
        out.append(t)
print(json.dumps(out))
