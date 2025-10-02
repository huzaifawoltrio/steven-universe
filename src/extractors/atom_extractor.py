import json
from prefect import task
from typing import List, Dict, Any

@task
def extract_elements_from_json(file_path: str = "PeriodicTableJSON.json") -> List[Dict[str, Any]]:
    """
    Reads the periodic table data from a JSON file.

    Args:
        file_path: The path to the JSON file.

    Returns:
        A list of dictionaries, where each dictionary represents an element.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        elements = data.get("elements")
        if not elements:
            raise ValueError("Could not find 'elements' key in the JSON file.")
            
        print(f"Successfully extracted {len(elements)} elements from {file_path}")
        return elements
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file at {file_path} is not a valid JSON file.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred during extraction: {e}")
        return []
