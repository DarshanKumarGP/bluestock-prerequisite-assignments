"""
Week 2 - REST APIs & JSON
Call a public API, inspect the JSON response, and convert it into a CSV.

Reuses the mfapi.in API from the Bluestock capstone -- same public,
auth-free REST API, but this time the focus is on the API mechanics
(status code, JSON structure, query/endpoint behaviour) rather than
just fetching data for a pipeline.

Run:
    python api_to_csv.py
"""

import requests
import pandas as pd

SCHEME_CODE = "119551"  # SBI Bluechip Fund
URL = f"https://api.mfapi.in/mf/{SCHEME_CODE}"


def main():
    print(f"Calling GET {URL}")
    response = requests.get(URL)

    # Inspect the response, same as you would in Postman
    print(f"Status code: {response.status_code}")
    print(f"Content-Type header: {response.headers.get('Content-Type')}")

    if response.status_code != 200:
        print("Request failed -- stopping here.")
        return

    data = response.json()  # parses the raw JSON text into a Python dict

    # Inspect the JSON structure before converting anything
    print(f"\nTop-level keys: {list(data.keys())}")
    print(f"Scheme name: {data['meta']['scheme_name']}")
    print(f"Number of NAV records: {len(data['data'])}")
    print(f"\nFirst record: {data['data'][0]}")

    # Convert the nested 'data' list into a flat table
    df = pd.DataFrame(data["data"])
    df["scheme_name"] = data["meta"]["scheme_name"]
    df["fund_house"] = data["meta"]["fund_house"]

    output_path = "api_response_converted.csv"
    df.to_csv(output_path, index=False)
    print(f"\nSaved {len(df)} rows to {output_path}")


if __name__ == "__main__":
    main()
