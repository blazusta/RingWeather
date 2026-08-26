import json, csv, os

class Storage:
    """
    Handles saving/retrieving user settings (JSON) and logging wake-up times 
    and weather data (CSV).
    """

    def __init__(self, csv_path:str, json_path:str):
        self.csv_path = csv_path
        self.json_path = json_path


    def save_settings(self, favorite_ringtone=None, city=None, alarm_date=None):
        """
        Performs a Partial Update of the settings.
        Reads the old file first, and only updates the passed values to avoid 
        overwriting other data.
        """

        current_settings = self.load_settings()

        if favorite_ringtone is not None:
            current_settings["Favorite Ringtone"] = favorite_ringtone

        if city is not None:
            current_settings["Current City"] = city

        if alarm_date is not None:
            current_settings["Last Logged Date"] = alarm_date

        with open(file=self.json_path, mode='w') as file:
            json.dump(current_settings, file, indent=4)
        
        return (favorite_ringtone, city, alarm_date)


    def save_logs(self, date, wake_time, city, weather:list):
        """Logs data into a CSV file. Appends headers only if the file is empty or newly created."""
        
        headers = ["Date", "Waking Time", "City", "Temperature", "Weather Status"]
        logs = [date, wake_time, city, weather[0], weather[1]]

        has_headers = True

        # Check the file size. If it's 0 bytes (empty) or doesn't exist, we need to write the headers
        if not os.path.exists(self.csv_path) or os.path.getsize(self.csv_path) == 0:
            has_headers = False

        with open(file=self.csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not has_headers:
                writer.writerow(headers)
            writer.writerow(logs)

        return True
    

    def load_settings(self) -> dict:
        """Reads user settings. Fully protected against empty or corrupted files."""
        
        try:
            with open(file=self.json_path, mode='r') as file:
                # If the file exists but is completely empty, return an empty dict to avoid JSONDecodeError
                if os.path.getsize(self.json_path) == 0:
                    return {}
                else:
                    settings = json.load(file)
        except FileNotFoundError:
            # If load_settings returns an empty dict
            # It means the user has not set their settings / preferences yet
            # So, the program will ask them to enter their city / ringtone
            return {}
        
        except json.JSONDecodeError:
            # File exists but data is corrupted or doesn't follow JSON format
            print(f"[ERROR]: {self.json_path} is corrupted.")
            return {}
        
        return settings
    

    def show_data(self):
        """Prints the content of the CSV file as a simple table in the Terminal."""
        try:
            with open(file=self.csv_path, mode='r', newline='') as file:

                if os.path.getsize(self.csv_path) == 0:
                    print("[WARN]: No data.")
                else:
                    content = csv.reader(file)
                    for row in content:
                        for index in range(len(row)):
                            print(f"| {row[index]:<15}", end="")
                        print(" |")

        except FileNotFoundError:
            print("[WARN]: No data.")