# Alex Geoffrey
# CIS 322
# export_data.sh

# Made directory if it doesn't exist
mkdir $2

# Call function to generate all CSV files
python3 export_assets.py $1

# Move all CSV files to the destination directory
mv users.csv $2
mv facilities.csv $2
mv assets.csv $2
mv transfers.csv $2




