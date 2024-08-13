
# Student Result Fetcher

This project consists of a script that fetches student results from the JNTUH results portal, processes the data, and stores it in a JSON file. It also includes a web interface to upload and view the JSON data, along with options to calculate and sort CGPA.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages: `requests`, `json`
- Basic HTML knowledge for web interface

### Fetching Student Information

1. **Input Details:**
   The script prompts the user to input several pieces of information:
   - **Prefix**: A prefix that is part of the Hall Ticket Number.
   - **Start Digit**: The starting digit of the range for Hall Ticket Numbers.
   - **End Digit**: The ending digit of the range for Hall Ticket Numbers.
   - **Code**: The code used for fetching results.
        - **R22 2-1**: 1771
        - **R22 1-2**: 1704
        - **R22 1-1**: 1662

   - **Semester**: The semester for which the results are being fetched.

2. **Generate Hall Ticket Numbers:**
   Using the provided prefix and digit range, the script generates a list of Hall Ticket Numbers.

3. **Fetch and Save Results:**
   The script sends requests to the results portal and retrieves the results. It then saves the data into a JSON file with a dynamically created filename based on the prefix and semester.

### `sgpaUploadJSON.html`

The `sgpaUploadJSON.html` file provides a web interface to upload the JSON file containing student results. It includes features for viewing CGPA and sorting the data as needed.

**Features:**
- **Upload JSON**: Allows users to upload the results JSON file.
- **View CGPA**: Displays CGPA information for the students.
- **Sort Data**: Provides options to sort the results based on different criteria.

### Usage

1. **Run the Python Script:**
   Execute the Python script to generate the JSON file containing student results.

   ```bash
   python semResultJSON.py
   ```

2. **Open the HTML File:**
   Open `sgpaUploadJSON.html` in a web browser.

3. **Upload the JSON File:**
   Use the upload feature in the HTML file to select and upload the JSON file generated by the Python script.

4. **View and Sort Data:**
   Once uploaded, the web interface will display the results. You can view CGPA and use the sorting options to organize the data as required.

### Contributing

Feel free to submit issues and pull requests to enhance the functionality of this project.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
