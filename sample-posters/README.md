You may set poster arts to your collections like the ones in sample-posters/ (inspired by reddit's [/u/alexnyc1998](https://www.reddit.com/user/alexnyc1998)).

If you wish to use the provided arts, simply rename `sample-posters/` to `posters/`.

If you would like to create your own posters matching the provided style, you can use the template.psd file to create your own (requires Photoshop). When setting up your own poster, organize them in a posters/ directory like the provided ones are in the sample-posters/.

The directories must match the media type (movies, shows, anime). There can be also a directory named 'general', for the 'Anime' and 'Non-Anime' collections (see the **Standard media and anime are mixed** setup option). The posters' names must match the collections' names without any prefix (either PLEX_COLLECTION_PREFIX or the '\[A\] for anime genres). The names must be completely lowercase and any spaces in it must be replaced by dashes (-).

Examples:
* If you have PLEX_COLLECTION_PREFIX="\*", your "Science Fiction" collection in Plex would be named "\*Science Fiction" and your art poster should be titled "science-fiction.png";
* Likewise, if you have a mixed media library, your anime genre "Seinen" collection in Plex would be named "\[A] Seinen" and your art poster should be titled "seinen.png" and placed in the "posters/anime/" directory;
