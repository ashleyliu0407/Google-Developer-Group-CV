#!/usr/bin/env python3
"""
Dataset download script for ASL Classifier
Handles the download and setup of the ASL dataset using Kaggle API
"""

import os
import json
import argparse
from pathlib import Path
import kaggle
import zipfile
import shutil

def setup_kaggle_credentials(kaggle_json_path: str = None):
    """Set up Kaggle credentials from kaggle.json file"""
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_dir.mkdir(exist_ok=True)
    
    kaggle_json = kaggle_dir / 'kaggle.json'
    
    if kaggle_json_path:
        # Copy provided credentials
        with open(kaggle_json_path, 'r') as src, open(kaggle_json, 'w') as dst:
            credentials = json.load(src)
            json.dump(credentials, dst)
    elif not kaggle_json.exists():
        raise FileNotFoundError(
            "Kaggle credentials not found. Please provide a kaggle.json file or "
            "place it in ~/.kaggle/kaggle.json"
        )
    
    # Set proper permissions
    os.chmod(kaggle_json, 0o600)

def download_dataset(dataset_name: str = "ayuraj/asl-dataset", 
                    output_path: str = "asl_dataset"):
    """Download and extract the ASL dataset"""
    try:
        print(f"Downloading dataset: {dataset_name}")
        
        # Create output directory if it doesn't exist
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Download the dataset
        kaggle.api.dataset_download_files(dataset_name, quiet=False)
        
        # Extract the dataset
        zip_file = "asl-dataset.zip"
        if os.path.exists(zip_file):
            print(f"Extracting dataset to {output_path}")
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(output_path)
            
            # Clean up zip file
            os.remove(zip_file)
            print("Dataset setup complete!")
            
            # Create a model_serialization directory if it doesn't exist
            model_dir = Path("model_serialization")
            model_dir.mkdir(exist_ok=True)
            
        else:
            raise FileNotFoundError(f"Downloaded file {zip_file} not found")
            
    except Exception as e:
        print(f"Error downloading dataset: {str(e)}")
        raise

def cleanup_dataset(output_path: str = "asl_dataset"):
    """Optional cleanup of dataset directory"""
    try:
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
            print(f"Cleaned up {output_path} directory")
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Download and setup ASL dataset')
    parser.add_argument('--kaggle-json', type=str, 
                       help='Path to kaggle.json file')
    parser.add_argument('--output-path', type=str, default='asl_dataset',
                       help='Path where dataset should be extracted')
    parser.add_argument('--cleanup', action='store_true',
                       help='Clean up existing dataset before downloading')
    
    args = parser.parse_args()
    
    try:
        if args.cleanup:
            cleanup_dataset(args.output_path)
            
        setup_kaggle_credentials(args.kaggle_json)
        download_dataset(output_path=args.output_path)
        
    except Exception as e:
        print(f"Error setting up dataset: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
