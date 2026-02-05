"""
Data Loader Module
------------------
This module handles loading and preprocessing data from various sources:
- CSV files (employee_master.csv)
- JSON files (attendance_logs_detailed.json)
- Excel files (leave_intelligence.xlsx)
- PDF files (Helix_Pro_Policy_v2.pdf)
"""

import pandas as pd
import json
import logging
from typing import List, Dict, Any
from datetime import datetime
import re

logger = logging.getLogger(__name__)


class DataLoader:
    """
    Handles loading and preprocessing data from various file formats.
    """
    
    def __init__(self):
        """Initialize the data loader."""
        self.loaded_data = {}
    
    def load_csv(self, file_path: str, encoding: str = 'utf-8') -> pd.DataFrame:
        """
        Load data from a CSV file.
        
        Args:
            file_path: Path to the CSV file
            encoding: File encoding (default: utf-8)
            
        Returns:
            DataFrame containing the CSV data
        """
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            logger.info(f"✓ Loaded CSV file: {file_path}")
            logger.info(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
            return df
        except Exception as e:
            logger.error(f"✗ Error loading CSV file {file_path}: {e}")
            raise
    
    def load_json(self, file_path: str, encoding: str = 'utf-8') -> Dict:
        """
        Load data from a JSON file.
        
        Args:
            file_path: Path to the JSON file
            encoding: File encoding (default: utf-8)
            
        Returns:
            Dictionary containing the JSON data
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                data = json.load(f)
            logger.info(f"✓ Loaded JSON file: {file_path}")
            logger.info(f"  Top-level keys: {len(data)}")
            return data
        except Exception as e:
            logger.error(f"✗ Error loading JSON file {file_path}: {e}")
            raise
    
    def load_excel(self, file_path: str, sheet_name: str = None) -> pd.DataFrame:
        """
        Load data from an Excel file.
        
        Args:
            file_path: Path to the Excel file
            sheet_name: Name of the sheet to load (None loads first sheet)
            
        Returns:
            DataFrame containing the Excel data
        """
        try:
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                logger.info(f"✓ Loaded Excel sheet '{sheet_name}' from: {file_path}")
            else:
                df = pd.read_excel(file_path)
                logger.info(f"✓ Loaded Excel file: {file_path}")
            
            logger.info(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
            return df
        except Exception as e:
            logger.error(f"✗ Error loading Excel file {file_path}: {e}")
            raise
    
    def get_excel_sheets(self, file_path: str) -> List[str]:
        """
        Get list of sheet names in an Excel file.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            List of sheet names
        """
        try:
            excel_file = pd.ExcelFile(file_path)
            sheets = excel_file.sheet_names
            logger.info(f"✓ Found {len(sheets)} sheets in {file_path}: {sheets}")
            return sheets
        except Exception as e:
            logger.error(f"✗ Error reading Excel sheets: {e}")
            raise
    
    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess a DataFrame.
        
        Args:
            df: DataFrame to clean
            
        Returns:
            Cleaned DataFrame
        """
        try:
            # Make a copy to avoid modifying original
            df_clean = df.copy()
            
            # Convert column names to lowercase and replace spaces with underscores
            df_clean.columns = [col.lower().replace(' ', '_') for col in df_clean.columns]
            
            # Handle missing values
            # For numeric columns, fill with 0
            numeric_cols = df_clean.select_dtypes(include=['float64', 'int64']).columns
            df_clean[numeric_cols] = df_clean[numeric_cols].fillna(0)
            
            # For string columns, fill with empty string
            string_cols = df_clean.select_dtypes(include=['object']).columns
            df_clean[string_cols] = df_clean[string_cols].fillna('')
            
            # Strip whitespace from string columns
            for col in string_cols:
                if df_clean[col].dtype == 'object':
                    df_clean[col] = df_clean[col].astype(str).str.strip()
            
            logger.info(f"✓ Cleaned DataFrame - {len(df_clean)} rows")
            return df_clean
        except Exception as e:
            logger.error(f"✗ Error cleaning DataFrame: {e}")
            raise
    
    def dataframe_to_documents(self, df: pd.DataFrame, id_field: str = None) -> List[Dict]:
        """
        Convert DataFrame to a list of documents (dictionaries).
        
        Args:
            df: DataFrame to convert
            id_field: Field to use as document ID
            
        Returns:
            List of documents
        """
        try:
            documents = df.to_dict('records')
            
            # If id_field specified, ensure it exists and is unique
            if id_field and id_field in df.columns:
                for doc in documents:
                    doc['_id'] = doc[id_field]
            
            logger.info(f"✓ Converted DataFrame to {len(documents)} documents")
            return documents
        except Exception as e:
            logger.error(f"✗ Error converting DataFrame to documents: {e}")
            raise
    
    def flatten_json(self, data: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """
        Flatten a nested JSON structure.
        
        Args:
            data: Dictionary to flatten
            parent_key: Parent key for nested items
            sep: Separator between keys
            
        Returns:
            Flattened dictionary
        """
        items = []
        
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            
            if isinstance(v, dict):
                items.extend(self.flatten_json(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Keep lists as is, don't flatten
                items.append((new_key, v))
            else:
                items.append((new_key, v))
        
        return dict(items)
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text
        """
        try:
            import PyPDF2
            
            text = ""
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            
            logger.info(f"✓ Extracted {len(text)} characters from PDF: {file_path}")
            return text
        except ImportError:
            logger.error("PyPDF2 not installed. Install with: pip install PyPDF2")
            raise
        except Exception as e:
            logger.error(f"✗ Error extracting text from PDF: {e}")
            raise
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk in characters
            overlap: Number of characters to overlap between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size // 2:  # Only break if reasonable
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        logger.info(f"✓ Created {len(chunks)} text chunks")
        return chunks
    
    def load_helix_employee_data(self, csv_path: str) -> List[Dict]:
        """
        Load and process Helix employee master data.
        
        Args:
            csv_path: Path to employee_master.csv
            
        Returns:
            List of employee documents
        """
        try:
            df = self.load_csv(csv_path)
            df = self.clean_dataframe(df)
            
            # Convert joining_date to datetime
            if 'joining_date' in df.columns:
                df['joining_date'] = pd.to_datetime(df['joining_date'], errors='coerce')
            
            documents = self.dataframe_to_documents(df, id_field='emp_id')
            logger.info(f"✓ Processed {len(documents)} employee records")
            return documents
        except Exception as e:
            logger.error(f"✗ Error loading employee data: {e}")
            raise
    
    def load_helix_attendance_data(self, json_path: str) -> List[Dict]:
        """
        Load and process Helix attendance logs.
        
        Args:
            json_path: Path to attendance_logs_detailed.json
            
        Returns:
            List of attendance documents
        """
        try:
            data = self.load_json(json_path)
            
            documents = []
            for emp_id, emp_data in data.items():
                # Process each employee's attendance records
                if 'records' in emp_data:
                    for record in emp_data['records']:
                        doc = {
                            '_id': f"{emp_id}_{record.get('date', '')}",
                            'emp_id': emp_id,
                            'date': record.get('date'),
                            'check_in': record.get('check_in'),
                            'check_out': record.get('check_out'),
                            'location_logged': record.get('location_logged'),
                            'device': record.get('metadata', {}).get('device'),
                            'ip': record.get('metadata', {}).get('ip'),
                            'period': emp_data.get('period'),
                        }
                        documents.append(doc)
            
            logger.info(f"✓ Processed {len(documents)} attendance records")
            return documents
        except Exception as e:
            logger.error(f"✗ Error loading attendance data: {e}")
            raise
    
    def load_helix_leave_data(self, excel_path: str) -> Dict[str, List[Dict]]:
        """
        Load and process Helix leave intelligence data.
        
        Args:
            excel_path: Path to leave_intelligence.xlsx
            
        Returns:
            Dictionary with 'history' and 'balances' keys
        """
        try:
            result = {}
            
            # Load Leave_History sheet
            df_history = self.load_excel(excel_path, sheet_name='Leave_History')
            df_history = self.clean_dataframe(df_history)
            result['history'] = self.dataframe_to_documents(df_history)
            
            # Load Available_Balances sheet
            df_balances = self.load_excel(excel_path, sheet_name='Available_Balances')
            df_balances = self.clean_dataframe(df_balances)
            result['balances'] = self.dataframe_to_documents(df_balances, id_field='emp_id')
            
            logger.info(f"✓ Processed leave data: {len(result['history'])} history records, "
                       f"{len(result['balances'])} balance records")
            return result
        except Exception as e:
            logger.error(f"✗ Error loading leave data: {e}")
            raise
