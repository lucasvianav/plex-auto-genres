If you wish run this script every time a new media is added to server, I suggest you use \[Tautulli\](https://github.com/Tautulli/Tautulli)'s very useful [script notification agent](https://github.com/Tautulli/Tautulli-Wiki/wiki/Custom-Scripts). I've implemented an `update.py` script that you may use, but you also can implement your own, as Tautulli support many file types: `.bat, .cmd, .php, .pl, .ps1, .py, .pyw, .rb, .sh`.

The provided provided update script will simply run `python3 plexmngcollections.py -l <LIBRARY> -t <TYPE> -g -s -y` on all libraries specified. In order to use it, follow the instructions below:
1. Go to the `update-script/` directory
2. Rename `libraries.json.example` to `libraries.json`
3. Following the template, edit `libraries.json` and list all the libraries you want the script to run on, as well as it's corresponding types
4. On your Tautulli page, go to Settings > Notification Agents > Add a new notification agent > Script
5. On the "Script Folder" fuekd, select the full path to `plex-manage-collections/update-script`
6. Likewise, on the "Script File" field, select `update.py`
7. On the "Triggers" tab, select the "Recently Added" trigger
8. Set any other settings as you wish and finally hit "Save"

![Tautulli Trigger Setup (1)](/images/tautulli-trigger-1.png)
![Tautulli Trigger Setup (2)](/images/tautulli-trigger-2.png)
