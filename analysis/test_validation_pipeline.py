"""
CareFlow - Day 26
Automated regression tests for the validation pipeline.

All test files are created inside temporary directories.
The real CareFlow reports and validation history remain untouched.
"""

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = Path(__file__).resolve().parent

PIPELINE_SCRIPT = ANALYSIS_DIR / "run_validation_pipeline.py"
HISTORY_SCRIPT = ANALYSIS_DIR / "track_validation_history.py"

REQUIRED_PIPELINE_COLUMNS = {
    "Pipeline_Name",
    "Total_Checks",
    "Passed_Checks",
    "Failed_Checks",
    "Pipeline_Status",
    "Unexpected_Statuses",
}


class TestValidationPipeline(unittest.TestCase):

    def run_script(self, script_path, working_directory):
        """Run a Python script and return its completed process."""
        return subprocess.run(
            [sys.executable, str(script_path)],
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=60,
        )

    def create_fake_validator(self, folder, should_fail=False):
        """Create a temporary validator with the real report schema."""
        validator_path = folder / "validate_operational_data.py"

        status = "FAIL" if should_fail else "PASS"
        details = (
            "Simulated failure for testing"
            if should_fail
            else "Simulated success for testing"
        )

        code = f"""
import csv
from pathlib import Path

report_path = Path(__file__).resolve().parent / "data_quality_report.csv"

with report_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["Dataset", "Check_Name", "Status", "Details"]
    )
    writer.writeheader()
    writer.writerow({{
        "Dataset": "Test dataset",
        "Check_Name": "Simulated check",
        "Status": {status!r},
        "Details": {details!r}
    }})

print("Temporary validation report created.")
"""
        validator_path.write_text(code, encoding="utf-8")
        return validator_path
        validator_path.write_text(code, encoding="utf-8")
        return validator_path, report_path

    def create_fake_pipeline_report(self, folder, valid=True):
        """Create a temporary pipeline report for history-tracker tests."""
        report_path = folder / "validation_pipeline_report.csv"

        if valid:
            row = {
                "Pipeline_Name": "CareFlow Test",
                "Total_Checks": "1",
                "Passed_Checks": "1",
                "Failed_Checks": "0",
                "Pipeline_Status": "PASS",
                "Unexpected_Statuses": "0",
            }
            columns = list(REQUIRED_PIPELINE_COLUMNS)
        else:
            row = {
                "Wrong_Column": "invalid",
                "Another_Wrong_Column": "data",
            }
            columns = list(row.keys())

        with report_path.open(
            "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerow(row)

        return report_path

    def test_missing_validation_script(self):
        """Pipeline should fail clearly if the validator is missing."""
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            script = folder / "run_validation_pipeline.py"

            # Copy the actual pipeline runner into the isolated folder.
            script.write_text(
                PIPELINE_SCRIPT.read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            result = self.run_script(script, folder)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "Validation script not found",
                result.stdout + result.stderr,
            )

    def test_missing_pipeline_report(self):
        """History tracker should fail if the report is missing."""
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            script = folder / "track_validation_history.py"

            script.write_text(
                HISTORY_SCRIPT.read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            result = self.run_script(script, folder)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "Pipeline report not found",
                result.stdout + result.stderr,
            )

    def test_invalid_pipeline_report_schema(self):
        """History tracker should reject a report with wrong columns."""
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            script = folder / "track_validation_history.py"

            script.write_text(
                HISTORY_SCRIPT.read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            self.create_fake_pipeline_report(folder, valid=False)

            result = self.run_script(script, folder)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "Missing report columns",
                result.stdout + result.stderr,
            )

    def test_failed_quality_check_returns_nonzero(self):
        """A failed quality check should make the pipeline fail."""
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)

            pipeline_copy = folder / "run_validation_pipeline.py"
            pipeline_copy.write_text(
                PIPELINE_SCRIPT.read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            self.create_fake_validator(folder, should_fail=True)

            result = self.run_script(pipeline_copy, folder)
            output = result.stdout + result.stderr

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FAIL", output)

            report_path = folder / "validation_pipeline_report.csv"
            self.assertTrue(report_path.exists())

            with report_path.open(
                newline="", encoding="utf-8"
            ) as file:
                report = next(csv.DictReader(file))

            self.assertEqual(report["Pipeline_Status"], "FAIL")
            self.assertEqual(report["Failed_Checks"], "1")

    def test_successful_quality_check(self):
        """A passing quality check should produce a PASS report."""
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)

            pipeline_copy = folder / "run_validation_pipeline.py"
            pipeline_copy.write_text(
                PIPELINE_SCRIPT.read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            self.create_fake_validator(folder, should_fail=False)

            result = self.run_script(pipeline_copy, folder)
            output = result.stdout + result.stderr

            self.assertEqual(
                result.returncode,
                0,
                msg=f"Pipeline unexpectedly failed:\n{output}",
            )

            report_path = folder / "validation_pipeline_report.csv"
            self.assertTrue(report_path.exists())

            with report_path.open(
                newline="", encoding="utf-8"
            ) as file:
                report = next(csv.DictReader(file))

            self.assertEqual(report["Pipeline_Status"], "PASS")
            self.assertEqual(report["Passed_Checks"], "1")
            self.assertEqual(report["Failed_Checks"], "0")


if __name__ == "__main__":
    unittest.main(verbosity=2)