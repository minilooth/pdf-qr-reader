# declare constants
data_encoding = 'utf-8'
current_qr_version = 'v2'
qr_version_json_path = '$.version'
qr_number_json_path = '$.qrNumber'
qr_value_json_path = '$.value'

replacements = {
    '\'': '\"',
    'None': 'null',
    'False': 'false',
    'True': 'true'
}
