# Plex Manage Collections

Plex Manage Collections is a simple script that will add genre collection tags to your media making it much easier to search for genre specific content.

1. [Requirements](#requirements)
2. [Compatible Setups](#compatible)
3. [Optional Features](#optional)
4. [Getting Started](#getting_started)
5. [Credits](#credits)
6. [Auto-Run Whenever New Media Are Added](#tautulli)
7. [Troubleshooting](#troubleshooting)
8. [Docker Usage](#docker_usage)

###### Movies example (with cover art set using --set-posters flag)
![Movie Collections](/images/movies.png)

###### Anime example
![Anime Collections](/images/animes.png)

## Requirements
1. Python 3
3. Python dependencies listed in `requirements.txt` (if you have pip, simply do `pip install -r requirements.txt`).
3. [TMDB Api Key](https://developers.themoviedb.org/3/getting-started/introduction) (Only required for non-anime media)

## <a id="compatible"></a>Compatible Setups

For either setup, proper titles for your media are necessary. This makes it easier to find the media (see https://support.plex.tv/articles/naming-and-organizing-your-tv-show-files/).

### Standard media and anime are separated
1. Anime shows and movies are in their own library on your plex server. **_(Anime shows and movies can share the same library)_**
2. Standard TV Shows are in their own library on your plex server.
3. Standard Movies are in their own library on your plex server.

In this setup, the script'll simply create genres collections for your media in each library (also with anime-specific genres for the anime libraries).

###### Note: this setup works well with [ZeroQI](https://github.com/ZeroQI)'s [Absolute Series Scanner (ASS)](https://github.com/ZeroQI/Absolute-Series-Scanner) and [Hama.bundle agent](https://github.com/ZeroQI/Hama.bundle).

### Standard media and anime are mixed
1. Anime and standard TV shows share their own library on your plex server.
2. Anime and standard movies share their own library on your plex server.

In this setup, the script'll create three types of collections:
* Type of media: "Non-Anime" and "Anime" collections
* Standard genres: contain only standard media
* Anime genres: contain only anime and the collections' names are preceded by "\[A\]"

## <a id="optional"></a>Optional Features
### Set posters
You may set poster arts to your collections like the ones in sample-posters/ (inspired by reddit's [/u/alexnyc1998](https://www.reddit.com/user/alexnyc1998)).

If you wish to use the provided arts, simply rename `sample-posters/` to `posters/`.

If you would like to create your own posters matching the provided style, you can use the template.psd file to create your own (requires Photoshop). When setting up your own poster, organize them in a posters/ directory like the provided ones are in the sample-posters/.

The directories must match the media type (movies, shows, anime). There can be also a directory titled "general", for the "Anime" and "Non-Anime" collections (see the **Standard media and anime are mixed** setup option). The posters' names must match the collections' names without any prefix (either PLEX_COLLECTION_PREFIX or the "\[A\]" for anime genres). The names must be completely lowercase and any spaces in it must be replaced by dashes (-).

Examples:
* If you have PLEX_COLLECTION_PREFIX="\*", your "Science Fiction" collection in Plex would be named "\*Science Fiction" and your art poster should be titled "science-fiction.png";
* Likewise, if you have a mixed-media library, your anime genre "Seinen" collection in Plex would be named "\[A] Seinen" and your art poster should be titled "seinen.png" and placed in the "posters/anime/" directory;

### Sort collections
This feature is only available to mixed-media libraries (see the **Standard media and anime are mixed** setup option).

It'll edit the generated collections' title sort in a way that the "type of media" collections will be at the top and all of the anime genres' collections will be at the bottom.
* Non-Anime's title sort --> "01"
* Anime's title sort --> "02"
* \[A\] \*'s title sort --> "zzzzzz\<ORIGINAL GENRE NAME\>"
    
*e.g.*: \[A\] Sci-Fi's title sort will be set to "zzzzzzSci-Fi".

## <a id="getting_started"></a>Getting Started 
1. Read the **Requirements** and **Compatible Setups** sections above
2. Rename the `.env.example` file to `.env`
3 Edit the `.env` file and set your plex username, password, and server name or plex base url and auth token. If you are generating collections for standard media, you'll also need to set your [TMDB Api Key](https://developers.themoviedb.org/3/getting-started/introduction).

    |Variable|Authentication method|Value|
    |---|---|---|
    |PLEX_USERNAME|Username and password|Your Plex Username|
    |PLEX_PASSWORD|Username and password|Your Plex Password|
    |PLEX_SERVER_NAME|Username and password|Your Plex Server Name|
    |PLEX_BASE_URL|Token|Your Plex Server base URL|
    |PLEX_TOKEN|Token|Your Plex Token|
    |PLEX_COLLECTION_PREFIX||(Optional) Prefix for the created Plex collections. For example, with a value of "\*", a collection named "Adventure", the name would instead be "*Adventure".<br><br>Default value : ""|
    |TMDB_API_KEY||Your TMDB api key (not required for anime library tagging)|

##You are now ready to run the script
```
usage: plexmngcollections.py [-h] [-l LIBRARY]
                             [-t {anime,standard-movies,standard-shows,mixed-movies,mixed-shows}]
                             [-p] [-g] [-s] [-n] [-y] [-f]

Adds collection genre tags to your Plex media as well as helps you manage it.

optional arguments:
  -h, --help            show this help message and exit
  
  -l, --library LIBRARY
                        The exact name of the Plex library to generate genre
                        collections for.
                        
  -t, --type {anime,standard-movies,standard-shows,mixed-movies,mixed-shows}
                        The type of media contained in the library. Mixed
                        libraries contain both standard media and anime ('Non-
                        Anime' and 'Anime' collections will be generated and
                        anime's genre collections will be preceded by '[A]').
                        
  -p, --set-posters     Uploads posters located in posters/$media-type - media-
                        type {anime, movies, shows}. Supports .PNG
                        
  -g, --generate-collections
                        Generate genre collections for the selected media.
                        
  -s, --sort            Only applies to mixed libraries. Updates the
                        collections' sorting titles so that 'Non-Anime' and
                        'Anime' will be the first collections and the anime
                        genres' collections will be the last.
                        
  -n, --nono, -d, --dry
                        Do not modify plex collections (debugging feature).
                        
  -y, --yes             Do not prompt.
  
  -f, --force           Force proccess on all media (independently of proggress
                        recorded in logs/).

examples: 
python3 plexmngcollections.py -l "Anime Movies" -t anime --generate-collections
python3 plexmngcollections.py -l "Anime Shows" -t anime --generate-collections --set-posters
python3 plexmngcollections.py -l Movies -t standard-movies --generate-collections --set-posters
python3 plexmngcollections.py -l "TV Shows" -t standard-shows --set-posters

python3 plexmngcollections.py -l Movies -t mixed-movies --generate-collections --set-posters --sort
python3 plexmngcollections.py -l "TV Shows" -t mixed-shows --generate-collections --set-posters --sort
```

![Example Usage](/images/example-usage.gif)

## <a id="tautulli"></a>Auto-Run Whenever New Media Are Added


## <a id="credits"></a>Credits
This script is a fork from [ShaneIsrael](https://github.com/ShaneIsrael)'s [Plex Auto Genres](https://github.com/ShaneIsrael/plex-auto-genres), which works great for the **Standard media and anime are separated** setup option. I've only done some cleanup/modularization and made it compatible with the **Standard media and anime are mixed** setup option (as it is the one I use) and the Tautulli trigger.

## <a id="troubleshooting"></a>Troubleshooting
1. If you are not seeing any new collections or updates in posters and sorting, try to realod your Plex client or to close it and re-open it.
2. Delete the generated `logs/plex-*-successful.txt`  and `logs/plex-*-failures.txt` files if you want the script to generate collections from scratch. You may want to do this if you delete your collections and need them re-created. Another option is to use the `-f, --force` flag.
3. Having the release year in the title of a tv show or movie can cause the lookup to fail in some instances. For example `Battlestar Galactica (2003)` will fail, but `Battlestar Galactica` will not.

## <a id="docker_usage"></a>Docker Usage
Unfortunately, this fork isn't available to run this via a Docker Container, but the original script is, see [fdarveau](https://github.com/fdarveau) [Plex Auto Genres Docker](https://github.com/fdarveau/plex-auto-genres-docker).
