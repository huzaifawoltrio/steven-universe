from sqlalchemy import Column, Integer, String, Float, Boolean, Index, ForeignKey
from .database import Base


class Bond(Base):
    """
    SQLAlchemy model for the 'bonds' table.
    Stores computed possible chemical bonds based on valence and electronegativity rules.
    """
    __tablename__ = 'bonds'

    bond_id = Column(Integer, primary_key=True, autoincrement=True, comment="Unique identifier for each bond.")
    atom1_symbol = Column(String(3), nullable=False, comment="Chemical symbol of the first atom.")
    atom2_symbol = Column(String(3), nullable=False, comment="Chemical symbol of the second atom.")
    bond_type = Column(String(20), nullable=False, comment="Type of bond: Nonpolar Covalent, Polar Covalent, or Ionic.")
    bond_orders = Column(String(10), nullable=False, comment="Possible bond orders as comma-separated string (e.g., '1,2,3').")
    delta_en = Column(Float, nullable=False, comment="Electronegativity difference (ΔEN).")
    can_form = Column(Boolean, nullable=False, default=True, comment="Whether the bond can form based on rules.")

    # Indexes
    __table_args__ = (
        Index('ix_bonds_atom1_symbol', 'atom1_symbol'),
        Index('ix_bonds_atom2_symbol', 'atom2_symbol'),
    )

    def __repr__(self):
        return f"<Bond(atom1={self.atom1_symbol}, atom2={self.atom2_symbol}, type={self.bond_type}, orders={self.bond_orders})>"
