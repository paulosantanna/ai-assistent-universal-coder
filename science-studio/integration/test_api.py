"""Isolated FastAPI contracts; no production database or service restart."""
import importlib.util
import json
import sys
import tempfile
import unittest
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, 'D:/Git/dark-videos/backend')
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

source = ROOT / 'science-studio/integration/dark_api.py'
spec = importlib.util.spec_from_file_location('science_studio_integration_test', source)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class IntegrationContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='science-api-')
        self.folder = Path(self.temp.name)
        self.home = ROOT / 'science-studio'
        self.app = FastAPI()
        self.app.include_router(module.router)
        self.client = TestClient(self.app)
        self.config_patch = patch.object(module, 'settings', return_value=({'config': None}, self.home, self.folder))
        self.config_patch.start()
        self.app.dependency_overrides[module.require_operator] = lambda: SimpleNamespace(user=SimpleNamespace(id=uuid.uuid4()))

    def tearDown(self):
        self.config_patch.stop()
        self.temp.cleanup()

    def create(self):
        response = self.client.post('/api/science-studio/projects', json={'topic': 'Fixture topic'})
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()['id']

    def test_auth_required_on_reads_and_writes(self):
        def deny(): raise HTTPException(401, 'not_authenticated')
        self.app.dependency_overrides[module.require_operator] = deny
        self.assertEqual(self.client.get('/api/science-studio/projects').status_code, 401)
        self.assertEqual(self.client.post('/api/science-studio/projects', json={'topic': 'Fixture'}).status_code, 401)

    def test_real_cli_creation_and_listing(self):
        identifier = self.create()
        self.assertEqual(json.loads((self.folder / identifier / 'project.json').read_text())['duration'], 60)
        self.assertEqual(self.client.get('/api/science-studio/projects').json()['projects'][0]['id'], identifier)

    def test_generation_blocks_missing_config(self):
        identifier = self.create()
        response = self.client.post(f'/api/science-studio/projects/{identifier}/jobs', json={'action': 'generate'})
        self.assertEqual(response.status_code, 409)
        self.assertFalse((self.folder / identifier / '.job.lock').exists())

    def test_no_browser_paths_argv_or_publishing_action(self):
        for extra in ({'path': 'C:/'}, {'providers': ['python']}, {'config': 'local.json'}):
            response = self.client.post('/api/science-studio/projects', json={'topic': 'Fixture', **extra})
            self.assertEqual(response.status_code, 422)
        identifier = self.create()
        self.assertEqual(self.client.post(f'/api/science-studio/projects/{identifier}/jobs', json={'action': 'publish'}).status_code, 422)
        self.assertEqual(self.client.get('/api/science-studio/projects/not-a-uuid/files/preview.mp4').status_code, 422)

    def test_human_checks_and_job_exclusivity(self):
        identifier = self.create()
        endpoint = f'/api/science-studio/projects/{identifier}/jobs'
        self.assertEqual(self.client.post(endpoint, json={'action': 'review', 'checks': ['science']}).status_code, 422)
        (self.folder / identifier / '.job.lock').touch()
        self.assertEqual(self.client.post(endpoint, json={'action': 'render'}).status_code, 409)

    def test_only_allowlisted_artifacts(self):
        identifier = self.create()
        self.assertEqual(self.client.get(f'/api/science-studio/projects/{identifier}/files/project.json').status_code, 200)
        self.assertEqual(self.client.get(f'/api/science-studio/projects/{identifier}/files/config.json').status_code, 422)
        self.assertEqual(self.client.get(f'/api/science-studio/projects/{identifier}/files/final.mp4').status_code, 404)


if __name__ == '__main__':
    unittest.main(verbosity=2)
