import os
from datetime import datetime
from typing import Dict, Any


def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)



def build_overview_md(overview: Dict[str, Any]) -> str:
    return f"""
## 📊 Dataset Overview

- **Total Rows:** {overview.get("rows")}
- **Total Columns:** {overview.get("columns")}
"""


def build_column_types_md(column_types: Dict[str, Any]) -> str:
    md = "## 🧩 Column Types\n"
    for k, v in column_types.items():
        md += f"\n**{k.title()} Columns ({len(v)}):**\n"
        md += ", ".join(v) if v else "None"
        md += "\n"
    return md


def build_summary_md(stats: Dict[str, Any]) -> str:
    md = "## 📈 Summary Statistics\n"
    for col, values in stats.items():
        md += f"\n### {col}\n"
        for k, v in values.items():
            md += f"- {k}: {round(v, 4) if isinstance(v, float) else v}\n"
    return md


def build_missing_md(missing: Dict[str, int]) -> str:
    md = "## ❗ Missing Values\n"
    for col, cnt in missing.items():
        md += f"- {col}: {cnt}\n"
    return md


def build_outliers_md(outliers: Dict[str, Any]) -> str:
    md = "## 🚨 Outlier Analysis\n"
    for col, o in outliers.items():
        md += (
            f"\n### {col}\n"
            f"- Lower Bound: {o['lower_bound']}\n"
            f"- Upper Bound: {o['upper_bound']}\n"
            f"- Outliers Count: {o['outliers_count']}\n"
        )
    return md


def build_insights_md(insights) -> str:
    md = "## 🧠 AI-Generated Insights\n"

    if hasattr(insights, "key_insights"):
        for i, insight in enumerate(insights.key_insights, 1):
            md += f"\n{i}. {insight}\n"

    if hasattr(insights, "recommendations"):
        md += "\n### 📌 Recommendations\n"
        for r in insights.recommendations:
            md += f"- {r}\n"

    if hasattr(insights, "risks"):
        md += "\n### ⚠️ Risks & Anomalies\n"
        for r in insights.risks:
            md += f"- {r}\n"

    return md




def markdown_to_html(md: str) -> str:
    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Automated Data Report</title>
<style>
body {{ font-family: Arial; padding: 40px; }}
h1, h2, h3 {{ color: #2c3e50; }}
code {{ background: #f4f4f4; padding: 2px 4px; }}
</style>
</head>
<body>
<pre>
{md}
</pre>
</body>
</html>
"""



def report_agent(
    eda: Dict[str, Any],
    charts: Dict[str, Any],
    insights: Dict[str, Any],
    output_dir: str = "reports",
    format: str = "markdown"
) -> Dict[str, Any]:
    """
    Generate automated data analysis report
    """

    ensure_dir(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"data_report_{timestamp}"

    md = f"# 📘 Automated Data Analysis Report\n\nGenerated on **{timestamp}**\n\n"

    md += build_overview_md(eda["overview"])
    md += build_column_types_md(eda["column_types"])
    md += build_summary_md(eda["summary_statistics"])
    md += build_missing_md(eda["missing_values"])
    md += build_outliers_md(eda["outliers"])
    md += build_insights_md(insights)

    md_path = os.path.join(output_dir, f"{base_name}.md")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    result = {
        "status": "success",
        "markdown_path": md_path
    }

    if format in ["html", "pdf"]:
        html = markdown_to_html(md)
        html_path = os.path.join(output_dir, f"{base_name}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        result["html_path"] = html_path

    return result



import os
from pprint import pprint
from Agents.data_cleaning import Preprocess_data
from Agents.eda import run_eda_agent
from Agents.visualization import visualization_agent
from Agents.insight import insight_agent

if __name__ == "__main__":
    print("DataSage Pipeline Started...\n")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(
        BASE_DIR,
        "Data",
        "Heart_Disease_Prediction.csv"
    )
    preprocess_response = Preprocess_data(file_path=filepath)

    if preprocess_response["status"] != "success":
        raise RuntimeError(preprocess_response["message"])

    df = preprocess_response["dataframe"]
    metadata = preprocess_response["metadata"]

    print("Data Cleaning Completed\n")

    eda_response = run_eda_agent(df=df)
    print("EDA Completed\n")

    charts = visualization_agent(df=df,metadata=metadata)
    print("Visualization Metadata Generated\n")


    insights = insight_agent(
        eda=eda_response,
        metadata=metadata
    )
    print("LLM Insights Generated\n")

    report = report_agent(
        eda=eda_response,
        charts=charts,
        insights=insights,
        format="html"   
    )

    print("Report Generated Successfully\n")

    pprint({
        "rows": metadata["rows"],
        "columns": len(metadata["columns"]),
        "report": report
    })

    print("\nDataSage Pipeline Finished Successfully!")
