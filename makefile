## NOTE to the external reader:
## The google app engine SDK is *not* committed to the repo. You can find it at
## https://developers.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python
## Recommended Python version 2.7
SDK = google_appengine

APPCFG = python2 $(SDK)/appcfg.py
APPSERVER = python2 $(SDK)/dev_appserver.py

APP = app
SRC = $(APP)/src
LIB = $(APP)/lib

.PHONY: all
all:
	echo TODO make all

.PHONY: clean
clean:
	rm -f $(find $(SRC) -iname '*.pyc')

.PHONY: deps
deps:
	mkdir $(LIB)
	pip2 install Flask -t $(LIB)
	pip2 install simplejson -t $(LIB)

# Start the local App Engine server
# accessed via http://localhost:8080
.PHONY: demo
demo:
	$(APPSERVER) $(APP) 

# Return the local App Engine to a clean slate,
# i.e. wipe local database. Does not touch any
# additional downloaded resources (e.g. Council data).
.PHONY: demo-wipe
demo-wipe:
	$(APPSERVER) --clear_datastore=yes $(APP)

# Push the source tree up to App Engine
.PHONY: push
push:
	$(APPCFG) update $(APP)
