const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = process.argv[2] || './output/html';
const DIAGRAMS_DIR = process.argv[3] || './diagrams';
const BASE_DIR = process.argv[4] || './output';

function main() {
  const outputPath = path.resolve(OUTPUT_DIR);
  fs.mkdirSync(outputPath, { recursive: true });

  const diagramSvgs = loadDiagramSVGs();
  const dataDictionary = loadDataDictionary(BASE_DIR);
  const views = loadViews(BASE_DIR);
  const layers = loadLayers(BASE_DIR);
  const improvements = loadImprovements(BASE_DIR);

  const html = generateHTML({ diagramSvgs, dataDictionary, views, layers, improvements });

  fs.writeFileSync(path.join(outputPath, 'documentacao.html'), html, 'utf-8');
  console.log('Generated: documentacao.html');
}

function loadDiagramSVGs() {
  const svgDir = path.resolve(DIAGRAMS_DIR, 'svg');
  if (!fs.existsSync(svgDir)) return {};
  const files = fs.readdirSync(svgDir).filter(f => f.endsWith('.svg'));
  const svgs = {};
  files.forEach(f => {
    svgs[path.basename(f, '.svg')] = fs.readFileSync(path.join(svgDir, f), 'utf-8');
  });
  return svgs;
}

function loadDataDictionary(baseDir) {
  const dataDir = path.resolve(baseDir, 'data');
  if (!fs.existsSync(dataDir)) return '';
  const yamlFile = path.join(dataDir, 'dicionario_de_dados.yaml');
  if (!fs.existsSync(yamlFile)) return '';
  return fs.readFileSync(yamlFile, 'utf-8');
}

function loadViews(baseDir) {
  const viewsDir = path.resolve(baseDir, 'views');
  if (!fs.existsSync(viewsDir)) return {};
  const views = {};
  ['visao_negocio.md', 'visao_desenvolvedor.md', 'visao_diretoria.md'].forEach(f => {
    const p = path.join(viewsDir, f);
    if (fs.existsSync(p)) views[f] = fs.readFileSync(p, 'utf-8');
  });
  return views;
}

function loadLayers(baseDir) {
  const dataDir = path.resolve(baseDir, 'data');
  if (!fs.existsSync(dataDir)) return '';
  const yamlFile = path.join(dataDir, 'analise_camadas.yaml');
  if (!fs.existsSync(yamlFile)) return '';
  return fs.readFileSync(yamlFile, 'utf-8');
}

function loadImprovements(baseDir) {
  const impDir = path.resolve(baseDir, 'improvement');
  if (!fs.existsSync(impDir)) return '';
  const mdFile = path.join(impDir, 'plano_de_melhorias.md');
  if (!fs.existsSync(mdFile)) return '';
  return fs.readFileSync(mdFile, 'utf-8');
}

function generateHTML(data) {
  const { diagramSvgs, dataDictionary, views, layers, improvements } = data;

  const diagramNav = Object.keys(diagramSvgs).map(name => {
    const label = name.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    return `<li><a href="#" onclick="showDiagram('${name}')">${label}</a></li>`;
  }).join('\n');

  const diagramPanels = Object.entries(diagramSvgs).map(([name, svg]) => {
    const label = name.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    const entities = extractEntities(svg);
    const entityLinks = entities.map(e =>
      `<span class="entity-link" onclick="highlightEntity('${name}', '${e}')">${e}</span>`
    ).join(', ');
    return `
      <div class="diagram-panel" id="diagram-${name}">
        <h3>${label}</h3>
        <div class="diagram-entities">Entities: ${entityLinks}</div>
        <div class="diagram-svg" id="svg-${name}">${svg}</div>
      </div>`;
  }).join('\n');

  const viewTabs = Object.entries(views).map(([file, content]) => {
    const name = file.replace('.md', '').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    return `
      <div class="view-panel" id="view-${file}">
        <h3>${name}</h3>
        <pre class="markdown-content">${escapeHtml(content)}</pre>
      </div>`;
  }).join('\n');

  const viewNav = Object.keys(views).map(file => {
    const name = file.replace('.md', '').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
    return `<li><a href="#" onclick="showView('${file}')">${name}</a></li>`;
  }).join('\n');

  return `<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Documentação do Projeto — AEOS Documentation Mapper</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Segoe UI', Tahoma, sans-serif; display: flex; min-height: 100vh; background: #f5f7fa; color: #333; }
  #sidebar { width: 280px; background: #1a1a2e; color: #e0e0e0; padding: 20px; overflow-y: auto; position: fixed; top: 0; left: 0; height: 100vh; z-index: 100; }
  #sidebar h1 { font-size: 18px; margin-bottom: 20px; color: #fff; border-bottom: 2px solid #e94560; padding-bottom: 10px; }
  #sidebar h2 { font-size: 14px; color: #e94560; margin: 15px 0 8px 0; text-transform: uppercase; letter-spacing: 1px; }
  #sidebar ul { list-style: none; margin-bottom: 15px; }
  #sidebar ul li a { display: block; padding: 6px 10px; color: #b0b0b0; text-decoration: none; font-size: 13px; border-radius: 4px; transition: all 0.2s; }
  #sidebar ul li a:hover { background: #16213e; color: #fff; }
  #content { margin-left: 280px; flex: 1; padding: 30px; max-width: calc(100vw - 280px); }
  #search-box { width: 100%; padding: 12px 16px; font-size: 15px; border: 2px solid #ddd; border-radius: 8px; margin-bottom: 25px; }
  .diagram-panel { display: none; background: #fff; border-radius: 12px; padding: 25px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
  .diagram-panel.active { display: block; }
  .diagram-panel h3 { font-size: 20px; color: #1a1a2e; margin-bottom: 15px; }
  .diagram-entities { margin-bottom: 15px; font-size: 13px; color: #666; }
  .diagram-entities .entity-link { display: inline-block; background: #eef2ff; color: #4f46e5; padding: 2px 8px; border-radius: 4px; margin: 2px 4px 2px 0; cursor: pointer; font-size: 12px; border: 1px solid #c7d2fe; transition: all 0.2s; }
  .diagram-entities .entity-link:hover { background: #4f46e5; color: #fff; }
  .diagram-svg { overflow-x: auto; }
  .diagram-svg svg { max-width: 100%; height: auto; }
  .view-panel { display: none; }
  .view-panel.active { display: block; }
  .markdown-content { background: #f8f9fa; padding: 20px; border-radius: 8px; white-space: pre-wrap; font-family: 'Consolas', monospace; font-size: 13px; line-height: 1.6; overflow-x: auto; }
  .data-dictionary { background: #fff; border-radius: 12px; padding: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
  .data-dictionary pre { background: #f8f9fa; padding: 15px; border-radius: 8px; overflow-x: auto; font-size: 13px; }
  .improvement-panel { background: #fff; border-radius: 12px; padding: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
  .improvement-panel pre { background: #f8f9fa; padding: 15px; border-radius: 8px; overflow-x: auto; font-size: 13px; }
  .tab-bar { display: flex; gap: 4px; margin-bottom: 20px; flex-wrap: wrap; }
  .tab-bar button { padding: 10px 20px; background: #e0e0e0; border: none; border-radius: 8px 8px 0 0; cursor: pointer; font-size: 14px; font-weight: 600; color: #555; transition: all 0.2s; }
  .tab-bar button:hover { background: #d0d0d0; }
  .tab-bar button.active { background: #1a1a2e; color: #fff; }
  #layers-content { background: #fff; border-radius: 12px; padding: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
  #layers-content pre { background: #f8f9fa; padding: 15px; border-radius: 8px; overflow-x: auto; font-size: 13px; white-space: pre-wrap; }
  .highlight { transition: all 0.3s; }
  .highlight rect { fill: #e94560 !important; }
  .highlight text { fill: #fff !important; }
  #print-btn { position: fixed; bottom: 20px; right: 20px; padding: 12px 24px; background: #e94560; color: #fff; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 12px rgba(233,69,96,0.4); z-index: 200; }
  #print-btn:hover { background: #d63851; }
  @media print { #sidebar, #search-box, #print-btn, .tab-bar { display: none !important; } #content { margin-left: 0; max-width: 100%; } }
  @media (max-width: 768px) { #sidebar { width: 100%; height: auto; position: relative; } #content { margin-left: 0; max-width: 100%; padding: 15px; } }
</style>
</head>
<body>
<nav id="sidebar">
  <h1>📋 Documentação do Projeto</h1>
  <div id="search-box-div"><input type="text" id="search-box" placeholder="Pesquisar..." oninput="searchContent(this.value)"></div>
  <h2>Diagramas</h2>
  <ul>${diagramNav}</ul>
  <h2>Visões</h2>
  <ul>${viewNav}</ul>
  <h2>Seções</h2>
  <ul>
    <li><a href="#" onclick="showSection('layers')">Análise de Camadas</a></li>
    <li><a href="#" onclick="showSection('dictionary')">Dicionário de Dados</a></li>
    <li><a href="#" onclick="showSection('improvements')">Plano de Melhorias</a></li>
  </ul>
</nav>
<main id="content">
  <div class="tab-bar">
    <button class="active" onclick="switchTab('diagrams', this)">Diagramas</button>
    <button onclick="switchTab('views', this)">Visões</button>
    <button onclick="switchTab('layers', this)">Camadas</button>
    <button onclick="switchTab('dictionary', this)">Dicionário</button>
    <button onclick="switchTab('improvements', this)">Melhorias</button>
  </div>

  <div id="tab-diagrams">
    ${diagramPanels}
  </div>

  <div id="tab-views" style="display:none">
    <div class="tab-bar">
      ${Object.keys(views).map((file, i) => {
        const name = file.replace('.md', '').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
        return `<button class="${i === 0 ? 'active' : ''}" onclick="switchSubview('${file}', this)">${name}</button>`;
      }).join('\n')}
    </div>
    ${viewTabs}
  </div>

  <div id="tab-layers" style="display:none">
    <div id="layers-content">
      <pre>${escapeHtml(layers || '# Nenhuma análise de camadas disponível')}</pre>
    </div>
  </div>

  <div id="tab-dictionary" style="display:none">
    <div class="data-dictionary">
      <h3>Dicionário de Dados</h3>
      <pre>${escapeHtml(dataDictionary || '# Nenhum dicionário de dados disponível')}</pre>
    </div>
  </div>

  <div id="tab-improvements" style="display:none">
    <div class="improvement-panel">
      <h3>Plano de Melhorias</h3>
      <pre>${escapeHtml(improvements || '# Nenhum plano de melhorias disponível')}</pre>
    </div>
  </div>

  <button id="print-btn" onclick="window.print()">📄 Exportar PDF</button>
</main>

<script>
  const entityMap = {};
  let searchIndex = [];

  function buildSearchIndex() {
    searchIndex = [];
    document.querySelectorAll('.diagram-panel').forEach(p => {
      const title = p.querySelector('h3')?.textContent || '';
      const text = p.textContent || '';
      searchIndex.push({ id: p.id, title, text, type: 'diagram' });
    });
    document.querySelectorAll('.view-panel').forEach(p => {
      const title = p.querySelector('h3')?.textContent || '';
      const text = p.textContent || '';
      searchIndex.push({ id: p.id, title, text, type: 'view' });
    });
    if (document.getElementById('layers-content')) {
      searchIndex.push({ id: 'layers-content', title: 'Análise de Camadas', text: document.getElementById('layers-content').textContent, type: 'layers' });
    }
    if (document.querySelector('.data-dictionary')) {
      searchIndex.push({ id: 'dictionary-content', title: 'Dicionário de Dados', text: document.querySelector('.data-dictionary').textContent, type: 'dictionary' });
    }
    if (document.querySelector('.improvement-panel')) {
      searchIndex.push({ id: 'improvements-content', title: 'Plano de Melhorias', text: document.querySelector('.improvement-panel').textContent, type: 'improvements' });
    }
  }

  function searchContent(query) {
    if (!query.trim()) {
      document.querySelectorAll('[id^="diagram-"], [id^="view-"], #layers-content, .data-dictionary, .improvement-panel').forEach(el => {
        if (el.id?.startsWith('diagram-') || el.id?.startsWith('view-') || el.id === 'layers-content') {
          el.style.display = '';
        }
      });
      return;
    }
    const q = query.toLowerCase();
    searchIndex.forEach(item => {
      const el = document.getElementById(item.id);
      if (!el) return;
      if (item.text.toLowerCase().includes(q)) {
        el.style.display = '';
        if (item.id.startsWith('diagram-')) {
          document.getElementById('tab-diagrams').style.display = '';
          showDiagram(item.id.replace('diagram-', ''));
        }
      } else {
        el.style.display = 'none';
      }
    });
  }

  function showDiagram(name) {
    document.querySelectorAll('.diagram-panel').forEach(p => p.classList.remove('active'));
    const panel = document.getElementById('diagram-' + name);
    if (panel) panel.classList.add('active');
    switchTab('diagrams', document.querySelector('.tab-bar button:first-child'));
  }

  function showView(file) {
    document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active'));
    const panel = document.getElementById('view-' + file);
    if (panel) panel.classList.add('active');
    switchTab('views', document.querySelectorAll('.tab-bar button')[1]);
    document.querySelectorAll('#tab-views .tab-bar button').forEach((b, i) => {
      b.classList.toggle('active', b.textContent.toLowerCase().includes(file.replace('.md','').replace(/_/g,' ')));
    });
  }

  function showSection(section) {
    if (section === 'layers') switchTab('layers', document.querySelectorAll('.tab-bar button')[2]);
    else if (section === 'dictionary') switchTab('dictionary', document.querySelectorAll('.tab-bar button')[3]);
    else if (section === 'improvements') switchTab('improvements', document.querySelectorAll('.tab-bar button')[4]);
  }

  function switchTab(tabName, btn) {
    document.querySelectorAll('.tab-bar:first-of-type button').forEach(b => b.classList.remove('active'));
    ['diagrams','views','layers','dictionary','improvements'].forEach(t => {
      document.getElementById('tab-' + t).style.display = t === tabName ? '' : 'none';
    });
    if (btn) btn.classList.add('active');
  }

  function switchSubview(file, btn) {
    document.querySelectorAll('#tab-views .view-panel').forEach(p => p.classList.remove('active'));
    const panel = document.getElementById('view-' + file);
    if (panel) panel.classList.add('active');
    document.querySelectorAll('#tab-views .tab-bar button').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
  }

  function highlightEntity(diagramName, entityName) {
    showDiagram(diagramName);
    const svg = document.querySelector('#diagram-' + diagramName + ' svg');
    if (!svg) return;
    svg.querySelectorAll('.highlight').forEach(e => e.classList.remove('highlight'));
    const entities = svg.querySelectorAll('*');
    entities.forEach(e => {
      if (e.textContent && e.textContent.includes(entityName)) {
        e.classList.add('highlight');
      }
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    const firstDiagram = document.querySelector('.diagram-panel');
    if (firstDiagram) firstDiagram.classList.add('active');
    buildSearchIndex();
  });
</script>
</body>
</html>`;
}

function extractEntities(svg) {
  const entities = [];
  const regex = />(.*?)</g;
  let match;
  while ((match = regex.exec(svg)) !== null) {
    const text = match[1].trim();
    if (text && text.length > 2 && text.length < 50 && !text.includes(' ') === false) {
      if (!entities.includes(text)) entities.push(text);
    }
  }
  return entities.slice(0, 20);
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

main();
