import requests
import urllib3
import os
from dotenv import load_dotenv

load_dotenv()

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

NAS_URL = os.getenv("NAS_URL")
NAS_USERNAME = os.getenv("NAS_USERNAME")
NAS_PASSWORD = os.getenv("NAS_PASSWORD")

session = requests.Session()

def get_sid():  
    params = {
        "api": "SYNO.API.Auth",
        "version": "2",
        "method": "login",
        "account": NAS_USERNAME,
        "passwd": NAS_PASSWORD,
        "session": "DownloadStation",
        "format": "sid"
    }

    response = session.get(
        f"{NAS_URL}/webapi/auth.cgi",
        params=params,
        verify=False
    )

    sid = response.json()["data"]["sid"]
    return sid



def download_torrent(magnet):
    sid = get_sid()
    params = {
        "api": "SYNO.DownloadStation.Task",
        "version": "1",
        "method": "create",
        "uri": magnet,
        "destination": "video/Movies",
        "_sid": sid
    }

    response = session.get(
        f"{NAS_URL}/webapi/DownloadStation/task.cgi",
        params=params,
        verify=False
    )
    return response.json()["success"]



def get_download():
    sid = get_sid()

    params = {
        "api": "SYNO.DownloadStation.Task",
        "version": "1",
        "method": "list",
        "additional": "transfer",
        "_sid": sid
    }

    response = session.get(
        f"{NAS_URL}/webapi/DownloadStation/task.cgi",
        params=params,
        verify=False
    )
    data = response.json()["data"]["tasks"]
    return data





def format_downloads():
    tasks = get_download()

    downloads = []
    for task in tasks:
        transfer = task["additional"]["transfer"]

        size = task["size"]
        downloaded = transfer["size_downloaded"]

        progress = 0

        if size > 0:
            progress = downloaded / size * 100

        
        downloads.append(
            {
                "id":task["id"],
                "title": task["title"],
                "status": task["status"],
                "size": size,
                "downloaded": downloaded,
                "speed": transfer["speed_download"],
                "progress": progress
            }
        )

    return downloads

def pause_download(task_id):
    sid = get_sid()
    params = {
        "api": "SYNO.DownloadStation.Task",
        "version": "1",
        "method": "pause",
        "id": task_id,
        "_sid": sid
    }

    response = requests.get(
        f"{NAS_URL}/webapi/DownloadStation/task.cgi",
        params=params,
        verify=False
    )

    return response.json()


def change_download(task_id, status):
    sid = get_sid()
    print(task_id, status)
    if status == "downloading":
        params = {
            "api": "SYNO.DownloadStation.Task",
            "version": "1",
            "method": "pause",
            "id": task_id,
            "_sid": sid
        }

        response = requests.get(
            f"{NAS_URL}/webapi/DownloadStation/task.cgi",
            params=params,
            verify=False
        )

        return response.json()
    elif status == "paused":
        params = {
            "api": "SYNO.DownloadStation.Task",
            "version": "1",
            "method": "resume",
            "id": task_id,
            "_sid": sid
        }

        response = requests.get(
            f"{NAS_URL}/webapi/DownloadStation/task.cgi",
            params=params,
            verify=False
        )

        return response.json()  

    elif status == "finished":
        params = {
            "api": "SYNO.DownloadStation.Task",
            "version": "1",
            "method": "delete",
            "id": task_id,
            "_sid": sid
        }

        response = requests.get(
            f"{NAS_URL}/webapi/DownloadStation/task.cgi",
            params=params,
            verify=False
        )

        return response.json()

#pause_result = pause_download("dbid_34")
#print(pause_download)