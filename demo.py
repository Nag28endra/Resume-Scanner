#!/usr/bin/env python3
"""
Demo script showing how to use the Resume Scanner programmatically.
"""

import sys
import os

# Add project root to path so the `src` package can be imported
sys.path.insert(0, os.path.dirname(__file__))

from src.model.train import build_training_dataset
from src.model.inference import build_resume_index, rank_resumes

def main():
    # Path to resume data
    data_dir = os.path.join(os.path.dirname(__file__), 'data', 'raw')

    print("Loading and processing resumes...")
    resumes = build_training_dataset(data_dir)

    if not resumes:
        print("No resumes found in data/raw directory.")
        print("Please add some PDF, DOCX, or TXT resume files to data/raw/")
        return

    print(f"Loaded {len(resumes)} resumes")

    print("Building semantic index...")
    resume_index = build_resume_index(resumes)
    print("Index built successfully")

    # Example job description
    job_description = """
    We are looking for a Python developer with experience in machine learning and web development.
    Required skills: Python, machine learning, SQL, React, AWS.
    Experience: 3+ years in software development.
    """

    print("\nScoring resumes against job description...")
    results = rank_resumes(job_description, resume_index, top_k=3)

    print("\nTop 3 matches:")
    print("-" * 50)

    for i, result in enumerate(results, 1):
        print(f"{i}. {result['file_name']}")
        print(f"   Score: {result['final_score']}/100")
        print(f"   Decision: {result['decision']}")
        print(f"   Reason: {result['reason']}")
        print()

if __name__ == "__main__":
    main()