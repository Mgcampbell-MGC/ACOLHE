"""PNCP harvesting.

The client in pncp_client.py is the only sanctioned way into PNCP. It knows
both API families, caches to disk, resumes from a cursor, and reports what it
failed to get. Nothing downstream should open a socket to pncp.gov.br itself:
an uncached, unlogged fetch is how a silent short harvest happens.
"""

from harvest.pncp_client import (
    BASE_A,
    BASE_B,
    FAMILY_A,
    FAMILY_B,
    MODALIDADES,
    Cursor,
    DiskCache,
    Failure,
    HarvestReport,
    PNCPClient,
    PNCPError,
    Response,
    Unavailable,
    USER_AGENT,
    jsonl_sink,
    keys_in_jsonl,
)

__all__ = [
    "BASE_A",
    "BASE_B",
    "FAMILY_A",
    "FAMILY_B",
    "MODALIDADES",
    "Cursor",
    "DiskCache",
    "Failure",
    "HarvestReport",
    "PNCPClient",
    "PNCPError",
    "Response",
    "Unavailable",
    "USER_AGENT",
    "jsonl_sink",
    "keys_in_jsonl",
]
