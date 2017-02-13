# !/usr/bin/bash

# Alex Geoffrey
# Assignment 3
# Preflight.sh

#./sql/import_data.sh $1 8080


# Confirms name of database
echo "Entered DBName: " $1

# Copies files to wsgi directory
cp src/app.py ../wsgi
cp -r src/templates ../wsgi
cp src/config.py ../wsgi
cp src/lost_config.json ../wsgi

# Writes to a non-corrputed repo for commits/pushes (cwd got corrupted)
cp src/app.py ../nd/322/src
cp -r src/templates ../nd/322/src
cp src/config.py ../nd/322/src
cp src/lost_config.json ../nd/322/src
cp import_data.sh ../nd/322

# Runs Flask App
python3 ../wsgi/app.py $1



