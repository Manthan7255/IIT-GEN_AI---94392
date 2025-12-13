import requests
import json
import os


api_url="https://jsonplaceholder.typicode.com/posts"
output_file="output.json"

def fetch_data(api_url):
    response=requests.get(api_url)
    if response.status_code==200:
        return response.json()
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return None
    
def save_to_json(data, output_file):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {output_file}")

#save data to local json file
path=os.path.join(os.getcwd(), 'data.json')


if __name__=="__main__":
    data=fetch_data(api_url)
    if data:
        save_to_json(data, output_file)
    else:
        print("No data to save.")

    
    
        
    