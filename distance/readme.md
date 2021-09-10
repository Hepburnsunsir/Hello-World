## mips.py 
**functions:**

1. get target functions and target blocks, and need manually change the goal/(Vulnerability point list) in mips.py
2. get call graph and control flow graphs for a binary

**usage**

1. this script is manually used  in IDA 
2. change the goal/(Vulnerability point list) in mips.py


## block_distance.py

output file containing distance for each block

eg：
/usr/bin/python3 ./block_distance.py -j ./data/dir802-httpd/httpd_cfg.json -tb ./data/dir802-httpd/httpdBBtargets.txt -tf ./data/dir802-httpd/httpdTtargets.txt  -ob ./data/dir802-httpd/block_distance.txt > ./data/dir802-httpd/log.txt 2>&1


