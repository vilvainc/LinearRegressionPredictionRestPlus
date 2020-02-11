import requests
"""
    Test the end point with requests
    curl -X GET "http://127.0.0.1:5000/simple/" -H "accept: application/json"
    curl -X POST "http://127.0.0.1:5000/simple/predict" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"yearsofexperience\": 10.2}"
"""

def test_get():
    """
    Just to show how detailed this can get.
    Might fail if WinError 10061 in case of firewall/antivirus on windows
    :return:
    """
    from urllib3.util.retry import Retry
    from requests.adapters import HTTPAdapter

    url = 'http://127.0.0.1:5000/simple'
    s = requests.Session()
    retries = Retry(total=2,
                    backoff_factor=0.2,
                    status_forcelist=[ 500, 502, 503, 504 ])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    response = s.get(url)
    print(response.text)
    # print(response.json())

def test_post():
    """
    Just to show how simple using requests is
    :return:
    """
    url = 'http://127.0.0.1:5000/predict'
    data = {'yearsofexperience':1.8}
    response = requests.post(url, json=data)
    print(response.text)
    print(response.json())

def test_curl():
    import shlex
    import subprocess
    cmd1 = '''curl -X GET "http://127.0.0.1:5000/simple/" -H "accept: application/json"'''
    args = shlex.split(cmd1)
    process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout)

test_curl()