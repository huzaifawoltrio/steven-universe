from prefect import task
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.atoms import Atom

@task
def load_atoms_to_db(atoms_data: List[Dict[str, Any]]):
    """
    Loads a list of atom data into the PostgreSQL database.
    It checks if an atom already exists before inserting.

    Args:
        atoms_data: A list of dictionaries with atom data.
    """
    db: Session = SessionLocal()
    
    try:
        loaded_count = 0
        for atom_data in atoms_data:
            # Check if atom already exists by its primary key (atom_id)
            exists = db.query(Atom).filter(Atom.atom_id == atom_data["atom_id"]).first()
            
            if not exists:
                atom = Atom(**atom_data)
                db.add(atom)
                loaded_count += 1
        
        if loaded_count > 0:
            db.commit()
            print(f"Successfully loaded {loaded_count} new atoms into the database.")
        else:
            print("No new atoms to load. Database is already up-to-date.")

    except Exception as e:
        db.rollback()
        print(f"An error occurred during loading: {e}")
    finally:
        db.close()
