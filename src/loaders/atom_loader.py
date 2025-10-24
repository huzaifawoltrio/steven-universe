from prefect import task
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models.database import SessionLocal
from ..models.atoms import Atom

@task
def load_atoms_to_db(atoms_data: List[Dict[str, Any]]):
    """
    Loads a list of atom data into the PostgreSQL database.
    It checks if an atom already exists before inserting or updating.

    Args:
        atoms_data: A list of dictionaries with atom data.
    """
    db: Session = SessionLocal()
    
    try:
        loaded_count = 0
        updated_count = 0
        
        for atom_data in atoms_data:
            # Check if atom already exists by its primary key (atom_id)
            existing_atom = db.query(Atom).filter(Atom.atom_id == atom_data["atom_id"]).first()
            
            if existing_atom:
                # Update existing atom with new data
                for key, value in atom_data.items():
                    setattr(existing_atom, key, value)
                updated_count += 1
            else:
                # Insert new atom
                atom = Atom(**atom_data)
                db.add(atom)
                loaded_count += 1
        
        db.commit()
        
        if loaded_count > 0 or updated_count > 0:
            print(f"Successfully loaded {loaded_count} new atoms and updated {updated_count} existing atoms.")
        else:
            print("No changes to make. Database is already up-to-date.")

    except Exception as e:
        db.rollback()
        print(f"An error occurred during loading: {e}")
    finally:
        db.close()
