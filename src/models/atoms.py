# in models/atom.py

from sqlalchemy import Column, Integer, String, Float
from .database import Base  # Import Base from a central database file

class Atom(Base):
    """
    SQLAlchemy model for the 'atoms' table.
    """
    __tablename__ = 'atoms'

    atom_id = Column(Integer, primary_key=True, comment="Unique identifier for each atom, corresponds to atomic number.")
    element_symbol = Column(String(3), nullable=False, unique=True, comment="Chemical symbol of the element (e.g., H, He).")
    protons = Column(Integer, nullable=False, comment="Number of protons in the nucleus.")
    electrons = Column(Integer, nullable=False, comment="Number of electrons orbiting the nucleus.")
    neutrons = Column(Integer, nullable=False, comment="Number of neutrons in the nucleus.")
    electron_config = Column(String(100), comment="The electron configuration string.")
    atomic_mass = Column(Float, nullable=False, comment="The standard atomic weight of the element.")
    atomic_radius = Column(Float, default=0.0, comment="The atomic radius in picometers (defaulted to 0).")
    valence_electrons = Column(Integer, comment="The number of electrons in the outermost shell.")

    def __repr__(self):
        return f"<Atom(atom_id={self.atom_id}, symbol='{self.element_symbol}')>"