Summary
=======

This is a script that should quickly determine what users may have authorized potentially malicious Google API clients. This was written in response to the latest [Google Docs Phishing Attack](https://www.theverge.com/2017/5/3/15534768/google-docs-phishing-attack-share-this-document-with-you-spam). 

Given the malicious client ID, and some credentials, this scripts go through Gsuite's Admin Reports and lists all authorizations to it.

Usage
-----

Before you can use this script, you will need to create a [service account with GSuite domain delegation enabled](https://developers.google.com/admin-sdk/reports/v1/guides/delegation). Once you have created 
the service account and granted appropriate permissions, generate and download the key in JSON format.

To run the script, you will also need to be a GSuite Admin, or know someone who is.

The script takes the following arguments, in order:
`service_account_file`
`google_admin_email`
`client_id` (of the malicious client)
`start_time` (when to start looking for auths)

Before you run the script, please install the requirements specified in the `requirements.txt` file.

### Example Run

The following will detect all authorizations to 1024674817942-fstip2shineo1lsego38uvsg8n2d3421.apps.googleusercontent.com since 5PM PST on May 2nd

`python detect_phishing.py alerts.json karthik@karthikrangarajan.com 1024674817942-fstip2shineo1lsego38uvsg8n2d3421.apps.googleusercontent.com 2017-05-02T17:00:00Z`
