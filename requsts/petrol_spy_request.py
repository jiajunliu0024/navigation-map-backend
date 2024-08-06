import requests

from services.fetch_station_service import update_petrol_and_petrol_station_data


def fetch(params):
    # Define the URL
    url = "https://petrolspy.com.au/webservice-1/station/box"

    # Make the GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Get JSON data
        data = response.json()
        # Print the JSON data
        print(f"Failed to retrieve data: {data}")
        return data
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None


def init_param(line):
    param_line = line.split("?")[1]
    param_list = param_line.split("&")
    param_dict = {}
    for param in param_list:
        key, value = param.split("=")
        param_dict[key] = value
    return param_dict




def read_local_spy_petrol_file():
    # read the hub file to fetch the data
    try:
        # Open the file in read mode
        with open('./petrol_spy.txt', 'r') as file:
            # Read the entire content of the file
            for line in file:
                if line.__contains__("/webservice-1/station/box"):
                    param = init_param(line)
                    petro_spy_json = fetch(param)
                    update_petrol_and_petrol_station_data(petro_spy_json)

    except FileNotFoundError:
        print("The file was not found.")
