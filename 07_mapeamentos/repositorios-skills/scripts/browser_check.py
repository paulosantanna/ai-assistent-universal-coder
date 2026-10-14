"""Exercise generated report via file:// using an installed headless browser."""
import csv
import io
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from inventory import OUT

URL=(OUT/'relatorio.html').as_uri()


def run():
    checks, errors, requests = [], [], []
    def check(condition, description):
        checks.append({'check':description,'passed':bool(condition)})
        if not condition:
            errors.append(description)
    with sync_playwright() as p:
        # Explicit channels only; no downloads or profile/session reuse.
        browser=p.chromium.launch(channel='msedge',headless=True)
        page=browser.new_page(viewport={'width':1440,'height':1000},accept_downloads=True)
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.on('request',lambda req:requests.append(req.url))
        page.goto(URL)
        check(page.locator('#tbody tr').count()==11,'file:// abre os 11 projetos')
        check(page.locator('.details').count()==11,'11 mapas individuais com drill-down')
        page.locator('#search').fill('Flutter')
        check(page.locator('#tbody tr').count()==1,'Busca textual encontra apenas iBunny por Flutter')
        page.locator('#search').fill('')
        page.locator('[data-filter="0"]').fill('dark-videos')
        check(page.locator('#tbody tr').count()==2,'Filtro de coluna inclui app e pacote relacionado')
        page.locator('#reset').click()
        page.locator('#view').select_option('skills')
        check(page.locator('#tbody tr').count()==3322,'Matriz mostra todas as 3.322 combinações sem limite oculto')
        page.locator('#status').select_option('direta')
        check(page.locator('#tbody tr').count()==161,'Filtro de aplicabilidade retorna 161 associações diretas')
        page.locator('[data-filter="0"]').fill('pdfcraft')
        page.locator('[data-filter="1"]').fill('rust-expert')
        check(page.locator('#tbody tr').count()==1,'Filtros de coluna combinados por AND')
        csv_text=page.evaluate('window.exportCsv()')
        rows=list(csv.reader(io.StringIO(csv_text)))
        check(len(rows)==2 and rows[1][:2]==['pdfcraft','rust-expert'],'CSV reflete exatamente a seleção')
        with page.expect_download() as pending:
            page.locator('#export').click()
        download=pending.value
        check(download.suggested_filename.endswith('.csv'),'Botão realiza download CSV real')
        downloaded=Path(download.path()).read_bytes().decode('utf-8-sig')
        check(downloaded==csv_text,'Conteúdo exportado confere com matriz filtrada')
        page.locator('#reset').click()
        check(len(list(csv.reader(io.StringIO(page.evaluate('window.exportCsv()')))))==3323,'Exportação completa inclui 3.322 decisões e cabeçalho')
        page.locator('#view').select_option('repos')
        page.locator('[data-sort="0"]').click()
        first=page.locator('#tbody tr').first.locator('td').first.inner_text()
        page.locator('[data-sort="0"]').click()
        check(page.locator('#tbody tr').first.locator('td').first.inner_text()!=first,'Ordenação crescente e decrescente altera ordem')
        page.locator('#reset').click()
        page.locator('[data-open="0"]').first.click()
        check(page.locator('#repo-0').evaluate('(e)=>e.open'),'Drill-down abre o projeto correto')
        page.locator('#repo-0').get_by_role('link',name='Voltar à consulta').click()
        page.locator('[data-sort="0"]').focus()
        check(page.locator('#tooltip').is_visible(),'Tooltip acessível via foco e ancorado no body')
        page.keyboard.press('Escape')
        check(not page.locator('#tooltip').is_visible(),'Escape fecha tooltip')
        page.locator('#search').focus()
        check(page.evaluate('document.activeElement.id')=='search','Campo de busca acessível por foco')
        page.locator('#search').press('Tab')
        check(page.evaluate('document.activeElement.id')=='reset','Tab pula select desativado e chega ao botão')
        page.locator('#grid > details > summary').click()
        page.locator('[data-width="0"]').fill('500')
        check(page.locator('#cols col').first.evaluate('(e)=>e.style.width')=='500px','Ajuste de largura modifica coluna real')
        check(page.locator('#thead th').first.evaluate('(e)=>getComputedStyle(e).position')=='sticky','Cabeçalho congelado')
        check(page.locator('#tbody td').first.evaluate('(e)=>getComputedStyle(e).position')=='sticky','Primeira coluna congelada')
        check(page.locator('#tbody td').nth(1).evaluate('(e)=>getComputedStyle(e).whiteSpace')=='normal','Células preservam wrapping completo')
        page.emulate_media(reduced_motion='reduce')
        page.screenshot(path=str(OUT/'desktop.png'),full_page=False)
        page.set_viewport_size({'width':390,'height':844})
        page.locator('#reset').click()
        check(page.evaluate('document.documentElement.scrollWidth <= innerWidth'),'Mobile sem overflow global; tabela tem rolagem própria')
        page.screenshot(path=str(OUT/'mobile.png'),full_page=False)
        check(not any(u.startswith(('http:','https:')) for u in requests),'Nenhuma requisição de rede no relatório offline')
        browser.close()
    result={'status':'PASS' if not errors else 'FAIL','url_mode':'file://','browser':'Chromium / installed Microsoft Edge headless',
            'checks':checks,'errors':errors,'network_requests':[u for u in requests if u.startswith(('http:','https:'))],
            'screenshots':['desktop.png','mobile.png'],
            'scope':'Interações do relatório gerado; não é teste das aplicações mapeadas.'}
    (OUT/'browser-verificacao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__=='__main__':
    run()
