import json
import sqlite3

# --------------------------------------------------
# Configuration
# --------------------------------------------------
INPUT_JSON_FILE = "Dataset.json"  
DB_FILE = "providers.db"
TARGET_STATES = {"NY", "CA", "TX"}

# --------------------------------------------------
# Helper Functions
# --------------------------------------------------
def extract_addresses(addresses):
    """
    Extract LOCATION and MAILING addresses separately.
    If an address type is missing, populate fields with 'Unknown'.
    """

    location = {
        "address_1": "Unknown",
        "city": "Unknown",
        "state": "Unknown",
        "postal_code": "Unknown"
    }

    mailing = {
        "address_1": "Unknown",
        "city": "Unknown",
        "state": "Unknown",
        "postal_code": "Unknown"
    }

    for addr in addresses:
        if addr.get("address_purpose") == "LOCATION":
            location = {
                "address_1": addr.get("address_1", "Unknown"),
                "city": addr.get("city", "Unknown"),
                "state": addr.get("state", "Unknown"),
                "postal_code": addr.get("postal_code", "Unknown")
            }
        elif addr.get("address_purpose") == "MAILING":
            mailing = {
                "address_1": addr.get("address_1", "Unknown"),
                "city": addr.get("city", "Unknown"),
                "state": addr.get("state", "Unknown"),
                "postal_code": addr.get("postal_code", "Unknown")
            }

    return location, mailing


def get_primary_specialty(taxonomies):
    """
    Return the primary specialty (taxonomy) if present.
    """
    for tax in taxonomies:
        if tax.get("primary") is True:
            return tax
    return None


# --------------------------------------------------
# Main ETL Processing
# --------------------------------------------------
def main():

    # Load JSON dataset
    with open(INPUT_JSON_FILE, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    # Connect to SQLite database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create provider_registry table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS provider_registry ( 
            npi TEXT PRIMARY KEY,
            enumeration_type TEXT,
            first_name TEXT,
            middle_name TEXT,
            last_name TEXT,
            full_name TEXT,
            credential TEXT,
            gender TEXT,
            primary_specialty TEXT,
            license_number TEXT,

            -- Location address
            location_address_line1 TEXT,
            location_city TEXT,
            location_state TEXT,
            location_postal_code TEXT,

            -- Mailing address
            mailing_address_line1 TEXT,
            mailing_city TEXT,
            mailing_state TEXT,
            mailing_postal_code TEXT
        )
    """)

    processed_rows = 0

    # Dataset structure: [<city/state>, {results: [...]}]
    for _, block in raw_data:
        for provider in block.get("results", []):

            # Filter: only individual providers (NPI-1)
            if provider.get("enumeration_type") != "NPI-1":
                continue

            # Extract both address types
            location_addr, mailing_addr = extract_addresses(
                provider.get("addresses", [])
            )

            # Filter based on LOCATION state first, then MAILING
            state_for_filter = (
                location_addr["state"]
                if location_addr["state"] != "Unknown"
                else mailing_addr["state"]
            )

            if state_for_filter not in TARGET_STATES:
                continue

            # Basic provider info
            basic = provider.get("basic", {})
            first_name = basic.get("first_name")
            middle_name = basic.get("middle_name")
            last_name = basic.get("last_name")
            credential = basic.get("credential")
            gender = basic.get("gender")

            #non empty values are joined, none or empty skipped
            full_name = " ".join(
                part for part in [first_name, middle_name, last_name] if part
            )

            # Primary specialty
            primary_specialty = get_primary_specialty(
                provider.get("taxonomies", [])
            )
            specialty_desc = (
                primary_specialty.get("desc") if primary_specialty else None
            )
            license_number = (
                primary_specialty.get("license") if primary_specialty else None
            )

            # Insert into SQLite (avoid duplicates)
            cursor.execute("""
                INSERT OR IGNORE INTO provider_registry (
                    npi,
                    enumeration_type,
                    first_name,
                    middle_name,
                    last_name,
                    full_name,
                    credential,
                    gender,
                    primary_specialty,
                    license_number,

                    location_address_line1,
                    location_city,
                    location_state,
                    location_postal_code,

                    mailing_address_line1,
                    mailing_city,
                    mailing_state,
                    mailing_postal_code
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                provider.get("number"),
                provider.get("enumeration_type"),
                first_name,
                middle_name,
                last_name,
                full_name,
                credential,
                gender,
                specialty_desc,
                license_number,

                location_addr["address_1"],
                location_addr["city"],
                location_addr["state"],
                location_addr["postal_code"],

                mailing_addr["address_1"],
                mailing_addr["city"],
                mailing_addr["state"],
                mailing_addr["postal_code"]
            ))

            processed_rows += 1

    # Commit and summarize
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM provider_registry")
    rows_in_table = cursor.fetchone()[0]
    conn.close()

    print("\n📊 ETL Summary:")
    print(f"   • Processed providers: {processed_rows}")
    print(f"   • Loaded into DB: {rows_in_table}")
    print(f"   • Duplicates skipped: {processed_rows - rows_in_table}")
    print(f"\n✅ SQLite database '{DB_FILE}' ready for analysis.")


if __name__ == "__main__":
    main()
