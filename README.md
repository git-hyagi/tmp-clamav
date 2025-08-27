# RUNNING

* run the clamav container:
```
docker run -it --rm --name "clamav" clamav/clamav:1.4.3
```

* gather the container ip
```
docker inspect clamav -f '{{.NetworkSettings.IPAddress}}'
```

* modify the `clamd_host` in `main.py` with the container ip
```
clamd_host = '172.17.0.2'
```

* download the eicar test file from [https://www.eicar.org/download-anti-malware-testfile/](https://www.eicar.org/download-anti-malware-testfile/)
* modify the `test_file` in `main.py` with the path to eicar test file
```
test_file='/home/hyagi/Downloads/eicarcom2.zip'
```

* install the requirements and run the app
```
pip install -r requirements.txt
python main.py
```