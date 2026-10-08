# NeuroSync Protocol Python SDK & CLI

The official Python Client SDK and CLI for interacting with the **NeuroSync Protocol** decentralized science (DeSci) oracle and gas-free transaction relayer.

## Installation

```bash
pip install -e sdk/
```

## Quick Start (SDK)

```python
from neurosync import NeuroSyncClient, SleepMetricSubmission

# Initialize client pointing to local or remote relayer
client = NeuroSyncClient(base_url="https://neurosync-protocol.onrender.com")

# Check node health and retrieve cryptographic keys
health = client.get_health()
print(f"Oracle Public Key: {health['oracle_public_key']}")
print(f"Relayer Public Key: {health['relayer_public_key']}")

# Submit sleep metrics through the Gas Master Relayer
result = client.submit_sleep_proof(
    SleepMetricSubmission(
        user_address="GD73...YOUR_STELLAR_ADDRESS",
        sleep_duration=8.2,
        stress_level=2,
        physical_activity_level=75,
        daily_steps=11500,
        heart_rate=59,
        age=29,
        gender="Female",
        bmi_category="Normal",
        sleep_disorder="None",
        occupation="Biochemist"
    )
)

print(f"Proof transaction hash: {result.tx_hash}")
print(f"Verified sleep score: {result.sleep_score}")
```

## CLI Usage

```bash
# Ping relayer node
neurosync ping --url http://localhost:8000

# View participants
neurosync participants --url http://localhost:8000

# Submit a sleep shard proof
neurosync submit \
  --address GD73... \
  --sleep-duration 8.0 \
  --stress-level 2 \
  --steps 10500 \
  --heart-rate 60
```
