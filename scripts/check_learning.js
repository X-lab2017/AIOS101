/* Verify records learners must not lose, and the complete worksheet contract. */
'use strict';
const assert=require('node:assert/strict');
const C=require('../site/learning-core.js');
const D=require('../site/learning-data.js');
const definitions=D.activities;
const old={schema:1,reading:true,start:{product:'我的工具',question:'材料支持什么？',contribution:'改进文档'},lab:{layer:3,choice:'unknown',explanation:'证'.repeat(8000),revision:'旧修订'},review:{page:'lab',comment:'原始评审'},updatedAt:null};
const migrated=C.validate(old,definitions);
assert.equal(migrated.start.question,old.start.question);
assert.equal(migrated.legacy.lab.explanation,old.lab.explanation);
assert.equal(migrated.legacy.review.comment,'原始评审');
assert.equal(migrated.reading.PREFACE.legacyRead,true);
assert.deepEqual(migrated.reading.PREFACE.done,[]);
assert.deepEqual(C.validate(migrated,definitions),migrated,'Migration must survive reload');

const state=C.empty();
for(const def of definitions){
  const fields=C.fieldsOf(def), ids=fields.map(f=>f.id);
  assert.equal(new Set(ids).size,ids.length,'Field IDs must be unique');
  const record=C.activity(state,def.id);
  assert.equal(C.missing(def,record).length,fields.length);
  for(const field of fields)record.fields[field.id]=field.type==='select'?field.options[0]:'核验：'+field.id;
  C.snapshot(record,'初稿');
  record.fields[ids[0]]='修订后的表述';
  assert.notEqual(record.history[0].fields[ids[0]],record.fields[ids[0]]);
  assert.equal(C.missing(def,record).length,0);
  const exported=C.toMarkdown(def,record,'https://example.test/source');
  for(const field of fields)assert.ok(exported.includes(field.label));
  assert.ok(exported.includes('修订后的表述')&&exported.includes('初稿'));
  if(def.simulated)assert.ok(exported.includes('未向真实社区提交'));
}
assert.deepEqual(C.validate(state,definitions),state);
const a=definitions[0], current=C.clone(state), incoming=C.empty();
const rec=C.activity(incoming,a.id);rec.fields.tool='导入内容';
incoming.notes['CH01__s-0123456789']={text:'<img src=x onerror=alert(1)>',version:'v0.4',digest:'',updatedAt:null};
current.reading.CH01={done:['s-0000000000'],bookmark:'s-0000000000',legacyRead:false,updatedAt:null};
incoming.reading.CH01={done:['s-1111111111'],bookmark:'s-1111111111',legacyRead:false,updatedAt:null};
const merged=C.validate(C.merge(current,incoming),definitions);
assert.equal(merged.activities[a.id].fields.tool,'导入内容');
assert.equal(merged.activities[a.id].history[0].fields.tool,current.activities[a.id].fields.tool);
assert.deepEqual(merged.activities[definitions[1].id],current.activities[definitions[1].id]);
assert.equal(merged.reading.CH01.done.length,2);
assert.equal(current.activities[a.id].fields.tool,'修订后的表述','Merge cannot mutate original');

for(const mutate of [s=>s.schema=99,s=>s.lastRoute='javascript:alert(1)',s=>s.notes.bad={text:'x'},s=>s.activities[a.id].fields.unknown='x',s=>s.activities[a.id].fields.history='invalid option',s=>s.activities[a.id].step=100,s=>s.activities[a.id].history={},s=>s.start.product='x'.repeat(6001)]){
  const invalid=C.clone(state);mutate(invalid);assert.throws(()=>C.validate(invalid,definitions));
}
const unsafe=C.clone(state.activities[a.id]);unsafe.fields.tool='<script>alert(1)</script>';
assert.ok(!C.toMarkdown(a,unsafe,'source').includes('<script>'));
for(let i=0;i<25;i++)C.snapshot(unsafe,'revision '+i);
assert.equal(unsafe.history.length,20);
// Worksheet-specific coverage: matrices must not collapse to a summary field.
assert.equal(C.fieldsOf(definitions[0]).filter(f=>f.id.startsWith('actions_')).length,12);
assert.equal(C.fieldsOf(definitions[1]).filter(f=>f.id.startsWith('evidence_')).length,14);
assert.equal(C.fieldsOf(definitions[2]).filter(f=>/^release_\d_/.test(f.id)).length,12);
assert.equal(C.fieldsOf(definitions[2]).filter(f=>/^collaboration_.+_(evidence|missing)$/.test(f.id)).length,14);
assert.ok(C.fieldsOf(definitions[3]).some(f=>f.id==='proposal'));
console.log('PASS: migration/reload, four complete worksheets, snapshots, safe imports, merge recovery and full exports');

// The public site is now reading-first; retained activity modules remain recoverable.
require('./check_reading.js');
