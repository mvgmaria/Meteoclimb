METEOCLIMB PROJECT

Folders: 
- Main: Meteoclimb
    - regions_csv (separate csv files of the regions, and combined ones)
- Virtual env.: .climbproject


Files
- Meteoclimb:
    - get_region_crag_names.py // gets the regions names and puts it in a csv (will be used in the following scritps)
    - get_crags_simpler_onebyone.py // gets crags urls
    - get_coordinates.py // gets coordinates and names (from previous urls)
    - combined_crag_csv.py // combines existing csv files 
    

## Setup Instructions
1. Clone the repository:
   git clone https://github.com/username/myproject.git

2. Install the required libraries:

    pip install -r requirements.txt

## Virtual env. activation

1. Navigate to the meteoclimb folder

    cd METEOCLIMB

2. .\.climbproject\Scripts\Activate

## Update files from Github

1. git status

2. If there are uncommitted changes:

    git add .
    git commit -m "Describe your changes here"

3. Pull changes from Github and merges them to the local repository:

    git pull origin main
