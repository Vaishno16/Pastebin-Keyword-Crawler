
# Pastebin Crypto Keyword Monitor

## Overview

This Python script monitors recent pastes on [Pastebin](https://pastebin.com) for content related to cryptocurrency and blockchain by scanning for a predefined list of keywords. When matching pastes are found, it logs the details into a JSON Lines (`.jsonl`) file for further analysis or alerting.

I have add mostly keywords related to the crypto.

---

## Features

- Scrapes the Pastebin archive page to fetch recent paste IDs.
- Retrieves raw content of each paste.
- Searches for a comprehensive list of cryptocurrency-related keywords in the paste content.
- Saves matched paste details including the paste ID, URL, keywords found, and timestamp to an output JSONL file.
- Handles network errors gracefully with retries.
- Respects polite scraping practices by adding delays between requests.
- Stops monitoring after a defined number of retries with no new matches.

---

## Requirements

- Python 3.6 or higher
- Dependencies:
  - `requests`
  - `beautifulsoup4`

Install dependencies using pip:

```bash
pip install requests beautifulsoup4
```

---

## Configuration

### Constants

- `ARCHIVE_URL`: URL to Pastebin's archive page.
- `RAW_URL`: URL template to access raw paste content, requires paste ID.
- `KEYWORDS`: List of cryptocurrency-related keywords to scan for in paste content.
- `OUTPUT_FILE`: File name for storing matched paste data in JSON Lines format.
- `HEADERS`: HTTP headers used for requests to mimic a browser user-agent.
- `MAX_RETRIES`: Maximum consecutive attempts to fetch pastes without matches before stopping.

---

## Usage

Run the script directly:

```bash
python pastebin_crypto_monitor.py
```

### What happens:

1. The script scrapes the Pastebin archive page to get a list of recent paste IDs.
2. For each new paste ID not previously checked, it fetches the raw paste content.
3. It scans the paste text for any of the keywords in the list.
4. If any keywords are found, it appends a JSON record describing the match to `keyword_matches.jsonl`.
5. The script continues to monitor until it hits `MAX_RETRIES` consecutive cycles with no new matches.
6. Each cycle waits 2 seconds between paste requests and 5 seconds or 10 seconds between retries to avoid overloading Pastebin.

---

## Output File Format

The output file `keyword_matches.jsonl` contains one JSON object per line, for example:

```json
{
	"source": "pastebin", 
	"context": "Found crypto content in paste sMFJhQyW", 
	"paste_id": "sMFJhQyW", 
	"url": "https://pastebin.com/raw/sMFJhQyW", 
	"discovered_at": "2025-05-21T15:38:12.057559Z", 
	"keywords_found": ["ICO"], 
	"status": "pending"
}

{
	"source": "pastebin", 
	"context": "Found crypto content in paste zFyjWFEu", 
	"paste_id": "zFyjWFEu", 
	"url": "https://pastebin.com/raw/zFyjWFEu", 
	"discovered_at": "2025-05-21T15:39:01.725214Z", 
	"keywords_found": ["DEX"], 
	"status": "pending"
}

```
Pastebin Keyword Crawler (Crypto / t.me).ipynb
---

## Code Structure

- `get_recent_pastes(limit=100)`: Fetches recent paste IDs from the archive page.
- `get_paste_content(paste_id)`: Fetches raw paste text by paste ID.
- `find_keywords(text)`: Returns a list of matched keywords found in the paste text.
- `save_result(paste_id, keywords)`: Saves matched paste data in the output file.
- `monitor()`: Main loop controlling the monitoring process, handling retries and delays.

---
