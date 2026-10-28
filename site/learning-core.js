/* Pure state, migration and export logic; shared with Node verification. */
'use strict';
const LearningCore = (()=>{
  const clone=o=>JSON.parse(JSON.stringify(o));
  const empty=()=>({schema:2,updatedAt:null,lastRoute:'#/learn/PREFACE',reading:{},notes:{},activities:{},explorations:{},start:{product:'',question:'',contribution:''},legacy:null});
  const object=v=>v!==null&&typeof v==='object'&&!Array.isArray(v);
  const text=(v,max=12000)=>{if(typeof v!=='string'||v.length>max)throw Error('Invalid text');return v;};
  const stamp=v=>v===null||v===undefined?null:text(v,80);
  const unit=k=>/^(PREFACE|APP-A|CH(0[1-9]|1[0-2]))$/.test(k);
  const section=k=>/^(opening|s-[a-f0-9]{10})$/.test(k);
  function fieldsOf(def){return def.steps.flatMap(s=>s.fields);}
  function validate(raw,definitions){
    if(!object(raw)||JSON.stringify(raw).length>2000000)throw Error('Invalid or oversized backup');
    if(raw.schema===1)return migrate(raw);
    if(raw.schema!==2)throw Error('Unsupported schema');
    const result=empty();result.updatedAt=stamp(raw.updatedAt);
    const route=text(raw.lastRoute||'#/learn/PREFACE',160);
    if(!/^#\/(?:learn\/(?:PREFACE|APP-A|CH\d\d)(?:\?section=(?:opening|s-[a-f0-9]{10}))?|activity\/ACT-CH0[12]-0[12](?:\?step=\d+)?)$/.test(route))throw Error('Invalid route');
    result.lastRoute=route;
    for(const name of ['reading','notes','activities','explorations','start'])if(!object(raw[name]))throw Error('Missing data '+name);
    if(Object.keys(raw.reading).length>14||Object.keys(raw.notes).length>300||Object.keys(raw.activities).length>4)throw Error('Too many records');
    for(const [key,value] of Object.entries(raw.reading)){
      if(!unit(key)||!object(value)||!Array.isArray(value.done)||value.done.length>100||value.done.some(s=>!section(s)))throw Error('Invalid reading');
      if(value.bookmark&&!section(value.bookmark))throw Error('Invalid bookmark');
      if(typeof value.legacyRead!=='undefined'&&typeof value.legacyRead!=='boolean')throw Error('Invalid reading flag');
      result.reading[key]={done:[...new Set(value.done)],bookmark:value.bookmark||'',legacyRead:!!value.legacyRead,updatedAt:stamp(value.updatedAt)};
    }
    for(const [key,value] of Object.entries(raw.notes)){
      const [u,s,...extra]=key.split('__');if(!unit(u)||!section(s)||extra.length||!object(value))throw Error('Invalid note');
      result.notes[key]={text:text(value.text,6000),version:text(value.version||'',80),digest:text(value.digest||'',64),updatedAt:stamp(value.updatedAt)};
    }
    for(const [id,value] of Object.entries(raw.activities)){
      const def=definitions.find(a=>a.id===id);if(!def||!object(value)||!object(value.fields))throw Error('Invalid activity');
      const allowed=Object.fromEntries(fieldsOf(def).map(f=>[f.id,f]));
      const cleanFields=values=>{
        if(!object(values)||Object.keys(values).length>200)throw Error('Invalid fields');
        const clean={};for(const [k,v] of Object.entries(values)){if(!Object.hasOwn(allowed,k))throw Error('Unknown field');clean[k]=text(v);if(allowed[k].type==='select'&&v&&!allowed[k].options.includes(v))throw Error('Invalid choice');}return clean;
      };
      if(!Number.isInteger(value.step)||value.step<0||value.step>=def.steps.length||!['draft','complete'].includes(value.status))throw Error('Invalid step');
      if(!Array.isArray(value.history)||value.history.length>20)throw Error('Invalid history');
      result.activities[id]={fields:cleanFields(value.fields),step:value.step,status:value.status,updatedAt:stamp(value.updatedAt),history:value.history.map(h=>{if(!object(h))throw Error('Invalid snapshot');return {at:stamp(h.at),label:text(h.label||'',100),fields:cleanFields(h.fields)};})};
    }
    if(Object.keys(raw.explorations).length>4)throw Error('Invalid observations');
    for(const [key,v] of Object.entries(raw.explorations)){
      if(!['system','materials','collaboration','releases'].includes(key)||!object(v)||!Number.isInteger(v.index)||v.index<0||v.index>5)throw Error('Invalid exploration');
      result.explorations[key]={index:v.index,decision:text(v.decision||'',80),explanation:text(v.explanation||'',6000),revision:text(v.revision||'',6000),updatedAt:stamp(v.updatedAt)};
    }
    for(const k of ['product','question','contribution'])result.start[k]=text(raw.start[k]||'',6000);
    if(raw.legacy!==null&&raw.legacy!==undefined){if(!object(raw.legacy)||JSON.stringify(raw.legacy).length>300000)throw Error('Invalid legacy data');result.legacy=clone(raw.legacy);}
    return result;
  }
  function migrate(old){
    if(!object(old)||old.schema!==1||!object(old.start)||!object(old.lab)||!object(old.review)||typeof old.reading!=='boolean')throw Error('Invalid legacy backup');
    const result=empty();for(const key of ['product','question','contribution'])result.start[key]=text(old.start[key]||'',6000);
    const lab={layer:Number.isInteger(old.lab.layer)&&old.lab.layer>=0&&old.lab.layer<=4?old.lab.layer:0,choice:text(old.lab.choice||'',80),explanation:text(old.lab.explanation||'',10000),revision:text(old.lab.revision||'',10000)};
    result.legacy={schema:1,reading:old.reading,start:clone(result.start),lab,review:{page:text(old.review.page||'',80),comment:text(old.review.comment||'',10000)},updatedAt:stamp(old.updatedAt)};
    result.reading.PREFACE={done:[],bookmark:'',legacyRead:old.reading,updatedAt:stamp(old.updatedAt)};
    result.explorations.system={index:lab.layer,decision:lab.choice,explanation:lab.explanation.slice(0,6000),revision:lab.revision.slice(0,6000),updatedAt:stamp(old.updatedAt)};
    return result;
  }
  function activity(state,id){return state.activities[id]||(state.activities[id]={fields:{},step:0,status:'draft',updatedAt:null,history:[]});}
  function missing(def,record){return fieldsOf(def).filter(f=>!(record?.fields[f.id]||'').trim());}
  function snapshot(record,label){record.history.push({at:new Date().toISOString(),label,fields:clone(record.fields)});record.history=record.history.slice(-20);}
  function merge(current,incoming){
    const out=clone(current);
    for(const [key,value] of Object.entries(incoming.reading))out.reading[key]={...value,done:[...new Set([...(out.reading[key]?.done||[]),...value.done])]};
    Object.assign(out.notes,clone(incoming.notes));
    for(const [id,value] of Object.entries(incoming.activities)){
      const previous=out.activities[id];out.activities[id]=clone(value);
      if(previous&&Object.keys(previous.fields).length){out.activities[id].history.unshift({at:new Date().toISOString(),label:'导入前本机草稿 / Before import',fields:clone(previous.fields)});out.activities[id].history=out.activities[id].history.slice(0,20);}
    }
    Object.assign(out.explorations,clone(incoming.explorations));
    for(const key of ['product','question','contribution'])if(incoming.start[key])out.start[key]=incoming.start[key];
    out.legacy=incoming.legacy||out.legacy;out.lastRoute=incoming.lastRoute;out.updatedAt=new Date().toISOString();return out;
  }
  const markdownText=v=>String(v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  function toMarkdown(def,record,source){
    const absent=missing(def,record);const result=[`# ${def.title}`,`\n活动：${def.id} · 学习证据：${def.evidence}`,`\n${def.simulated?'**模拟学习活动，未向真实社区提交。**\n':''}`,`状态：${record.status==='complete'?'本人已检查填写':'草稿'}；不代表教师评价或能力达成。`,`\n教材来源：${source}`,`\n尚缺 ${absent.length} 项：${absent.map(f=>f.label).join('、')||'无'}`];
    for(const step of def.steps){result.push('\n## '+step.title);for(const f of step.fields)result.push('\n### '+(f.row?f.row+' · ':'')+f.label+'\n\n'+markdownText(record.fields[f.id]||'（尚未填写）'));}
    result.push('\n## 修订快照');for(const h of record.history){result.push('\n### '+h.at+' · '+markdownText(h.label));for(const f of fieldsOf(def))if(h.fields[f.id])result.push('\n**'+(f.row?f.row+' · ':'')+f.label+'**\n\n'+markdownText(h.fields[f.id]));}
    return result.join('\n')+'\n';
  }
  return {empty,validate,migrate,fieldsOf,activity,missing,snapshot,merge,toMarkdown,clone};
})();
if(typeof module!=='undefined')module.exports=LearningCore;
