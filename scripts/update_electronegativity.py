"""
Script to update electronegativity values in the atoms table from PeriodicTableJSON.json
"""
import json
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL found in environment variables")

# Create database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def update_electronegativity():
    """Update electronegativity values from JSON file."""
    
    # Load JSON data
    json_path = project_root / "PeriodicTableJSON.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    session = SessionLocal()
    
    try:
        updated_count = 0
        skipped_count = 0
        
        for element in data['elements']:
            symbol = element.get('symbol')
            electronegativity = element.get('electronegativity_pauling')
            
            if symbol and electronegativity is not None:
                # Update the atom with this symbol
                result = session.execute(
                    text("UPDATE atoms SET electronegativity = :en WHERE element_symbol = :symbol"),
                    {"en": electronegativity, "symbol": symbol}
                )
                
                if result.rowcount > 0:
                    updated_count += 1
                    print(f"Updated {symbol}: electronegativity = {electronegativity}")
                else:
                    print(f"Warning: Symbol {symbol} not found in database")
            else:
                skipped_count += 1
                if symbol:
                    print(f"Skipped {symbol}: no electronegativity value in JSON")
        
        session.commit()
        
        print(f"\n✓ Successfully updated {updated_count} atoms")
        print(f"✓ Skipped {skipped_count} atoms (no electronegativity data)")
        
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    print("Updating electronegativity values from PeriodicTableJSON.json...\n")
    update_electronegativity()
