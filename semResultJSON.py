import os
import requests
import json
from bs4 import BeautifulSoup
def generate_trimmed_array(prefix, start_digit, end_digit):
    # Create the initial array
    array = [f"{i:02d}" for i in range(1, 100)]  # Numbers from 01 to 99

    # Add letters A0 to Z9
    for letter in range(ord('A'), ord('Z') + 1):
        for number in range(0, 10):
            array.append(f"{chr(letter)}{number}")

    # Find indices for the start and end digits
    start_index = array.index(start_digit)
    end_index = array.index(end_digit) + 1 
    trimmed_array = array[start_index:end_index]
    modified_array = [f"{prefix}{item}" for item in trimmed_array]

    return modified_array

def fetch_and_save_results(hall_ticket_numbers, url, code, sem, output_file):
    # Load existing data from JSON file
    try:
        with open(output_file, 'r') as json_file:
            existing_data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    # Process each hall ticket number
    for htno in hall_ticket_numbers:
        if any(entry['personal_info']['HTNO'] == htno for entry in existing_data):
            print(f"{htno} is already present, skipping.")
        else:
            print(f"{htno} is not present.")
            try:
                print(f"Processing Hall Ticket Number: {htno}")
                data = {
                    'degree': 'btech',
                    'examCode': code,
                    'etype': 'r17',
                    'result': 'null',
                    'grad': 'null',
                    'type': 'intgrade',
                    'htno': htno
                }
                # Send POST request
                response = requests.post(url, data=data)
                html_content = response.text
                # Save HTML File
                file_path = f'results/html/{sem}_{htno}.html'
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(html_content)
                # Parse the HTML using BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                # Extract personal information
                personal_info_table = soup.find_all('table')[0]
                personal_info = {}
                for row in personal_info_table.find_all('tr'):
                    cols = row.find_all('td')
                    if len(cols) > 1:
                        key = cols[0].get_text(strip=True).strip(':')
                        value = cols[1].get_text(strip=True)
                        personal_info[key] = value
                        if len(cols) > 2:
                            key = cols[2].get_text(strip=True).strip(':')
                            value = cols[3].get_text(strip=True)
                            personal_info[key] = value
                personal_info['sem'] = sem
                result_data = {'personal_info': personal_info}
                # Extract subject details
                subject_table = soup.find_all('table')[1]
                subject_data = []
                for row in subject_table.find_all('tr')[1:]:  # Skip the header row
                    cols = row.find_all('td')
                    if len(cols) > 0:
                        entry = {
                            'subject_code': cols[0].get_text(strip=True),
                            'subject_name': cols[1].get_text(strip=True),
                            'internal': cols[2].get_text(strip=True),
                            'external': cols[3].get_text(strip=True),
                            'total': cols[4].get_text(strip=True),
                            'grade': cols[5].get_text(strip=True),
                            'credits': cols[6].get_text(strip=True)
                        }
                        subject_data.append(entry)
                
                result_data['subject_details'] = subject_data
                # Append the new data to existing data
                existing_data.append(result_data)
        # Save the updated data to JSON file
                with open(output_file, 'w') as json_file:
                    json.dump(existing_data, json_file, indent=4)
        
            except Exception as e:
                print(f"An error occurred with {htno}: {e}")
                continue
    
    with open(output_file, 'r') as file:
        data = json.load(file)
    sorted_data = sorted(data, key=lambda x: x['personal_info']['HTNO'])
    with open(output_file, 'w') as file:
        json.dump(sorted_data, file, indent=4)
    print(f"Data has been updated and saved to {output_file}")

# Example usage
prefix = input("Enter the prefix (e.g., '22Q91A66'): ")
start_digit = input("Enter the start digit (e.g., '01'): ")
end_digit = input("Enter the end digit (e.g., '91'): ")
code = int(input("Enter the code (e.g., 1771): "))
sem = input("Enter the semester (e.g., '2-1'): ")
# prefix = '22Q91A66'
# start_digit = '01'
# end_digit = '91'
# hall_ticket_numbers = ['23Q95A6601', '23Q95A6691']
# code = 1771
# sem = '2-1'
url = 'http://results.jntuh.ac.in/resultAction'
output_file=f"results/{prefix[2:4]}_{prefix[-2:]}_{sem}_data.json"
hall_ticket_numbers = generate_trimmed_array(prefix, start_digit, end_digit)
print(hall_ticket_numbers)
fetch_and_save_results(hall_ticket_numbers, url, code, sem, output_file)