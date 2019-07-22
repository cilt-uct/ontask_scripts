# OnTask Scripts

This repository contains 1 python scripts. 
The script does scheduled data imports from Vula to OnTask.

## Script One -  DataImport.py

This script imports data from Sakai into ontask via a CSV. The process it follows is as follows:
1. Got all containers.
2. Iterated through the containers, each has the course site ID as a container description.
3. Foreach container, get all existing data-sources.
4. Check if each of the 2 data-sources that we would like to update exist (if yes, update, if no, create).
5. Pull data from Vula, for specific site and data-source.
6. Create CSV with retrieved data.
7. Upload CSV to data-source in OnTask.

## Configuration

### Script

1. Create a file named `config.py` in the config directory.
2. Add the following:
    
        #Your domain and credentials
        ONTASK_CREDENTIALS = {
            'url': '<YOUR_URL>' #e.g. ontask.com/
            'email': '<YOUR_EMAIL>',
            'password': '<YOUR_PASSWORD>'
        }

        #Your domain and credentials
        VULA_CREDENTIALS = {
            'url': '<YOUR_URL>' #e.g. lms.com/
            'username': '<YOUR_USERNAME>',
            'password': '<YOUR_PASSWORD>'
         }
3. Create a new directory named log.
4. Create a new directory named csv.

### UI

1. Create a new container.
    1. Code can be a name of your choosing.
    2. Description has to be the site ID of the site containing data.
    
The UI process is to be automated on OnTask at a later date.    
 