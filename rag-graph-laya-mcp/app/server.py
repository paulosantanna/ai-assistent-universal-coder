"""Official MCP SDK transport; the HTTP service owns jobs and model state."""
import asyncio
import json
import os
from urllib.parse import urlparse

import httpx
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from pydantic import ValidationError

from .config import ROOT
from .contracts import OPERATIONS, tool_specs


async def list_tools(ctx, params):
    return types.ListToolsResult(tools=[types.Tool(**spec) for spec in tool_specs()])


async def call_tool(ctx, params):
    name, arguments = params.name, params.arguments
    if name not in OPERATIONS:
        raise ValueError('Unknown tool')
    try:
        validated = OPERATIONS[name][0].model_validate(arguments or {}).model_dump()
    except ValidationError:
        return types.CallToolResult(isError=True, content=[types.TextContent(type='text', text='Input does not match the declared tool schema')])
    endpoint = os.getenv('RGL_SERVICE_URL', 'http://127.0.0.1:8765')
    if urlparse(endpoint).hostname not in {'127.0.0.1', 'localhost', '::1'}:
        raise ValueError('The execution service must be local')
    try:
        async with httpx.AsyncClient(timeout=330) as client:
            response = await client.post(endpoint.rstrip('/') + '/api/tools/' + name, json=validated)
            if response.status_code >= 400:
                return types.CallToolResult(isError=True, content=[types.TextContent(type='text', text=json.dumps({'error': response.json().get('detail', 'Service failure')}))])
            result = response.json()
    except httpx.ConnectError:
        if name == 'health':
            result = {'mcp': 'available', 'service': 'offline', 'action': 'Run python server.py --web'}
        elif name == 'sources_list':
            result = json.loads((ROOT / 'knowledge/sources.json').read_text(encoding='utf-8'))
            for source in result['sources']:
                source['status'] = 'discovered'
        else:
            raise ValueError('Execution service is offline; run python server.py --web') from None
    return types.CallToolResult(content=[types.TextContent(type='text', text=json.dumps(result, ensure_ascii=False))])


async def list_resources(ctx, params):
    return types.ListResourcesResult(resources=[types.Resource(uri='knowledge://rag-graph-laya/sources', name='Primary sources catalog', mimeType='application/json'),
            types.Resource(uri='knowledge://rag-graph-laya/research', name='Research synthesis', mimeType='text/markdown')])


async def list_resource_templates(ctx, params):
    return types.ListResourceTemplatesResult(resourceTemplates=[types.ResourceTemplate(
        uriTemplate='knowledge://rag-graph-laya/source/{source_id}/{ordinal}',
        name='Acquired primary-source passage', mimeType='application/json',
        description='Progressive reading of acquired sources;12000characters per passage, with hash/revision provenance.')])


async def read_resource(ctx, params):
    uri = params.uri
    mapping = {'knowledge://rag-graph-laya/sources': ('sources.json', 'application/json'),
               'knowledge://rag-graph-laya/research': ('research.md', 'text/markdown')}
    if str(uri) not in mapping:
        parts = urlparse(str(uri))
        path = parts.path.strip('/').split('/')
        if parts.netloc != 'rag-graph-laya' or len(path) != 3 or path[0] != 'source' or not path[2].isdigit():
            raise ValueError('Unknown knowledge resource')
        endpoint = os.getenv('RGL_SERVICE_URL', 'http://127.0.0.1:8765')
        if urlparse(endpoint).hostname not in {'127.0.0.1', 'localhost', '::1'}:
            raise ValueError('The execution service must be local')
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(endpoint.rstrip('/') + '/api/sources/' + path[1] + '/chunks/' + path[2])
                response.raise_for_status()
        except httpx.HTTPError:
            raise ValueError('Source passage unavailable; start the execution service and acquire this source') from None
        return types.ReadResourceResult(contents=[types.TextResourceContents(uri=uri, text=response.text, mimeType='application/json')])
    filename, mime = mapping[str(uri)]
    return types.ReadResourceResult(contents=[types.TextResourceContents(uri=uri, text=(ROOT / 'knowledge' / filename).read_text(encoding='utf-8'), mimeType=mime)])


server = Server('rag-graph-laya', version='0.1.0', on_list_tools=list_tools, on_call_tool=call_tool,
                on_list_resources=list_resources, on_read_resource=read_resource,
                on_list_resource_templates=list_resource_templates)


async def run():
    async with stdio_server() as (reader, writer):
        await server.run(reader, writer, server.create_initialization_options())


def main():
    import sys
    if '--web' in sys.argv:
        import uvicorn
        uvicorn.run('app.web:app', host='127.0.0.1', port=8765, log_level='warning')
    else:
        asyncio.run(run())
