import struct
from clamav_client import clamd
from io import BytesIO

clamd_host = '172.17.0.2'
clamd_port = 3310
test_file='/home/hyagi/Downloads/eicarcom2.zip'


clamd_client = clamd.ClamdNetworkSocket(host=clamd_host, port=clamd_port)

# The binary data to scan
#binary_data = b'X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'
with open(test_file,'rb') as file:
    binary_data = file.read()

# Create a BytesIO object (in-memory stream) from the binary data
data_stream = BytesIO(binary_data)

try:
    clamd_client._init_socket()
    clamd_client._send_command("INSTREAM")
    max_chunk_size = 100
    chunk = data_stream.read(max_chunk_size)
    while chunk:
        size = struct.pack(b"!L", len(chunk))
        clamd_client.clamd_socket.send(size + chunk)
        chunk = data_stream.read(max_chunk_size)
    clamd_client.clamd_socket.send(struct.pack(b"!L", 0))
    result = clamd_client._recv_response()
    if len(result) > 0:
        if result == "INSTREAM size limit exceeded. ERROR":
            print("ERROR!!!")
        filename, reason, status = clamd_client._parse_response(result)
        print({filename: (status, reason)})
    else:
        print({})
finally:
    clamd_client._close_socket()
