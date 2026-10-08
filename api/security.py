import time
import collections
from typing import Dict, Set, Tuple, Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from stellar_sdk import Keypair

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Applies production-grade security headers to all incoming HTTP responses.
    """
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()"
        return response


class RateLimiter:
    """
    Sliding window in-memory rate limiter per IP/client key.
    Enforces maximum requests within a defined window in seconds.
    """
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.history: Dict[str, collections.deque] = collections.defaultdict(collections.deque)

    def is_allowed(self, client_id: str) -> Tuple[bool, int]:
        now = time.time()
        deq = self.history[client_id]

        # Prune expired timestamps
        while deq and deq[0] <= now - self.window_seconds:
            deq.popleft()

        if len(deq) >= self.max_requests:
            retry_after = int(self.window_seconds - (now - deq[0])) + 1
            return False, retry_after

        deq.append(now)
        return True, 0


class NonceReplayProtector:
    """
    Protects against replay attacks by tracking processed signatures and hashes,
    and enforcing timestamp validity windows (e.g. ±15 minutes).
    """
    def __init__(self, max_skew_seconds: int = 900, max_cache_size: int = 10000):
        self.max_skew_seconds = max_skew_seconds
        self.max_cache_size = max_cache_size
        self.seen_signatures: Dict[str, float] = {}

    def validate_and_record(self, signature_or_hash: str, timestamp: Optional[int] = None) -> Tuple[bool, str]:
        now = time.time()

        if timestamp is not None:
            skew = abs(now - timestamp)
            if skew > self.max_skew_seconds:
                return False, f"Timestamp rejected: clock skew {int(skew)}s exceeds maximum allowed {self.max_skew_seconds}s"

        if signature_or_hash in self.seen_signatures:
            return False, "Replay rejected: signature or proof hash has already been processed"

        # Prune cache if limit exceeded
        if len(self.seen_signatures) >= self.max_cache_size:
            cutoff = now - (self.max_skew_seconds * 2)
            self.seen_signatures = {k: v for k, v in self.seen_signatures.items() if v > cutoff}

        self.seen_signatures[signature_or_hash] = now
        return True, "OK"


def validate_stellar_address(address: str) -> bool:
    """
    Validates whether an address string is a well-formed Stellar public key (G...).
    """
    if not address or not isinstance(address, str):
        return False
    if not address.startswith("G") or len(address) != 56:
        return False
    try:
        Keypair.from_public_key(address)
        return True
    except Exception:
        return False
