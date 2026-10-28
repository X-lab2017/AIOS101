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
for(const id of ['CH01','CH02','CH03','CH04','CH05','CH06'])assert(home.includes('href="#/learn/'+id+'"'));
for(const id of Object.keys(context.payload.units)){
 context.id=id;
 const html=vm.runInContext('reader(id,new URLSearchParams())',context);
 for(const sec of context.payload.units[id].sections)assert(html.includes(sec.html),'Full canonical section retained: '+id);
 for(const forbidden of ['data-mark=','data-note=','reading-notes','after-reading','margin-note','#/activity/','#/workshop','#/notebook'])assert(!html.includes(forbidden),id+' '+forbidden);
 const expected={CH01:4,CH02:4,CH03:8,CH04:9,CH05:9,CH06:10}[id];if(expected)assert.equal((html.match(/class="textbook-figure"/g)||[]).length,expected);
 assert(html.includes('source-trail')&&html.includes('chapter-pagination'));
}
const index=fs.readFileSync('site/index.html','utf8');
for(const unused of ['learning-core.js','learning-data.js','brand.js','import-file','app-dialog'])assert(!index.includes(unused));
assert(reads.every(k=>k==='aios101.preferences.v1'));assert.equal(writes.length,0);
for(const route of ['#/notebook','#/workshop','#/activity/ACT-CH01-01','#/identity','#/explore/materials']){
 let redirect='';context.location.hash=route;context.location.replace=v=>{redirect=v;};vm.runInContext('render()',context);assert(redirect==='#/map'||redirect==='#/learn/CH01');
}
assert(fs.readFileSync('dist/index.html','utf8').includes('app.js?v='));
console.log('PASS: reading-only home and all units, 44 figures, complete canonical sections, retired route fallback, old records untouched, release-bound assets');
