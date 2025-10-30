from datetime import timezone
import json
import requests
from flask import abort


class CheckmkClient:  
    def __init__(self, base_url, username, password, verify_ssl=True, timeout_s=10):
        self.base_url = base_url.strip("/")
        self.auth = (username, password)
        self.verify_ssl = verify_ssl
        self.timeout_s = timeout_s
        self.headers = {"Content-Type": "application/json"}

    def add_host(self, host_name, ip_address, folder_name):
        url = f"{self.base_url}/domain-types/host_config/collections/all"
        host_name = host_name.strip()
        ip_address = ip_address.strip()
        folder_name = folder_name.strip().lower()

        payload = {
            "folder": "~" if not folder_name else f"~{folder_name}",
            "host_name": host_name,
            "attributes": {"ipaddress": ip_address},
        }

        try:
            resp = requests.post(
                url,
                auth=self.auth,
                headers=self.headers,
                data=json.dumps(payload),
                verify=self.verify_ssl,
                timeout=self.timeout_s,
            )
        except requests.Timeout:
            abort(504)
        except requests.RequestException:
            abort(503)

        if resp.status_code >= 200 and resp.status_code <= 299:
            return

        abort(resp.status_code)

    def delete_host(self, host_name):
        host_name = host_name.strip()
        url = f"{self.base_url}/objects/host_config/{host_name}"

        try:
            resp = requests.delete(
                url,
                auth=self.auth,
                headers=self.headers,
                verify=self.verify_ssl,
                timeout=self.timeout_s,
            )
        except requests.Timeout:
            abort(504)
        except requests.RequestException:
            abort(503)

        if resp.status_code >= 200 and resp.status_code <= 299:
            return

        abort(resp.status_code)

    def show_host(self, host_name):
        host_name = host_name.strip()
        url = f"{self.base_url}/objects/host_config/{host_name}"

        try:
            resp = requests.get(
                url,
                auth=self.auth,
                headers=self.headers,
                verify=self.verify_ssl,
                timeout=self.timeout_s,
            )
        except requests.Timeout:
            abort(504)
        except requests.RequestException:
            abort(503)

        if resp.status_code >= 200 and resp.status_code <= 299:
            return resp.json()

        abort(resp.status_code)

    def update_host(self, host_name, new_ip, new_alias):
        host_name = host_name.strip()
        new_ip = new_ip.strip()
        new_alias = new_alias.strip()
        url = f"{self.base_url}/objects/host_config/{host_name}"

        try:
            resp = requests.get(
                url,
                auth=self.auth,
                headers=self.headers,
                verify=self.verify_ssl,
                timeout=self.timeout_s,
            )
        except requests.Timeout:
            abort(504)
        except requests.RequestException:
            abort(503)

        if not (resp.status_code >= 200 and resp.status_code <= 299):
            abort(resp.status_code)

        etag = resp.headers.get("ETag")
        if not etag:
            abort(412)

        payload = {
            "attributes": {
                "ipaddress": new_ip,
                "alias": new_alias,
            }
        }

        headers = dict(self.headers)
        headers["If-Match"] = etag

        try:
            resp = requests.put(
                url,
                auth=self.auth,
                headers=headers,
                data=json.dumps(payload),
                verify=self.verify_ssl,
                timeout=self.timeout_s,
            )
        except requests.Timeout:
            abort(504)
        except requests.RequestException:
            abort(503)

        if resp.status_code >= 200 and resp.status_code <= 299:
            return

        abort(resp.status_code)


    def create_downtime_host(self, host_name, downtime_start, downtime_end, comment):
        host_name = host_name.strip()
        downtime_start = f'{downtime_start.strip()}Z'
        downtime_end = f'{downtime_end.strip()}Z'   
        url = f"{self.base_url}/domain-types/downtime/collections/host"

        downtime_host_data = {
            "host_name": host_name,
            "start_time": downtime_start,
            "end_time": downtime_end,
            "comment": comment,
            "downtime_type": "host"
        }

        try:
            resp = requests.post(
                url,
                auth=self.auth,
                headers=self.headers,
                json=downtime_host_data,
                verify=self.verify_ssl,
                timeout=self.timeout_s,
            )
        except requests.Timeout:
            abort(504)
        except requests.RequestException:
            abort(503)

        if resp.status_code >= 200 and resp.status_code <= 299:
            return

        abort(resp.status_code)


    def create_downtime_service(self, host_name, service, downtime_start, downtime_end, comment):
        host_name = host_name.strip()
        service = service.strip()
        downtime_start = downtime_start.strip()
        downtime_end = downtime_end.strip()
        url = f"{self.base_url}/domain-types/downtime/collections/service"

        downtime_service_data = {
                "host_name": host_name,
                "start_time": downtime_start,
                "end_time": downtime_end,
                "comment": comment,
                "downtime_type": "service",
                "service_descriptions": [service]
        }

        try:
            resp = requests.post(
                url,
                auth=self.auth,
                headers=self.headers,
                json=downtime_service_data,
                verify=self.verify_ssl,
                timeout=self.timeout_s,
            )
        except requests.Timeout:
            abort(504)
        except requests.RequestException:
            abort(503)

        if resp.status_code >= 200 and resp.status_code <=299:
            return
        
        abort(resp.status_code)


    def acknowledge_problem_service(self, host_name, service, expire_date, comment):
        url = f"{self.base_url}/domain-types/acknowledge/collections/service"
        
        host_name = host_name.strip()
        service = service.strip()
        expire_date = expire_date.strip()
        expire_date = f"{expire_date}Z"

        acknowledge_data = {
            "comment": comment,
            "expire_on": expire_date,
            "acknowledge_type": "service",
            "host_name": host_name,
            "service_description": service,
        }

        try:
            resp = requests.post(
                url,
                auth=self.auth,
                headers=self.headers,
                json=acknowledge_data,
                verify=self.verify_ssl,
                timeout=self.timeout_s,
            )
        except requests.Timeout:
            abort(504)
        except requests.RequestException:
            abort(503)

        if resp.status_code >= 200 and resp.status_code <= 299:
            return
        abort(resp.status_code)



    def get_one_downtime(self, host_name):
        url = f"{self.base_url}/domain-types/downtime/collections/all"
        
        try:
            resp = requests.get(url, auth=self.auth, headers=self.headers, verify=self.verify_ssl)
        except requests.Timeout:
            abort(504)
        except requests.RequestException:
            abort(503)

        if resp.status_code >= 200 and resp.status_code <=299:
            downtime_data = resp.json()
            data = downtime_data['value']
            return [downtime for downtime in data if downtime['extensions']['host_name'] == host_name]
        
        abort(resp.status_code)



    def get_all_downtimes(self):
        url = f"{self.base_url}/domain-types/downtime/collections/all"
        
        try:
            resp = requests.get(url, auth=self.auth, headers=self.headers, verify=self.verify_ssl)
        except requests.Timeout:
            abort(504)
        except requests.RequestException:
            abort(503)

        if resp.status_code >= 200 and resp.status_code <=299:
            return resp.json()

        abort(resp.status_code)        



    def get_current_problems(self, is_netops=None):
        url = f"{self.base_url}/domain-types/service/collections/all"

        service_query = {
            "op": "and",
            "expr": [
                {
                    "op": "or",
                    "expr": [
                        {"op": "=", "left": "state", "right": "1"},  
                        {"op": "=", "left": "state", "right": "2"}   
                    ]
                },
                {"op": "=", "left": "acknowledged", "right": "0"},
                {"op": "=", "left": "scheduled_downtime_depth", "right": "0"},
                {"op": "=", "left": "host_scheduled_downtime_depth", "right": "0"},
                {"op": "=", "left": "host_state", "right": "0"}
            ]
        }
        
        service_columns = [
            "host_name",
            "host_state",
            "description",
            "state",
            "state_type",
            "acknowledged",
            "scheduled_downtime_depth",
            "host_scheduled_downtime_depth",
            "plugin_output",
            "last_check"
        ]
        
        
        if is_netops == True or is_netops == False:
            service_columns.append("host_labels")

        params = {
            "columns": service_columns,
            "query": json.dumps(service_query)
        }

        headers = {
            "Accept": "application/json"
        }

        try:
            resp = requests.get(
                url, 
                params=params, 
                headers=headers, 
                auth=self.auth, 
                verify=self.verify_ssl,
                timeout=self.timeout_s
            )
        except requests.Timeout:
            abort(504)
        except requests.RequestException:
            abort(503)
        
        
        if resp.status_code >= 200 and resp.status_code <= 299:
            result = resp.json()  
            
            
            if is_netops == True and "value" in result:
                result["value"] = [
                    service for service in result["value"]
                    if service.get("extensions", {}).get("host_labels", {}).get("permission") == "netops"
                ]
            elif is_netops == False and 'value' in result:
                result["value"] = [
                    service for service in result["value"]
                    if service.get("extensions", {}).get("host_labels", {}).get("permission") != "netops"
                ]
            return result
        
        
        abort(resp.status_code)


        
