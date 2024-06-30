import argparse
import numpy as np
from scipy import stats

def calculate_sample_sizes(total_size):
    confidence_levels = np.linspace(0, 1, num=101)  # Generate confidence levels from 0% to 100%
    sample_sizes = []
    
    for confidence in confidence_levels:
        try:
            z_score = stats.norm.ppf(confidence + (1 - confidence) / 2)
            sample_size = (z_score**2) / (0.05**2)  # Assuming margin of error (0.05) and standard deviation (1)
            sample_size = int(np.ceil(sample_size))
            sample_sizes.append((int(confidence * 100), sample_size))  # Store confidence level as integer percentage
        except OverflowError:
            sample_sizes.append((int(confidence * 100), float('inf')))  # Handle overflow gracefully
    
    return sample_sizes

def calculate_sample_size(total_size, desired_confidence):
    try:
        if desired_confidence < 0 or desired_confidence > 100:
            raise ValueError("Confidence level must be between 0 and 100.")
        
        desired_confidence = desired_confidence / 100.0  # Convert percentage to fraction
        z_score = stats.norm.ppf(desired_confidence + (1 - desired_confidence) / 2)
        sample_size = (z_score**2) / (0.05**2)  # Assuming margin of error (0.05) and standard deviation (1)
        sample_size = int(np.ceil(sample_size))
        return sample_size
    except ValueError as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate sample sizes based on confidence levels.")
    parser.add_argument("--total_size", type=int, help="Total size of the population")
    parser.add_argument("--confidence", type=float, help="Desired confidence level (0 to 100)")
    args = parser.parse_args()

    if args.total_size and args.confidence:
        if args.total_size > 0 and 0 <= args.confidence <= 100:
            # Calculate required sample size for given total size and confidence level
            sample_size = calculate_sample_size(args.total_size, args.confidence)
            if sample_size is not None:
                print(f"Required Sample Size for {args.confidence}% confidence level: {sample_size}")
        else:
            print("Error: Invalid input values. Please ensure total size > 0 and 0 <= confidence <= 100.")
    
    elif args.total_size:
        if args.total_size > 0:
            # Calculate sample sizes for increasing confidence levels given total size
            sample_sizes = calculate_sample_sizes(args.total_size)
            print("Sample Sizes for Increasing Confidence Levels:")
            for confidence, size in sample_sizes:
                print(f"Confidence Level {confidence}%: Sample Size = {size}")
        else:
            print("Error: Total size must be greater than 0.")
    
    else:
        parser.print_help()
