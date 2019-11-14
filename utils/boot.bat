echo "booting DNS server"
start cmd /k python DNS.py --DSLIST="127.0.0.1:18888,127.0.0.1:18889,127.0.0.1:18890"
echo "DNS server booted"

echo "booting directory servers"
start cmd /k python DirectoryServer.py -p 18888 --server="127.0.0.1:8888"
start cmd /k python DirectoryServer.py -p 18889 --server="127.0.0.1:8888"
start cmd /k python DirectoryServer.py -p 18890 --server="127.0.0.1:8888"
echo "directory servers booted"

echo "booting storage nodes"
start cmd /k python StorageNode.py -p 20001 --server="127.0.0.1:8888" -d SN1_storage
start cmd /k python StorageNode.py -p 20002 --server="127.0.0.1:8888" -d SN2_storage
start cmd /k python StorageNode.py -p 20003 --server="127.0.0.1:8888" -d SN3_storage
start cmd /k python StorageNode.py -p 20004 --server="127.0.0.1:8888" -d SN4_storage
start cmd /k python StorageNode.py -p 20005 --server="127.0.0.1:8888" -d SN5_storage
start cmd /k python StorageNode.py -p 20006 --server="127.0.0.1:8888" -d SN6_storage
start cmd /k python StorageNode.py -p 20007 --server="127.0.0.1:8888" -d SN7_storage
start cmd /k python StorageNode.py -p 20008 --server="127.0.0.1:8888" -d SN8_storage
echo "storage nodes booted"