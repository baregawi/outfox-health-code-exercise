import csv

from app.accessdata.dataaccess import get_engine
from app.accessdata.datatypes import Provider
from app.accessdata.geolocation import get_gps_coordinates

from geoalchemy2.functions import ST_MakePoint
from sqlalchemy.orm import Session


def import_from_csv(csv_filename: str) -> None:
    """Import provider data from a CSV file into the database."""

    session = Session(bind=get_engine())

    with open(csv_filename, 'r', encoding='latin1') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        print(f"Header: {header}")

        for row in csvreader:
            address = f"{row[3]},+{row[2]},+{row[5]},+{row[6]}"
            latlong = get_gps_coordinates(address)
            if not latlong:
                print(f"Could not get GPS coordinates for address: {address}")
                continue
            lat, long = latlong

            provider = Provider(
                provider_ccn=int(row[0]),
                provider_org_name=row[1],
                city=row[2],
                street_address=row[3],
                state_fips=row[4],
                zipcode=row[5],
                state_abbr=row[6],
                ruca=row[7],
                ruca_description=row[8],
                drg_cd=row[9],
                drg_description=row[10],
                total_discharges=int(row[11]),
                avg_submited_cvrd_charge=float(row[12]),
                avg_total_payment_amount=float(row[13]),
                avg_mdcr_payment_amt=float(row[14]),
                location=ST_MakePoint(lat, long),
            )

            session.add(provider)
    
    session.commit()
    session.close()

if __name__ == "__main__":
    # The location API I used is unfortunately slow so we use a reduced dataset instead.
    # import_from_csv("data/MUP_INP_RY24_P03_V10_DY22_PrvSvc.csv")
    import_from_csv("data/MUP_INP_RY24_P03_V10_DY22_PrvSvc_reduced.csv")
    print("Data import completed.")