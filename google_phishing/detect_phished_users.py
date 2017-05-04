import argparse
import json

import httplib2
from googleapiclient import discovery
from oauth2client.client import SignedJwtAssertionCredentials


def check_if_client_id_authorized(items, client_id):
    for item in items:
        # we know there is only one event because that's what we have requested
        parameters = item["events"][0]["parameters"]
        for parameter in parameters:
            if parameter["name"] == "client_id":
                if parameter["value"] == client_id:
                    print item["actor"]["email"]


def retrieve_authorizations_for_client(service_account_json,
                                       user_email,
                                       client_id,
                                       start_time):
    service_account_credentials = json.loads(
        open(service_account_json, 'r').read())
    client_email = service_account_credentials["client_email"]
    private_key = service_account_credentials["private_key"]
    user_email = user_email

    credentials = SignedJwtAssertionCredentials(client_email, private_key,
                                                ['https://www.googleapis.com/'
                                                 'auth/'
                                                 'admin.reports.audit.readonly'],
                                                sub=user_email)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('admin', 'reports_v1', http=http)

    activity_response = service.activities().\
        list(applicationName="token",
             userKey="all",
             eventName="authorize",
             startTime=start_time).execute()

    check_if_client_id_authorized(activity_response.get("items"), client_id)

    while activity_response.get("nextPageToken"):
        activity_response = service.activities().\
            list(applicationName="token",
                 userKey="all",
                 eventName="authorize",
                 pageToken=activity_response.get("nextPageToken"),
                 startTime=start_time).execute()
        check_if_client_id_authorized(activity_response.get("items"), client_id)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("service_account_file", type=str,
                        help="Google Service Account JSON file")
    parser.add_argument("admin_email", type=str,
                        help="Google Admin email account")
    parser.add_argument("client_id", type=str,
                        help="Client ID to see authorizations for")
    parser.add_argument("start_time", type=str,
                        help="Time in format yyyy-mm-ddT00:00:00Z")
    args = parser.parse_args()

    retrieve_authorizations_for_client(args.service_account_file,
                                       args.admin_email,
                                       args.client_id,
                                       args.start_time)

if __name__ == "__main__":
    main()
