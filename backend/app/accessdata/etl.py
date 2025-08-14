import csv

from dataaccess import get_engine
from datatypes import Provider

from sqlalchemy.orm import Session


def import_from_csv(csv_filename: str) -> None:
    session = Session(bind=get_engine())

    with open(csv_filename, 'r', encoding='latin1') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        print(f"Header: {header}")

        for row in csvreader:
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
            )

            session.add(provider)
    
    session.commit()
    session.close()

if __name__ == "__main__":
    import_from_csv("data/MUP_INP_RY24_P03_V10_DY22_PrvSvc.csv")