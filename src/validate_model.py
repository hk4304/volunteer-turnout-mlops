"""
Model Validation Script
Compares new model performance against baseline.
Fails if new model is significantly worse.
"""

import json
import sys
import os

# Configuration
R2_MINIMUM_THRESHOLD = 0.90  # Never deploy models below this
DEGRADATION_TOLERANCE = 0.02  # Allow 2% R² drop from baseline
MAE_MAX_INCREASE = 2.0  # Allow MAE increase up to 2 volunteers

def load_metrics(filepath):
    """Load metrics from JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def validate_model():
    """
    Validate new model against baseline.
    Returns 0 if model passes, 1 if it fails.
    """
    
    # Load new model metrics
    new_metrics = load_metrics('metrics/metrics.json')
    if not new_metrics:
        print("❌ ERROR: Could not load new model metrics")
        return 1
    
    # Load baseline metrics
    baseline_metrics = load_metrics('metrics/baseline_metrics.json')
    
    # If no baseline exists, accept first model (but check minimum threshold)
    if not baseline_metrics:
        print("📊 No baseline found - validating against minimum threshold only")
        if new_metrics['r2'] >= R2_MINIMUM_THRESHOLD:
            print(f"✅ PASSED: First model accepted (R²={new_metrics['r2']:.4f})")
            
            # Save as baseline for future comparisons
            with open('metrics/baseline_metrics.json', 'w') as f:
                json.dump(new_metrics, f, indent=2)
            
            return 0
        else:
            print(f"❌ FAILED: Model R²={new_metrics['r2']:.4f} below minimum {R2_MINIMUM_THRESHOLD}")
            return 1
    
    # Compare against baseline
    new_r2 = new_metrics['r2']
    baseline_r2 = baseline_metrics['r2']
    new_mae = new_metrics['mae']
    baseline_mae = baseline_metrics['mae']
    
    print("\n" + "="*60)
    print("MODEL VALIDATION REPORT")
    print("="*60)
    print(f"\n📊 New Model Performance:")
    print(f"   R² Score: {new_r2:.4f}")
    print(f"   MAE:      {new_mae:.2f} volunteers")
    print(f"   MSE:      {new_metrics['mse']:.2f}")
    
    print(f"\n📈 Baseline Model Performance:")
    print(f"   R² Score: {baseline_r2:.4f}")
    print(f"   MAE:      {baseline_mae:.2f} volunteers")
    print(f"   MSE:      {baseline_metrics['mse']:.2f}")
    
    print(f"\n📉 Performance Change:")
    r2_change = new_r2 - baseline_r2
    mae_change = new_mae - baseline_mae
    print(f"   R² Change:  {r2_change:+.4f} ({r2_change*100:+.2f}%)")
    print(f"   MAE Change: {mae_change:+.2f} volunteers")
    
    # Validation checks
    checks_passed = []
    checks_failed = []
    
    # Check 1: Minimum R² threshold
    if new_r2 >= R2_MINIMUM_THRESHOLD:
        checks_passed.append(f"✓ R² above minimum threshold ({R2_MINIMUM_THRESHOLD})")
    else:
        checks_failed.append(f"✗ R² below minimum threshold ({R2_MINIMUM_THRESHOLD})")
    
    # Check 2: R² degradation tolerance
    if new_r2 >= (baseline_r2 - DEGRADATION_TOLERANCE):
        checks_passed.append(f"✓ R² within degradation tolerance ({DEGRADATION_TOLERANCE})")
    else:
        checks_failed.append(f"✗ R² degraded more than {DEGRADATION_TOLERANCE}")
    
    # Check 3: MAE increase tolerance
    if new_mae <= (baseline_mae + MAE_MAX_INCREASE):
        checks_passed.append(f"✓ MAE increase acceptable ({MAE_MAX_INCREASE} volunteers)")
    else:
        checks_failed.append(f"✗ MAE increased more than {MAE_MAX_INCREASE} volunteers")
    
    # Display results
    print(f"\n🔍 Validation Checks:")
    for check in checks_passed:
        print(f"   {check}")
    for check in checks_failed:
        print(f"   {check}")
    
    print("\n" + "="*60)
    
    # Decision
    if len(checks_failed) == 0:
        print("✅ VALIDATION PASSED: Deploying new model")
        print("="*60 + "\n")
        
        # Update baseline
        with open('metrics/baseline_metrics.json', 'w') as f:
            json.dump(new_metrics, f, indent=2)
        print("📝 Updated baseline metrics")
        
        return 0
    else:
        print("❌ VALIDATION FAILED: Keeping current model")
        print("="*60 + "\n")
        print("💡 Recommendation: Review hyperparameters and try again")
        return 1

if __name__ == "__main__":
    sys.exit(validate_model())
