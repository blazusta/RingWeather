# RingWeather ⏰

A Python-based CLI tool that helps users track their wake-up routines. It acts as an alarm clock and automatically fetches the day's local weather upon waking up, securely logging your daily wake-up times and environment data.

## ⭐ Features

1. **Standalone Alarm Thread**: Set your alarm without freezing the program's main interface. 
2. **Data Autosave**: Automatically logs your wake-up date, time, city, and weather (Temperature + Status) into `data/user_logs.csv` as soon as you stop the alarm.
3. **Editable Settings**: On the first run, it saves your city and ringtone preferences into `data/settings.json`. These can be easily updated anytime from the main menu.

## ⚙️ Technologies Used

* **Python**: The core engine (v3.13).
* **OOP**: Implemented for better scalability, isolation, and organization.
* **Multithreading**: Ensures the alarm waiting process don't interrupt the CLI flow.
* **JSON & CSV**: Lightweight databases for user settings and historical logs.
* **APIs**: Integrated with OpenWeatherMap for weather info fetching.
* **Modules**: 
   1. *requests*: for weather API requests. 
   2. *datetime*: to handle time and date. 
   3. *time*: to implement the sleep() function.
   4. *json* and *csv*: to save settings and logs.
   5. *threading*: to handle the alarm thread alongside program's main thread.
   6. *msvcrt*: to clear the stdin buffer.
   7. *os*: to remove any unnecessary output in the terminal,
      (*path*): to handle file paths.
   8. *sys*: to safely quit from the program.
   9. *pygame* (*mixer*): to handle program audio.

## 📥 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/blazusta/RingWeather.git
   cd RingWeather
   ```
2. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```
3. **API Key Setup**
   * Get a free API key from https://openweathermap.org/
   * Navigate to the `data/` folder.
   * Rename `api_key_example.txt` to `api_key.txt`.
   * Paste your actual API key inside it and save.
4. **Run The Program**
    ```bash
    python main.py
    ```

## 📁 Project Structure
```
RingWeather/
├── main.py                   
├── README.md                 
├── requirements.txt
├── .gitignore
│
├── modules/                 
│   ├── __init__.py           
│   ├── weather_api.py       
│   ├── storage.py            
│   └── alarm.py              
│
├── data/                     
│   ├── settings.json       
│   ├── user_logs.csv          
│   └── api_key_example.txt
│
└── assets/                   
    ├── Alarm1.mp3      
    ├── Alarm2.mp3 
    ├── Alarm3.mp3       
    ├── Alarm4.mp3 
    └── Alarm5.mp3
```