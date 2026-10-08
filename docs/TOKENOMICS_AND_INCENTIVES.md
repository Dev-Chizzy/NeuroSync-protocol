# Tokenomics & Incentive Design

## 1. $NSYNC Token Specification

The **$NSYNC** token is the native utility and reward token powering the NeuroSync DeSci ecosystem on Stellar.

- **Token Name**: NeuroSync Protocol Token
- **Symbol**: `NSYNC`
- **Decimals**: 7 (matching Stellar native precision of $10^7$ stroops)
- **Standard**: SEP-41 compliant smart contract

---

## 2. Habit Streak Incentive Engine

The `RewardDistributor` contract aligns user health habits with token incentives by rewarding consistent daily sleep tracking.

### 2.1 Daily Reward Formula

For a user with an active streak count $S$ ($S \ge 1$), the daily reward allocation $R$ in stroops ($10^{-7}$ NSYNC) is calculated as:

$$R(S) = (50 + 5 \times S) \times 10^7$$

| Streak Count ($S$) | Daily Reward ($NSYNC$) | Cumulative 7-Day Total |
| :---: | :---: | :---: |
| Day 1 | 55 NSYNC | 55 NSYNC |
| Day 2 | 60 NSYNC | 115 NSYNC |
| Day 3 | 65 NSYNC | 180 NSYNC |
| Day 7 | 85 NSYNC | 490 NSYNC |
| Day 30 | 200 NSYNC | 3,825 NSYNC |

### 2.2 Streak Rules & Epoch Enforcement

1. **Epoch Day Check**: Rewards can be claimed at most once per Day Epoch ($\lfloor t_{\text{ledger}} / 86,400 \rfloor$).
2. **Grace Period**: Users have up to 48 hours (172,800 seconds) between submissions to maintain their streak.
3. **Streak Reset**: If more than 48 hours elapse without an authenticated telemetry submission, the streak count resets to 0.
4. **Gasless Claiming**: Transactions can be relayed through the Gas Master Relayer, ensuring that research participants do not need native XLM balances to participate and claim earned rewards.
