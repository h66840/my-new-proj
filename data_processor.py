"""
Data Processing Module for Package Tracker
==========================================

This module provides enhanced data processing capabilities for the package tracking system.
It includes functions for data cleaning, transformation, and validation.
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional


class DataProcessor:
    """Enhanced data processor for package tracking data."""
    
    def __init__(self):
        self.processed_count = 0
        self.error_count = 0
        
    def clean_package_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and standardize package data.
        
        Args:
            raw_data: Raw package data dictionary
            
        Returns:
            Cleaned package data dictionary
        """
        try:
            cleaned_data = {}
            
            # Clean tracking number
            if 'tracking_number' in raw_data:
                tracking_num = str(raw_data['tracking_number']).strip().upper()
                cleaned_data['tracking_number'] = re.sub(r'[^A-Z0-9]', '', tracking_num)
            
            # Standardize status
            if 'status' in raw_data:
                status = str(raw_data['status']).lower().strip()
                status_mapping = {
                    'in transit': 'IN_TRANSIT',
                    'delivered': 'DELIVERED',
                    'pending': 'PENDING',
                    'shipped': 'SHIPPED',
                    'out for delivery': 'OUT_FOR_DELIVERY'
                }
                cleaned_data['status'] = status_mapping.get(status, 'UNKNOWN')
            
            # Clean location data
            if 'location' in raw_data:
                location = str(raw_data['location']).strip().title()
                cleaned_data['location'] = location
            
            # Parse and validate timestamp
            if 'timestamp' in raw_data:
                timestamp = self._parse_timestamp(raw_data['timestamp'])
                cleaned_data['timestamp'] = timestamp
            
            # Clean recipient information
            if 'recipient' in raw_data:
                recipient = str(raw_data['recipient']).strip().title()
                cleaned_data['recipient'] = recipient
                
            self.processed_count += 1
            return cleaned_data
            
        except Exception as e:
            self.error_count += 1
            raise ValueError(f"Error cleaning package data: {str(e)}")
    
    def transform_for_analytics(self, package_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform package data for analytics purposes.
        
        Args:
            package_data: Cleaned package data
            
        Returns:
            Transformed data suitable for analytics
        """
        analytics_data = {
            'package_id': package_data.get('tracking_number'),
            'status_code': package_data.get('status'),
            'location_normalized': self._normalize_location(package_data.get('location', '')),
            'delivery_date': package_data.get('timestamp'),
            'processing_timestamp': datetime.now().isoformat(),
            'data_quality_score': self._calculate_quality_score(package_data)
        }
        
        return analytics_data
    
    def validate_package_data(self, package_data: Dict[str, Any]) -> bool:
        """
        Validate package data integrity.
        
        Args:
            package_data: Package data to validate
            
        Returns:
            True if data is valid, False otherwise
        """
        required_fields = ['tracking_number', 'status', 'timestamp']
        
        # Check required fields
        for field in required_fields:
            if field not in package_data or not package_data[field]:
                return False
        
        # Validate tracking number format
        tracking_num = package_data['tracking_number']
        if not re.match(r'^[A-Z0-9]{8,20}$', tracking_num):
            return False
        
        # Validate status
        valid_statuses = ['IN_TRANSIT', 'DELIVERED', 'PENDING', 'SHIPPED', 'OUT_FOR_DELIVERY']
        if package_data['status'] not in valid_statuses:
            return False
        
        return True
    
    def batch_process(self, raw_data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process multiple package records in batch.
        
        Args:
            raw_data_list: List of raw package data dictionaries
            
        Returns:
            Processing results summary
        """
        processed_data = []
        errors = []
        
        for i, raw_data in enumerate(raw_data_list):
            try:
                # Clean data
                cleaned = self.clean_package_data(raw_data)
                
                # Validate data
                if self.validate_package_data(cleaned):
                    # Transform for analytics
                    analytics_data = self.transform_for_analytics(cleaned)
                    processed_data.append(analytics_data)
                else:
                    errors.append(f"Record {i}: Validation failed")
                    
            except Exception as e:
                errors.append(f"Record {i}: {str(e)}")
        
        return {
            'processed_records': processed_data,
            'total_processed': len(processed_data),
            'total_errors': len(errors),
            'errors': errors,
            'success_rate': len(processed_data) / len(raw_data_list) if raw_data_list else 0
        }
    
    def _parse_timestamp(self, timestamp_str: str) -> str:
        """Parse various timestamp formats to ISO format."""
        try:
            # Try different timestamp formats
            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d',
                '%m/%d/%Y %H:%M:%S',
                '%m/%d/%Y'
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(str(timestamp_str).strip(), fmt)
                    return dt.isoformat()
                except ValueError:
                    continue
            
            # If no format matches, return current timestamp
            return datetime.now().isoformat()
            
        except Exception:
            return datetime.now().isoformat()
    
    def _normalize_location(self, location: str) -> str:
        """Normalize location strings for consistency."""
        if not location:
            return "UNKNOWN"
        
        # Remove extra spaces and standardize format
        normalized = re.sub(r'\s+', ' ', location.strip().upper())
        
        # Common location abbreviations
        abbreviations = {
            'DISTRIBUTION CENTER': 'DC',
            'SORTING FACILITY': 'SF',
            'LOCAL FACILITY': 'LF'
        }
        
        for full, abbrev in abbreviations.items():
            normalized = normalized.replace(full, abbrev)
        
        return normalized
    
    def _calculate_quality_score(self, data: Dict[str, Any]) -> float:
        """Calculate data quality score based on completeness and validity."""
        score = 0.0
        total_checks = 5
        
        # Check for required fields
        if data.get('tracking_number'):
            score += 0.3
        if data.get('status'):
            score += 0.2
        if data.get('timestamp'):
            score += 0.2
        if data.get('location'):
            score += 0.15
        if data.get('recipient'):
            score += 0.15
        
        return min(score, 1.0)


def integrate_with_package_tracker(processor: DataProcessor, tracker_data: List[Dict]) -> Dict:
    """
    Integration function to connect with existing package tracker.
    
    Args:
        processor: DataProcessor instance
        tracker_data: Data from package tracker
        
    Returns:
        Processed and enhanced tracking data
    """
    # Process the data using the new processor
    results = processor.batch_process(tracker_data)
    
    # Add integration metadata
    results['integration_timestamp'] = datetime.now().isoformat()
    results['processor_version'] = '1.0.0'
    
    return results