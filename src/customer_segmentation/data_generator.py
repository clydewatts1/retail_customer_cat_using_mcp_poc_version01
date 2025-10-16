"""
Data generator for retail customer sales data.
Generates synthetic sales data for customer segmentation proof of concept.
"""
import numpy as np
import pandas as pd
from typing import Optional


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
    
    def __init__(self, seed: Optional[int] = 42):
        """
        Initialize the data generator.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        np.random.seed(seed)
    
    def generate_customer_data(self, n_customers: int = 500) -> pd.DataFrame:
        """
        Generate synthetic customer sales data.
        
        Args:
            n_customers: Number of customers to generate
        Returns:
            DataFrame with customer sales summary features
        """
        # Generate customer IDs
        customer_ids = [f"CUST_{i:05d}" for i in range(1, n_customers + 1)]
        # Define customer segments with different characteristics
        segment_probs = [0.20, 0.35, 0.30, 0.15]
        segments = np.random.choice([1, 2, 3, 4], size=n_customers, p=segment_probs)
        # Example departments, classes, and sizes (should match your hierarchy)
        departments = ["Accessories & Footwear", "Health & Wellness", "Home & Lifestyle"]
        classes = ["Bags & Wallets", "Soft & Hard Accessories", "Consumables", "Personal Care", "Bedding"]
        child_ages = ["Baby", "Child"]
        adult_sizes = ["XS", "S", "M", "L", "XL"]
        data = []
        for i, (cust_id, segment) in enumerate(zip(customer_ids, segments)):
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

            # Calculate derived metrics
            total_revenue = total_purchases * avg_order_value
            customer_lifetime_months = np.random.uniform(3, 36)

            # Simulate department/class purchases and size breakdowns
            dept_totals = {f"dept_total_value_{d}": 0.0 for d in departments}
            dept_units = {f"dept_total_units_{d}": 0 for d in departments}
            class_totals = {f"class_total_value_{c}": 0.0 for c in classes}
            class_units = {f"class_total_units_{c}": 0 for c in classes}
            child_age_counts = {f"count_{age}": 0 for age in child_ages}
            adult_size_counts = {f"count_size_{size}": 0 for size in adult_sizes}

            for _ in range(int(round(total_purchases))):
                dept = np.random.choice(departments)
                cls = np.random.choice(classes)
                value = np.random.uniform(10, avg_order_value)
                dept_totals[f"dept_total_value_{dept}"] += value
                dept_units[f"dept_total_units_{dept}"] += 1
                class_totals[f"class_total_value_{cls}"] += value
                class_units[f"class_total_units_{cls}"] += 1
                # Assign to child age or adult size
                if np.random.rand() < 0.2:
                    age = np.random.choice(child_ages)
                    child_age_counts[f"count_{age}"] += 1
                else:
                    size = np.random.choice(adult_sizes)
                    adult_size_counts[f"count_size_{size}"] += 1

            row = {
                'customer_id': cust_id,
                'total_purchases': round(total_purchases),
                'total_revenue': round(total_revenue, 2),
                'avg_order_value': round(avg_order_value, 2),
                'recency_days': round(recency_days),
                'frequency_per_month': round(frequency_per_month, 2),
                'customer_lifetime_months': round(customer_lifetime_months, 1),
                'return_rate': round(return_rate, 3),
                'true_segment': segment  # Ground truth for validation
            }
            row.update(dept_totals)
            row.update(dept_units)
            row.update(class_totals)
            row.update(class_units)
            row.update(child_age_counts)
            row.update(adult_size_counts)
            data.append(row)
        return pd.DataFrame(data)
