#start DNS server
echo "booting DNS server"
python3 DNS.py --DSLIST="127.0.0.1:18888,127.0.0.1:18889,127.0.0.1:18890" 1>DNS.log 2>DNS.errlog &
echo "DNS server booted"

#start the directory servers
echo "booting directory servers"
python3 DirectoryServer.py -p 18888 --server="127.0.0.1:8888"  1>DNS_18888.log 2>DNS_18888.err &
python3 DirectoryServer.py -p 18889 --server="127.0.0.1:8888"  1>DNS_18889.log 2>DNS_18889.err &
python3 DirectoryServer.py -p 18890 --server="127.0.0.1:8888"  1>DNS_18890.log 2>DNS_18890.err &
echo "directory servers booted"

#start the storage nodes
echo "booting storage nodes"
python3 StorageNode.py -p 20001 --server="127.0.0.1:8888" -d 'SN1_storage' 1>SN_20001.log 2>SN_20001.err &
python3 StorageNode.py -p 20002 --server="127.0.0.1:8888" -d 'SN2_storage' 1>SN_20002.log 2>SN_20002.err &
python3 StorageNode.py -p 20003 --server="127.0.0.1:8888" -d 'SN3_storage' 1>SN_20003.log 2>SN_20003.err &
python3 StorageNode.py -p 20004 --server="127.0.0.1:8888" -d 'SN4_storage' 1>SN_20004.log 2>SN_20004.err &
python3 StorageNode.py -p 20005 --server="127.0.0.1:8888" -d 'SN5_storage' 1>SN_20005.log 2>SN_20005.err &
python3 StorageNode.py -p 20006 --server="127.0.0.1:8888" -d 'SN6_storage' 1>SN_20006.log 2>SN_20006.err &
python3 StorageNode.py -p 20007 --server="127.0.0.1:8888" -d 'SN7_storage' 1>SN_20007.log 2>SN_20007.err &
python3 StorageNode.py -p 20008 --server="127.0.0.1:8888" -d 'SN8_storage' 1>SN_20008.log 2>SN_20008.err &
echo "storage nodes booted"


