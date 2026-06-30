import pandas as pd
import great_expectations as gx
from great_expectations.core.expectation_suite import ExpectationSuite


def build_patient_expectation_suite() -> ExpectationSuite:
    context = gx.get_context()
    suite = context.add_expectation_suite("patient_data_suite")

    df = pd.read_csv("data/raw/patients_raw.csv")
    validator = context.sources.pandas_default.read_dataframe(df)

    validator.expect_column_values_to_not_be_null("patient_id")

    validator.expect_column_value_lengths_to_equal(
        column="cccd",
        value=12
    )

    validator.expect_column_values_to_be_between(
        column="ket_qua_xet_nghiem",
        min_value=0,
        max_value=50
    )

    valid_conditions = ["Tiểu đường", "Huyết áp cao", "Tim mạch", "Khỏe mạnh"]
    validator.expect_column_values_to_be_in_set(
        column="benh",
        value_set=valid_conditions
    )

    validator.expect_column_values_to_match_regex(
        column="email",
        regex=r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"
    )

    validator.expect_column_values_to_be_unique(column="patient_id")

    validator.save_expectation_suite()
    return suite


def validate_anonymized_data(filepath: str) -> dict:
    df = pd.read_csv(filepath)
    original_df = pd.read_csv("data/raw/patients_raw.csv")

    failed_checks = []

    cccd_raw = original_df["cccd"].astype(str)
    cccd_anon = df["cccd"].astype(str)
    overlapping = cccd_anon[cccd_anon.isin(cccd_raw)]
    if len(overlapping) > 0:
        failed_checks.append("Original CCCD values found in anonymized output")
        success = False

    null_cols = [col for col in ["ho_ten", "cccd", "so_dien_thoai", "email", "patient_id"]
                 if df[col].isnull().any()]
    if null_cols:
        failed_checks.append(f"Null values found in columns: {null_cols}")

    if len(df) != len(original_df):
        failed_checks.append(f"Row count mismatch: anonymized={len(df)}, original={len(original_df)}")

    results = {
        "success": len(failed_checks) == 0,
        "failed_checks": failed_checks,
        "stats": {
            "total_rows": len(df),
            "columns": list(df.columns)
        }
    }

    return results
