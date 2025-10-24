from prefect import task
from sqlalchemy import text
from src.models.database import get_session
from src.models.bonds import Bond


@task(name="load_bonds_to_db", log_prints=True)
def load_bonds_to_db(bonds):
    """
    Load computed bonds into the database.
    Truncates the bonds table first, then inserts all new bonds.
    
    Args:
        bonds: List of bond dictionaries
    """
    print(f"Loading {len(bonds)} bonds to database...")
    
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        # Truncate the bonds table
        print("Truncating bonds table...")
        session.execute(text("TRUNCATE TABLE bonds RESTART IDENTITY CASCADE"))
        session.commit()
        
        # Insert all bonds
        for bond_data in bonds:
            bond = Bond(**bond_data)
            session.add(bond)
        
        session.commit()
        print(f"Successfully loaded {len(bonds)} bonds to database")
    finally:
        session.close()
