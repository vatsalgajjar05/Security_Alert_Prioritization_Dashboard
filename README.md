# Security Alert Prioritization Dashboard

A practical SOC-style mini project built during internship work to help analysts prioritize alerts faster using a weighted risk score.

This dashboard takes raw security alerts, calculates a final risk score, maps each alert to a priority bucket, and presents the results in a clean Streamlit UI for quick triage.

## Internship Task Context

The goal of this task was to simulate a real analyst workflow where multiple alerts arrive together and need to be handled in the right order. Instead of reviewing alerts manually one by one, this project creates a repeatable scoring method so higher-risk alerts naturally move to the top.

## What This Project Does

- Reads sample alert data from a CSV file.
- Calculates a weighted risk score for each alert.
- Assigns priority levels: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.
- Provides filter/search controls for investigation.
- Shows top-priority alerts first.
- Displays analytics charts and score breakdown cards.

## Risk Scoring Logic

The final score is computed on a 0-100 scale:

`Risk Score = (Severity x 0.40) + (Asset Criticality x 0.30) + (Event Context x 0.30)`

### Event Context Inputs

Event context increases based on signals such as:
- Number of failed attempts
- Malicious IP flag
- After-hours activity
- Number of affected users

### Priority Thresholds

- `CRITICAL`: 90-100
- `HIGH`: 70-89
- `MEDIUM`: 40-69
- `LOW`: 0-39

## Screenshots

### 1) Dashboard Home

![Dashboard Home](assets/homepage.png)

### 2) Alert Analytics View

![Alert Analytics](assets/graphpage.png)

### 3) Risk Score Breakdown View

![Risk Score Breakdown](assets/scorebreakdownpage.png)

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

## Project Structure

```text
security-alert-prioritization/
|-- app.py
|-- scoring_engine.py
|-- requirements.txt
|-- data/
|   |-- alerts.csv
|-- assets/
|   |-- homepage.png
|   |-- graphpage.png
|   |-- scorebreakdownpage.png
```

## Run Locally

1. Clone or open the project folder.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
streamlit run app.py
```

4. Open the local URL shown in terminal (usually `http://localhost:8501`).

## Notes

- This project uses a sample dataset for demonstration.
- Scoring weights can be tuned based on SOC policy.
- The code is split into:
  - `app.py` for UI + data flow
  - `scoring_engine.py` for scoring logic

## Future Improvements

- Export prioritized alerts to CSV/PDF.
- Integrate real-time alert ingestion from SIEM.
- Add authentication for role-based access.

---

Developed as an internship task to demonstrate risk-based alert triage and dashboard reporting.