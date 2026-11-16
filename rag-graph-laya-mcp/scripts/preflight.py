"""Read-only environment report: no implicit weights download."""
import importlib.metadata
import json
import platform
import sys

report = {'python': sys.version, 'platform': platform.platform(), 'packages': {}, 'cuda': False}
for name in ['mcp', 'graphiti-core', 'laya', 'torch', 'transformers', 'trl', 'peft', 'bitsandbytes']:
    try:
        report['packages'][name] = importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        report['packages'][name] = None
if report['packages']['torch']:
    import torch
    report.update(cuda=torch.cuda.is_available(), torch_cuda=torch.version.cuda)
    if report['cuda']:
        report.update(gpu=torch.cuda.get_device_name(), vram_bytes=torch.cuda.get_device_properties(0).total_memory)
        x = torch.ones(16, device='cuda')
        report['cuda_kernel'] = float(x.sum()) == 16
print(json.dumps(report, indent=2))
