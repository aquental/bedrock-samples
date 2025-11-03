from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from fastmcp import FastMCP

app = FastMCP("aws-assistant-mcp")

_FAKE_USERS = [
    {"username": "alice", "arn": "arn:aws:iam::123456789012:user/alice",
        "created_at": "2023-10-01"},
    {"username": "bob", "arn": "arn:aws:iam::123456789012:user/bob",
        "created_at": "2024-02-15"},
    {"username": "charlie", "arn": "arn:aws:iam::123456789012:user/charlie",
        "created_at": "2024-11-03"},
    {"username": "dora", "arn": "arn:aws:iam::123456789012:user/dora",
        "created_at": "2025-01-20"},
]

_FAKE_CLUSTERS: Dict[str, Dict[str, Any]] = {
    "eks-dev":   {"type": "EKS", "region": "us-west-2", "nodes": 3,  "status": "green",  "k8s": "1.29"},
    "eks-prod":  {"type": "EKS", "region": "eu-west-1", "nodes": 12, "status": "yellow", "k8s": "1.28"},
    "emr-etl":   {"type": "EMR", "region": "us-east-1", "nodes": 6,  "status": "green",  "hadoop": "3.3"},
}

_FAKE_INSTANCES: Dict[str, Dict[str, Any]] = {
    "i-1234567890abcdef0": {"type": "t3.micro",  "state": "running", "az": "us-west-2a", "tags": {"Name": "web-1"}},
    "i-a1b2c3d4e5f6g7h8i": {"type": "m5.2xlarge", "state": "stopped", "az": "eu-west-1b", "tags": {"Name": "etl-2"}},
    "i-aaaaaaaaaaaaaaaaa": {"type": "c6i.large", "state": "running", "az": "us-east-1c", "tags": {"Name": "app-7"}},
}


def _fake_costs(seed: str = "7d") -> Dict[str, Any]:
    # Simple deterministic-ish generator based on seed string
    h = abs(hash(seed)) % (10**6)

    def pick(lo, hi):
        return round(lo + (h % 1000) / 1000 * (hi - lo), 2)
    ec2 = pick(20, 250)
    s3 = pick(3, 45)
    rds = pick(5, 120)
    total = round(ec2 + s3 + rds, 2)
    return {
        "period": seed,
        "currency": "USD",
        "breakdown": {"EC2": ec2, "S3": s3, "RDS": rds},
        "total": total,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }

# ---------------------------
# Tools
# ---------------------------


@app.tool()
def list_users(prefix: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List IAM users (simulated). Optionally filter by username prefix.

    Args:
        prefix: If provided, only users whose usernames start with this prefix are returned.

    Returns:
        A list of user dicts: [{username, arn, created_at}, ...]
    """
    users = _FAKE_USERS
    if prefix:
        users = [u for u in users if u["username"].startswith(prefix)]
    return users


@app.tool()
def get_user(username: str) -> Dict[str, Any]:
    """
    Get details for a specific user (simulated).

    Args:
        username: The username to look up.

    Returns:
        A dict with user details or {"error": "..."} if not found.
    """
    for u in _FAKE_USERS:
        if u["username"] == username:
            # Toss in a fake "last_login" for flavor.
            return {
                **u,
                "last_login": (datetime.utcnow() - timedelta(days=len(username))).isoformat() + "Z",
                "groups": ["developers"] if username in {"alice", "charlie"} else ["data-team"],
                "mfa_enabled": username in {"alice", "dora"},
            }
    return {"error": f"user '{username}' not found"}


@app.tool()
def list_clusters(kind: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List compute clusters (simulated).

    Args:
        kind: Optional filter (e.g., "EKS" or "EMR").

    Returns:
        A list of clusters with basic metadata.
    """
    items = []
    for name, meta in _FAKE_CLUSTERS.items():
        if kind and meta["type"].lower() != kind.lower():
            continue
        items.append({"name": name, **meta})
    return items


@app.tool()
def get_cluster_status(name: str) -> Dict[str, Any]:
    """
    Get status for a specific cluster (simulated).

    Args:
        name: Cluster name (e.g., "eks-prod").

    Returns:
        Status dict (or {"error": "..."} if missing).
    """
    data = _FAKE_CLUSTERS.get(name)
    if not data:
        return {"error": f"cluster '{name}' not found"}
    # Add a few dynamic/semi-randomized readings:
    pods = 20 + len(name)
    cpu_util = 35 + (len(name) * 3) % 40
    return {
        "name": name,
        **data,
        "observability": {
            "pods_running": pods,
            "avg_cpu_util_percent": cpu_util,
            "avg_mem_util_percent": 50 + (cpu_util // 2),
        },
        "checked_at": datetime.utcnow().isoformat() + "Z",
    }


@app.tool()
def describe_instance(instance_id: str) -> Dict[str, Any]:
    """
    Describe a single EC2 instance (simulated).

    Args:
        instance_id: e.g., "i-1234567890abcdef0"

    Returns:
        Dict of instance properties or {"error": "..."} if not found.
    """
    return _FAKE_INSTANCES.get(instance_id, {"error": f"instance '{instance_id}' not found"})


@app.tool()
def list_instances(state: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List EC2 instances (simulated); optionally filter by state.

    Args:
        state: Optional filter (e.g., "running", "stopped").

    Returns:
        A list of instance dicts (each includes id as 'instance_id').
    """
    items = []
    for iid, meta in _FAKE_INSTANCES.items():
        if state and meta.get("state") != state:
            continue
        items.append({"instance_id": iid, **meta})
    return items


@app.tool()
def cost_overview(period: str = "7d") -> Dict[str, Any]:
    """
    Simulated cost snapshot.

    Args:
        period: A label like "7d", "30d", "mtd" (month-to-date). Free-form; only used as a seed.

    Returns:
        A dict with a fake cost breakdown and total in USD.
    """
    return _fake_costs(seed=period)


@app.tool()
def ping() -> Dict[str, str]:
    """Basic liveness check."""
    return {"ok": "pong", "server": "aws-edu-mcp", "ts": datetime.utcnow().isoformat() + "Z"}


if __name__ == "__main__":
    app.run()
