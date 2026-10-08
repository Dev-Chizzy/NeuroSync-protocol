import time
from typing import Optional, Dict, Any, List
import requests
from pydantic import BaseModel, Field

class SleepMetricSubmission(BaseModel):
    user_address: str
    sleep_duration: float = Field(..., ge=1.0, le=24.0, description="Hours of sleep")
    stress_level: int = Field(..., ge=1, le=10, description="Perceived stress rating (1-10)")
    physical_activity_level: int = Field(..., ge=0, le=100, description="Activity index (0-100)")
    daily_steps: int = Field(..., ge=0, description="Total daily steps")
    heart_rate: int = Field(..., ge=30, le=220, description="Average resting heart rate in bpm")
    age: int = Field(default=28, ge=18, le=120)
    gender: str = Field(default="Female")
    bmi_category: str = Field(default="Normal")
    sleep_disorder: str = Field(default="None")
    occupation: str = Field(default="Engineer")


class ProofResult(BaseModel):
    status: str
    tx_hash: str
    sleep_score: Optional[float] = None
    interpretation: Optional[str] = None
    signature: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    relayer_public_key: Optional[str] = None
    oracle_public_key: Optional[str] = None
    user_gas_cost_xlm: int = 0
    message: str


class NeuroSyncClient:
    """
    Client for interacting with the NeuroSync Protocol Oracle and Relayer network.
    """
    def __init__(self, base_url: str = "http://localhost:8000", timeout: int = 15):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "NeuroSync-SDK/0.1.0"})

    def get_health(self) -> Dict[str, Any]:
        """Queries node health, verifying oracle and relayer status."""
        resp = self.session.get(f"{self.base_url}/health", timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def get_root_status(self) -> Dict[str, Any]:
        """Queries root protocol metadata and public keys."""
        resp = self.session.get(f"{self.base_url}/", timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def get_participants(self) -> List[str]:
        """Retrieves active registered participants on the relayer."""
        resp = self.session.get(f"{self.base_url}/participants", timeout=self.timeout)
        resp.raise_for_status()
        return resp.json().get("participants", [])

    def generate_signature(self, submission: SleepMetricSubmission) -> Dict[str, Any]:
        """
        Sends raw telemetry to the ML Oracle and returns a cryptographically signed payload.
        """
        payload = {
            "user_address": submission.user_address,
            "Sleep_Duration": submission.sleep_duration,
            "Stress_Level": submission.stress_level,
            "Physical_Activity_Level": submission.physical_activity_level,
            "Daily_Steps": submission.daily_steps,
            "Heart_Rate": submission.heart_rate,
            "Age": submission.age,
            "Gender": submission.gender,
            "BMI_Category": submission.bmi_category,
            "Sleep_Disorder": submission.sleep_disorder,
            "Occupation": submission.occupation
        }
        resp = self.session.post(f"{self.base_url}/generate_signature", json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def submit_sleep_proof(self, submission: SleepMetricSubmission) -> ProofResult:
        """
        Processes sleep metrics through the Gas Master Relayer, achieving zero-gas on-chain settlement.
        """
        payload = {
            "user_address": submission.user_address,
            "Sleep_Duration": submission.sleep_duration,
            "Stress_Level": submission.stress_level,
            "Physical_Activity_Level": submission.physical_activity_level,
            "Daily_Steps": submission.daily_steps,
            "Heart_Rate": submission.heart_rate,
            "Age": submission.age,
            "Gender": submission.gender,
            "BMI_Category": submission.bmi_category,
            "Sleep_Disorder": submission.sleep_disorder,
            "Occupation": submission.occupation,
            "timestamp": int(time.time())
        }
        resp = self.session.post(f"{self.base_url}/submit-proof", json=payload, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()

        payload_info = data.get("payload", {})
        return ProofResult(
            status=data.get("status", "unknown"),
            tx_hash=data.get("tx_hash", ""),
            sleep_score=payload_info.get("sleep_score"),
            interpretation=payload_info.get("interpretation"),
            signature=data.get("signature"),
            payload=payload_info,
            relayer_public_key=data.get("relayer_public_key"),
            oracle_public_key=data.get("oracle_public_key"),
            user_gas_cost_xlm=data.get("user_gas_cost_xlm", 0),
            message=data.get("message", "")
        )
