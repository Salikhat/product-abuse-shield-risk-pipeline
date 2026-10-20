import pandas as pd

def detect_unauthorized_resale(df):
    """Processes corporate team seat distribution for resale anomalies."""
    df['email_domain'] = df['provisioned_user_email'].str.split('@').str[1]
    metrics = df.groupby('team_subscription_id').agg(
        total_seats_used=('provisioned_user_email', 'count'),
        unique_hardware_profiles=('user_hardware_hash', 'nunique'),
        unique_email_domains=('email_domain', 'nunique')
    ).reset_index()
    
    metrics['resale_risk_score'] = 0
    metrics.loc[metrics['unique_email_domains'] > 2, 'resale_risk_score'] += 60
    return metrics[metrics['resale_risk_score'] >= 50]