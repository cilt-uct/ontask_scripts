# Ontask Scripts

This repository contains 1 python scripts. 
The script does scheduled data imports from Vula to OnTask.

## Script One -  DataImport.py

This script imports data from Sakai into ontask via a CSV.

## Configuration

1. Create a file named `config.py`.
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
