import sys
import argparse
import json
from .client import NeuroSyncClient, SleepMetricSubmission

def main():
    parser = argparse.ArgumentParser(
        prog="neurosync",
        description="NeuroSync Protocol CLI - Interact with the DeSci Oracle and Gas Master Relayer"
    )
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of the NeuroSync node")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: ping
    ping_parser = subparsers.add_parser("ping", help="Check node health and connectivity")

    # Subcommand: participants
    part_parser = subparsers.add_parser("participants", help="List registered network participants")

    # Subcommand: submit
    submit_parser = subparsers.add_parser("submit", help="Submit sleep metrics to oracle and relayer")
    submit_parser.add_argument("--address", required=True, help="User's Stellar G-address")
    submit_parser.add_argument("--sleep-duration", type=float, default=8.0, help="Sleep duration in hours")
    submit_parser.add_argument("--stress-level", type=int, default=2, help="Stress rating 1-10")
    submit_parser.add_argument("--activity-level", type=int, default=65, help="Physical activity level 0-100")
    submit_parser.add_argument("--steps", type=int, default=10000, help="Daily steps count")
    submit_parser.add_argument("--heart-rate", type=int, default=60, help="Resting heart rate in bpm")
    submit_parser.add_argument("--age", type=int, default=28, help="Participant age")
    submit_parser.add_argument("--gender", default="Female", help="Participant gender")
    submit_parser.add_argument("--bmi", default="Normal", help="BMI Category")
    submit_parser.add_argument("--disorder", default="None", help="Sleep disorder if any")
    submit_parser.add_argument("--occupation", default="Engineer", help="Occupation")

    args = parser.parse_args()
    client = NeuroSyncClient(base_url=args.url)

    try:
        if args.command == "ping":
            health = client.get_health()
            print("NeuroSync Node Status:")
            print(json.dumps(health, indent=2))

        elif args.command == "participants":
            participants = client.get_participants()
            print(f"Total Participants: {len(participants)}")
            for idx, addr in enumerate(participants, 1):
                print(f"  [{idx}] {addr}")

        elif args.command == "submit":
            submission = SleepMetricSubmission(
                user_address=args.address,
                sleep_duration=args.sleep_duration,
                stress_level=args.stress_level,
                physical_activity_level=args.activity_level,
                daily_steps=args.steps,
                heart_rate=args.heart_rate,
                age=args.age,
                gender=args.gender,
                bmi_category=args.bmi,
                sleep_disorder=args.disorder,
                occupation=args.occupation
            )
            print(f"Submitting sleep proof for address: {args.address}...")
            res = client.submit_sleep_proof(submission)
            print("\nProof Submission Successful!")
            print(f"Transaction Hash: {res.tx_hash}")
            print(f"Sleep Score:      {res.sleep_score}/10")
            print(f"Interpretation:   {res.interpretation}")
            print(f"Oracle Signature: {res.signature}")
            print(f"User Gas Cost:    {res.user_gas_cost_xlm} XLM (Gasless)")

    except Exception as e:
        print(f"Error executing command: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
