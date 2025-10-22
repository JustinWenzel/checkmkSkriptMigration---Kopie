import requests
import json
import logging
import checkmk



#Banner
RED = '\033[0;31m'
GREEN = '\033[0;32m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
NC = '\033[0m'  # No Color

def print_banner():
    banner = f"""
{CYAN} ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███╗   ███╗██╗  ██╗{NC}
{CYAN}██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝████╗ ████║██║ ██╔╝{NC}
{CYAN}██║     ███████║█████╗  ██║     █████╔╝ ██╔████╔██║█████╔╝ {NC}
{CYAN}██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██║╚██╔╝██║██╔═██╗ {NC}
{CYAN}╚██████╗██║  ██║███████╗╚██████╗██║  ██╗██║ ╚═╝ ██║██║  ██╗{NC}
{CYAN} ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝{NC}
"""
    print(banner)

if __name__ == "__main__":
    print_banner()

#Query
def main_menu():
    while True:
        print("\nMain menu")
        print(f"{RED}__________{NC}")
        print(f"{RED}___HOST___|{NC}")
        print("1. create Host")
        print("2. delete Host")
        print("3. show Host")
        print("4. update Host")
        print(f"{RED}______________{NC}")
        print(f"{RED}___DOWNTIME___|{NC}")
        print("5. create downtime for host")
        print("6. create downtime for service")
        print("7. show downtime")
        print("8. show all downtimes")
        print(f"{RED}___________{NC}")
        print(f"{RED}0. exit___/{NC}")

        choice = input("Please select an Option: ")

        if choice == '1':
            option_1()
        elif choice == '2':
            option_2()
        elif choice == '3':
            option_3()
        elif choice == '4':
            option_4()
        elif choice == '5':
            option_5()
        elif choice == '6':
            option_6()
        elif choice == '7':
            option_7()
        elif choice == '8':
            option_8()
        elif choice == '0':
            print("Exit Program.")
            break
        else:
            print("INVALID SELECTION. TRY AGAIN")

#Option1
# Konfiguration
base_url = "https://checkmk-01.dc.gls/yasin/check_mk/api/1.0/"
username = "checkmk_admin_api_user"
password = "Z9BsRZKNQTrOd2Q*"
site_id = "yasin"


# Authentifizierung
auth = (username, password)

# Header
headers = {
    "Content-Type": "application/json"
}

def option_1():
    print("---create Host---")
    input_host_name = input("hostname: ")
    input_host_ip = input("ip-adress: ")
    input_folder_name = "~" + input(f"folder {RED}(IMPORTANT: only small letters):{NC} ")
    #input_alias = input("Alias: ")
    #input_label = input("Label: ")
    #print(f"Test: {hostname}{ip}{folder}{alias}{label}")

    global host_name
    global host_ip
    global folder_name
    host_name = input_host_name
    host_ip = input_host_ip
    folder_name = input_folder_name
    
    def add_host():
        attributes = {
            "ipaddress": host_ip,
        }

        url = f"{base_url}/domain-types/host_config/collections/all"
        payload = {
            "folder": folder_name,
            "host_name": host_name,
            "attributes": attributes
        }
        response = requests.post(url, auth=auth, headers=headers, data=json.dumps(payload), verify=False)

        if response.status_code == 200 or response.status_code == 201:
            print(f"{GREEN}Host '{host_name}' added successfully{NC}")
        else:
            print(f"{RED}ERROR while adding Host: {response.status_code} - {response.text}{NC}")

    if __name__ == "__main__":
        add_host()



def option_2():
    print("---delete Host---")
    input_host_name = input("hostname: ")

    global host_name
    host_name = input_host_name

    def delete_host():
        url = f"{base_url}/objects/host_config/{host_name}"
        response = requests.delete(url, auth=auth, headers=headers, verify=False)

        if response.status_code == 204:
            print(f"{GREEN}Host '{host_name}' deleted successfully{NC}.")
        else:
            print(f"{RED}ERROR while deleting Hosts: {response.status_code} - {response.text}{NC}")

        print(url, response)

    if __name__ == "__main__":
        delete_host()


def option_3():
    print("---show Host---")
    input_host_name = input("hostname: ")

    global host_name
    host_name = input_host_name
    
    def show_host():
        url = f"{base_url}/objects/host_config/{host_name}"
        response = requests.get(url, auth=auth, headers=headers, verify=False)

        if response.status_code == 200:
            print(f"{GREEN}Host '{host_name}' details: {NC}")
            host_data = response.json()
            print("Host:", host_data["title"])
            print("Alias:", host_data["extensions"]["attributes"].get("alias"))
            print("Folder:", host_data["extensions"].get("folder"))
            print("IP-Adress:", host_data["extensions"]["attributes"].get("ipaddress"))
            print("Labels:", host_data["extensions"]["attributes"].get("labels"))
            print("Created by:", host_data["extensions"]["attributes"]["meta_data"].get("created_by"))
            print("Created at:", host_data["extensions"]["attributes"]["meta_data"].get("created_at"))
            print("Last time updated:", host_data["extensions"]["attributes"]["meta_data"].get("updated_at"))

        else:
            print(f"{RED}ERROR while showing Hosts: {response.status_code} - {response.text}{NC}")

    if __name__ == "__main__":
        show_host()


def option_4():
    print("---update Host---")
    input_host_name = input("hostname: ")
    input_new_ipaddress = input("new ipaddress: ")
    input_new_alias = input("new alias: ")

    global host_name
    global new_ip
    global new_alias
    host_name = input_host_name
    new_ip = input_new_ipaddress
    new_alias = input_new_alias
    

    def update_host():
        url = f"{base_url}/objects/host_config/{host_name}"
        response_get = requests.get(url, auth=auth, headers=headers, verify=False)
        response_get.raise_for_status()
        etag = response_get.headers["ETag"]

        #new data
        new_host_data = {
             "attributes": {
                 "ipaddress": new_ip,
                 "alias": new_alias
             }
        }
        
        headers["If-Match"] = etag
        try:
            response = requests.put(url, auth=auth, headers=headers, data=json.dumps(new_host_data), verify=False)
            response.raise_for_status()

        except requests.exeptions.RequestException as e:
            logging.error(f"ERROR: {e}")
        except Exception as e:
            logging.error(f"ERROR: {e}")

        if response.status_code == 200:
            print(f"{GREEN}Host '{host_name}' was changed! {NC}")

        else:
            print(f"{RED}ERROR while changing '{host_name}' {response.status_code} - {response.text}{NC}")
 
    if __name__ == "__main__":
        update_host()


from datetime import datetime
import requests

def option_5():
    print("---create Downtime for Host---")
    input_host_name = input("hostname: ")
    print("Format: Y-M-DTH:M:S (e.g., 2025-10-06T14:30:00)")
    input_downtime_start = input("start: ")
    input_downtime_end = input("end: ")
    input_comment = input("comment: ")

    # Parse string inputs to datetime objects
    try:
        downtime_start = datetime.strptime(input_downtime_start, '%Y-%m-%dT%H:%M:%S')
        downtime_end = datetime.strptime(input_downtime_end, '%Y-%m-%dT%H:%M:%S')
    except ValueError as e:
        print(f"ERROR: Invalid datetime format. Use Y-M-DTH:M:S (e.g., 2025-10-06T14:30:00)")
        return

    # Convert to timezone-aware format for Checkmk
    downtime_start_str = downtime_start.strftime('%Y-%m-%dT%H:%M:%SZ')  # Changed variable name
    downtime_end_str = downtime_end.strftime('%Y-%m-%dT%H:%M:%SZ')      # Changed variable name

    downtime_host_data = {
        "host_name": input_host_name,
        "start_time": downtime_start_str,
        "end_time": downtime_end_str,
        "comment": input_comment,
        "downtime_type": "host"
    }

    url = f"{base_url}/domain-types/downtime/collections/host"
    
    try:
        response = requests.post(
            url, 
            auth=auth, 
            headers=headers, 
            json=downtime_host_data, 
            verify=False
        )

        if response.status_code in (200, 201, 204):
            print(f"✓ Successfully created downtime for Host '{input_host_name}' from {downtime_start_str} to {downtime_end_str}")
        else:
            print(f"✗ ERROR: {response.status_code} - {response.text}")
    
    except requests.RequestException as e:
        print(f"✗ Network ERROR: {e}")


def option_6():
    print("---create Downtime for Service---")
    input_host_name = input("hostname: ")
    input_service = input("service: ")
    print("y-m-dT00:00:00,00:00")
    input_downtime_start = input("start: ")
    input_downtime_end = input("end: ")
    input_comment = input("comment: ")

    global host_name
    global service
    global downtime_start
    global downtime_end
    global comment
    host_name = input_host_name
    service = input_service
    downtime_start = input_downtime_start
    downtime_end = input_downtime_end
    comment = input_comment

    def downtime_service():

        downtime_service_data = {
                "host_name": host_name,
                "start_time": downtime_start,
                "end_time": downtime_end,
                "comment": comment,
                "downtime_type": "service",
                "service_descriptions": [service]
        }

        url = f"{base_url}/domain-types/downtime/collections/service"
        response = requests.post(url, auth=auth, headers=headers, json=downtime_service_data, verify=False)

        if response.status_code == 200:
            print(f"{GREEN}Successfully created downtime for Host '{response.status_code}' from start: '{downtime_start}' to end: '{downtime_end}'{NC}")

        elif response.status_code == 204:
            print(f"{GREEN}Successfully created downtime for Host '{host_name}' from start: '{downtime_start}' to end: '{downtime_end}'{NC}")

        else:
            print(f"{RED}ERROR while creating downtime for Host '{host_name}': {response.status_code} - {response.text}{NC}")

    if __name__ == "__main__":
        downtime_service()


def option_7():
    print("---show specific downtime---")
    input_host_name = input("hostname: ")

    global host_name
    host_name = input_host_name

    def show_one_downtime():
        url = f"{base_url}/domain-types/downtime/collections/all"
        response = requests.get(url, auth=auth, headers=headers, verify=False)

        if response.status_code == 200:
            print(f"{GREEN}planned downtimes for '{host_name}': {NC}")
            downtime_data = response.json()
            data = downtime_data['value']
            filtered_data = [downtime for downtime in data if downtime['extensions']['host_name'] == host_name]
            for downtime in filtered_data:
                print(f"Host: {downtime['extensions']['host_name']}")
                print(f"start time: {downtime['extensions']['start_time']}")
                print(f"end time: {downtime['extensions']['end_time']}")
                print(f"comment: {downtime['extensions']['comment']}")
                print(f"downtime id: {downtime['id']}")
                print("-" * 40)
        else:
            print(f"{RED}ERROR while showing all downtimes: {response.status_code} - {response.text}{NC}")

    if __name__ == "__main__":
        show_one_downtime()



def option_8():
    print("---show all downtimes---")

    def show_all_downtimes():
        url = f"{base_url}/domain-types/downtime/collections/all"
        response = requests.get(url, auth=auth, headers=headers, verify=False)

        if response.status_code == 200:
            print(f"{GREEN}planned downtimes: {NC}")
            downtime_data = response.json()
            for downtime in downtime_data['value']:
                print(f"Host: {downtime['extensions']['host_name']}")
                print(f"start time: {downtime['extensions']['start_time']}")
                print(f"end time: {downtime['extensions']['end_time']}")
                print(f"comment: {downtime['extensions']['comment']}")
                print(f"downtime id: {downtime['id']}")
                print("-" * 40)
        else:
            print(f"{RED}ERROR while showing all downtimes: {response.status_code} - {response.text}{NC}")

    if __name__ == "__main__":
        show_all_downtimes()
            



if __name__ == "__main__":
    main_menu()

