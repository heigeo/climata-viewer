#!/bin/sh

# Exit on error
set -e

# Save climata version and REST config to AMD modules
cd db
CLIMATA_VERSION=`python -c "from climata.version import VERSION; print VERSION"`;
CONFIG=`./manage.py db_config`;
cd ../
echo "define(function(){return '$CLIMATA_VERSION';});" > app/js/data/climata_version.js
echo "define($CONFIG);" > app/js/data/config.js

# Build javascript with wq.app
cd app;
wq build $1;

# Force important files through any unwanted server caching
cd ../;
sed -i "s/climata_viewer.js/climata_viewer.js?v="$1"/" htdocs-build/climata_viewer.appcache
sed -i "s/climata_viewer.css/climata_viewer.css?v="$1"/" htdocs-build/climata_viewer.appcache

# Preserve Django's static files (e.g. admin)
if [ -d htdocs/static ]; then
    cp -a htdocs/static htdocs-build/static
fi;

# Replace existing htdocs with new version
rm -rf htdocs/;
mv -i htdocs-build/ htdocs;

# Restart Django
touch db/climata_viewer/wsgi.py
