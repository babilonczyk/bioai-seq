# Helpers

This directory contains helpers - scripts I have used to create datasets used later on in the project and may need to be reused in the future to update them.

## convert_xml_to_db

Script that converts the xml swissprot dataset into sqllite database. The intention behind it was to not use the uniprot api and make the tool free of 3rd party apis. Since the dataset was free and MIT I have converted it into sqllite3 database and hosted it on huggingface gradio free tier space.

Last time conversion took 7:28min
