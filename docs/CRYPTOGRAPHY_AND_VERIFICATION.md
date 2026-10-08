# Cryptographic Verification Specification

## 1. Mathematical & Canonical Model

The integrity of sleep telemetry submitted to NeuroSync relies on an off-chain cryptographic oracle paired with an on-chain verification smart contract.

### 1.1 Payload Canonicalization
Before signing, the payload dictionary is serialized into a deterministic string representation to guarantee reproducible byte-for-byte hashing across heterogeneous platforms:

```json
{
  "interpretation": "High Sleep Quality / High Performance Readiness",
  "sleep_score": 8.45,
  "timestamp": 1723048590,
  "user_address": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5"
}
```

**Canonicalization Rules:**
- JSON object keys are strictly sorted in lexicographical order (`sort_keys=True`).
- Separators are stripped of whitespace (`separators=(',', ':')`).
- Encoded as UTF-8 bytes prior to cryptographic signing.

---

## 2. Cryptographic Signatures

### 2.1 Off-Chain Signing (Oracle)
The Oracle holds an Ed25519 private key ($sk_{\text{oracle}}$) corresponding to public key ($pk_{\text{oracle}}$).
The signature $\sigma$ is generated as:

$$\sigma = \text{Ed25519Sign}(sk_{\text{oracle}}, M)$$

Where $M$ is the UTF-8 byte stream of the canonical JSON payload string.

### 2.2 On-Chain Verification (Soroban)
When a user invokes `submit_shard` on the `NeuroSyncContract`, the contract performs:

```rust
env.crypto().ed25519_verify(&oracle_pub_key, &payload, &signature);
```

If the signature does not match the canonical byte sequence and the stored oracle public key, the host execution halts immediately, reverting transaction state changes.

---

## 3. Replay Protection & Anti-Tamper Mechanisms

1. **Timestamp Bounds**: The backend relayer verifies $|t_{\text{current}} - t_{\text{payload}}| \le 900\text{s}$ (15 minutes maximum skew).
2. **Signature Deduplication**: The relayer maintains a high-performance in-memory cache of previously processed signature digests. Identical submissions are rejected with HTTP 409 Conflict.
3. **On-Chain Habit Linearization**: The smart contract inspects the ledger timestamp:
   - If $t_{\text{current}} < t_{\text{last}}$, the transaction reverts.
   - If $t_{\text{current}} - t_{\text{last}} < 86,400\text{s}$ (less than 24 hours), the streak count is preserved without increment.
   - If $86,400\text{s} \le t_{\text{current}} - t_{\text{last}} \le 172,800\text{s}$, the streak increments by 1.
   - If $t_{\text{current}} - t_{\text{last}} > 172,800\text{s}$, the streak resets to 1.
