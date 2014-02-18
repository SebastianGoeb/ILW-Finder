# Finder

An interactive map to determine communities/natural neighbourhoods in Edinburgh based on citizens' perceived neighbourhoods, and demographic preferences for various social venues selected by the user.

## Dependencies

* Google App Engine ([Download SDK](https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python))

* Python 2.7 (i.e. package python2)

* pip for Python 2.7 (to install Flask)

* make

## Building

###### Install flask to local dir (requires pip)
> make deps

###### Local review ([http://localhost:8080](http://localhost:8080))
> make demo

###### Deploy to Google App Engine [http://ilw-finder.appspot.com/](http://ilw-finder.appspot.com/)
> make push

