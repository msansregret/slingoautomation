"""Process raw json stored in output.json, and send them.

To use this file, just enter this in terminal:

    python send_json.py

If JSONs in /output.json are processed and loaded sucessfully,
this file will delete /output.json content automatically;
repeated calling 'python send_json.py' won't make anything happen.

"""

import json
import requests

catfish_url = 'http://192.168.8.167:4711/api/results/'
headers = { 
    'User-Agent': 
    'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'
}


def process_json():
    """Modify output.json to put everything inside a [], then send back status code.

    status code:
    0: output.json is empty.
    1: output.json is not empty, and processing went successfully.
    2: output.json is not empty, but it can't be processed.
    
    """
    with open('output.json', 'rb+') as output:
        content = output.read()

        # if the previous send operation has succeeded, we would have deleted
        # contents in output.json. So if we call this file again, do nothing.
        if content == '':
            return 0

        # wrap the whole thing inside a []
        elif content[0] != '[':

            # our unprocessed output.json should start with '{'.
            if content[0] != '{':
                return 2

            # strip the trailing comma, otherwise json won't parse.
            # use this manual approach instead of rstrip() because the file
            # ends in some weird line_end/file_end character.
            index = -1
            while content[index] != ',':
                content = content[:index]

            content = content[:index]
            # add a ] in the end
            output.seek(0, 0)
            output.write('[' + content + ']')

            return 1

        else:
            return 2


def load_then_send():
    """Load JSON file inside output.json, and send all of them to server.

    If any POST request returns any status code rather than 200, that
    request has failed. Print out the status code, and return False.
    
    """
    with open('output.json', 'r') as output:
        # load JSON
        results = json.load(output)
        print("*" * 50)

    success = True
    for result in results:
        r = requests.post(catfish_url, data=result, headers=headers)
        print("About to send:")
        print(result)
        if r.status_code == 200:
            print("Successfully sent JSON to server.")
        else:
            print("Failed to send JSON to server. Status code: " + 
                  r.status_code)
        print("*" * 50)

        if r.status_code != 200:
            success = False

    return success


def delete_content():
    """Now that we've sent JSON, delete this file for future use."""
    """
    with open('output.json', 'w'):
        pass
    """


def main():
    """Process output.json, send JSON to server, then delete output.json."""
    process_success = process_json()
    if process_success == 1:
        send_success = load_then_send()
        if send_success is True:
            delete_content()
        else:
            print("Oh no! We failed to load and send JSON to server!")
    elif process_success == 0:
        print("output.json is empty, do nothing.")
    else:
        print("send_json.py seems to fail to delete content inside"
              " output.json last time it ran. Please check output.json."
              " If you know what you're doing, you can delete content in "
              "output.json yourself.")


if __name__ == '__main__':
    main()
