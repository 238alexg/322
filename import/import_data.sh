# Alex Geoffrey
# CIS 322
# import_data.sh

# Download the testable export file
curl https://classes.cs.uoregon.edu//17W/cis322/files/lost_data.tar.gz

# Unpack files to /lost_data
tar -xvzf legacy_data.tar.gz

# Run import script
python3 imports.py $1 /lost_data

# Destroy data
#rm -R lost_data

