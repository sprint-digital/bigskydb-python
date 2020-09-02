import requests
import os
import logging
import sys
import getopt

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
log = logging.getLogger('console-logger')


def main(argv):
    input_file = None
    device_id = None
    try:
        opts, args = getopt.getopt(argv, "hi:d:", ["input=", "device_id="])
    except getopt.GetoptError:
        log.error("upload_zip.py -i <inputfilename.zip> -d <device_id>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('upload_zip.py -i <inputfilename.zip> -d <device_id>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-d", "--device_id"):
            device_id = arg

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, './zips/' + str(input_file).strip())
    fileobj = open(filename, 'rb')

    # TODO: replace the device_id field with the
    res = requests.post("https://portal-staging.turnkeybi.com.au/api/v1/webhook/organisations/4/files",
                        data={"device_id": str(device_id).strip()},
                        files={"file": (os.path.basename(
                            fileobj.name), fileobj)},
                        headers={"Accept": "application/json"})

    if res.status_code == 201:
        log.debug('Upload Success')
    else:
        log.error('Upload Failed. HTTP Response ' + str(res.status_code))


if __name__ == "__main__":
    main(sys.argv[1:])
