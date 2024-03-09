# avcx-scraper

This is a scraper which will download all AVCX crosswords from the website.

**Note: You must be an active subscriber to AVCX.**

## Usage

1. [Install `pipenv`](https://pipenv.pypa.io/en/latest/installation.html) if it's not already installed. For Arch:
```
sudo pacman -Sy python-pipenv
```
2. Clone the `avcx-scraper` repository:
```
git clone --depth=1 https://github.com/mesmere/avcx-scraper.git
cd avcx-scraper
```
3. Run `avcx-scraper` with your AVCX credentials:
```
pipenv run python3 avcx_scraper.py --email=YOUR_EMAIL --password=YOUR_PASSWORD
```
4. Wait for it to complete and then check the `out/` directory to find your files.

## FAQ

**Q. Why am I only getting .puz files?**

**A.** `avcx-scraper` only downloads files in the AcrossLite format because that's all I care about. Some puzzles (e.g. the trivias) don't have .puz files, so they won't be downloaded. If you want a full backup of everything, it would be trivial to modify the code. 🤷‍♀️ Seriously, it's one line.

**Q. Why are the filenames in this awful scheme that doesn't sort cleanly?**

**A.** Those are the filenames chosen by AVCX themselves via the Content-Disposition header. 

**Q. Will my account be banned for downloading like a thousand files at once?**

**A.** I don't know, maybe. `avcx-scraper` uses very reasonable timeouts and tries to look as much as possible like a normal user, but if anyone is ever looking through the logs it's pretty obvious.
