import json
import sys
import time
import requests
import zipfile
import io
import os

NOTARY_LIST_URL = 'https://notary.cdn.sos.ca.gov/export/active-notary.zip'


def fetch_current_notary_list(NOTARY_LIST_URL=NOTARY_LIST_URL):
    timestamp = time.strftime("[%m/%d/%y %H:%M:%S]")

    r = requests.request("GET", NOTARY_LIST_URL)

    if r.status_code != 200:
        msg = f"{timestamp} Status Code: {
            r.status_code}\nError Message: {r.content}"
        with open("../log/notaryscope.log", "a") as l:
            l.write(msg)
        exit(1)

    return r.content


def extract_notary_list(zip_bytes):
    ts = time.strftime("%m%d%y-%H%M%S")
    target_file = 'active-notary.txt'
    output_file = f"../tmp/active-notary_{ts}.txt"

    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        if target_file in zf.namelist():

            with open(output_file, 'wb') as extracted:
                extracted.write(zf.read(target_file))

            with open("../log/notaryscope.log", "a") as l:
                timestamp = time.strftime("[%m/%d/%y %H:%M:%S]")
                l.write(f"{timestamp} Extracted to {output_file}")
        else:
            with open("../log/notaryscope.log", "a") as l:
                timestamp = time.strftime("[%m/%d/%y %H:%M:%S]")
                l.write(f"{timestamp} File {target_file} not found.")
            exit(1)

    return output_file


def convert_file_to_json(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    # Extract the header fields from the first line
    headers = lines[0].strip().split('\t')

    # Convert each subsequent line to a dictionary
    data = []
    for line in lines[1:]:
        fields = line.strip().split('\t')
        # Ensure fields and headers align
        if len(fields) == len(headers):
            entry = dict(zip(headers, fields))
            data.append(entry)
        else:
            print(f"Skipping malformed line: {line}")

    # Write to output JSON file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=2)

    with open("../log/notaryscope.log", "a") as l:
        timestamp = time.strftime("[%m/%d/%y %H:%M:%S]")
        l.write(f"{timestamp} Conversion complete. {
                len(data)} entries written to {output_file}")


# Example usage
if __name__ == "__main__":
    timestamp = time.strftime("%m%d%y-%H%M%S")
    json_out = f"../tmp/notaries_{timestamp}.json"
    zip_bytes = fetch_current_notary_list()
    notary_list_text = extract_notary_list(zip_bytes)
    convert_file_to_json(notary_list_text, json_out)
    with open('../notaries.json', 'w') as nf:
        dump = None
        with open(json_out, 'r') as f:
            dump = f.read()
        nf.write(dump)
    with open("../log/notaryscope.log", "a") as l:
        timestamp = time.strftime("[%m/%d/%y %H:%M:%S]")
        l.write(f"{timestamp} Notary Public Listing Successfully Updated")
    exit(0)
