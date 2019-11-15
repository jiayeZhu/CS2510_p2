#start DNS server
echo "booting DNS server"
python3 DNS.py --DSLIST="127.0.0.1:18888,127.0.0.1:18889,127.0.0.1:18890" 1>DNS.log 2>&1 &
echo "DNS server booted"

#start the directory servers
echo "booting directory servers"
python3 DirectoryServer.py -p 18888 --server="127.0.0.1:8888"  1>DS_18888.log 2>&1 &
python3 DirectoryServer.py -p 18889 --server="127.0.0.1:8888"  1>DS_18889.log 2>&1 &
python3 DirectoryServer.py -p 18890 --server="127.0.0.1:8888"  1>DS_18890.log 2>&1 &
echo "directory servers booted"

#start the storage nodes
echo "booting storage nodes"
python3 StorageNode.py -p 20001 --server="127.0.0.1:8888" -d 'SN1_storage' 1>SN_20001.log 2>&1 &
python3 StorageNode.py -p 20002 --server="127.0.0.1:8888" -d 'SN2_storage' 1>SN_20002.log 2>&1 &
python3 StorageNode.py -p 20003 --server="127.0.0.1:8888" -d 'SN3_storage' 1>SN_20003.log 2>&1 &
python3 StorageNode.py -p 20004 --server="127.0.0.1:8888" -d 'SN4_storage' 1>SN_20004.log 2>&1 &
python3 StorageNode.py -p 20005 --server="127.0.0.1:8888" -d 'SN5_storage' 1>SN_20005.log 2>&1 &
python3 StorageNode.py -p 20006 --server="127.0.0.1:8888" -d 'SN6_storage' 1>SN_20006.log 2>&1 &
python3 StorageNode.py -p 20007 --server="127.0.0.1:8888" -d 'SN7_storage' 1>SN_20007.log 2>&1 &
python3 StorageNode.py -p 20008 --server="127.0.0.1:8888" -d 'SN8_storage' 1>SN_20008.log 2>&1 &
echo "storage nodes booted"


