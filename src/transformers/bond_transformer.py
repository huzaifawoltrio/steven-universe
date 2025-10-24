from prefect import task
from itertools import combinations


@task(name="transform_atoms_to_bonds", log_prints=True)
def transform_atoms_to_bonds(atoms):
    """
    Generate all possible chemical bonds based on valence electrons and electronegativity.
    
    Args:
        atoms: List of atom dictionaries with keys: atom_id, element_symbol, valence_electrons, electronegativity
    
    Returns:
        List of bond dictionaries
    """
    print(f"Transforming {len(atoms)} atoms into possible bonds...")
    
    bonds = []
    noble_gases = {'He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn'}
    
    # Generate all unique unordered pairs
    for atom_a, atom_b in combinations(atoms, 2):
        # Skip if either atom is missing required data
        if atom_a['valence_electrons'] is None or atom_b['valence_electrons'] is None:
            continue
        
        if atom_a['electronegativity'] is None or atom_b['electronegativity'] is None:
            continue
        
        symbol_a = atom_a['element_symbol']
        symbol_b = atom_b['element_symbol']
        
        # Rule 1: Calculate bonding capacity
        if symbol_a == 'H':
            capacity_a = 1
        elif symbol_a in noble_gases:
            capacity_a = 0
        else:
            capacity_a = 8 - atom_a['valence_electrons']
        
        if symbol_b == 'H':
            capacity_b = 1
        elif symbol_b in noble_gases:
            capacity_b = 0
        else:
            capacity_b = 8 - atom_b['valence_electrons']
        
        # Skip if either has no bonding capacity
        if capacity_a <= 0 or capacity_b <= 0:
            continue
        
        # Rule 2: Calculate electronegativity difference
        delta_en = abs(atom_a['electronegativity'] - atom_b['electronegativity'])
        
        # Rule 3: Bond formation conditions
        can_form = True
        if delta_en >= 3.0:
            can_form = False
        if symbol_a in noble_gases or symbol_b in noble_gases:
            can_form = False
        
        # Rule 4: Determine bond type based on ΔEN
        if delta_en < 0.4:
            bond_type = "Nonpolar Covalent"
        elif delta_en < 1.7:
            bond_type = "Polar Covalent"
        else:
            bond_type = "Ionic"
        
        # Rule 5: Calculate possible bond orders
        max_bonds = min(capacity_a, capacity_b)
        
        # Rule 6: Special case for Hydrogen
        if symbol_a == 'H' or symbol_b == 'H':
            bond_orders = "1"
        else:
            # Generate bond orders up to max (1, 2, 3)
            orders = [str(i) for i in range(1, min(max_bonds, 3) + 1)]
            bond_orders = ",".join(orders)
        
        # Create bond record
        bond = {
            'atom1_symbol': symbol_a,
            'atom2_symbol': symbol_b,
            'bond_type': bond_type,
            'bond_orders': bond_orders,
            'delta_en': round(delta_en, 4),
            'can_form': can_form
        }
        
        bonds.append(bond)
    
    print(f"Generated {len(bonds)} possible bonds")
    print(f"Bonds that can form: {sum(1 for b in bonds if b['can_form'])}")
    
    return bonds
