"""CLI for persistent API jobs. Does not repeat an uncertain job automatically."""
import argparse
import asyncio
import json
import sys
from pathlib import Path

import httpx


async def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument('operation')
    parser.add_argument('--args', default='{}')
    parser.add_argument('--args-file', type=Path)
    parser.add_argument('--job-id')
    parser.add_argument('--wait', action='store_true')
    args = parser.parse_args()
    payload = json.loads(args.args_file.read_text(encoding='utf-8')) if args.args_file else json.loads(args.args)
    if args.job_id:
        payload['job_id'] = args.job_id
    async with httpx.AsyncClient(timeout=330) as client:
        response = await client.post('http://127.0.0.1:8765/api/tools/' + args.operation, json=payload)
        response.raise_for_status()
        value = response.json()
        print(json.dumps(value, ensure_ascii=False), flush=True)
        if args.wait and value.get('job_id'):
            job_id = value['job_id']
            previous = None
            while True:
                response = await client.post('http://127.0.0.1:8765/api/tools/job_status', json={'job_id': job_id})
                response.raise_for_status()
                job = response.json()
                status = (job['status'], round(job['progress'], 2))
                if status != previous:
                    print(json.dumps({'job_id': job_id, 'status': job['status'], 'progress': job['progress'], 'error': job['error']}), flush=True)
                    previous = status
                if job['status'] not in {'queued', 'running'}:
                    print(json.dumps(job, ensure_ascii=False), flush=True)
                    if job['status'] != 'succeeded':
                        sys.exit(1)
                    break
                await asyncio.sleep(2)


if __name__ == '__main__':
    asyncio.run(main())
