import wfdb
import os

def download_ecg_data(record_names, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for record in record_names:
        print(f"Downloading record {record}...")
        wfdb.dl_database('mitdb', output_dir, records=[record], overwrite=True)
        print(f"Record {record} downloaded successfully.")

if __name__ == "__main__":
    records = ['100', '106']
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/mitdb'))
    download_ecg_data(records, data_dir)
