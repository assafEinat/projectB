import os
import requests
import time

API_KEY = '9fb34688c8e846020b3ed159c511339dff9f9be97916839b7c78a4b6d5160dea'


def get_analysis_results(analysis_id):
    url = f'https://www.virustotal.com/api/v3/analyses/{analysis_id}'
    headers = {'x-apikey': API_KEY}

    while True:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()

        if result['data']['attributes']['status'] == 'completed':
            return result
        else:
            time.sleep(10)


def scan_for_virus(directory, infected_files):
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            with open(path, 'rb') as file:
                try:
                    response = requests.post(
                        'https://www.virustotal.com/api/v3/files',
                        headers={'x-apikey': API_KEY},
                        files={'file': file}
                    )
                    response.raise_for_status()
                    result = response.json()

                    if 'data' in result and 'id' in result['data']:
                        analysis_id = result['data']['id']
                        analysis_result = get_analysis_results(analysis_id)

                        if 'data' in analysis_result and 'attributes' in analysis_result['data'] and 'stats' in \
                                analysis_result['data']['attributes']:
                            if analysis_result['data']['attributes']['stats']['malicious'] > 0:
                                infected_files.append(path)
                                print(f"Malicious file detected: {path}")
                        else:
                            print(f"Unexpected response format for file {path}: {analysis_result}")
                    else:
                        print(f"Unexpected response format for file {path}: {result}")

                except requests.exceptions.RequestException as e:
                    print(f"Error scanning file {path}: {e}")
        elif os.path.isdir(path):
            scan_for_virus(path, infected_files)


if __name__ == "__main__":
    directory = input("Enter the directory you want to start from: ")
    if os.path.isdir(directory):
        infected_files = []
        scan_for_virus(directory, infected_files)
        if not infected_files:
            print("No malicious files detected.")
        else:
            print("List of malicious files:")
            for infected_file in infected_files:
                print(infected_file)
    else:
        print(f"{directory} is not a valid directory")
