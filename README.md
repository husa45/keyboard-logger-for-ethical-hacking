# keyboard logger for ethical hacking


## ⚠️ Intended use: This project is provided FOR AUTHORIZED SECURITY TESTING, RESEARCH, AND EDUCATIONAL PURPOSES ONLY. Do NOT use this tool on any device, network, or account without explicit written authorization from the owner. By using this software you confirm you have such authorization. The author disclaims all liability for misuse or damage resulting from this software.


<br/>
**This is a keylogger that is used to log all key strokes on the target , plus capturing everything  copied to the clipboard .**<br/>

### Installation : 
First : clone the repository to the intended destination<br/>
```
git clone https://github.com/husa45/keyboard-logger-for-ethical-hacking 
```
<br/>
Then download the dependencies by typing :
<br/>

```
pip3 install -r requirements.txt
```

## Linux support :
Now , if you are in a linux machine ,then this key logger supports key logging and clipboard capture , with the ability to clean the clipboard every time it is captured , to avoid recapturing previuosly captured stuff. <br/>


If you want to use the script in  an editor , make sure to press 'esc'
when you finish , as this is the way to break out of the key logger thread.

This tool will automatically log the results to a file in the current working directory ,unless specified elsewhere .

Also , after the script is finished , the log will be sent automatically to your email (**From the log file path that you specified in the keylogging scipt**)

For this tool to function as  it is intended , it should be used as an infinit running cronjob , 
or preferably as a daemon(Systemd unit).

To do that ,first , create a unit by typing the following :
```
sudo nano /etc/systemd/system/key_logger.service
```
Then copy the contents of keylogger.service provided in the repository files to the newly created systemd file 

‼️ **Important note** : you should change the DISPLAY environment variable , to whatever your current DISPLAY environment variable is ,
type : ```echo $DISPLAY```
then change the **Environment=DISPLAY=:1** line to whatever value you got.

**If the environment variable DISPLAY isnt set correctly , pynput wont be able to connect to the display manager and the script wont run**.<br/><br/>

**you should also change the variable ExecStart as guided inside the file ( here you specify the path of python interpreter + the path of the tool script).**<br/>


finally ,type the following :
```
systemctl daemon-reload
systemctl start keylogger.service
```
Check if the unit is running :
```
systemctl status keylogger.service
```

**And now the tool is running in the background ,and captures everything typed by the keyboard or copied to the clipboard ,and then sent to the email that you want**

❕**Note :** the systemd daemon file was written so that whenever the script finsihes (by typing esc or any other forcing reason) , it will be restarted automatically . 

👀 **Future updates :adding support for windows**.
