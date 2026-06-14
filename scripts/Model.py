import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_absolute_error, r2_score
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
filepath_Training = BASE_DIR / 'data set' / 'training_data.csv'

# Load the training dataset built in Phase 2
training_data = pd.read_csv(filepath_Training)

# Split into features (X) and target (y)
X = training_data.drop(columns=['bacterium', 'antibiotic', 'observed_resistance', 'n_isolates'])
y = training_data['observed_resistance']

# Train final model on all data and save
final_model = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=3,
    random_state=42
)


final_model.fit(X, y)

# --- Leave-One-Out Validation ---
loo = LeaveOneOut()
predictions = []
actuals = []

for train_index, test_index in loo.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    model = GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
    model.fit(X_train, y_train)

    pred = model.predict(X_test)[0]
    predictions.append(pred)
    actuals.append(y_test.values[0])

# --- Model Metrics ---
model_mae = mean_absolute_error(actuals, predictions)
model_r2 = r2_score(actuals, predictions)

# --- Baseline: always predict the mean ---
baseline_pred = np.mean(actuals)
baseline_mae = mean_absolute_error(actuals, [baseline_pred] * len(actuals))

# --- Print Results ---
print("=== Model Performance ===")
print(f"Model MAE:    {model_mae:.4f}")
print(f"Model R²:     {model_r2:.4f}")
print()
print("=== Baseline (predict the mean) ===")
print(f"Baseline MAE: {baseline_mae:.4f}")
print()
print("=== Comparison ===")
improvement = (baseline_mae - model_mae) / baseline_mae * 100
print(f"Improvement over baseline: {improvement:.1f}%")
if model_mae < baseline_mae:
    print("Model beats baseline — mechanism features carry predictive signal.")
elif model_mae > baseline_mae:
    print("Model is worse than baseline — check for overfitting or data issues.")
else:
    print("Model matches baseline — features don't appear to help.")

# --- Save predictions to CSV ---
results = pd.DataFrame({
    'bacterium': training_data['bacterium'] if 'bacterium' in training_data.columns else range(len(actuals)),
    'antibiotic': training_data['antibiotic'] if 'antibiotic' in training_data.columns else range(len(actuals)),
    'observed': actuals,
    'predicted': [round(p, 4) for p in predictions]
})
results.to_csv(BASE_DIR / 'website' / 'data' / 'predictions.csv', index=False)

# --- Save metrics to text file ---
with open('metrics.txt', 'w') as f:
    f.write("Model Performance\n")
    f.write(f"  MAE:  {model_mae:.4f}\n")
    f.write(f"  R²:   {model_r2:.4f}\n\n")
    f.write("Baseline (predict the mean)\n")
    f.write(f"  MAE:  {baseline_mae:.4f}\n\n")
    f.write(f"Improvement over baseline: {improvement:.1f}%\n")

print()
print("Saved predictions.csv and metrics.txt")

# --- Predict ALL pairs (grounded + ungrounded) ---
output_df = pd.read_csv(BASE_DIR  / 'data set' / 'supertable.csv')


# Use the actual mechanism columns from the supertable
feature_df = output_df.reindex(columns=X.columns, fill_value=0)

all_predictions = final_model.predict(feature_df)

# Merge observed values where they exist
observed_lookup = dict(zip(
    zip(results['bacterium'], results['antibiotic']),
    results['observed']
))

all_results = pd.DataFrame({
    'bacterium': output_df['Bacteria Name'],
    'antibiotic': output_df['Antibiotic Name'],
    'observed': [observed_lookup.get((b, a), None) for b, a in zip(output_df['Bacteria Name'], output_df['Antibiotic Name'])],
    'predicted': [round(p, 4) for p in all_predictions]
})

all_results.to_csv(BASE_DIR  / 'data set' / 'predictions.csv', index=False)
print(f"Saved predictions.csv: {len(all_results)} total pairs ({all_results['observed'].notna().sum()} with ATLAS data)")