"""
Basic tests for customer segmentation components.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import numpy as np
import pandas as pd
from customer_segmentation import (
    RetailDataGenerator,
    FuzzyCustomerSegmentation,
    NeuralCustomerSegmentation,
    ClusterEnrichment
)


class TestDataGenerator(unittest.TestCase):
    """Test retail data generator."""
    
    def test_generate_customer_data(self):
        """Test customer data generation."""
        generator = RetailDataGenerator(seed=42)
        data = generator.generate_customer_data(n_customers=100)
        
        self.assertEqual(len(data), 100)
        self.assertIn('customer_id', data.columns)
        self.assertIn('total_purchases', data.columns)
        self.assertIn('total_revenue', data.columns)
        
    def test_data_quality(self):
        """Test generated data quality."""
        generator = RetailDataGenerator(seed=42)
        data = generator.generate_customer_data(n_customers=100)
        
        # Check no missing values
        self.assertEqual(data.isnull().sum().sum(), 0)
        
        # Check positive values for key metrics
        self.assertTrue((data['total_purchases'] > 0).all())
        self.assertTrue((data['total_revenue'] > 0).all())


class TestFuzzyClustering(unittest.TestCase):
    """Test fuzzy clustering."""
    
    def setUp(self):
        """Set up test data."""
        generator = RetailDataGenerator(seed=42)
        self.data = generator.generate_customer_data(n_customers=100)
        
    def test_fit_predict(self):
        """Test fuzzy clustering fit and predict."""
        model = FuzzyCustomerSegmentation(n_clusters=4, seed=42)
        labels, membership = model.fit_predict(self.data)
        
        self.assertEqual(len(labels), len(self.data))
        self.assertEqual(membership.shape[1], len(self.data))
        self.assertEqual(membership.shape[0], 4)
        
        # Check membership sums to 1 for each customer
        membership_sums = membership.sum(axis=0)
        np.testing.assert_array_almost_equal(membership_sums, np.ones(len(self.data)))
        
    def test_cluster_centers(self):
        """Test cluster center extraction."""
        model = FuzzyCustomerSegmentation(n_clusters=4, seed=42)
        model.fit(self.data)
        centers = model.get_cluster_centers()
        
        self.assertEqual(len(centers), 4)
        self.assertTrue(all(col in centers.columns for col in ['total_purchases', 'total_revenue']))
        
    def test_evaluate(self):
        """Test clustering evaluation."""
        model = FuzzyCustomerSegmentation(n_clusters=4, seed=42)
        model.fit(self.data)
        metrics = model.evaluate(self.data)
        
        self.assertIn('silhouette_score', metrics)
        self.assertIn('partition_coefficient', metrics)
        self.assertIn('partition_entropy', metrics)


class TestNeuralClustering(unittest.TestCase):
    """Test neural network clustering."""
    
    def setUp(self):
        """Set up test data."""
        generator = RetailDataGenerator(seed=42)
        self.data = generator.generate_customer_data(n_customers=100)
        
    def test_fit_predict(self):
        """Test neural clustering fit and predict."""
        model = NeuralCustomerSegmentation(n_clusters=4, epochs=10, seed=42)
        labels = model.fit_predict(self.data, verbose=0)
        
        self.assertEqual(len(labels), len(self.data))
        self.assertTrue(all(0 <= label < 4 for label in labels))
        
    def test_cluster_centers(self):
        """Test cluster center extraction."""
        model = NeuralCustomerSegmentation(n_clusters=4, epochs=10, seed=42)
        model.fit(self.data, verbose=0)
        centers = model.get_cluster_centers(self.data)
        
        self.assertEqual(len(centers), 4)


class TestClusterEnrichment(unittest.TestCase):
    """Test cluster enrichment."""
    
    def setUp(self):
        """Set up test data and clustering."""
        generator = RetailDataGenerator(seed=42)
        self.data = generator.generate_customer_data(n_customers=100)
        
        model = FuzzyCustomerSegmentation(n_clusters=4, seed=42)
        self.labels, _ = model.fit_predict(self.data)
        self.centers = model.get_cluster_centers()
        
    def test_enrich_clusters(self):
        """Test cluster enrichment."""
        enrichment = ClusterEnrichment()
        profiles = enrichment.enrich_clusters(self.data, self.labels, self.centers)
        
        self.assertEqual(len(profiles), 4)
        for profile in profiles.values():
            self.assertIn('segment_name', profile)
            self.assertIn('description', profile)
            self.assertIn('characteristics', profile)
            self.assertIn('interaction_strategies', profile)
            
    def test_characteristics(self):
        """Test characteristics analysis."""
        enrichment = ClusterEnrichment()
        characteristics = enrichment.analyze_cluster_characteristics(
            self.data, self.labels, self.centers
        )
        
        for char in characteristics.values():
            self.assertIn('size', char)
            self.assertIn('avg_total_revenue', char)
            self.assertIn('avg_frequency', char)


if __name__ == '__main__':
    unittest.main()
