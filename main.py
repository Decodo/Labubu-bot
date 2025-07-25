import subprocess
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta

# Maximum number of retries for scraper
MAX_RETRIES = 5
RETRY_DELAY = 10

# Scheduled time for daily scraper run
HOUR = 6
MINUTE = 0
scheduler = BlockingScheduler()

def run_daily_scraper():
    # This function runs the popmart-scraper.py script and schedules job-scheduler.py to run shortly after.
    print(f"\nRunning popmart-scraper at {datetime.now().strftime('%H:%M:%S')}")
    for attempt in range(1, MAX_RETRIES + 1):
        print(f"Attempt {attempt} to run scraper...")

        try:
            subprocess.run(["python3", "popmart-scraper.py"], check=True)
            print("New arrival scraper launched successfully.")
            
            # Schedule job-scheduler to run shortly after
            run_time = datetime.now() + timedelta(seconds=5)
            scheduler.add_job(run_job_scheduler, trigger='date', run_date=run_time)
            print(f"The job-scheduler.py will run at {run_time.strftime('%H:%M:%S')}")
            return  # Exit early on success

        except subprocess.CalledProcessError as e:
            print(f"Scraper failed (attempt {attempt}) with exit code {e.returncode}")
            if attempt < MAX_RETRIES:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)

    print("All attempts to run the scraper failed. Check popmart-scraper.py for issues.")

def run_job_scheduler():
    print(f"\nRunning job-scheduler.py")
    try:
        subprocess.run(["python3", "job-scheduler.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Job scheduler failed with exit code {e.returncode}")
        print("Please check job-scheduler.py for issues.")

if __name__ == "__main__":
    print("main.py started...")
    run_daily_scraper()  # run once immediately on startup

    # Schedule scraper to run daily at configured time
    scheduler.add_job(run_daily_scraper, 'cron', hour=HOUR, minute=MINUTE)
    print(f"Daily scraper has been scheduled to run at {HOUR:02d}:{MINUTE:02d} every day.")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped.")