def calculate_context_score(alert):
    """
    Builds the event-context score from supporting signals.
    Caps the value at 100.
    """

    score = 0

    
    if alert["failed_attempts"] >= 50:
        score += 35
    elif alert["failed_attempts"] >= 10:
        score += 25
    elif alert["failed_attempts"] >= 5:
        score += 15

    
    if alert["malicious_ip"] == 1:
        score += 30

   
    if alert["after_hours"] == 1:
        score += 15

    if alert["affected_users"] >= 10:
        score += 20
    elif alert["affected_users"] >= 5:
        score += 10

    return min(score, 100)


def calculate_threat_score(alert):
    """
    Computes a threat-indicator score and caps it at 100.

    Kept as an extra indicator for analysts.
    """

    score = 0

    if alert["malicious_ip"] == 1:
        score += 60

    if alert["failed_attempts"] >= 50:
        score += 40
    elif alert["failed_attempts"] >= 10:
        score += 25

    return min(score, 100)


def calculate_risk_score(alert):
    """
    Calculates the final security risk score.

    Core prioritization factors:
    Severity          = 40%
    Asset Importance  = 30%
    Event Context     = 30%

    Threat indicators are included inside
    the Event Context calculation.
    """

    # How severe the alert itself is
    severity_score = alert["severity"]

    # Business criticality of the impacted asset
    asset_importance_score = alert["asset_criticality"]

    # Supporting context around this event
    event_context_score = calculate_context_score(alert)

    # Weighted final score
    risk_score = (
        severity_score * 0.40
        + asset_importance_score * 0.30
        + event_context_score * 0.30
    )

    return round(risk_score, 2)


def get_priority(score):
    """
    Maps a risk score into a priority label.
    """

    if score >= 90:
        return "CRITICAL"

    elif score >= 70:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    else:
        return "LOW"


def get_score_breakdown(alert):
    """
    Returns the weighted score breakdown used in the final result.
    """

    severity_score = alert["severity"]
    asset_importance_score = alert["asset_criticality"]
    event_context_score = calculate_context_score(alert)

    severity_contribution = severity_score * 0.40
    asset_contribution = asset_importance_score * 0.30
    context_contribution = event_context_score * 0.30

    final_score = (
        severity_contribution
        + asset_contribution
        + context_contribution
    )

    return {
        "severity_score": severity_score,
        "severity_contribution": round(severity_contribution, 2),
        "asset_score": asset_importance_score,
        "asset_contribution": round(asset_contribution, 2),
        "context_score": event_context_score,
        "context_contribution": round(context_contribution, 2),
        "final_score": round(final_score, 2),
    }


def get_priority_reason(alert, score):
    """
    Builds readable reasons for the alert's assigned priority.
    """

    reasons = []

    if alert["severity"] >= 80:
        reasons.append("High severity event")

    if alert["asset_criticality"] >= 80:
        reasons.append("Critical/high-value asset")

    if alert["malicious_ip"] == 1:
        reasons.append("Known malicious IP")

    if alert["failed_attempts"] >= 10:
        reasons.append("Repeated authentication attempts")

    if alert["after_hours"] == 1:
        reasons.append("Activity outside business hours")

    if alert["affected_users"] >= 5:
        reasons.append("Multiple users affected")

    if not reasons:
        reasons.append("No major risk indicators detected")

    return reasons