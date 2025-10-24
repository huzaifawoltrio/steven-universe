from prefect import task
from typing import List, Dict, Any
import math

@task
def transform_elements_to_atoms(elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transforms the raw element data into a format that matches the Atom model,
    performing necessary calculations.

    Args:
        elements: A list of raw element data from the extractor.

    Returns:
        A list of dictionaries, where each dictionary is ready to be loaded.
    """
    transformed_atoms = []
    
    for element in elements:
        # Skip elements with missing essential data
        if "number" not in element or "atomic_mass" not in element or not element.get("symbol"):
            print(f"Skipping element due to missing data: {element.get('name', 'N/A')}")
            continue

        atomic_number = element["number"]
        atomic_mass = element["atomic_mass"]

        # --- Calculations ---
        protons = atomic_number
        electrons = atomic_number  # In a neutral atom, protons == electrons
        
        # Calculate neutrons: Mass Number (rounded atomic mass) - Protons
        # Some elements (like Technetium) have integer mass in the JSON, others are floats.
        neutrons = math.ceil(atomic_mass) - protons

        # Calculate valence electrons from the 'shells' array
        # The last element in the shells array is the number of valence electrons.
        valence_electrons = element.get("shells", [])[-1] if element.get("shells") else None

        # Extract first ionization energy
        ionization_energies = element.get("ionization_energies", [])
        ionization_energy = ionization_energies[0] if ionization_energies else None
        
        # Extract electronegativity (Pauling scale)
        electronegativity = element.get("electronegativity_pauling")

        atom_data = {
            "atom_id": atomic_number,
            "element_symbol": element["symbol"],
            "protons": protons,
            "electrons": electrons,
            "neutrons": neutrons,
            "electron_config": element.get("electron_configuration"),
            "atomic_mass": atomic_mass,
            "atomic_radius": 0.0,  # Defaulting as requested
            "valence_electrons": valence_electrons,
            "ionization_energy": ionization_energy,
            "electronegativity": electronegativity
        }
        transformed_atoms.append(atom_data)
        
    print(f"Successfully transformed {len(transformed_atoms)} elements.")
    return transformed_atoms
