// Gera a demonstração pública do Motor de Modelagem HAUMA (modelo diferente da ferramenta Modelagem de A a Z).
//
//   node fonte/demo/gerar_demo.js "C:\Users\jmari\OneDrive\BUDGET TELLO\Modelo_Financeiro_Modelagem_Completa.html"
//
// O motor de cálculo (calcMF) NÃO vai para o site: os resultados dos cenários são calculados aqui
// e gravados prontos na página. A página publicada só exibe os resultados, com premissas em modo leitura.
// O arquivo-fonte do modelo fica fora deste repositório (que é público) — nunca copie-o para cá.
'use strict';
const fs = require('fs');
const path = require('path');

const SRC = process.argv[2];
if (!SRC) { console.error('Informe o caminho do HTML do modelo.'); process.exit(1); }
const OUT = path.join(__dirname, '..', '..', 'public', 'servicos', 'motor-de-modelagem-demonstracao.html');
const WHATS = 'https://wa.me/5517997115321?text=' + encodeURIComponent(
  'Olá! Vi a demonstração do Motor de Modelagem HAUMA no site e quero usar com os dados da minha empresa.');

const html = fs.readFileSync(SRC, 'utf8').replace(/\r\n/g, '\n');
const js = html.split('<script>')[1].split('</script>')[0];
const MARK_UI = '/* ================= Interface';
const iUI = js.indexOf(MARK_UI), iCalc = js.indexOf('function calcMF(');
if (iUI < 0 || iCalc < 0 || iCalc > iUI) throw new Error('Estrutura do modelo mudou: revise o gerador.');

// ---------- 1. calcular os cenários com o motor (só aqui, nunca no site)
const engine = js.slice(0, iUI);
const { DEFMF, calcMF } = new Function(engine + '\nreturn {DEFMF,calcMF};')();
const defLine = js.slice(iUI).match(/const DEF=\(\(\)=>\{[\s\S]*?\}\)\(\);/)[0];
const DEF = new Function('DEFMF', 'const clone=o=>JSON.parse(JSON.stringify(o));' + defLine + '\nreturn DEF;')(DEFMF);
DEF.nome = 'Projeto Exemplo (dados fictícios)';

const round = (k, v) => (typeof v === 'number' && isFinite(v) && v !== Math.trunc(v)) ? +v.toPrecision(9) : v;
const RES = DEF.cen.nomes.map((_, i) => {
  const P = JSON.parse(JSON.stringify(DEF)); P.cen.sel = i;
  const R = calcMF(P);
  delete R.sumY; delete R.endY;
  return R;
});
const resJson = JSON.stringify(RES, round);

// ---------- 2. interface: helpers genéricos + telas, sem o motor
const helpers = js.slice(0, iCalc).replace(/const DEFMF=\{[\s\S]*?\};\n/, '');
let ui = js.slice(iUI);
const rep = (from, to, all) => {
  const n = all ? ui.split(from).length - 1 : (ui.includes(from) ? 1 : 0);
  if (!n) throw new Error('Trecho não encontrado: ' + String(from).slice(0, 70));
  ui = all ? ui.split(from).join(to) : ui.replace(from, to);
};
// fórmulas da planilha não aparecem na demonstração
ui = ui.replace(/fx:"(?:[^"\\]|\\.)*"/g, 'fx:""');
rep('return `<div class="row"><label>${l}<span class="h">${isAuto?"Automático: "+formula:"Manual (fórmula da planilha: "+formula.replace(/^= /,"")+")"}</span>',
    'return `<div class="row"><label>${l}<span class="h">${isAuto?"Automático":"Manual"}</span>');
// premissas fixas (sem localStorage para P); preferências de tela continuam salvas
rep('const STORE="mf-valora-varejo-v1";', 'const STORE="hauma-demo-modelagem-v1";');
rep('try{const s=localStorage.getItem(STORE);if(s){const o=JSON.parse(s);if(o&&o.un&&o.cen)P=o}}catch(e){}\n', '');
rep('const save=()=>{try{localStorage.setItem(STORE,JSON.stringify(P))}catch(e){}};', 'const save=()=>{};');
rep('const UI={tab:"painel",view:"A",year:"",unit:1000,fx:false,comp:false,indK:null};',
    'const UI={tab:"painel",view:"A",year:"",unit:1000,fx:false,comp:false,indK:null};const PREF=["tab","view","year","unit"];');
rep('try{Object.assign(UI,JSON.parse(localStorage.getItem(STORE+"-ui")||"{}"))}catch(e){}',
    'try{const o=JSON.parse(localStorage.getItem(STORE+"-ui")||"{}");PREF.forEach(k=>{if(o[k]!=null)UI[k]=o[k]})}catch(e){}');
// resultados prontos no lugar do motor
rep('const r=calcMF(Q);', 'const r=calcDemo(Q);');
rep('R=calcMF(P);', 'R=calcDemo(P);');
// premissas somente leitura (o comparativo da bridge continua livre)
rep('$("#main").innerHTML=RENDER[UI.tab]?RENDER[UI.tab]():"";',
    '$("#main").innerHTML=RENDER[UI.tab]?RENDER[UI.tab]():"";travar();');
rep('const p=el.dataset.p;if(!p)return;', 'const p=el.dataset.p;if(!p||!livre(p))return;');
rep('$("#fxBtn").addEventListener("click",()=>{UI.fx=!UI.fx;saveUI();render()});\n', '');
rep('$("#reset").addEventListener("click",()=>{if(confirm("Restaurar todas as premissas para os valores da planilha?")){P=clone(DEF);save();render()}});\n', '');
rep('$("#fxBtn").classList.toggle("on",UI.fx);', '');
rep('Entradas editáveis (valores da planilha)', 'Premissas do exemplo (somente leitura na demonstração)');
// a bridge já abre comparando Base × Estresse (em vez de Base × Base, que daria tudo zero)
rep('P.bridge={modo:"cen",orc:0,real:-1,', 'P.bridge={modo:"cen",orc:0,real:P.cen.nomes.length-1,');

const demoJs = `
const RES=${resJson};
const DEFMF=${JSON.stringify(DEF)};
function calcDemo(Q){const R=RES[Q.cen.sel];if(!R.sumY){const nY=R.nY;
  R.sumY=a=>{const o=Array(nY).fill(0);R.T.forEach(t=>o[R.yi[t]]+=a[t]);return o};
  R.endY=a=>{const o=Array(nY).fill(0);R.T.forEach(t=>{if(R.mo[t]===12)o[R.yi[t]]=a[t]});return o};}
  return R}
const livre=p=>p.startsWith("bridge");
function travar(){document.querySelectorAll("#main [data-p]").forEach(el=>{if(!livre(el.dataset.p)){el.disabled=true;el.title="Na demonstração as premissas são somente leitura"}})}
`;
// o DEF original usa DEFMF: já vem pronto (com o nome trocado)
ui = ui.replace(defLine, 'const DEF=clone(DEFMF);');

const script = (helpers + demoJs + ui).replace(/Projeto Valora/g, 'Motor de Modelagem HAUMA').replace(/Valora/g, 'HAUMA');
if (/function calcMF\(/.test(script)) throw new Error('O motor vazou para a página.');
new Function(script.replace(/render\(\);\s*$/, '')); // confere a sintaxe

// ---------- 3. estilo da HAUMA (tema claro) e cabeçalho do site
let style = html.match(/<style>([\s\S]*?)<\/style>/)[1];
style = style.replace(/:root\{[\s\S]*?\n\}/, `:root{
  --bg:#f7f5f0; --surface:#ffffff; --surface2:#f2efe8; --surface3:#ece8df; --text:#13233a; --muted:#4a5466;
  --border:#dcd7cc; --accent:#1f3a5f; --accent-soft:#e7ecf4; --pos:#1f7a38; --neg:#b3261e; --warn:#8c6a0f;
  --input:#f2efe8; --input-b:#c9c5bb; --input-t:#13233a; --out:#e7ecf4;
  --c1:#2a78d6; --c2:#c8871a; --c3:#7b5ea7; --c4:#1f7a38; --grid:#e8e4da;
  color-scheme:light;
}`).replace('font:14px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif', 'font:14px/1.45 Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif');
style += `
.site{background:#13233a;color:#fff}
.site .in2{max-width:1600px;margin:0 auto;padding:10px 16px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.site img{height:40px;width:auto;display:block}
.site .tt{font:600 15px/1.2 "Playfair Display",Georgia,serif}
.site .tt small{display:block;font:500 11px/1.4 Inter,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#e9c349}
.site a{color:#fff;text-decoration:none;font-size:13px;font-weight:600;border-radius:6px;padding:8px 12px;white-space:nowrap}
.site a.vol{border:1px solid rgba(255,255,255,.35)}
.site a.cta{background:#e9c349;color:#13233a}
.aviso{background:#fbf3dc;border-bottom:1px solid #ecdcaa;color:#5c4a12;font-size:12.5px}
.aviso div{max-width:1600px;margin:0 auto;padding:7px 16px}
input:disabled,select:disabled{opacity:1;cursor:not-allowed;background:var(--surface2);color:var(--text);border-color:var(--border)}
@media (max-width:640px){.site .tt{font-size:13px}.site a{padding:7px 9px;font-size:12px}}
`;

let body = html.match(/<body>([\s\S]*?)<script>/)[1];
body = body.replace('<h1>Modelo Financeiro · Modelagem Completa</h1>', '<h1>Motor de Modelagem HAUMA · Modelagem Completa</h1>')
  .replace('<button class="btn" id="fxBtn">Mostrar fórmulas</button>', '')
  .replace('<button class="btn" id="reset">Restaurar planilha</button>', '')
  .replace('<span id="user"></span>', '');
const topo = `<div class="site"><div class="in2">
  <a href="/" style="padding:0"><img src="/logo-hauma.png" width="426" height="154" alt="HAUMA Soluções Empresariais"></a>
  <div class="tt">Motor de Modelagem HAUMA<small>Demonstração</small></div>
  <div class="sp"></div>
  <a class="vol" href="/servicos/motor-de-modelagem">Voltar ao site</a>
  <a class="cta" href="${WHATS}" target="_blank" rel="noopener noreferrer">Quero usar com os dados da minha empresa</a>
</div></div>
<div class="aviso"><div>Demonstração com <strong>dados fictícios</strong> e premissas em modo leitura. Troque o cenário, a visão e as abas à vontade. Na versão para assinantes você edita todas as premissas e salva os seus projetos.</div></div>`;

const desc = 'Demonstração do Motor de Modelagem HAUMA: DRE, DFC e Balanço integrados, valuation, bridge de EBITDA e 4 cenários, com dados fictícios.';
const page = `<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Demonstração · Motor de Modelagem HAUMA | HAUMA Consultoria</title>
<meta name="description" content="${desc}">
<meta property="og:title" content="Demonstração · Motor de Modelagem HAUMA | HAUMA Consultoria">
<meta property="og:description" content="${desc}">
<link rel="canonical" href="https://haumaconsultoria.com.br/servicos/motor-de-modelagem-demonstracao">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600&display=swap" rel="stylesheet">
<style>${style}</style>
</head>
<body>
${topo}
${body}<script>${script}</script>
</body>
</html>
`;
fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, page);
console.log('ok', OUT, Math.round(page.length / 1024) + ' KB');
