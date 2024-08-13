def generate_trimmed_array(prefix, start_digit, end_digit):
    # Create the initial array
    array = [f"{i:02d}" for i in range(1, 100)]  # Numbers from 01 to 99

    # Add letters A0 to Z9
    for letter in range(ord('A'), ord('Z') + 1):
        for number in range(0, 10):
            array.append(f"{chr(letter)}{number}")

    # Find indices for the start and end digits
    start_index = array.index(start_digit)
    end_index = array.index(end_digit) + 1  # Slice is exclusive of end index

    # Trim the array
    trimmed_array = array[start_index:end_index]

    # Prepend '22Q91A66' to each element
    modified_array = [f"{prefix}{item}" for item in trimmed_array]

    return modified_array

import requests
import json
from bs4 import BeautifulSoup

def fetch_and_save_results(hall_ticket_numbers, url, code, sem, output_file):
    # Load existing data from JSON file
    try:
        with open(output_file, 'r') as json_file:
            existing_data = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    # Process each hall ticket number
    for htno in hall_ticket_numbers:
        try:
            print(f"Processing Hall Ticket Number: {htno}")
            
            # Data to be sent with the POST request
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
        # Handle the exception (optional)
            print(f"An error occurred with {htno}: {e}")
            # Continue with the next iteration
            continue
    
    
    print(f"Data has been updated and saved to {output_file}")

# Example usage
prefix = '22Q91A66'
start_digit = '01'
end_digit = '91'
# modified_array = generate_trimmed_array(prefix, start_digit, end_digit)
# Example usage
# hall_ticket_numbers = ['23Q95A6608', '23Q95A6615']  # Add your list of hall ticket numbers here
url = 'http://results.jntuh.ac.in/resultAction'  # Replace with the actual URL
code = 1771
sem = '2-1'
output_file=f"results/{prefix[2:4]}_{prefix[-2:]}_{sem}_data.json"
hall_ticket_numbers = generate_trimmed_array(prefix, start_digit, end_digit)  # Add your list of hall ticket numbers here
print(hall_ticket_numbers)
fetch_and_save_results(hall_ticket_numbers, url, code, sem, output_file)