# NeuroSync Protocol Architecture

## 1. System Overview

NeuroSync is a decentralized science (DeSci) and telemetry verification protocol built on the Stellar network. It enables individuals to submit sleep and circadian telemetry, verify health scores via an off-chain machine learning oracle, and mint proof-of-sleep credentials on Soroban smart contracts with zero user gas friction.

```
+--------------------+        +---------------------+        +--------------------+
|  Wearable Telemetry| -----> |    Next.js Web3     | -----> |  NeuroSync Python  |
|   (Sleep Metrics)  |        |    Client Portal    |        |     Client SDK     |
+--------------------+        +---------------------+        +--------------------+
                                         |                             |
                                         v                             v
                              +---------------------------------------------+
                              |         NeuroSync Oracle & Relayer          |
                              |   - FastAPI High-Throughput REST Gateway    |
                              |   - Scikit-Learn Regression Engine          |
                              |   - Ed25519 Cryptographic Signer            |
                              |   - Sliding-Window Rate Limiter             |
                              |   - Anti-Replay Nonce Protector             |
                              +---------------------------------------------+
                                         |
                        +----------------+----------------+
                        |                                 |
                        v                                 v
        +-------------------------------+  +-------------------------------+
        |      Gas Master Relayer       |  |     Cryptographic Oracle      |
        | - FeeBumpTransaction Envelope |  | - Ed25519 Deterministic Signs |
        | - Pays XLM Network Gas Fees   |  | - Sleep Quality Scoring Model |
        +-------------------------------+  +-------------------------------+
                        \                                 /
                         \                               /
                          v                             v
           +-----------------------------------------------------------+
           |                 Stellar Network (Soroban)                 |
           |  +---------------------+         +---------------------+  |
           |  |  NeuroSync Core     | ------> |  Reward Distributor |  |
           |  |  - Signature Verify |         |  - Streak Tracking  |  |
           |  |  - Shard Validation |         |  - $NSYNC Minting   |  |
           |  +---------------------+         +---------------------+  |
           |                                             |             |
           |                                             v             |
           |                                  +---------------------+  |
           |                                  |   $NSYNC Token      |  |
           |                                  |   (SEP-41 Token)    |  |
           |                                  +---------------------+  |
           +-----------------------------------------------------------+
```

---

## 2. Component Directory

### 2.1 Web3 User Portal (`frontend/`)
- Built with **Next.js 16**, **React 19**, and **Tailwind CSS**.
- Integrates with the **Freighter Wallet** to authenticate users with standard Stellar G-addresses.
- Renders real-time telemetry inputs, circadian cycle insights, streak status, and claimable reward metrics.

### 2.2 Oracle & Gas Master Relayer (`api/`)
- **FastAPI Engine**: Serves low-latency REST endpoints for telemetry verification.
- **ML Quality Predictor**: Evaluates multi-dimensional telemetry (duration, stress, activity level, step count, heart rate) using a pre-trained regression pipeline.
- **Gas Master Relayer**: Leverages Stellar's native `FeeBumpTransaction` capability to sponsor network fees for users, removing the requirement for participants to hold native XLM.
- **Security & Replay Guard**: Implements sliding-window rate limiting per client IP and rejects duplicated signatures and stale timestamps.

### 2.3 On-Chain Smart Contracts (`contracts/` & `neurosync-core/`)
- **NeuroSync Core Contract**: Validates the oracle's Ed25519 signature against the payload hash on-chain using Soroban host environment crypto functions.
- **Reward Distributor**: Calculates streak tenure, enforces a 24–48 hour daily submission window, and distributes $NSYNC tokens based on streak tiers.
- **NSync Token**: SEP-compatible utility token contract managing minting and balance ledgers.

### 2.4 Developer SDK & CLI (`sdk/`)
- Installable Python library (`neurosync-sdk`) enabling data scientists and researchers to query node status, programmatically sign telemetry, and submit zero-gas transactions.
