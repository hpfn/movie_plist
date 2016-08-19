# movie_plist
Based on smoviecat (sf.net).

Put a .desktop file inside of the movie's directory - drag and drop the url from imdb site to the file manager.
Tell a directory to do the scan - like /home/user/Videos.
A html file will be generated and choose QWebView or Firefox to see it.

Basic feature untill now - 2016-08-16.

Using sqlite3.
If a directory has only a .desktop file there is no problem.
A .desktop file look like this:

[Desktop Entry]
Encoding=UTF-8
Name=Link para Money Monster (2016) - IMDb
Type=Link
URL=http://www.imdb.com/title/tt2241351/?ref_=fn_al_tt_1
Icon=text-html

Stored data in a sqlite3 - 2016-08-19

