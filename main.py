from clamav_client import clamd
from io import BytesIO

clamd_host = '172.17.0.2'
clamd_port = 3310
clamd_client = clamd.ClamdNetworkSocket(host=clamd_host, port=clamd_port)

# The binary data to scan
binary_data = b'X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

# Create a BytesIO object (in-memory stream) from the binary data
data_stream = BytesIO(binary_data)

try:
    # Use the scan_stream method to send the data
    #result = clamd_client.scan_stream(data_stream)
    result = clamd_client.instream(data_stream)

    # The result is a dictionary with the filename as key
    if result['stream'][0] == 'OK':
        print("Scan successful, no threats found.")
    else:
        print(f"Malware found: {result['stream'][1]}")

except Exception as e:
    print(f"An error occurred: {e}")