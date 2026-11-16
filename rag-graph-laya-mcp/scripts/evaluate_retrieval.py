"""Compare retrieval strategies on one frozen source-level oracle, without training on it."""
import argparse
import json
import math
import time
from pathlib import Path

import httpx


def metrics(evidence, gold):
    ranking = list(dict.fromkeys(e['source_id'] for e in evidence))
    gain = [1 if source in gold else 0 for source in ranking]
    dcg = sum(value / math.log2(rank + 2) for rank, value in enumerate(gain))
    ideal = sum(1 / math.log2(rank + 2) for rank in range(min(len(gold), len(ranking))))
    return {'source_recall_at_k': len(set(ranking) & set(gold)) / max(1, len(gold)),
            'source_ndcg_at_k': dcg / ideal if ideal else 0, 'source_ranking': ranking}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cases', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    cases = json.loads(args.cases.read_text(encoding='utf-8'))
    output = {'scope': cases['scope'], 'measurements': []}
    with httpx.Client(timeout=900) as client:
        for case in cases['cases']:
            for strategy in ['hybrid', 'graph', 'laya']:
                started = time.perf_counter()
                response = client.post('http://127.0.0.1:8765/api/tools/search',
                    json={'query': case['query'], 'strategy': strategy, 'limit': 5})
                response.raise_for_status()
                value = response.json()
                record = {'query': case['query'], 'strategy': strategy, 'latency_ms': (time.perf_counter()-started)*1000,
                          **metrics(value['evidence'], case['expected_source_ids']),
                          'decisions': value['decisions'], 'index_version': value['index_version']}
                output['measurements'].append(record)
                args.output.write_text(json.dumps(output, indent=2), encoding='utf-8')
                print(json.dumps({k: v for k, v in record.items() if k != 'decisions'}), flush=True)


if __name__ == '__main__':
    main()
