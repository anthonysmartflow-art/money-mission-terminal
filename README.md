💰 Money Mission — Mac Menu Bar App

A lightweight goal tracker that lives in your Mac menu bar. Built by @a.j.does_stuff — not a developer, just someone who had an idea and built it.

Set your goal, track what you make, and see your progress every time you look at your screen.


What It Does


Lives in your Mac menu bar showing 💰 and the % of your money goal (your current progress)
Click it to see your full dashboard — total earned, daily pace, days left, projected finish
Add revenue entries in seconds
Saves everything locally so nothing resets on restart
Updates instantly every time you add money



What You Need


A Mac
Python 3 — download at python.org


Setup — Follow These Steps Exactly

STEP 1 — Download Python

Go to python.org, hit Download, and install it like any normal Mac app.


STEP 2 — Download the file

Download money_mission.py from this page. Click the file, then click the download button in the top right corner.


STEP 3 — Edit your goal

Open money_mission.py in any text editor (TextEdit works fine). At the very top of the file you will see:

pythonGOAL = 25000
GOAL_DATE = date(2026, 12, 31)
START_DATE = date(2026, 1, 1)

Change these three lines to match your own goal:


GOAL — your target amount in dollars
GOAL_DATE — the date you want to hit it by (year, month, day)
START_DATE — the date you started working toward this goal


Save the file.


STEP 4 — Open Terminal

Press ⌘ Space, type Terminal, hit Enter.


STEP 5 — Install rumps

Paste this into Terminal and hit Enter:

pip3 install rumps

Rumps is what allows the app to live in your Mac menu bar. This command downloads it automatically. Wait for it to finish before moving on.


STEP 6 — Move the file to your scripts folder

Paste these two commands into Terminal one at a time:

mkdir -p ~/scripts

mv ~/Downloads/money_mission.py ~/scripts/

The first command creates a dedicated folder to store your app. The second moves the file there. This matters because your Downloads folder is not permanent — files get cleaned out. Your scripts folder keeps everything in one safe place so the app never breaks.


STEP 7 — Run it

Paste this into Terminal and hit Enter:

python3 ~/scripts/money_mission.py

You will see 💰 0% appear in your menu bar. Click it to see your dashboard.


STEP 8 — Make it start automatically every time you restart your Mac

Paste this entire block into Terminal at once and hit Enter:

cat > ~/Library/LaunchAgents/com.moneymission.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.moneymission</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Library/Frameworks/Python.framework/Versions/3.14/bin/python3</string>
        <string>/Users/YOUR_MAC_USERNAME/scripts/money_mission.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF
launchctl load ~/Library/LaunchAgents/com.moneymission.plist

Important: Replace YOUR_MAC_USERNAME with your actual Mac username before running this. Your username is the name you see at the top of Terminal (e.g. anthonyrosenberger).

Restart your Mac and 💰 will appear automatically every time — no Terminal needed.


How to Use It


Click 💰 in your menu bar to open your dashboard
Click ➕ Add Revenue to log money you made
Type the amount and what it was for — it saves instantly
Your percentage and stats update in real time



Built With


Python 3
rumps — open source library for Mac menu bar apps
Claude AI — used to help write and build the code



Questions

Drop a comment on the video or follow @a.j.does_stuff for more.
