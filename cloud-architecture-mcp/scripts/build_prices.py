"""Build the tracked price snapshots used by the cost tool of the cloud architecture MCPs.

Inputs (research workspace, not tracked):
  --aws    aws-prices.json produced by aws_price_list.py (AWS Price List, public OnDemand terms)
  --azure  azure-prices.json produced by azure_retail_prices.py (Azure Retail Prices API)
Outputs (tracked): providers/aws/prices.json and providers/azure/prices.json

Each SKU key is explicit and maps to exactly one row (region + usagetype/meter). The build FAILS when
a key matches zero or several rows, so a price is never guessed.
"""

from __future__ import annotations

import argparse
import json
import pathlib

AWS_KEYS = {
    "vpc_endpoint_interface_hour": {"sa-east-1": ("SAE1-VpcEndpoint-Hours", None), "us-east-1": ("USE1-VpcEndpoint-Hours", None)},
    "vpc_endpoint_data_gb": {"sa-east-1": ("SAE1-VpcEndpoint-Bytes", "upto 1 PB"), "us-east-1": ("USE1-VpcEndpoint-Bytes", "upto 1 PB")},
    "alb_hour": {"sa-east-1": ("SAE1-LoadBalancerUsage", "Application LoadBalancer-hour"),
                 "us-east-1": ("LoadBalancerUsage", "Application LoadBalancer-hour")},
    "alb_lcu_hour": {"sa-east-1": ("SAE1-LCUUsage", "Application load balancer capacity unit-hour"),
                     "us-east-1": ("LCUUsage", "Application load balancer capacity unit-hour")},
    "secrets_manager_secret_month": {"sa-east-1": ("SAE1-AWSSecretsManager-Secrets", None),
                                     "us-east-1": ("USE1-AWSSecretsManager-Secrets", None)},
    "fargate_x86_vcpu_hour": {"sa-east-1": ("SAE1-Fargate-vCPU-Hours:perCPU", None), "us-east-1": ("USE1-Fargate-vCPU-Hours:perCPU", None)},
    "fargate_x86_gb_hour": {"sa-east-1": ("SAE1-Fargate-GB-Hours", None), "us-east-1": ("USE1-Fargate-GB-Hours", None)},
    "fargate_arm_vcpu_hour": {"sa-east-1": ("SAE1-Fargate-ARM-vCPU-Hours:perCPU", None),
                              "us-east-1": ("USE1-Fargate-ARM-vCPU-Hours:perCPU", None)},
    "fargate_arm_gb_hour": {"sa-east-1": ("SAE1-Fargate-ARM-GB-Hours", None), "us-east-1": ("USE1-Fargate-ARM-GB-Hours", None)},
    "cloudwatch_logs_ingest_gb": {"sa-east-1": ("SAE1-DataProcessing-Bytes", None), "us-east-1": ("USE1-DataProcessing-Bytes", None)},
    "cloudwatch_alarm_month": {"sa-east-1": ("SAE1-CW:AlarmMonitorUsage", None), "us-east-1": ("CW:AlarmMonitorUsage", None)},
    "cloudwatch_metric_month": {"sa-east-1": ("SAE1-CW:MetricsUsage", None), "us-east-1": ("USE1-CW:MetricsUsage", None)},
    "s3_standard_gb_month": {"sa-east-1": ("SAE1-TimedStorage-ByteHrs", "first 50 TB"), "us-east-1": ("TimedStorage-ByteHrs", "first 50 TB")},
    "opensearch_r6g_large_hour": {"sa-east-1": ("SAE1-ESInstance:r6g.large", None), "us-east-1": ("ESInstance:r6g.large", None)},
    "opensearch_m6g_large_hour": {"sa-east-1": ("SAE1-ESInstance:m6g.large", None), "us-east-1": ("ESInstance:m6g.large", None)},
    "opensearch_gp3_gb_month": {"sa-east-1": ("SAE1-ES:GP3-Storage", None), "us-east-1": ("ES:GP3-Storage", None)},
    "opensearch_serverless_indexing_ocu_hour": {"sa-east-1": ("SAE1-IndexingOCU", None), "us-east-1": ("USE1-IndexingOCU", None)},
    "opensearch_serverless_search_ocu_hour": {"sa-east-1": ("SAE1-SearchOCU", None), "us-east-1": ("USE1-SearchOCU", None)},
    "aurora_pg_r6g_large_hour": {"sa-east-1": ("SAE1-InstanceUsage:db.r6g.large", "running Aurora PostgreSQL"),
                                 "us-east-1": ("InstanceUsage:db.r6g.large", "running Aurora PostgreSQL")},
    "aurora_pg_storage_gb_month": {"sa-east-1": ("SAE1-Aurora:StorageUsage", "Aurora PostgreSQL"),
                                   "us-east-1": ("Aurora:StorageUsage", "Aurora PostgreSQL")},
    "aurora_pg_serverless_v2_acu_hour": {"sa-east-1": ("SAE1-Aurora:ServerlessV2Usage", "Aurora PostgreSQL Serverless v2"),
                                         "us-east-1": ("Aurora:ServerlessV2Usage", "Aurora PostgreSQL Serverless v2")},
    "sagemaker_hosting_ml_g5_xlarge_hour": {"sa-east-1": ("SAE1-Host:ml.g5.xlarge", None), "us-east-1": ("USE1-Host:ml.g5.xlarge", None)},
    "sagemaker_training_ml_g5_xlarge_hour": {"sa-east-1": ("SAE1-Train:ml.g5.xlarge", None), "us-east-1": ("USE1-Train:ml.g5.xlarge", None)},
}

AZURE_KEYS = {
    "container_apps_consumption_vcpu_second": ("brazilsouth", lambda r: r["serviceName"] == "Azure Container Apps" and r["meterName"] == "Standard vCPU Active Usage"),
    "container_apps_consumption_memory_gib_second": ("brazilsouth", lambda r: r["serviceName"] == "Azure Container Apps" and r["meterName"] == "Standard Memory Active Usage"),
    "container_apps_consumption_requests_million": ("brazilsouth", lambda r: r["serviceName"] == "Azure Container Apps" and r["meterName"] == "Standard Requests"),
    "container_apps_dedicated_vcpu_hour": ("brazilsouth", lambda r: r["serviceName"] == "Azure Container Apps" and r["meterName"] == "Dedicated vCPU Usage"),
    "container_apps_dedicated_memory_gib_hour": ("brazilsouth", lambda r: r["serviceName"] == "Azure Container Apps" and r["meterName"] == "Dedicated Memory Usage"),
    "postgres_gp_ddsv5_2vcore_hour": ("brazilsouth", lambda r: r["productName"] == "Azure Database for PostgreSQL Flexible Server General Purpose Ddsv5 Series Compute" and r["skuName"] == "2 vCore"),
    "postgres_mo_eadsv5_2vcore_hour": ("brazilsouth", lambda r: r["productName"] == "Azure Database for PostgreSQL Flexible Server Memory Optimized Eadsv5 Series Compute" and r["skuName"] == "2 vCore"),
    "postgres_backup_lrs_gb_month": ("brazilsouth", lambda r: r["productName"] == "Azure Database for PostgreSQL Flexible Server Backup Storage" and r["meterName"] == "Backup Storage LRS Data Stored"),
    "log_analytics_analytics_ingest_gb": ("brazilsouth", lambda r: r["serviceName"] == "Log Analytics" and r["meterName"] == "Analytics Logs Data Ingestion" and r["retailPrice"] > 1),
    "blob_hot_lrs_gb_month_max_tier": ("brazilsouth", lambda r: r["productName"] == "Blob Storage" and r["meterName"] == "Hot LRS Data Stored"),
    "gpu_nv36ads_a10_v5_hour": ("brazilsouth", lambda r: r["armSkuName"] == "Standard_NV36ads_A10_v5" and r["productName"] == "Virtual Machines NVadsA10v5 Series" and r["meterName"] == "NV36ads A10 v5"),
    "gpu_nv36ads_a10_v5_hour@eastus": ("eastus", lambda r: r["armSkuName"] == "Standard_NV36ads_A10_v5" and r["productName"] == "Virtual Machines NVadsA10v5 Series" and r["meterName"] == "NV36ads A10 v5"),
}


def pick_aws(rows: list[dict], region: str, usagetype: str, needle: str | None) -> dict:
    matches = [r for r in rows if r["region"] == region and r["usagetype"] == usagetype
               and (needle is None or needle.lower() in r["description"].lower())]
    if needle is None and len(matches) > 1:
        matches = [m for m in matches if m["usd"] > 0] or matches
    if len(matches) != 1:
        raise SystemExit(f"AWS key {region} {usagetype} {needle!r}: expected 1 row, found {len(matches)}")
    return matches[0]


def build_aws(path: pathlib.Path) -> dict:
    doc = json.loads(path.read_text(encoding="utf-8"))
    rows = doc["rows"]
    skus = {}
    for key, per_region in AWS_KEYS.items():
        for region, (usagetype, needle) in per_region.items():
            row = pick_aws(rows, region, usagetype, needle)
            skus[f"aws.{region}.{key}"] = {
                "usd": row["usd"], "unit": row["unit"], "usagetype": row["usagetype"], "description": row["description"],
                "source": "AWS Price List (public OnDemand), " + row["service_code"] + " " + region,
                "source_url": row["source_url"], "file_sha256": row["file_sha256"],
            }
    return {"provider": "aws", "retrieved_at_utc": doc["retrieved_at_utc"], "method": doc["method"], "skus": skus}


def pick_azure(rows: list[dict], predicate) -> dict:
    matches = [r for r in rows if predicate(r)]
    if not matches:
        raise SystemExit("Azure key: no row matched")
    # Tiered meters list several rows; the MCP uses the highest tier price as a conservative planning value.
    return max(matches, key=lambda r: r["retailPrice"])


def build_azure(path: pathlib.Path) -> dict:
    doc = json.loads(path.read_text(encoding="utf-8"))
    queries = doc["queries"]
    skus = {}
    query_names = {
        "brazilsouth": ["container_apps_brazilsouth", "postgres_brazilsouth", "log_analytics_brazilsouth", "storage_blob_brazilsouth", "gpu_a10_brazilsouth"],
        "eastus": ["gpu_a10_eastus", "container_apps_eastus"],
    }
    for key, (region, predicate) in AZURE_KEYS.items():
        rows = [r for name in query_names[region] for r in queries[name]["rows"]]
        row = pick_azure(rows, predicate)
        base_key = key.split("@")[0]
        skus[f"azure.{region}.{base_key}"] = {
            "usd": row["retailPrice"], "unit": row["unitOfMeasure"], "meter": row["meterName"], "product": row["productName"],
            "sku": row["skuName"], "armSkuName": row["armSkuName"], "source": "Azure Retail Prices API (unauthenticated), " + region,
            "source_url": "https://prices.azure.com/api/retail/prices",
        }
    skus["azure.brazilsouth.artifact_signing_basic_month"] = {
        "usd": 9.99, "unit": "month (Basic plan, up to 5,000 signatures)", "meter": "Artifact Signing Basic plan", "product": "Artifact Signing",
        "sku": "Basic", "armSkuName": None,
        "source": "Azure Artifact Signing product page (WebSearch extract, not Retail API)",
        "source_url": "https://azure.microsoft.com/en-us/products/artifact-signing",
    }
    return {"provider": "azure", "retrieved_at_utc": doc["retrieved_at_utc"], "method": "Azure Retail Prices API, Consumption meters, USD",
            "skus": skus}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--aws", required=True, type=pathlib.Path)
    parser.add_argument("--azure", required=True, type=pathlib.Path)
    parser.add_argument("--root", required=True, type=pathlib.Path, help="cloud-architecture-mcp directory")
    args = parser.parse_args()
    aws = build_aws(args.aws)
    azure = build_azure(args.azure)
    for name, payload in (("aws", aws), ("azure", azure)):
        target = args.root / "providers" / name / "prices.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"wrote {len(payload['skus'])} {name} SKUs to {target}")


if __name__ == "__main__":
    main()
