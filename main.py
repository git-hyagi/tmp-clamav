import datetime
import struct

from clamav_client import clamd
from io import BytesIO

clamd_host = '172.17.0.3'
clamd_port = 3310
test_file='/home/hyagi/pulp/sample_python_clamav_test/dist/sample_python_clamav_test-0.1.0-py3-none-any.whl'

# with 100MB chunk size
max_chunk_size = 104857600 # 100MB

clamd_client = clamd.ClamdNetworkSocket(host=clamd_host, port=clamd_port)

# The binary data to scan
with open(test_file,'rb') as file:
    binary_data = file.read()

total_chunks = len(binary_data) // max_chunk_size

# Create a BytesIO object (in-memory stream) from the binary data
data_stream = BytesIO(binary_data)

chunks_count=0
print(f"Scan started: {datetime.datetime.now()}")
try:
    clamd_client._init_socket()
    clamd_client._send_command("INSTREAM")
    chunk = data_stream.read(max_chunk_size)
    while chunk:
        if chunks_count == total_chunks: # this is the last chunk
            print(f"Streaming last chunk: {datetime.datetime.now()}")
        size = struct.pack(b"!L", len(chunk))
        clamd_client.clamd_socket.send(size + chunk)
        chunk = data_stream.read(max_chunk_size)
        chunks_count+=1
    clamd_client.clamd_socket.send(struct.pack(b"!L", 0))
    result = clamd_client._recv_response()
    print(f"Scan finished: {datetime.datetime.now()}")
    if len(result) > 0:
        if result == "INSTREAM size limit exceeded. ERROR":
            print("ERROR!!!")
        filename, reason, status = clamd_client._parse_response(result)
        print({filename: (status, reason)})
    else:
        print({})
finally:
    clamd_client._close_socket()
