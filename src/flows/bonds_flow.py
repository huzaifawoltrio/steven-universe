from prefect import flow
from src.extractors.bond_extractor import extract_atoms
from src.transformers.bond_transformer import transform_atoms_to_bonds
from src.loaders.bond_loader import load_bonds_to_db


@flow(name="bonds-etl-flow", log_prints=True)
def bonds_etl_flow():
    """
    Automated ETL pipeline that analyzes atomic data and computes possible chemical bonds.
    
    Steps:
    1. Extract atoms from PostgreSQL database
    2. Transform atoms into possible bonds using valence and electronegativity rules
    3. Load computed bonds back to database
    """
    print("Starting Bonds ETL Flow...")
    
    # Extract
    atoms = extract_atoms()
    
    # Transform
    bonds = transform_atoms_to_bonds(atoms)
    
    # Load
    load_bonds_to_db(bonds)
    
    print("Bonds ETL Flow completed successfully!")


if __name__ == "__main__":
    bonds_etl_flow()
