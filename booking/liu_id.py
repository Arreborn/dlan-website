import requests

cached_names = {}
cached_emails = {}

API_URL = 'https://kobra.karservice.se/api/v1/'
API_KEY = '405a4066a13c44df1bcc2819a13529b2903b4ae5'


def lookup_name(liu_id):
    if liu_id not in cached_names and not _lookup_liu_id(liu_id):
        return None

    return cached_names[liu_id]


def lookup_email(liu_id):
    if liu_id in cached_emails and not _lookup_liu_id(liu_id):
        return None

    return cached_emails[liu_id]


def reverse_lookup(rfid):
    """
    Looks up a student from his/hers rfid which is saved when a seat is reserved.
    :param rfid: (String) a unique identifier used to query student data from cobra.
    :return: (JSON) The student data as a json blob.
    """
    if rfid is None:
        return None
    return _query_student(rfid)


def _lookup_liu_id(liu_id):
    """
    Looks up a student from his/hers liu id which the user inputs when reserving a seat.
    :param liu_id: (String) A liu id contains of 5 letters and 3 digits like abcde123 and is unique for every student.
    :return: (JSON) The student data as a json blob.
    """
    json = _query_student(liu_id)
    if json:
        cached_names[liu_id] = json.get('name')
        cached_emails[liu_id] = json.get('email')

        return True

    return False


def _query_student(id, retry=True):
    """
    Query the cobra api for data about the student with certain liu id or rfid.
    :param id: (String) A liu id contains of 5 letters and 3 digits like abcde123 and is unique for every student. The
    rfid is also a unique for every students but not a human readable one. It comes with the student data as 'id'.
    :param retry: (Boolean) Should we try again if we don't get a response True for yes, False for no.
    :return: (JSON) Returns the data about the student like name, union membership and section student is in.
    """
    response = requests.request('GET', API_URL + 'students/' + id, headers={'Authorization': 'Token ' + API_KEY})
    if response.status_code == 200:
        return response.json()
    if retry:
        _query_student(id, retry=False)
    else:
        return None


def _get_email(json):
    return json['email']
