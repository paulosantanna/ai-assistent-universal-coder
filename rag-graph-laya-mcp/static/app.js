const $ = id => document.getElementById(id);
let sources = [], graph, stream, timer, highlighted = new Set();
const jobs = new Map();
function error(err) { $('error').textContent = err.message || String(err); $('error').hidden = false; }
async function call(name, data = {}) {
  const response = await fetch(`/api/tools/${name}`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data) });
  const value = await response.json();
  if (!response.ok) throw new Error(value.detail || 'Falha no serviço');
  if (value.job_id && value.status === 'queued') { jobs.set(value.job_id, value); renderJobs(); }
  return value;
}
function button(id, action) {
  $(id).addEventListener('click', async () => { $(id).disabled = true; $('error').hidden = true;
    try { await action(); } catch (err) { error(err); } finally { $(id).disabled = false; }
  });
}
function metadata() { const s = sources.find(s=>s.id===$('source').value); $('source-meta').textContent = s ? `${s.author} · ${s.license} · ${s.status}` : ''; }
async function loadSources() {
  const selected = $('source').value; sources = (await call('sources_list')).sources;
  $('source').replaceChildren(...sources.map(s=>{const o=document.createElement('option');o.value=s.id;o.textContent=s.title;return o;}));
  if (sources.some(s=>s.id===selected)) $('source').value=selected; metadata();
}
function renderJobs() {
  $('jobs').replaceChildren(...Array.from(jobs.values()).reverse().map(j=>{
    const el=document.createElement('div');el.className='job';
    const text=document.createElement('span');text.textContent=`${j.operation||'Trabalho'} · ${j.status} · ${Math.round((j.progress||0)*100)}% ${j.error||''}`;el.append(text);
    if(['queued','running'].includes(j.status)){const b=document.createElement('button');b.textContent='Cancelar';b.onclick=()=>call('job_cancel',{job_id:j.id||j.job_id}).catch(error);el.append(b);}
    if(j.result){const pre=document.createElement('pre');pre.textContent=JSON.stringify(j.result,null,2);el.append(pre);if(j.result.dataset_id)$('dataset-id').value=j.result.dataset_id;}
    return el;
  }));
}
function showDetail(item, isNode) {
  $('detail').textContent=JSON.stringify(item,null,2);
  if(!isNode)return;
  const expand=document.createElement('button');expand.textContent='Mostrar vizinhos';
  expand.onclick=async()=>{expand.disabled=true;try{
    const value=await call('graph_neighbors',{node_id:item.id});
    for(const neighbor of [...value.nodes,...value.edges])if(!graph.getElementById(neighbor.id).length)graph.add({data:neighbor});
    if(value.truncated)error(new Error('A exploração atingiu o limite de entidades desta visão.'));
  }catch(err){error(err);}finally{expand.disabled=false;}};
  $('detail').append(expand);
}
function table(snapshot) {
  const t=document.createElement('table');const head=document.createElement('tr');
  for(const text of ['Tipo','Nome/relação','Fontes']){const th=document.createElement('th');th.textContent=text;head.append(th);}t.append(head);
  for(const item of [...snapshot.nodes,...snapshot.edges]){const row=document.createElement('tr');
    for(const [index,value] of [item.type||'relação',item.label,(item.source_ids||[]).join(', ')].entries()){
      const cell=document.createElement('td');if(index===1){const select=document.createElement('button');select.textContent=value;select.onclick=()=>showDetail(item,!!item.type);cell.append(select);}else cell.textContent=value;row.append(cell);
    }t.append(row);}
  $('graph-table').replaceChildren(t);
}
async function snapshot() {
  const snap=await call('graph_snapshot'); table(snap);
  $('graph-count').textContent=`${snap.total_nodes} entidades · ${snap.edges.length} relações${snap.truncated?' · visão limitada':''}`;
  if(!window.cytoscape)throw new Error('Cytoscape local ausente; execute o bootstrap de recursos. A tabela continua disponível.');
  const elements=[...snap.nodes.map(n=>({data:{...n}})),...snap.edges.map(e=>({data:{...e}}))];
  if(!graph){graph=window.cytoscape({container:$('graph'),elements,style:[{selector:'node',style:{label:'data(label)','background-color':'#95c994',color:'#dfece1','font-size':10}},{selector:'edge',style:{'line-color':'#567f66','target-arrow-color':'#567f66','target-arrow-shape':'triangle','curve-style':'bezier',width:1.5}},{selector:'.highlight',style:{'background-color':'#efd082','line-color':'#efd082','border-color':'#efd082','border-width':3}}],layout:{name:'cose',animate:false}});
    graph.on('tap','node,edge',event=>showDetail(event.target.data(),event.target.isNode()));
  }else{const positions=new Map(graph.nodes().map(n=>[n.id(),n.position()]));graph.elements().remove();graph.add(elements);for(const n of graph.nodes()){if(positions.has(n.id()))n.position(positions.get(n.id()));}if(!positions.size)graph.layout({name:'cose',animate:false}).run();}
  graph.elements().removeClass('highlight'); graph.elements().filter(e=>highlighted.has(e.id())).addClass('highlight');
  if(!stream){stream=new EventSource(`/api/events?after=${snap.cursor}`);stream.onopen=()=>$('connection').textContent='Ao vivo';stream.onerror=()=>$('connection').textContent='Reconectando…';
    stream.addEventListener('graph.changed',()=>{clearTimeout(timer);timer=setTimeout(()=>snapshot().catch(error),150);});
    stream.addEventListener('job.changed',async event=>{const update=JSON.parse(event.data);try{const job=await call('job_status',{job_id:update.job_id});jobs.set(update.job_id,job);renderJobs();if(job.status==='succeeded')await loadSources();}catch(err){error(err);}});
    stream.addEventListener('query.retrieved',event=>{const value=JSON.parse(event.data);highlighted=new Set(value.graph_ids||value.evidence_ids);snapshot().catch(error);});
  }
}
$('source').addEventListener('change',metadata);
$('filter').addEventListener('input',()=>{if(graph){const query=$('filter').value.toLowerCase();graph.nodes().forEach(n=>n.style('opacity',n.data('label').toLowerCase().includes(query)?1:.15));}});
button('acquire',()=>call('sources_refresh',{source_ids:[$('source').value]}));
button('ingest',()=>call('ingest',{source_id:$('source').value}));
button('remove',async()=>{const s=sources.find(s=>s.id===$('source').value);if(!s.document_id)throw new Error('A fonte não possui documento adquirido.');return call('ingest',{source_id:s.id,action:'remove',document_id:s.document_id});});
button('ask',async()=>{const result=await call('answer',{query:$('query').value,strategy:$('strategy').value});$('answer').textContent=result.answer;
  $('detail').textContent=`Recuperação: ${result.effective_strategy||result.strategy}. `+(result.decisions.length?`Laya: ${result.decisions.filter(d=>d.used).length} decisões aplicadas; ${result.decisions.filter(d=>!d.used).length} mantidas no fallback por calibração/confiança.`:'');
  const list=document.createElement('ol');for(const citation of result.citations){const li=document.createElement('li'),a=document.createElement('a');const url=new URL(citation.url);if(!['https:','http:'].includes(url.protocol))continue;a.href=url.href;a.textContent=`[${citation.number}] ${citation.source_id}`;a.target='_blank';a.rel='noopener noreferrer';li.append(a);list.append(li);}$('answer').append(list);
});
button('dataset',()=>call('dataset_prepare',{count:Number($('count').value)}));
button('train',()=>call('train',{flow:$('flow').value,dataset_id:$('dataset-id').value}));
button('evaluate',()=>call('evaluate',{flow:$('flow').value,dataset_id:$('dataset-id').value}));
button('snapshot',snapshot);button('fit',()=>graph?.fit(undefined,25));
try{await loadSources();await snapshot();$('health').textContent=JSON.stringify(await call('health'),null,2);}catch(err){error(err);}
