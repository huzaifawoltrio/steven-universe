from prefect import task
from sqlalchemy.orm import Session
from src.models.database import get_session
from src.models.atoms import Atom


@task(name="extract_atoms", log_prints=True)
def extract_atoms():
    """
    Extract all atoms from the PostgreSQL database.
    Returns a list of Atom objects.
    """
    print("Extracting atoms from database...")
    
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        atoms = session.query(Atom).all()
        print(f"Extracted {len(atoms)} atoms from database")
        
        # Convert to list of dicts for easier processing
        atoms_data = []
        for atom in atoms:
            atoms_data.append({
                'atom_id': atom.atom_id,
                'element_symbol': atom.element_symbol,
                'valence_electrons': atom.valence_electrons,
                'electronegativity': atom.electronegativity if hasattr(atom, 'electronegativity') else None
            })
        
        return atoms_data
    finally:
        session.close()
