# Capsim Forecaster

## Overview
This project started as a personal challenge to learn basic webscraping. Previously, I have used basic bs4, however, this project is entirely in Selenium due to its convenient `.click()` navigational functions.

## License & Restrictions
Under `LICENSE.txt` is the current license of this project (GNU Affero General Public License v3.0). This program requires an active Capstone account as well as a current simulation.

## Aside
If you like this project, a star would be greatly appreciated! If you experience any issues with the program, please create a post under the `Issues` tab on the repository page, and write with as much detail as possible.

## Cheating
At the time of this program's creation, its use does not constitute cheating in accordance with the UIUC BUS 201 FA24 course syllabus. However, what constitutes cheating may vary by university, college, course, semester, and professor. **I am not responsible for any accusations or charges of cheating; users of this program are at their own discretion for the ethics of its use.**

## Directions For Use:
### Programming Environment Set Up:
Many of the directions in this step (particularly *Python*, *Pip*, and *Development Environment*) are standard/vital in ny programming workflow.

#### Python
Visit https://wiki.python.org/moin/BeginnersGuide/Download for Python installation instructions.

#### Pip
Pip should come preinstalled with Python. In the case that it is not, run
```
python get-pip.py
```
in your computer's terminal.

#### Libraries
The required libraries are mentioned in `requirements.txt`. Regardless, the directions for each of their installations are the following. Run each of these lines separately in your computer's terminal:
```
pip install pandas
pip install selenium
```

#### Development Environment
You can use any development environment of your choice. I recommend Spyder, with its useful UI that is naturally conducive to this program. Visit https://docs.spyder-ide.org/current/installation.html for Spyder installation instructions.

### Chrome Driver & Browser Path
Upon running the program for the first time, you should be prompted to input your Chrome driver path as well as your browser path. The directions to find both of these are the following.

#### Chrome Driver Path
Visit https://googlechromelabs.github.io/chrome-for-testing/ for the appropriate installation for your OS system. Copy the appropriate URL under the `Stable` table. Ensure `Platform` matches your OS and `Binary` matches "chromedriver". Paste the URL in a new tab to download the driver. Locate the compressed file you downloaded in your file explorer. 'Unzip' it (if on macOS, double click it) and open the new folder. Right click the file, `chromedriver` (or `chromedriver.exe` on Windows), and copy the pathname (if on macOS, right click and, while holding `option` on your keyboard, click `Copy "chromedriver" as Pathname`). Enter this into the program when prompted to do so.

#### Browser Path
Locate your typically used browser in your file explorer. Right click the file (should named similarly to `Chrome.app`, or `Safari.app`, if on macOS), and copy the pathname (if on macOS, right click and, while holding `option` on your keyboard, click `Copy "____" as Pathname`). Enter this into the program when prompted to do so.

### Running the Script
The script does not start on its own. You must run it first by clicking in the script text and press `shift`+`return`. (If you are using Spyder, prompts will appear in the bottom right.)

### "Enter step wait time (sec; >1)"
This is the amount of time in units seconds that the program waits for between navigation steps. Only when locating the appropriate 'round' button and when opening the Courier Report will the wait time be different. For slower systems and/or internet connections, a wait time of at least 3 is recommended. For faster systems and/or internet connections, a wait time of at least 1 is recommended.
