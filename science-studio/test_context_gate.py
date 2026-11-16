"""Contratos da trava de contexto visual (stdlib only; sem FFmpeg nem rede).

REGRA: PROIBIDO frame visual fora do contexto do roteiro. Falha fechada, sem bypass.
"""
import json
import tempfile
import unittest
from pathlib import Path

import context_gate


class Tokenizacao(unittest.TestCase):
    def test_familias_de_dominio_sao_dados_declarados(self):
        # átomo ↔ atom e música ↔ music casam pelas famílias; nunca por inferência semântica.
        self.assertEqual(context_gate.match_score({'atomo'}, {'atom'}), 1)
        self.assertEqual(context_gate.match_score({'musica'}, {'music'}), 1)

    def test_familia_desconhecida_nao_cria_parentesco(self):
        # Sem família declarada, 'foguete' não casa com 'átomo' (gate estrito).
        self.assertEqual(context_gate.match_score({'atomo'}, {'foguete'}), 0)

    def test_plural_e_acentos_sao_normalizados(self):
        tokens = context_gate.context_tokens('Os átomos de hidrogênio.', '')
        self.assertIn('atomo', tokens)
        self.assertIn('hidrogenio', tokens)

    def test_stopwords_e_tokens_curtos_ficam_fora(self):
        self.assertEqual(context_gate.context_tokens('O de da que e no com por para', ''), set())

    def test_contexto_combina_topico_narracao_e_visual(self):
        tokens = context_gate.context_tokens(
            'Cosmologia', 'O elétron orbita o núcleo.', 'átomo em close', '')
        self.assertTrue({'atomo', 'eletron'} <= tokens)


class ProvenienciaEGate(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='context-gate-')
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def projeto(self):
        return {
            'topic': 'História da música eletrônica',
            'scenes': [{
                'narration': 'A música dos anos 1980 mudou o rádio.',
                'visual': 'vinil girando em toca-discos vintage',
                'layers': [{'path': 'assets/0000-background.png', 'kind': 'image'}],
            }],
        }

    def test_asset_gerado_com_prompt_do_roteiro_passa(self):
        context_gate.record_generation(self.root, 'assets/0000-background.png', 0, 'background',
                                       'vinil girando em toca-discos vintage, comic art', 1000)
        ok, msg = context_gate.gate_visual_context(self.projeto(), self.root)
        self.assertTrue(ok, msg)
        report = json.loads((self.root / 'context_report.json').read_text(encoding='utf-8'))
        self.assertEqual(report['violations'], [])
        self.assertEqual(report['scenes'][0]['layers'][0]['verdict'], 'proven')

    def test_asset_gerado_para_outra_cena_bloqueia(self):
        context_gate.record_generation(self.root, 'assets/0000-background.png', 3, 'background',
                                       'vinil girando', 1000)
        ok, msg = context_gate.gate_visual_context(self.projeto(), self.root)
        self.assertFalse(ok)
        self.assertIn('cena 3', msg)

    def test_prompt_fora_do_contexto_bloqueia(self):
        context_gate.record_generation(self.root, 'assets/0000-background.png', 0, 'background',
                                       'foguete na estrada', 1000)
        ok, msg = context_gate.gate_visual_context(self.projeto(), self.root)
        self.assertFalse(ok)
        self.assertIn('FORA DO CONTEXTO', msg)

    def test_reutilizado_sem_prova_de_geracao_bloqueia(self):
        context_gate.record_generation(self.root, 'assets/0000-background.png', 0, 'background',
                                       'vinil girando', 1000, generated=False)
        ok, msg = context_gate.gate_visual_context(self.projeto(), self.root)
        self.assertFalse(ok)
        self.assertIn('generated=false', msg)

    def test_sem_ledger_exige_nome_citando_o_contexto(self):
        (self.root / 'assets').mkdir()
        (self.root / 'assets' / 'vinil-toca-discos.png').write_bytes(b'x')
        projeto = self.projeto()
        projeto['scenes'][0]['layers'][0]['path'] = 'assets/vinil-toca-discos.png'
        ok, msg = context_gate.gate_visual_context(projeto, self.root)
        self.assertTrue(ok, msg)

    def test_sem_ledger_e_sem_nome_em_contexto_bloqueia(self):
        (self.root / 'assets').mkdir()
        (self.root / 'assets' / '0000-background.png').write_bytes(b'x')
        ok, msg = context_gate.gate_visual_context(self.projeto(), self.root)
        self.assertFalse(ok)

    def test_ledger_ilegivel_falha_fechada(self):
        (self.root / 'assets').mkdir()
        (self.root / 'assets' / 'prompts.json').write_text('{quebrado', encoding='utf-8')
        ok, msg = context_gate.gate_visual_context(self.projeto(), self.root)
        self.assertFalse(ok)
        self.assertIn('ilegivel', msg)

    def test_cena_sem_tokens_de_roteiro_bloqueia(self):
        projeto = {'topic': '',
                   'scenes': [{'narration': 'o de da', 'visual': '', 'layers': []}]}
        ok, msg = context_gate.gate_visual_context(projeto, self.root)
        self.assertFalse(ok)
        self.assertIn('contexto do roteiro vazio', msg)


class SelecaoDoBuildLayers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import build_layers
        cls.build_layers = build_layers

    @staticmethod
    def indice():
        return [
            {'path': Path('atom-orbit.gif'),
             'tokens': context_gate.asset_name_tokens('atom-orbit')},
            {'path': Path('guitar-solo.gif'),
             'tokens': context_gate.asset_name_tokens('guitar-solo')},
        ]

    def test_cena_de_atomo_recebe_asset_de_atomo_e_nunca_o_aleatorio(self):
        scene = {'narration': 'O átomo de hidrogênio tem um elétron.', 'visual': 'modelo atômico'}
        foreground, background, score = self.build_layers.context_gate.select_scene_assets(
            self.indice(), scene, topic='Física quântica')
        self.assertEqual(foreground['path'].name, 'atom-orbit.gif')
        # Sem segundo asset em contexto, o fundo reusa o primeiro (nunca um fora de contexto).
        self.assertEqual(background['path'].name, 'atom-orbit.gif')
        self.assertGreaterEqual(score, 1)

    def test_cena_de_musica_recebe_asset_de_musica(self):
        scene = {'narration': 'O solo de guitarra marcou o estilo musical da década.',
                 'visual': ''}
        foreground, _, _ = self.build_layers.context_gate.select_scene_assets(
            self.indice(), scene)
        self.assertEqual(foreground['path'].name, 'guitar-solo.gif')

    def test_zero_match_levanta_erro_bloqueante(self):
        scene = {'narration': 'A fotossíntese acontece nas folhas verdes.',
                 'visual': 'clorofila na folha'}
        with self.assertRaises(self.build_layers.context_gate.OffContextError):
            self.build_layers.context_gate.select_scene_assets(self.indice(), scene)

    def test_narracao_sozinha_sustenta_o_contexto(self):
        scene = {'narration': 'Desenho do átomo de Bohr.', 'visual': ''}
        foreground, _, _ = self.build_layers.context_gate.select_scene_assets(
            self.indice(), scene)
        self.assertEqual(foreground['path'].name, 'atom-orbit.gif')


if __name__ == '__main__':
    unittest.main(verbosity=2)
