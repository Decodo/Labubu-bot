import json
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import os
import time

DATA_FILE = os.path.join("data", "products.json")
MAX_RETRIES = 5
RETRY_DELAY = 10

def parse_release_datetime(date_str, time_str):
    # Convert strings like "Upcoming JUL 11" and "09:00" into a datetime object. Assumes the current year.
    try:
        # Remove unwanted keywords
        for keyword in ["Upcoming", "In Stock"]:
            date_str = date_str.replace(keyword, "").strip()
        
        full_date_str = f"{date_str} {datetime.now().year} {time_str}"
        # Example: "JUL 11 2025 09:00"
        return datetime.strptime(full_date_str, "%b %d %Y %H:%M")
    except Exception as e:
        print(f"Failed to parse datetime from '{date_str} {time_str}': {e}")
        return None

def launch_purchase_bot(product):
    # Launch purchase-bot.py with retry logic
    url = product.get("url")
    title = product.get("title")
    
    for attempt in range(MAX_RETRIES + 1):  # +1 for initial attempt
        print(f"Launching purchase bot for '{title}' (attempt {attempt + 1}/{MAX_RETRIES + 1}) at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Run the purchase bot and wait for it to complete
            result = subprocess.run(
                ["python3", "purchase-bot.py", url],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                print(f"✅ Purchase bot succeeded for '{title}' on attempt {attempt + 1}")
                return  # Success - exit the retry loop
            else:
                print(f"Purchase bot failed for '{title}' on attempt {attempt + 1}")
                print(f"Return code: {result.returncode}")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"⏰ Purchase bot timed out for '{title}' on attempt {attempt + 1}")
        except Exception as e:
            print(f"💥 Exception running purchase bot for '{title}' on attempt {attempt + 1}: {e}")
        
        # If this wasn't the last attempt, wait before retrying
        if attempt < MAX_RETRIES:
            print(f"⏳ Waiting {RETRY_DELAY} seconds before retry...")
            time.sleep(RETRY_DELAY)
    
    print(f"All {MAX_RETRIES + 1} attempts failed for '{title}'.")

def schedule_all_jobs_from_json(json_path):
    scheduler = BackgroundScheduler()
    job_count = 0

    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    for product in products:
        run_time = parse_release_datetime(product["release_date"], product["release_time"])
        if not run_time:
            continue
        if run_time < datetime.now():
            continue
        
        scheduler.add_job(launch_purchase_bot, "date", run_date=run_time, args=[product])
        print(f"🧸 Scheduled '{product['title']}' for {run_time}")
        job_count += 1

    if job_count == 0:
        print("No upcoming valid jobs found in JSON. Nothing scheduled.")
        return

    scheduler.start()
    print("Scheduler started. Jobs will run at their scheduled times.")

    try:
        # Keep the scheduler alive
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped.")

if __name__ == "__main__":
    schedule_all_jobs_from_json(DATA_FILE)