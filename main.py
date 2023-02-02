import sys
from pyzbar.pyzbar import decode
import constant
from pdf2image import convert_from_path
import json
from jsonpath_ng import parse


class QrReadException(Exception):
    def __init__(self, message):
        super().__init__(message)


def parse_pdfs(filename):
    images = convert_from_path(filename, poppler_path='C:\\Program Files\\poppler-23.01.0\\Library\\bin')
    barcodes = []

    for image in images:
        decode_result = decode(image)
        if decode_result:
            barcodes.extend(decode_result)

    jsons = list(map(lambda barcode: barcode.data.decode(constant.data_encoding), barcodes))

    if not jsons:
        raise QrReadException("Unable to find QR codes in provided document")

    correct_qrs = list(filter(lambda item: extract_by_json_path(
        item, constant.qr_version_json_path) == constant.current_qr_version, jsons))

    if len(correct_qrs) != len(jsons):
        raise QrReadException(f'Some of QR codes is not in version {constant.current_qr_version}')

    jsons.sort(key=lambda item: extract_by_json_path(item, constant.qr_number_json_path))

    joined = "".join(list(map(lambda item: extract_by_json_path(item, constant.qr_value_json_path), jsons)))

    for key, value in constant.replacements.items():
        joined = joined.replace(key, value)

    return joined


def extract_by_json_path(json_data, json_path):
    json_data = json.loads(json_data)
    jsonpath_expr = parse(json_path)
    return jsonpath_expr.find(json_data)[0].value


if __name__ == '__main__':
    read = parse_pdfs(sys.argv[1])
    print(read)
