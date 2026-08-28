"""
RingWeather
A CLI program that sets an alarm, and upon waking up, 
logs the time and current weather status.
"""

# -----------------------------------------------------------------

# Imported modules
from modules import weather_api as wapi
from modules import alarm
from modules import storage
import threading, os, sys, time, msvcrt
from dotenv import load_dotenv
# -----------------------------------------------------------------
 
# Searches for the .env file and injects
# its key-value pairs into the temporary process environment.
load_dotenv() 

# Retrieves the environment variable's value, 
# returns None if the key is not found.
api_key = os.getenv("WEATHER_API_KEY") 

if not api_key:
    print("Error: API Key not found!")
    input("\nEnter anything to continue... ")
    sys.exit()

# -----------------------------------------------------------------

# Initializing main program objects (Global Objects)
weather = wapi.Weather(api_key)
user_alarm = alarm.Alarm("") 
user_data = storage.Storage("data/user_logs.csv", "data/settings.json")

# -----------------------------------------------------------------

def exit_program():
    print("\n[OK]: Program ended successfully!\n")
    sys.exit()


def menu():
    print("""
Available Options:
[1]: Set Alarm
[2]: Stop Alarm
[3]: Cancel Alarm
[4]: Change Ringtone
[5]: Change City
[6]: Show Settings
[7]: Show Data
[8]: Exit
""")


def weather_handling():
    """Calls the weather object to fetch coordinates and data, returning a list of temp and status."""

    while True:
        try:
            valid_city = weather.get_coordinates(weather.city_name)

            if valid_city:
                result = weather.get_weather()
                if result:
                    print(f"Temperature    : {result[0]} °C")
                    print(f"Weather Status : {result[1]}")
                    return [result[0], result[1]]
            return None
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.\n")
            sys.exit()

def select_ringtone():
    """Allows the user to preview and change ringtones."""
    ringtones = {
        # Key: Ringtone(Name, File_Path)
        "1": ("[AUDIO] -> Alarm1", "assets/Alarm1.mp3"),
        "2": ("[AUDIO] -> Alarm2", "assets/Alarm2.mp3"),
        "3": ("[AUDIO] -> Alarm3", "assets/Alarm3.mp3"),
        "4": ("[AUDIO] -> Alarm4", "assets/Alarm4.mp3"),
        "5": ("[AUDIO] -> Alarm5", "assets/Alarm5.mp3"),
    }

    while True:
        print()
        for key, value in ringtones.items():
            print(f"[{key}] : {value[0]}")

        choice = input("\nEnter 1-5 to select a ringtone: ")
        if choice not in ['1', '2', '3', '4', '5']:
            print("[ERROR]: Invalid option\n")
        else:
            while True:
                # Test the audio before confirming
                user_alarm.ringtone_path = ringtones.get(choice)[1]
                user_alarm.play_alarm()

                confirmation = input("Do you like this ringtone? (y/N): ").upper()
                if confirmation not in ['Y', 'N']:
                    print("[ERROR]: You may only enter Y/N\n")
                elif confirmation == 'N':
                    user_alarm.stop_alarm()
                    print()
                    break    # Return to select another ringtone
                else:
                    user_alarm.stop_alarm()
                    print(f"\n[OK]: Ringtone: {ringtones.get(choice)[0]} added successfully.")
                    user_data.save_settings(ringtones.get(choice)[1])
                    return ringtones.get(choice)[1]
                

def alarm_worker(hrs, min):
    """This function runs in the background (separate thread). It waits for the time and plays the audio."""
    success = user_alarm.set_alarm(hrs, min)

    # success = True means the time has come and the alarm wasn't cancelled
    if success:
        print()
        print('*' * 24)
        print("[ALARM]: WAKE UP... It's time!")
        print('*' * 24)
        print("Press [2] to stop the alarm.")
        print("Choose an option: ", end='', flush=True)
        user_alarm.play_alarm(rep=-1)
        

def create_alarm():
    """Gets the time from the user and starts the waiting thread."""
    # Check the lock to prevent overlapping alarms
    if user_alarm.is_active:
        print("[WARN]: An alarm is already active! Please stop or cancel it first.")
        return
    
    # Check if the user has already logged data today to prevent duplicates
    current_settings = user_data.load_settings()                
    if current_settings.get("Last Logged Date") == user_alarm.get_date():
        print("[WARN]: You have already logged your data for today!")
        return
    
    while True:
        try:
            set_hours = int(input("Set the hours: "))
        except ValueError:
            print("[ERROR]: You may only enter numbers\n")
            continue
        
        if not (0 <= set_hours <= 23):
            print("[ERROR]: Invalid value\n")
        else:
            while True:
                try:
                    set_minutes = int(input("Set the minutes: "))
                except ValueError:
                    print("[ERROR]: You may only enter numbers\n")
                    continue

                if not (0 <= set_minutes <= 59):
                    print("[ERROR]: Invalid value\n")
                else:
                    print(f"\n[OK]: Alarm has been set: {set_hours:02}:{set_minutes:02}")
                    user_alarm.is_active = True

                    # Create a worker thread so the program doesn't freeze while waiting
                    worker = threading.Thread(target=alarm_worker, args=(set_hours, set_minutes))
                    worker.daemon = True    # If the user closes the program, this thread dies instantly
                    worker.start()

                    return (set_hours, set_minutes)


def set_first_settings():
    """Called only once for new users to initialize the program settings."""
    while True:
        try:
            city = input("Enter your city: ").title()
            if not city:
                print("[ERROR]: you did not enter anything.")
            elif not city.replace(" ", "").isalpha():
                print("[ERROR]: city name must contain only alphabetical letters.")
            else:
                ringtone = select_ringtone()
                weather.city_name = city
                user_data.save_settings(ringtone, city)
                print("\n[OK]: Data saved successfully.")
                return [ringtone, city]
        except KeyboardInterrupt:
            exit_program()


def change_city():
    while True:
        try:
            city = input("Enter your city: ").title()
            if not city:
                print("[ERROR]: you did not enter anything.")
            elif not city.replace(" ", "").isalpha():
                print("[ERROR]: city name must contain only alphabetical letters.")
            else:
                weather.city_name = city
                user_data.save_settings(city=city)
                print("\n[OK]: City updated successfully.")
                break
        except KeyboardInterrupt:
            exit_program()


def show_settings():
    print(f"Ringtone : {user_alarm.ringtone_path[7:13]}")
    print(f"City     : {weather.city_name}")


# Dispatch Table
options = {
    '1': create_alarm,
    '2': user_alarm.stop_alarm,
    '3': user_alarm.cancel_alarm,
    '4': select_ringtone,
    '5': change_city,
    '6': show_settings,
    '7': user_data.show_data,
    '8': exit_program
}

# -----------------------------------------------------------------

settings = user_data.load_settings()

if not settings:
    # New user
    print()
    print('*' * 45)
    print("Welcome! Let's set up your Morning Assistant.")
    print('*' * 45)
    new_ringtone, new_city = set_first_settings()

    user_alarm.ringtone_path = new_ringtone
    weather.city_name = new_city

    input("\nEnter anything to continue... ")
else:
    # Returning user, load their data into the objects
    user_alarm.ringtone_path = settings.get("Favorite Ringtone")
    weather.city_name = settings.get("Current City")

# Initialize this variable outside the loop to avoid NameError
wake_time = None

while True:
    # os.name == 'nt' (new technology) it refers to the the name of Windows core
    # else (Example: os.name == posix) it refers to the name of Mac/Linux core
    # 'cls' will be executed if the os is Windows
    # 'clear' will be executed if the os is Mac/Linux
    # this line is used to clear the Terminal regularly to keep the program clean
    os.system('cls' if os.name == 'nt' else 'clear')
    menu()
    try:
        # Clean the stdin buffer from user random clicks (msvcrt is exclusive for Windows)
        if os.name == 'nt': 
            while msvcrt.kbhit(): msvcrt.getch()
        option = input("Choose an option: ")
        if option in ['1', '2', '3', '4', '5', '6', '7', '8']:
            # Execute the chosen function and save its return value in 'output'
            output = options[option]()
            match option:
                case '1': 
                    # If an alarm was set successfully, save the time
                    if output:
                        wake_time = f"{output[0]:02}:{output[1]:02}"
                case '2': 
                    # wake_time: Ensure the user actually set an alarm
                    # output: Ensure the alarm was actually ringing and stopped
                    if wake_time and output:
                        current_settings = user_data.load_settings()
                        
                        # Log data only if it hasn't been logged today
                        if not current_settings.get("Last Logged Date") == user_alarm.get_date():
                            weather_data = weather_handling()
                            if weather_data:
                                user_data.save_logs(user_alarm.get_date(), wake_time, weather.city_name, weather_data)
                                user_data.save_settings(alarm_date=user_alarm.get_date())
                                print("\n[OK]: Data logged successfully.")

        if option in ['6', '7'] or (option == '2' and wake_time and output):
            input("\nEnter anything to continue... ")
        elif option in ['1', '3', '4', '5'] or (option == '2'):
            time.sleep(5)
        else:
            print("[ERROR]: Invalid option.")
            time.sleep(3)
            
    except KeyboardInterrupt:
        exit_program()