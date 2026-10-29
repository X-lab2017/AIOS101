/* Render the reading-only UI against built canonical content without a browser. */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const nodes=new Map(), reads=[],writes=[];
const node=()=>({innerHTML:'',style:{setProperty(){}},classList:{toggle(){},contains(){return false;}},setAttribute(){},addEventListener(){},focus(){}});
const context={console,URLSearchParams,location:{hash:'#/',replace(){}},localStorage:{getItem(k){reads.push(k);return null;},setItem(k,v){writes.push(k);},removeItem(){throw Error('Old records must not be removed');}},document:{documentElement:{dataset:{},style:{setProperty(){}}},querySelector(s){if(!nodes.has(s))nodes.set(s,node());return nodes.get(s);},querySelectorAll(){return[];},addEventListener(){}},window:{addEventListener(){},scrollTo(){}},fetch(){return new Promise(()=>{});},setTimeout,clearTimeout};
vm.createContext(context);
vm.runInContext(fs.readFileSync('site/app.js','utf8'),context);
context.payload=JSON.parse(fs.readFileSync('dist/content.json','utf8'));
vm.runInContext('data=payload',context);
const home=vm.runInContext('home()',context);
// Chapter covers must use the current image version and canonical title.
for(const figure of ['1-2','2-1','3-1','4-1','5-3','6-4']) {
 const current=context.payload.figureCatalog[figure];
 assert(home.includes('textbook/assets/figures/'+current.file),'Stale home image: '+figure);
 assert(home.includes('alt="'+current.title+'"'),'Stale home title: '+figure);
}
for(const id of ['CH01','CH02','CH03','CH04','CH05','CH06'])assert(home.includes('href="#/learn/'+id+'"'));
for(const id of Object.keys(context.payload.units)){
 context.id=id;
 const html=vm.runInContext('reader(id,new URLSearchParams())',context);
 for(const sec of context.payload.units[id].sections)assert(html.includes(sec.html),'Full canonical section retained: '+id);
 for(const forbidden of ['data-mark=','data-note=','reading-notes','after-reading','margin-note','#/activity/','#/workshop','#/notebook'])assert(!html.includes(forbidden),id+' '+forbidden);
 const expected=(context.payload.units[id].markdown.match(/!\[图 /g)||[]).length;assert.equal((html.match(/class="textbook-figure"/g)||[]).length,expected);
 assert(html.includes('source-trail')&&html.includes('chapter-pagination'));
}
// A clear beginning and end, while the appendix remains available on demand.
assert(home.includes('class="btn primary" href="#/learn/PREFACE"'));
assert.deepEqual(Array.from(vm.runInContext('readingOrder()',context)),['PREFACE','CH01','CH02','CH03','CH04','CH05','CH06','ABOUT']);
assert(vm.runInContext('allUnits()',context).includes('APP-A'));
assert(!vm.runInContext('reader("APP-A",new URLSearchParams())',context).includes('`0cf7856`'));
const end=vm.runInContext('reader("CH06",new URLSearchParams())',context);
assert(end.includes('class="page-next" href="#/learn/ABOUT"'));
assert(vm.runInContext('reader("ABOUT",new URLSearchParams())',context).includes('class="page-next" href="#/map"'));
for(const [q,expected] of [['假设你想向新生介绍自己的专业','PREFACE'],['提交号','APP-A'],['早期尝试过学习记录与活动入口','ABOUT']]){
 context.query=q;vm.runInContext('mapQuery=query',context);
 const results=vm.runInContext('searchMatches()',context);
 assert(results.some(r=>r.id===expected),'Search includes '+expected);
 assert(vm.runInContext('catalogResults()',context).includes('?section='));
}
vm.runInContext('mapQuery="  提交号  "',context);
assert(vm.runInContext('searchMatches()',context).some(r=>r.id==='APP-A'));
assert(!vm.runInContext('snippet("[许可](https://example.org) `模型`", "许可")',context).includes('https://'));
vm.runInContext('mapQuery="不存在的关键词987654321"',context);
assert(vm.runInContext('catalogResults()',context).includes('找到 0 个阅读单元'));
vm.runInContext('mapQuery=""',context);
assert(vm.runInContext('catalogResults()',context).includes('#/learn/ABOUT'));
// A same-chapter deep link must not replace the article or lose loaded figures.
let scrolled=false,focused=false;
context.requestAnimationFrame=fn=>fn();
context.document.getElementById=()=>({scrollIntoView(){scrolled=true;},focus(){focused=true;}});
vm.runInContext('renderedUnit="CH02"',context);
context.location.hash='#/learn/CH02?section='+context.payload.units.CH02.sections[1].id;
const main=context.document.querySelector('#main');main.innerHTML='retained article';
vm.runInContext('render()',context);
assert.equal(main.innerHTML,'retained article');assert(scrolled&&focused);
vm.runInContext('renderedUnit=null;shell()',context);
assert(context.document.querySelector('#nav').innerHTML.includes('https://github.com/X-lab2017/AIOS101'));
assert(!context.document.querySelector('#nav').innerHTML.includes('aria-current="page"'));
context.location.hash='#/map';vm.runInContext('shell()',context);
assert(context.document.querySelector('#nav').innerHTML.includes('href="#/map" aria-current="page"'));
const index=fs.readFileSync('site/index.html','utf8');
for(const unused of ['learning-core.js','learning-data.js','brand.js','import-file','app-dialog'])assert(!index.includes(unused));
assert(reads.every(k=>k==='aios101.preferences.v1'));assert.equal(writes.length,0);
for(const route of ['#/notebook','#/workshop','#/activity/ACT-CH01-01','#/identity','#/explore/materials']){
 let redirect='';context.location.hash=route;context.location.replace=v=>{redirect=v;};vm.runInContext('render()',context);assert(redirect==='#/map'||redirect==='#/learn/CH01');
}
assert(fs.readFileSync('dist/index.html','utf8').includes('app.js?v='));
console.log('PASS: reading-only home and all units, canonical figure counts, complete canonical sections, search and same-chapter navigation, About path, retired route fallback, old records untouched, release-bound assets');
