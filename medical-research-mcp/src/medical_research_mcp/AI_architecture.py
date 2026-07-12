from __future__ import annotations
from .repository import architecture_inventory

def recommend_architecture(repository: str, team_size: int=1, deployment_targets: int=1) -> dict:
    inv=architecture_inventory(repository)
    independent=bool(inv["areas"]["training"] and inv["areas"]["simulation"])
    if team_size<=4 and deployment_targets<=2: choice="modular_monolith"
    elif independent: choice="hybrid"
    else: choice="modular_monolith"
    return {
      "recommendation":choice,
      "evidence":{"team_size":team_size,"deployment_targets":deployment_targets,
                  "areas":{k:len(v) for k,v in inv["areas"].items()}},
      "rule":"Use microservices only for stable boundaries, independent lifecycle, measured scaling or failure isolation."
    }
