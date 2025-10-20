"""
Data generator for retail customer sales data.
Generates synthetic sales data for customer segmentation proof of concept.

Enhancements:
- Optionally uses the Faker library to generate realistic customer profile fields
    (name, email, phone, address, etc.) while preserving existing numeric features.
- Persona-based customer generation with realistic behavioral patterns
- Full 21-department, 394-class product hierarchy support
- Dual dataset generation: basic (clustering only) vs enriched (full analysis)
"""
import numpy as np
import pandas as pd
import yaml
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime, timedelta

try:
    from faker import Faker  # Optional dependency; enabled if installed
except Exception:  # pragma: no cover
    Faker = None


class RetailDataGenerator:
    def save_data(self, data: pd.DataFrame, filepath: str):
        """
        Save generated data to CSV file.
        Args:
            data: DataFrame to save
            filepath: Path to save the CSV file
        """
        data.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")
    """Generate synthetic retail sales data for customer segmentation."""
    
    def __init__(self, seed: Optional[int] = 42, *, 
                 faker_enabled: bool = True, 
                 faker_locale: str = 'en_US',
                 use_personas: bool = True,
                 personas_config_path: Optional[str] = None,
                 hierarchy_config_path: Optional[str] = None):
        """
        Initialize the data generator.
        
        Args:
            seed: Random seed for reproducibility
            faker_enabled: Whether to generate realistic profile fields with Faker
            faker_locale: Locale for Faker profile data (e.g., 'en_US')
            use_personas: Whether to use persona-based generation (recommended)
            personas_config_path: Path to personas.yml config file
            hierarchy_config_path: Path to hierarchy_parsed.yml config file
        """
        self.seed = seed
        np.random.seed(seed)
        
        # Setup faker (optional, guarded if not installed)
        self.faker_enabled = bool(faker_enabled and Faker is not None)
        self.faker_locale = faker_locale
        self._faker = None
        if self.faker_enabled:
            self._faker = Faker(self.faker_locale)
            # Seed faker for reproducibility
            try:
                self._faker.random.seed(seed)
            except Exception:
                pass
        
        # Persona-based generation setup
        self.use_personas = use_personas
        self.personas = None
        self.hierarchy = None
        
        if self.use_personas:
            # Load personas configuration
            if personas_config_path is None:
                personas_config_path = "config/personas.yml"
            
            personas_path = Path(personas_config_path)
            if personas_path.exists():
                with open(personas_path, 'r') as f:
                    personas_data = yaml.safe_load(f)
                    self.personas = personas_data.get('customer_personas', {})
            else:
                print(f"Warning: Personas config not found at {personas_config_path}, falling back to legacy segments")
                self.use_personas = False
            
            # Load product hierarchy
            if hierarchy_config_path is None:
                hierarchy_config_path = "hierarchy_parsed.yml"
            
            hierarchy_path = Path(hierarchy_config_path)
            if hierarchy_path.exists():
                with open(hierarchy_path, 'r') as f:
                    hierarchy_data = yaml.safe_load(f)
                    self.hierarchy = hierarchy_data.get('departments', {})
            else:
                print(f"Warning: Hierarchy config not found at {hierarchy_config_path}, using legacy hierarchy")
                self.hierarchy = self._get_legacy_hierarchy()
        else:
            self.hierarchy = self._get_legacy_hierarchy()
    
    def _get_legacy_hierarchy(self) -> Dict[str, List[str]]:
        """Return the legacy 3-department hierarchy for backwards compatibility."""
        return {
            "Accessories & Footwear": ["Bags & Wallets", "Soft & Hard Accessories"],
            "Health & Wellness": ["Consumables", "Personal Care"],
            "Home & Lifestyle": ["Bedding"]
        }
    
    def _assign_persona(self) -> Tuple[str, Dict]:
        """
        Assign a persona to a customer based on persona weights.
        
        Returns:
            Tuple of (persona_name, persona_config_dict)
        """
        if not self.personas:
            return None, None
        
        persona_names = list(self.personas.keys())
        weights = [self.personas[p]['weight'] for p in persona_names]
        
        # Normalize weights to ensure they sum to 1.0
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]
        
        persona_name = np.random.choice(persona_names, p=normalized_weights)
        return persona_name, self.personas[persona_name]
    
    def _select_department_for_persona(self, persona_config: Dict) -> str:
        """
        Select a department based on persona's department preferences.
        
        Args:
            persona_config: Persona configuration dictionary
        
        Returns:
            Selected department name
        """
        dept_prefs = persona_config.get('department_preferences', {})
        
        if not dept_prefs:
            # Fallback to uniform random selection
            return np.random.choice(list(self.hierarchy.keys()))
        
        departments = list(dept_prefs.keys())
        weights = [dept_prefs[d] for d in departments]
        
        # Ensure departments exist in hierarchy
        valid_departments = [d for d in departments if d in self.hierarchy]
        if not valid_departments:
            return np.random.choice(list(self.hierarchy.keys()))
        
        valid_weights = [dept_prefs[d] for d in valid_departments]
        total_weight = sum(valid_weights)
        normalized_weights = [w / total_weight for w in valid_weights]
        
        return np.random.choice(valid_departments, p=normalized_weights)
    
    def _select_class_for_department(self, department: str, persona_config: Dict) -> str:
        """
        Select a class within a department based on persona preferences.
        
        Args:
            department: Department name
            persona_config: Persona configuration dictionary
        
        Returns:
            Selected class name
        """
        # Get available classes for this department
        available_classes = self.hierarchy.get(department, [])
        if not available_classes:
            return "Unknown"
        
        # Get persona's preferred classes for this department
        class_prefs = persona_config.get('class_preferences', {}).get(department, [])
        
        if class_prefs:
            # Filter to only preferred classes that exist in hierarchy
            preferred_classes = [c for c in class_prefs if c in available_classes]
            if preferred_classes:
                # 80% chance to pick from preferred classes, 20% random
                if np.random.rand() < 0.8:
                    return np.random.choice(preferred_classes)
        
        # Fallback to random selection from available classes
        return np.random.choice(available_classes)
    
    def _calculate_department_summaries(self, purchases: List[Dict]) -> Tuple[Dict, Dict]:
        """
        Calculate department-level summaries from individual purchases.
        
        Args:
            purchases: List of purchase dictionaries with 'department', 'class', 'value'
        
        Returns:
            Tuple of (dept_value_totals, dept_unit_totals) dictionaries
        """
        departments = list(self.hierarchy.keys())
        
        dept_value_totals = {f"dept_total_value_{d}": 0.0 for d in departments}
        dept_unit_totals = {f"dept_total_units_{d}": 0 for d in departments}
        
        for purchase in purchases:
            dept = purchase['department']
            value = purchase['value']
            
            dept_value_totals[f"dept_total_value_{dept}"] += value
            dept_unit_totals[f"dept_total_units_{dept}"] += 1
        
        return dept_value_totals, dept_unit_totals
    
    def generate_customer_data(self, n_customers: int = 500, 
                              dataset_type: str = 'enriched') -> pd.DataFrame:
        """
        Generate synthetic customer sales data.
        
        Args:
            n_customers: Number of customers to generate
            dataset_type: Type of dataset to generate
                - 'basic': Core RFM features + department totals (for clustering)
                - 'enriched': Full features + persona + class details (for analysis)
                - 'both': Generate both and save separately (returns enriched)
        
        Returns:
            DataFrame with customer sales summary features
        """
        # Generate customer IDs (preserve existing deterministic format)
        customer_ids = [f"CUST_{i:05d}" for i in range(1, n_customers + 1)]
        
        departments = list(self.hierarchy.keys())
        child_ages = ["Baby", "Child"]
        adult_sizes = ["XS", "S", "M", "L", "XL"]
        data = []
        
        # Reference "today" once for consistent date computations
        today = datetime.utcnow()
        
        # Choose generation mode
        if self.use_personas and self.personas:
            generation_mode = 'persona'
        else:
            generation_mode = 'legacy'
            # Legacy segment probabilities
            segment_probs = [0.20, 0.35, 0.30, 0.15]
            segments = np.random.choice([1, 2, 3, 4], size=n_customers, p=segment_probs)

        for i, cust_id in enumerate(customer_ids):
            # PERSONA-BASED or LEGACY GENERATION
            if generation_mode == 'persona':
                # Assign persona
                persona_name, persona_config = self._assign_persona()
                
                # Extract spending profile from persona
                spending_profile = persona_config.get('spending_profile', {})
                avg_order_value_range = spending_profile.get('avg_order_value', [50, 100])
                freq_range = spending_profile.get('frequency_per_month', [1, 3])
                typical_segment = spending_profile.get('typical_segment', 'medium_value_regular')
                
                # Generate customer characteristics based on persona
                avg_order_value = np.random.uniform(*avg_order_value_range)
                frequency_per_month = np.random.uniform(*freq_range)
                customer_lifetime_months = np.random.uniform(3, 36)
                
                # Calculate total purchases based on frequency and lifetime
                total_purchases = int(round(frequency_per_month * customer_lifetime_months))
                total_purchases = max(1, total_purchases)  # At least 1 purchase
                
                # Recency varies by segment activity
                if typical_segment == 'high_value_frequent':
                    recency_days = np.random.uniform(1, 30)
                    return_rate = np.random.uniform(0.01, 0.05)
                elif typical_segment == 'medium_value_regular':
                    recency_days = np.random.uniform(15, 60)
                    return_rate = np.random.uniform(0.05, 0.15)
                elif typical_segment == 'low_value_occasional':
                    recency_days = np.random.uniform(30, 120)
                    return_rate = np.random.uniform(0.10, 0.25)
                else:  # churned
                    recency_days = np.random.uniform(120, 365)
                    return_rate = np.random.uniform(0.20, 0.40)
                
                # Map typical_segment to numeric segment for backwards compatibility
                segment_map = {
                    'high_value_frequent': 1,
                    'medium_value_regular': 2,
                    'low_value_occasional': 3,
                    'churned_inactive': 4
                }
                segment = segment_map.get(typical_segment, 2)
                
            else:  # LEGACY MODE
                segment = segments[i]
                persona_name = None
                persona_config = None
                
                if segment == 1:  # High-value frequent
                    total_purchases = np.random.uniform(50, 100)
                    avg_order_value = np.random.uniform(150, 300)
                    recency_days = np.random.uniform(1, 30)
                    frequency_per_month = np.random.uniform(4, 8)
                    return_rate = np.random.uniform(0.01, 0.05)
                elif segment == 2:  # Medium-value regular
                    total_purchases = np.random.uniform(15, 50)
                    avg_order_value = np.random.uniform(75, 150)
                    recency_days = np.random.uniform(15, 60)
                    frequency_per_month = np.random.uniform(1.5, 4)
                    return_rate = np.random.uniform(0.05, 0.15)
                elif segment == 3:  # Low-value occasional
                    total_purchases = np.random.uniform(3, 15)
                    avg_order_value = np.random.uniform(30, 75)
                    recency_days = np.random.uniform(30, 120)
                    frequency_per_month = np.random.uniform(0.3, 1.5)
                    return_rate = np.random.uniform(0.10, 0.25)
                else:  # Churned/inactive
                    total_purchases = np.random.uniform(1, 5)
                    avg_order_value = np.random.uniform(20, 60)
                    recency_days = np.random.uniform(120, 365)
                    frequency_per_month = np.random.uniform(0.05, 0.3)
                    return_rate = np.random.uniform(0.20, 0.40)
                
                customer_lifetime_months = np.random.uniform(3, 36)

            # Optional: Generate realistic profile fields with Faker
            profile = {}
            if self._faker is not None and dataset_type in ['enriched', 'both']:
                first_name = self._faker.first_name()
                last_name = self._faker.last_name()
                email = self._faker.email()
                phone = self._faker.phone_number()
                street = self._faker.street_address()
                city = self._faker.city()
                state = getattr(self._faker, 'state_abbr', lambda: self._faker.state())()
                postcode = self._faker.postcode()
                country = getattr(self._faker, 'current_country', lambda: 'USA')()
                profile = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'phone': phone,
                    'address': street,
                    'city': city,
                    'state': state,
                    'zip_code': postcode,
                    'country': country,
                }

            # Calculate derived metrics
            total_revenue = total_purchases * avg_order_value
            
            # Simulate department/class purchases with proper hierarchy
            purchases_list = []
            
            for _ in range(int(round(total_purchases))):
                if generation_mode == 'persona' and persona_config:
                    # Use persona's department/class preferences
                    dept = self._select_department_for_persona(persona_config)
                    cls = self._select_class_for_department(dept, persona_config)
                else:
                    # Random selection (legacy)
                    dept = np.random.choice(departments)
                    dept_classes = self.hierarchy[dept]
                    cls = np.random.choice(dept_classes) if dept_classes else "Unknown"
                
                value = np.random.uniform(10, avg_order_value)
                purchases_list.append({
                    'department': dept,
                    'class': cls,
                    'value': value
                })
            
            # Calculate department summaries
            dept_totals, dept_units = self._calculate_department_summaries(purchases_list)
            
            # Calculate class-level summaries (only for enriched dataset)
            all_classes = [cls for classes in self.hierarchy.values() for cls in classes]
            class_totals = {f"class_total_value_{c}": 0.0 for c in all_classes}
            class_units = {f"class_total_units_{c}": 0 for c in all_classes}
            
            for purchase in purchases_list:
                cls = purchase['class']
                value = purchase['value']
                class_totals[f"class_total_value_{cls}"] += value
                class_units[f"class_total_units_{cls}"] += 1
            
            # Age/size counts (for enriched dataset)
            child_age_counts = {f"count_{age}": 0 for age in child_ages}
            adult_size_counts = {f"count_size_{size}": 0 for size in adult_sizes}
            
            for _ in range(int(round(total_purchases))):
                if np.random.rand() < 0.2:
                    age = np.random.choice(child_ages)
                    child_age_counts[f"count_{age}"] += 1
                else:
                    size = np.random.choice(adult_sizes)
                    adult_size_counts[f"count_size_{size}"] += 1

            # Derive a signup_date consistent with lifetime months
            signup_days = int(round(customer_lifetime_months * 30))
            signup_date = (today - timedelta(days=max(signup_days, 0))).date()

            # Build row based on dataset type
            row = {
                'customer_id': cust_id,
                'total_purchases': round(total_purchases),
                'total_revenue': round(total_revenue, 2),
                'avg_order_value': round(avg_order_value, 2),
                'recency_days': round(recency_days),
                'frequency_per_month': round(frequency_per_month, 2),
                'customer_lifetime_months': round(customer_lifetime_months, 1),
                'return_rate': round(return_rate, 3),
                'true_segment': segment,  # Ground truth for validation
                'signup_date': str(signup_date),
            }
            
            # Add department totals (included in both basic and enriched)
            row.update(dept_totals)
            row.update(dept_units)
            
            # Add enriched fields only for enriched dataset
            if dataset_type in ['enriched', 'both']:
                # Add persona information
                if persona_name:
                    row['persona_type'] = persona_name
                
                # Add Faker profile fields
                if profile:
                    row.update(profile)
                
                # Add class-level details
                row.update(class_totals)
                row.update(class_units)
                
                # Add age/size counts
                row.update(child_age_counts)
                row.update(adult_size_counts)
            
            data.append(row)
        
        df = pd.DataFrame(data)
        
        # If requested, generate both datasets
        if dataset_type == 'both':
            # Save basic dataset (clustering features only)
            basic_cols = ['customer_id', 'total_purchases', 'total_revenue', 
                         'avg_order_value', 'recency_days', 'frequency_per_month',
                         'customer_lifetime_months', 'return_rate', 'true_segment']
            
            # Add department totals to basic dataset
            dept_cols = [col for col in df.columns if col.startswith('dept_total_')]
            basic_cols.extend(dept_cols)
            
            basic_df = df[basic_cols].copy()
            basic_df.to_csv('data/customer_sales_data_basic.csv', index=False)
            print("✅ Basic dataset saved to data/customer_sales_data_basic.csv")
            
            # Return enriched dataset
            return df
        
        return df
