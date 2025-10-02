from prefect import flow

# Import tasks from your other files
from extractors.atom_extractor import extract_elements_from_json
from transformers.atom_transformer import transform_elements_to_atoms
from loaders.atom_loader import load_atoms_to_db

@flow(name="Periodic Table Ingestion Flow")
def ingest_elements_flow():
    """
    The main ETL flow to ingest periodic table data.
    
    1. Extracts element data from a JSON file.
    2. Transforms the data into the required format for the database.
    3. Loads the transformed data into the PostgreSQL 'atoms' table.
    """
    print("Starting the Periodic Table Ingestion Flow...")
    
    # 1. Extract
    raw_elements = extract_elements_from_json(file_path="PeriodicTableJSON.json")
    
    if not raw_elements:
        print("Extraction failed or returned no data. Stopping flow.")
        return
        
    # 2. Transform
    transformed_atoms = transform_elements_to_atoms(elements=raw_elements)
    
    if not transformed_atoms:
        print("Transformation failed or returned no data. Stopping flow.")
        return
        
    # 3. Load
    load_atoms_to_db(atoms_data=transformed_atoms)
    
    print("Periodic Table Ingestion Flow finished successfully.")

if __name__ == "__main__":
    ingest_elements_flow()
