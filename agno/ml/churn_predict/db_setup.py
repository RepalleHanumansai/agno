import pandas as pd
from database import engine

TRAIN_CSV = "data/vpn_churn_modified.csv"
TEST_CSV = "data/vpn_churn_test_modified.csv"

def create_tables_and_insert():
    print("Loading CSV files...")

    train_df = pd.read_csv(TRAIN_CSV)
    test_df = pd.read_csv(TEST_CSV)

    print("Creating PostgreSQL tables...")

    train_df.to_sql(
        name="vpn_churn_train",
        con=engine,
        if_exists="replace",
        index=False
    )

    test_df.to_sql(
        name="vpn_churn_test",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("Tables created & data inserted successfully!")

if __name__ == "__main__":
    create_tables_and_insert()
