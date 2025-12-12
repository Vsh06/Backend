from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='patient')  # doctor, researcher, patient, admin
    currently_logged_in = db.Column(db.Boolean, default=False)
    # reset_token = db.Column(db.String(100), nullable=True)
    # reset_token_expiry = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class UserActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    login_time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(50), nullable=False)  # Success, Failed
    ip_address = db.Column(db.String(45))  # IPv4/IPv6 support

class DrugBrandNames(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    canonical_drug_name = db.Column(db.String(255), nullable=False, index=True)  # e.g., "Paracetamol" or CHEMBL ID
    brand_names = db.Column(db.Text, nullable=False)  # JSON array, e.g., '["Dolo", "Crocin", "Tylenol"]'
    regions = db.Column(db.Text, nullable=True)  # JSON array, e.g., '["US", "India", "Global"]'
    source = db.Column(db.String(100), nullable=False)  # e.g., "DrugBank", "FDA", "ChEMBL"
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def get_brand_names_list(self):
        """Return brand names as a list."""
        try:
            return json.loads(self.brand_names)
        except json.JSONDecodeError:
            return []

    def get_regions_list(self):
        """Return regions as a list."""
        if not self.regions:
            return []
        try:
            return json.loads(self.regions)
        except json.JSONDecodeError:
            return []

class DiseaseDrugMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease_name = db.Column(db.String(255), nullable=False, index=True)  # e.g., "Diabetes", "PCOD", "Asthma"
    drug_name = db.Column(db.String(255), nullable=False, index=True)  # e.g., "Metformin", "Clomiphene"
    confidence_score = db.Column(db.Float, nullable=False, default=50.0)  # 0-100 confidence score
    mechanism_of_action = db.Column(db.Text, nullable=True)  # How the drug works for this disease
    protein_targets = db.Column(db.Text, nullable=True)  # JSON array of protein targets
    market_names = db.Column(db.Text, nullable=True)  # JSON array of brand/market names
    chemical_composition = db.Column(db.String(255), nullable=True)  # Molecular formula, e.g., "C4H11N5"
    molecular_weight = db.Column(db.Float, nullable=True)  # Molecular weight in g/mol
    iupac_name = db.Column(db.Text, nullable=True)  # IUPAC name
    synonyms = db.Column(db.Text, nullable=True)  # JSON array of synonyms
    source = db.Column(db.String(100), nullable=False, default="ChEMBL")  # Data source
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def get_protein_targets_list(self):
        """Return protein targets as a list."""
        if not self.protein_targets:
            return []
        try:
            return json.loads(self.protein_targets)
        except json.JSONDecodeError:
            return []

    def get_market_names_list(self):
        """Return market names as a list."""
        if not self.market_names:
            return []
        try:
            return json.loads(self.market_names)
        except json.JSONDecodeError:
            return []

    def get_synonyms_list(self):
        """Return synonyms as a list."""
        if not self.synonyms:
            return []
        try:
            return json.loads(self.synonyms)
        except json.JSONDecodeError:
            return []

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user_email = db.Column(db.Text, nullable=True)
    query = db.Column(db.Text, nullable=False)
    search_type = db.Column(db.Text, nullable=False)  # 'drug', 'disease', 'unknown'
    result_preview = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
