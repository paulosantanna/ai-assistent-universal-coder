"""Print only the official CUDA wheel matching this locked interpreter/platform."""
import re
import urllib.request

html = urllib.request.urlopen('https://download.pytorch.org/whl/cu130/torch/', timeout=30).read().decode()
links = re.findall(r'href="([^"]+torch-2\.14\.1[^\"]+cp312-cp312-win_amd64\.whl[^\"]*)"', html)
print('\n'.join(links) if links else 'No matching CUDA wheel; stop before claiming GPU support')
