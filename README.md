# Labubu Bot - Automated Collectible Purchase Tool

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Proxy Support](https://img.shields.io/badge/proxy-residential-orange)

<p align="center">
<a href="https://dashboard.decodo.com/?page=residential-proxies&utm_source=socialorganic&utm_medium=social&utm_campaign=resi_trial_GITHUB"><img src="https://github.com/user-attachments/assets/60bb48bd-8dcc-48b2-82c9-a218e1e4449c"></a>
</p>

[![](https://dcbadge.vercel.app/api/server/Ja8dqKgvbZ)](https://discord.gg/Ja8dqKgvbZ)

## Introduction

The Labubu Bot is a specialized automation tool designed to help collectors secure limited-edition Labubu figures from Pop Mart during high-demand drops that sell out in seconds. 

Built with Python and Playwright, this bot automatically monitors new arrivals, schedules purchase attempts, and handles the entire buying process up to checkout - giving you a competitive edge against resellers and manual buyers in the collectible toy market.

## Features

- **Automated product monitoring**. Continuously scrapes Pop Mart's New Arrivals page for Labubu and THE MONSTERS series releases.
- **Intelligent job scheduling**. Automatically schedules purchase attempts based on official release times and dates.
- **Residential proxy integration**. Built-in proxy rotation support to avoid IP bans and bypass geo-restrictions.
- **Anti-detection mechanisms**. Handles CAPTCHAs, pop-ups, and mimics human browsing behavior to evade bot detection.
- **Retry logic & error handling**. Robust error recovery with configurable retry attempts and delay intervals.

## Installation
### Prerequisites
- [Python 3.8+](https://www.python.org/downloads/release/python-380/)
- [Chrome](https://www.google.com/chrome/) or [Firefox](https://www.firefox.com/en-US/) browser
- [Playwright](https://playwright.dev/)
- [APScheduler](https://pypi.org/project/APScheduler/)

### Step-by-step setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/labubu-bot.git
cd labubu-bot
```

2. **Install dependencies**
```bash
pip install playwright apscheduler
python -m playwright install
```

3. **Configure proxy settings**
Edit the proxy credentials in both `popmart-scraper.py` and `purchase-bot.py`:
```python
PROXY_SERVER = "http://us.decodo.com:10001"
PROXY_USERNAME = "your_username"
PROXY_PASSWORD = "your_password"
```

## Usage examples

### Basic CLI usage
Launch the complete automation system:
```bash
python main.py
```

### Programmatic uzage
Run individual components:
```python
# Run the web scraper manually
python popmart-scraper.py

# Process scheduled jobs
python job-scheduler.py

# Execute purchase bot for specific URL
python purchase-bot.py "https://www.popmart.com/us/products/product-name"
```

### Sample output
The scraper generates a `data/products.json` file with upcoming releases:
```json
[
  {
    "title": "Labubu THE MONSTERS Series",
    "release_date": "Upcoming JUL 25",
    "release_time": "21:00",
    "url": "https://www.popmart.com/us/products/labubu-the-monsters-series"
  }
]
```

## Project structure

```
popmart-bot/
├── data/
│   └── products.json          # Scraped product data and release schedules
├── main.py                    # Main entry point and daily scheduler
├── popmart-scraper.py         # Web scraper for New Arrivals page
├── job-scheduler.py           # Automated job scheduling system
├── purchase-bot.py            # Purchase automation and cart management
└── README.md                  # Project documentation
```

## Configuration

### Proxy settings
For optimal performance, configure residential proxies in both scraper files.
Replace `PROXY_SERVER`, `PROXY_USERNAME`, and `PROXY_PASSWORD` with your credentials from the Decodo [dashboard](https://dashboard.decodo.com/).

### Scheduling options
Modify timing in `main.py`:
```python
HOUR = 6      # Daily scraper run hour (24h format)
MINUTE = 0    # Daily scraper run minute
```

### Target keywords
Customize product filtering in `popmart-scraper.py`:
```python
TARGET_KEYWORDS = ["THE MONSTERS", "Labubu", "Add product name"]
```

## Best practices

- **Use unique proxies**. Assign different residential IPs to each browser session.
- **Test before major drops**. Run the bot on regular products to verify functionality.  
- **Multiple payment methods**. Have backup payment options configured in Pop Mart accounts.
- **Check release patterns**. Pop Mart typically drops between 7-10 PM PT on weekdays.

## Documentation links

For advanced proxy configuration and troubleshooting:
- [Proxy setup guide](https://help.decodo.com/docs/residential-proxy-quick-start)
- [Proxy code integration]([docs/api-reference.md](https://help.decodo.com/docs/code-integration))

## License

This project is licensed under the [MIT License](https://github.com/Decodo/Decodo/blob/master/LICENSE).

## Related projects & resources

🔗 **Explore More Automation Tools:**
- [Google Maps scraper](https://github.com/Decodo/google-maps-scraper)
- [Google Lens scraper](https://github.com/Decodo/google-lens-scraper)
- [Reddit scraper](https://github.com/Decodo/reddit-python-scraper)
