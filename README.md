# timeTrackerAutoFiller

dependencies
selenium
chrome driver: https://chromedriver.chromium.org/downloads
keyring: https://stackoverflow.com/questions/7014953/i-need-to-securely-store-a-username-and-password-in-python-what-are-my-options


To Fix:
DeprecationWarning: executable_path has been deprecated, please pass in a Service object
https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python

```
crontab -e
25 11 * * 1-5 export DISPLAY=:0 && /usr/bin/python <pathToCode>/timeTrackerAutoFiller/src/logger.py >> output.log 2>&1
```
