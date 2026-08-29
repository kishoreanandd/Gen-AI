import pyautogui
import time
import os
import re
import tkinter as tk
from datetime import datetime


# ============================================================
# SETTINGS
# ============================================================

WEATHER_URL = "https://www.google.com/search?q=weather+Chennai"

# Create a fixed local folder on Desktop
DESKTOP = os.path.join(
    os.path.expanduser("~"),
    "Desktop"
)

REPORT_FOLDER = os.path.join(
    DESKTOP,
    "daily_reports"
)

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)


# ============================================================
# DATE AND FILE NAMES
# ============================================================

# Generated automatically at runtime
now = datetime.now()

current_date = now.strftime("%Y-%m-%d")
current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

excel_filename = f"daily_report_{current_date}"
excel_path = f"daily_report_{current_date}.xlsx"
screenshot_filename = f"daily_report_{current_date}.png"

excel_path = os.path.join(
    REPORT_FOLDER,
    excel_path
)

screenshot_path = os.path.join(
    REPORT_FOLDER,
    screenshot_filename
)


# ============================================================
# HELPER
# ============================================================

def wait(seconds):
    time.sleep(seconds)


# ============================================================
# OPEN CHROME
# ============================================================

def open_chrome():

    print("Opening Chrome...")

    pyautogui.hotkey("win", "r")
    wait(1)

    pyautogui.write(
        "chrome",
        interval=0.05
    )

    pyautogui.press("enter")

    wait(5)


# ============================================================
# OPEN WEBSITE
# ============================================================

def open_weather():

    print("Opening weather website...")

    pyautogui.hotkey("ctrl", "l")

    pyautogui.write(
        WEATHER_URL,
        interval=0.01
    )

    pyautogui.press("enter")

    wait(7)


# ============================================================
# COPY WEBSITE DATA
# ============================================================

def copy_page_data():

    print("Copying website information...")

    pyautogui.hotkey("ctrl", "a")

    wait(1)

    pyautogui.hotkey("ctrl", "c")

    wait(2)

    root = tk.Tk()
    root.withdraw()

    try:
        text = root.clipboard_get()
    except Exception:
        text = ""

    root.destroy()

    return text


# ============================================================
# EXTRACT TEMPERATURE
# ============================================================

def extract_temperature(text):

    patterns = [
        r"(-?\d{1,3})\s*°\s*C",
        r"(-?\d{1,3})\s*°\s*F",
        r"(-?\d{1,3})\s*C",
        r"(-?\d{1,3})\s*F"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = match.group(1)

            if "F" in match.group(0).upper():
                return f"{value}°F"

            return f"{value}°C"

    return "Temperature not detected"


# ============================================================
# GET WEATHER
# ============================================================

def get_weather():

    open_chrome()

    open_weather()

    page_text = copy_page_data()

    temperature = extract_temperature(
        page_text
    )

    print()
    print("Fetched data:", temperature)
    print()

    return temperature


# ============================================================
# CREATE COMMENT
# ============================================================

def create_comment(temperature):

    try:

        number = int(
            re.search(
                r"-?\d+",
                temperature
            ).group()
        )

        if "°F" in temperature:

            celsius = (
                (number - 32) * 5 / 9
            )

        else:

            celsius = number


        if celsius <= 20:

            return "Cool weather today."

        elif celsius <= 30:

            return "Good weather for outdoor activities."

        elif celsius <= 35:

            return "Warm weather. Stay hydrated."

        else:

            return "Very hot weather. Avoid long outdoor activities."

    except Exception:

        return "Weather information recorded."


# ============================================================
# CLOSE CHROME
# ============================================================

def close_chrome():

    print("Closing Chrome...")

    pyautogui.hotkey(
        "alt",
        "f4"
    )

    wait(3)


# ============================================================
# OPEN EXCEL LOCALLY
# ============================================================

def open_excel():

    print("Opening Microsoft Excel locally...")

    pyautogui.hotkey(
        "win",
        "r"
    )

    wait(1)

    # Start Excel application directly
    pyautogui.write(
        "excel",
        interval=0.05
    )

    pyautogui.press(
        "enter"
    )

    print("Waiting for Excel...")

    wait(8)


# ============================================================
# CREATE NEW WORKBOOK
# ============================================================

def create_new_workbook():

    print("Creating new Excel workbook...")

    pyautogui.hotkey(
        "ctrl",
        "n"
    )

    wait(5)


# ============================================================
# ENTER DATA INTO EXCEL
# ============================================================

def enter_data(
    temperature,
    comment
):

    print("Entering data into Excel...")

    # Go to first cell
    pyautogui.hotkey(
        "ctrl",
        "home"
    )

    wait(1)


    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    pyautogui.write(
        "Date & Time",
        interval=0.05
    )

    pyautogui.press("tab")

    pyautogui.write(
        "Fetched Data",
        interval=0.05
    )

    pyautogui.press("tab")

    pyautogui.write(
        "Comment",
        interval=0.05
    )


    # --------------------------------------------------------
    # MOVE TO A2
    # --------------------------------------------------------

    pyautogui.press("home")

    pyautogui.press("down")


    # --------------------------------------------------------
    # DATE AND TIME
    # --------------------------------------------------------

    pyautogui.write(
        current_datetime,
        interval=0.03
    )

    pyautogui.press("tab")


    # --------------------------------------------------------
    # FETCHED DATA
    # --------------------------------------------------------

    pyautogui.write(
        temperature,
        interval=0.03
    )

    pyautogui.press("tab")


    # --------------------------------------------------------
    # COMMENT
    # --------------------------------------------------------

    pyautogui.write(
        comment,
        interval=0.03
    )

    wait(3)

    print("Data entered successfully.")


# ============================================================
# SAVE EXCEL LOCALLY
# ============================================================

def save_excel():

    print()
    print("Starting Excel Save As...")
    print()

    # --------------------------------------------------------
    # Open Save As
    # --------------------------------------------------------

    pyautogui.hotkey(
        "ctrl",
        "s"
    )

    wait(5)


    # --------------------------------------------------------
    # Windows Save As dialog
    #
    # Alt + N normally focuses File name
    # --------------------------------------------------------

    pyautogui.hotkey(
        "alt",
        "n"
    )

    wait(1)


    # Select whatever is currently in filename box
    pyautogui.hotkey(
        "ctrl",
        "a"
    )

    wait(1)


    # excel file name without extension
    pyautogui.write(
        excel_filename,
        interval=0.02
    )

    wait(2)


    # Click Save by pressing Enter
    pyautogui.press(
        "enter"
    )

    wait(6)


    # --------------------------------------------------------
    # Check if Excel asks about replacing existing file
    # --------------------------------------------------------

    if os.path.exists(excel_path):

        print()
        print("Excel file exists.")
        print("Saved successfully:")
        print(excel_path)
        print()

        return True


    # --------------------------------------------------------
    # If file does not exist, handle possible confirmation
    # --------------------------------------------------------

    print(
        "Excel file not detected yet."
    )

    wait(2)

    # Press Enter for possible format confirmation
    pyautogui.press(
        "enter"
    )

    wait(5)


    # --------------------------------------------------------
    # Verify again
    # --------------------------------------------------------

    if os.path.exists(excel_path):

        print()
        print("Excel file saved successfully.")
        print(excel_path)
        print()

        return True


    # --------------------------------------------------------
    # LAST FALLBACK
    # --------------------------------------------------------

    print(
        "First Save As attempt did not create the file."
    )

    print(
        "Trying Save As one more time..."
    )


    pyautogui.hotkey(
        "ctrl",
        "shift",
        "s"
    )

    wait(4)


    pyautogui.hotkey(
        "alt",
        "n"
    )

    wait(1)


    pyautogui.hotkey(
        "ctrl",
        "a"
    )

    pyautogui.write(
        excel_path,
        interval=0.02
    )

    wait(1)

    pyautogui.press(
        "enter"
    )

    wait(6)


    # --------------------------------------------------------
    # Final verification
    # --------------------------------------------------------

    if os.path.exists(excel_path):

        print()
        print("Excel file saved successfully.")
        print(excel_path)
        print()

        return True


    print()
    print("ERROR: Excel file could not be saved.")
    print()
    print("Expected location:")
    print(excel_path)
    print()

    return False


# ============================================================
# SCREENSHOT
# ============================================================

def take_screenshot():

    print("Taking screenshot...")

    wait(3)

    screenshot = pyautogui.screenshot()

    screenshot.save(
        screenshot_path
    )


    if os.path.exists(
        screenshot_path
    ):

        print()
        print("Screenshot saved successfully.")
        print(screenshot_path)
        print()

        return True

    else:

        print(
            "ERROR: Screenshot was not saved."
        )

        return False


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("DAILY REPORT BOT STARTED")
    print("=" * 60)

    print()
    print("Date:", current_date)
    print("Date & Time:", current_datetime)
    print()
    print("Report folder:")
    print(REPORT_FOLDER)
    print()


    # --------------------------------------------------------
    # STEP 1
    # Get data from website
    # --------------------------------------------------------

    temperature = get_weather()


    # --------------------------------------------------------
    # STEP 2
    # Create comment
    # --------------------------------------------------------

    comment = create_comment(
        temperature
    )

    print("Comment:", comment)


    # --------------------------------------------------------
    # STEP 3
    # Close Chrome
    # --------------------------------------------------------

    close_chrome()


    # --------------------------------------------------------
    # STEP 4
    # Open Excel locally
    # --------------------------------------------------------

    open_excel()


    # --------------------------------------------------------
    # STEP 5
    # Create new workbook
    # --------------------------------------------------------

    create_new_workbook()


    # --------------------------------------------------------
    # STEP 6
    # Enter data
    # --------------------------------------------------------

    enter_data(
        temperature,
        comment
    )


    # --------------------------------------------------------
    # STEP 7
    # Save Excel
    # --------------------------------------------------------

    excel_saved = save_excel()


    # --------------------------------------------------------
    # STEP 8
    # Screenshot
    # --------------------------------------------------------

    screenshot_saved = take_screenshot()


    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print()
    print("=" * 60)

    if excel_saved and screenshot_saved:

        print(
            "DAILY REPORT COMPLETED SUCCESSFULLY"
        )

    elif screenshot_saved:

        print(
            "SCREENSHOT SAVED, BUT EXCEL FILE FAILED"
        )

    elif excel_saved:

        print(
            "EXCEL FILE SAVED, BUT SCREENSHOT FAILED"
        )

    else:

        print(
            "DAILY REPORT FAILED"
        )

    print("=" * 60)

    print()
    print("Excel expected at:")
    print(excel_path)

    print()
    print("Screenshot expected at:")
    print(screenshot_path)

    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()