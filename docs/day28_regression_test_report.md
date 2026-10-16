# CareFlow — Day 28: Regression Test Report

## 1. Objective

Document the automated regression tests for the CareFlow data validation pipeline and record the observed test results.

## 2. Test Environment

- **Project:** CareFlow — Clinical Pathway Process Mining
- **Language:** Python
- **Test framework:** Python `unittest`
- **Pipeline:** `analysis/run_validation_pipeline.py`
- **History tracker:** `analysis/track_validation_history.py`
- **Regression suite:** `analysis/test_validation_pipeline.py`

## 3. Test Results

| Test | Expected behavior | Result |
|---|---|---|
| Missing validation script | Pipeline exits with an error | PASS |
| Missing pipeline report | History tracker exits with an error | PASS |
| Invalid report schema | Missing required columns are rejected | PASS |
| Failed quality check | Pipeline reports failure and returns a nonzero exit code | PASS |
| Successful quality check | Pipeline produces a PASS report and returns exit code 0 | PASS |

**Observed result:** 5 tests passed; 0 tests failed.

## 4. Test Isolation

The regression tests use temporary directories for test scripts and reports. This helps prevent simulated test data from overwriting the project's actual validation reports and history files.

## 5. How to Run the Tests

From the project root directory, run:

```cmd
python -m unittest analysis.test_validation_pipeline -v
```

## 6. Conclusion

The five regression tests passed in the observed test run. They cover important missing-file, schema-validation, pipeline-failure, and pipeline-success scenarios.

These tests provide a repeatable check of the current pipeline behavior. They do not, by themselves, establish that every possible failure scenario has been tested.
