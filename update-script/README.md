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

<a id="tautulli-bug"></a>
I recommend you test the notification (select the `./update.py` on the "Test Notifications" tab and test it) and check the Tautulli logs to see the script's output. You may run into the following error: `ModuleNotFoundError: No module named 'dotenv'`. 

If so, you'll need to execute a few more steps:
1. Install the required modules on the `plex-managecollections/` directory (using pip, you can execute `pip3 install --target=path/to/plex-manage-collections/ -r path/to/plex-manage-collections/requirements.txt`)
2. If you the same error persists, install again specifically the not found module (I had to do it to "idna_ssl": `pip3 install --upgrade --target=path/to/plex-manage-collections/ idna_ssl`)
3. Change the `plex-manage-collections` directory's permission in order for the user running Tautulli will be able to read, write and execute files inside it (in my case, I simply ran `chmod -R 777 path/to/plex-manage-collections/` so that any user will have rwx permissons)

###### Note: The `update.py` script'll only generate and sort the collections, but no update their posters (you'll have to do it manually). If you want it to set posters everytime it runs, simply swap the script's 6th line from `for lib in libraries: os.system(f'cd ..; python3 plexmngcollections.py -l {lib["name"]} -t {lib["type"]} -g -s -y')` to `for lib in libraries: os.system(f'cd ..; python3 plexmngcollections.py -l {lib["name"]} -t {lib["type"]} -g -s -y -p')`
