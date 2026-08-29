from playwright.sync_api import sync_playwright
from datetime import datetime
import os
import re


# ============================================================
# SETTINGS
# ============================================================

CRICBUZZ_URL = "https://www.cricbuzz.com/"

# Local folder
DESKTOP = os.path.join(
    os.path.expanduser("~"),
    "Desktop"
)

SAVE_FOLDER = os.path.join(
    DESKTOP,
    "cricbuzz_reports"
)

os.makedirs(
    SAVE_FOLDER,
    exist_ok=True
)


# ============================================================
# DATE AND FILE NAME
# ============================================================

now = datetime.now()

date_string = now.strftime("%Y-%m-%d")
time_string = now.strftime("%Y-%m-%d %H:%M:%S")

filename = f"cricbuzz_score_{date_string}.txt"

file_path = os.path.join(
    SAVE_FOLDER,
    filename
)


# ============================================================
# GET LATEST MATCH SCORE
# ============================================================

def get_latest_score(page):

    print("Opening Cricbuzz...")

    page.goto(
        CRICBUZZ_URL,
        wait_until="domcontentloaded",
        timeout=30000
    )

    print("Waiting for Cricbuzz page...")

    page.wait_for_timeout(5000)


    # --------------------------------------------------------
    # Get visible text from page
    # --------------------------------------------------------

    page_text = page.locator("body").inner_text()


    # --------------------------------------------------------
    # Extract score-like information
    #
    # Cricbuzz scores commonly look like:
    #
    # 180/5
    # 180-5
    # 180/5 (20)
    # --------------------------------------------------------

    score_patterns = [
        r"\b\d{1,3}/\d{1,2}\b",
        r"\b\d{1,3}-\d{1,2}\b"
    ]

    scores = []

    for pattern in score_patterns:

        matches = re.findall(
            pattern,
            page_text
        )

        scores.extend(matches)


    # Remove duplicates
    scores = list(
        dict.fromkeys(scores)
    )


    if not scores:

        print("Score could not be detected.")

        return "Latest score could not be detected."


    # --------------------------------------------------------
    # Take the first score found
    # --------------------------------------------------------

    latest_score = scores[0]

    print("Latest score:", latest_score)

    return latest_score


# ============================================================
# SAVE SCORE TO LOCAL TEXT FILE
# ============================================================

def save_score(score):

    print("Saving score to local text file...")

    content = f"""
CRICBUZZ DAILY SCORE REPORT
===========================

Date & Time:
{time_string}

Latest Match Score:
{score}

Source:
Cricbuzz
"""


    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)


    # Verify file exists
    if os.path.exists(file_path):

        print()
        print("SUCCESS: File saved.")
        print()
        print("File location:")
        print(file_path)
        print()

        return True

    else:

        print("ERROR: File was not saved.")

        return False


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print()
    print("=" * 60)
    print("CRICBUZZ SCORE BOT")
    print("=" * 60)
    print()


    with sync_playwright() as p:

        # ----------------------------------------------------
        # Open Chromium
        # ----------------------------------------------------

        print("Opening Chrome browser...")

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()


        # ----------------------------------------------------
        # Get score
        # ----------------------------------------------------

        score = get_latest_score(
            page
        )


        # ----------------------------------------------------
        # Save score
        # ----------------------------------------------------

        save_score(
            score
        )


        # ----------------------------------------------------
        # Keep browser open for a few seconds
        # ----------------------------------------------------

        page.wait_for_timeout(3000)


        # ----------------------------------------------------
        # Close browser
        # ----------------------------------------------------

        browser.close()


    print("=" * 60)
    print("BOT COMPLETED")
    print("=" * 60)


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":

    main()