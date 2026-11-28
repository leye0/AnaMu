/* Explicit, source-checked extraction publisher for the connected GitHub host.
 * Inject tools, text, branch, batchSpec. Never execute source documents.
 * batchSpec contains id, scope, entries (path, material_id, label, scope, role,
 * target or null, optional sense_id, aspect, limitation, assertions).
 * Each assertion supplies rule_key, polarity, statement, requires_evidence.
 * Editorial decisions are supplied by the reader; nothing is inferred from headings.
 * The named branch must already exist. Publication is atomic at one frozen head.
 */
const repo="leye0/AnaMu";
const root="analysis/knowledge/";
const prime=[];for(let n=2;prime.length<64;n++){
  let p=true;for(let d=2;d*d<=n;d++)if(n%d===0){p=false;break}
  if(p)prime.push(n)
}
const fractional=n=>n-Math.floor(n);
const K=prime.map(n=>(fractional(Math.cbrt(n))*4294967296)>>>0);
const INITIAL=prime.slice(0,8).map(n=>(fractional(Math.sqrt(n))*4294967296)>>>0);
function sha256(raw){
  const binary=unescape(encodeURIComponent(raw)),a=[];
  for(let i=0;i<binary.length;i++)a.push(binary.charCodeAt(i));
  const bits=a.length*8;
  a.push(128);while(a.length%64!==56)a.push(0);
  for(let j=7;j>=0;j--)a.push(Math.floor(bits/2**(8*j))&255);
  const h=INITIAL.slice();
  for(let offset=0;offset<a.length;offset+=64){
    const w=[];
    for(let j=0;j<16;j++){
      const b=offset+4*j;
      w[j]=((a[b]<<24)|(a[b+1]<<16)|(a[b+2]<<8)|a[b+3])>>>0
    }
    for(let j=16;j<64;j++){
      const x=w[j-15],y=w[j-2];
      const s0=(((x>>>7)|(x<<25))^((x>>>18)|(x<<14))^(x>>>3))>>>0;
      const s1=(((y>>>17)|(y<<15))^((y>>>19)|(y<<13))^(y>>>10))>>>0;
      w[j]=(w[j-16]+s0+w[j-7]+s1)>>>0
    }
    let [x,y,z,v,q,r,s,t]=h;
    for(let j=0;j<64;j++){
      const a1=(((q>>>6)|(q<<26))^((q>>>11)|(q<<21))^((q>>>25)|(q<<7)))>>>0;
      const t1=(t+a1+((q&r)^(~q&s))+K[j]+w[j])>>>0;
      const a0=(((x>>>2)|(x<<30))^((x>>>13)|(x<<19))^((x>>>22)|(x<<10)))>>>0;
      const t2=(a0+((x&y)^(x&z)^(y&z)))>>>0;
      t=s;s=r;r=q;q=(v+t1)>>>0;v=z;z=y;y=x;x=(t1+t2)>>>0
    }
    for(let j=0;j<8;j++)h[j]=(h[j]+[x,y,z,v,q,r,s,t][j])>>>0
  }
  return h.map(x=>x.toString(16).padStart(8,"0")).join("")
}
if(sha256("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
  throw Error("SHA256 self-check failed");

const fail=m=>{throw Error(m)};
const requireText=(v,k)=>typeof v==="string"&&v.trim()?v:fail("Missing "+k);
const unique=(values,label)=>{if(new Set(values).size!==values.length)fail("Duplicate "+label)};
const packetMode=batchSpec.mode==="packet";
const id=packetMode?"read-only-packet":requireText(batchSpec.id,"batch id");
if(!/^[a-z0-9][a-z0-9-]{2,60}$/.test(id))fail("Invalid batch id");
if(!packetMode&&(!Array.isArray(batchSpec.entries)||!batchSpec.entries.length))fail("Empty extraction batch");
if(packetMode&&(!Array.isArray(batchSpec.paths)||!batchSpec.paths.length))fail("Packet requires source paths");
const info=JSON.parse((await tools.mcp__GitHub__fetch({url:"https://api.github.com/repos/"+repo+"/branches/"+branch})).result.content);
const parent=info.commit.sha;
if(batchSpec.expected_head&&batchSpec.expected_head!==parent)fail("Source packet head has changed; refresh before publishing");
const read=async path=>{
  let f=(await tools.mcp__GitHub__fetch_file({repository_full_name:repo,ref:parent,path})).result;
  if(!f.content)f=(await tools.mcp__GitHub__fetch_blob({repository_full_name:repo,blob_sha:f.sha})).result;
  if(!f.content)fail("Missing content "+path);
  return f.content
};
const batchPath=root+"mentions/"+id+".json";
const [index,links,senses,concepts,manifest,listing]=await Promise.all([
  read(root+"material-index.json").then(JSON.parse),
  read(root+"material-knowledge-maps/links.json").then(JSON.parse),
  read(root+"candidate-senses.json").then(JSON.parse),
  read(root+"concepts.json").then(JSON.parse),
  read(root+"source-manifest.json").then(JSON.parse),
  tools.mcp__GitHub__fetch({url:"https://api.github.com/repos/"+repo+"/contents/"+root+"mentions?ref="+parent}).then(x=>JSON.parse(x.result.content))
]);
if(!packetMode&&listing.some(f=>f.path===batchPath))fail("Batch already exists: "+id);
const sourceMap=new Map(manifest.sources.map(s=>[s.path,s]));
const conceptIds=new Set(concepts.concepts.map(c=>c.id));
const senseIds=new Set(senses.candidates.map(c=>c.id));
const newSenses=batchSpec.new_senses||[];
unique(newSenses.map(s=>s.id),"new sense ID");
for(const sense of newSenses){
  if(senseIds.has(sense.id)||sense.canonical_concept_id!==null||sense.decision!=="pending_reconciliation")fail("Invalid new candidate sense "+sense.id);
  const e=batchSpec.entries.find(e=>e.material_id===sense.source_material_id&&e.path===sense.source_document_path&&e.sense_id===sense.id);
  if(!e)fail("New sense lacks its source entry "+sense.id);
  senseIds.add(sense.id);senses.candidates.push(sense)
}
const documents=new Map();
for(const path of new Set(packetMode?batchSpec.paths:batchSpec.entries.map(e=>e.path))){
  const source=sourceMap.get(path);
  if(!source||!["course_markdown","shared_markdown"].includes(source.kind))fail("Not a manifest Markdown source "+path);
  const [raw,chunk]=await Promise.all([read(path),read(root+"materials/sources/"+sha256(path).slice(0,20)+".json").then(JSON.parse)]);
  if(chunk.source_document!==path)fail("Chunk mismatch "+path);
  const ids=chunk.units.map(u=>u.id);
  unique(ids,"material ID in "+path);
  if(ids.length!==index.by_document[path]?.length||ids.some(v=>!index.by_document[path].includes(v)))fail("Index mismatch "+path);
  documents.set(path,{raw,chunk,lines:raw.match(/[^\r\n\v\f\x1c-\x1e\x85\u2028\u2029]*(?:\r\n|[\r\n\v\f\x1c-\x1e\x85\u2028\u2029])|[^\r\n\v\f\x1c-\x1e\x85\u2028\u2029]+$/g)||[],sha:sha256(raw)})
}
// Read-only packets include the actual bounded text, never only the title.
if(packetMode){
  const requested=batchSpec.material_ids?new Set(batchSpec.material_ids):null;
  const packets=[];
  for(const [path,d] of documents)for(const unit of d.chunk.units){
    if(unit.lifecycle!=="active"||(requested&&!requested.has(unit.id)))continue;
    const b=unit.source_bindings.find(x=>x.role==="primary"),l=b.locator;
    const passage=d.lines.slice(l.start_line-1,l.end_line).join("");
    if(b.document_sha256!==d.sha||sha256(passage)!==b.content_sha256)fail("Invalid packet source "+unit.id);
    packets.push({path,material_id:unit.id,revision:unit.revision,title:unit.title,content_sha256:b.content_sha256,locator:l,source_content:passage});
  }
  if(requested&&packets.length!==requested.size)fail("Some requested packet IDs not found");
  text({head:parent,packets});return
}
unique(batchSpec.entries.map(e=>e.material_id),"material within batch");
unique(batchSpec.entries.flatMap(e=>e.assertions.map(a=>a.rule_key)),"rule key within batch");
const mentions=[],assertions=[],reviews=[];
let linkNumber=Math.max(0,...links.bindings.map(b=>Number(b.id.split(":").at(-1))));
for(const [j,e] of batchSpec.entries.entries()){
  const d=documents.get(e.path);
  const unit=d.chunk.units.find(u=>u.id===e.material_id);
  if(!unit||unit.lifecycle!=="active")fail("Unknown active material "+e.material_id);
  const s=unit.source_bindings.find(b=>b.role==="primary"),loc=s.locator;
  const passage=d.lines.slice(loc.start_line-1,loc.end_line).join("");
  if(s.document_path!==e.path||s.document_sha256!==d.sha||s.content_sha256!==sha256(passage))fail("Source fingerprint mismatch "+e.material_id);
  if(e.expected_content_sha256!==s.content_sha256)fail("Reader must name exact reviewed content SHA "+e.material_id);
  if(e.expected_material_revision!==unit.revision)fail("Reader must name exact reviewed material revision "+e.material_id);
  const span={document_path:e.path,document_sha256:s.document_sha256,content_sha256:s.content_sha256,locator:loc};
  const review={material_id:e.material_id,reviewed_material_revision:unit.revision,source_span:span,disposition:e.disposition||"partial_extraction",reason:requireText(e.reason,"review reason"),review_state:"assistant_source_checked",remaining_questions:e.remaining_questions||[]};
  if(!["partial_extraction","no_analytic_assertion_in_passage","extraction_complete_for_passage"].includes(review.disposition))fail("Invalid disposition");
  if(review.disposition==="no_analytic_assertion_in_passage"&&e.assertions.length)fail("No assertion disposition with assertions");
  if(!Array.isArray(review.remaining_questions)||review.remaining_questions.some(q=>typeof q!=="string"||!q.trim()))fail("Invalid remaining questions");
  if(review.disposition==="partial_extraction"&&!review.remaining_questions.length)fail("Partial review needs remaining questions");
  if(review.disposition!=="partial_extraction"&&review.remaining_questions.length)fail("Closed review cannot have remaining extraction questions");
  review.review_contract="passage_review_v2";
  review.review_dimensions=e.review_dimensions;
  const dims=["definitions","methods","conditions","exceptions","counterexamples","source_attribution"];
  if(!review.review_dimensions||dims.some(k=>!["examined","not_present","open"].includes(review.review_dimensions[k])))fail("Review must classify every extraction dimension");
  if(review.disposition!=="partial_extraction"&&dims.some(k=>review.review_dimensions[k]==="open"))fail("Closed review has open dimensions");
  reviews.push(review);
  if(!e.assertions.length){
    if(review.disposition!=="no_analytic_assertion_in_passage")fail("Empty assertions for extracted passage");
    continue
  }
  if(!e.target&&!e.sense_id&&!e.unresolved_subject)fail("An extraction must name a concept, sense or unresolved subject");
  if(e.target&&!conceptIds.has(e.target))fail("Unknown concept "+e.target);
  if(e.sense_id&&!senseIds.has(e.sense_id))fail("Unknown candidate sense "+e.sense_id);
  if(e.target&&e.sense_id)fail("Choose a canonical or candidate sense, not both");
  const mentionId="mention:"+id+":"+String(j+1).padStart(4,"0");
  const assertionIds=[];
  for(const a of e.assertions){
    if(!["method","negative","positive","conditional","exception","definition","counterexample","open_question"].includes(a.polarity))fail("Unknown polarity "+a.polarity);
    if(!Array.isArray(a.requires_evidence)||!a.requires_evidence.every(x=>typeof x==="string"&&x.trim()))fail("Missing evidence requirements");
    unique(a.requires_evidence,"evidence requirement");
    const excerpt=requireText(a.source_excerpt,"assertion source excerpt");
    if(excerpt.length<8||passage.indexOf(excerpt)<0||passage.indexOf(excerpt)!==passage.lastIndexOf(excerpt))fail("Excerpt must locate one exact span: "+a.rule_key);
    const offset=passage.indexOf(excerpt);
    const start=Array.from(passage.slice(0,offset)).length;
    const end=start+Array.from(excerpt).length;
    const anchor={kind:"exact_source_excerpt",start_codepoint:start,end_codepoint_exclusive:end,excerpt_sha256:sha256(excerpt)};
    const aid="candidate-assertion:"+id+":"+String(assertions.length+1).padStart(4,"0");
    assertionIds.push(aid);
    assertions.push({id:aid,mention_id:mentionId,material_id:e.material_id,reviewed_material_revision:unit.revision,rule_key:requireText(a.rule_key,"rule key"),polarity:a.polarity,statement:requireText(a.statement,"statement"),scope:requireText(e.scope,"scope"),requires_evidence:a.requires_evidence,review_state:"assistant_source_checked_candidate",source_role:requireText(e.role,"source role"),source_is_direct_citation:false,source_span:span,source_anchor:anchor,applicability_conditions:requireText(a.applicability_conditions,"applicability conditions"),inference_limit:requireText(a.inference_limit,"inference limit"),causal_claim:false,warning:"Candidate fondée sur ce passage, non règle universelle ni capacité validée."})
  }
  mentions.push({id:mentionId,material_id:e.material_id,reviewed_material_revision:unit.revision,source_document_path:e.path,source_section_heading:unit.title,source_span:span,label:requireText(e.label,"label"),language:"fr",attribution_role:e.role,concept_sense_candidate:e.target||null,candidate_sense_id:e.sense_id||null,unresolved_subject:e.unresolved_subject||null,state:"assistant_source_checked_candidate",scope_note:e.scope,candidate_assertion_ids:assertionIds});
  if(e.target||e.sense_id){
    const target=e.target?{kind:"concept",id:e.target,registry_path:root+"concepts.json"}:{kind:"unresolved_concept_or_assertion",id:null,proposed_subject:e.label,candidate_sense_id:e.sense_id};
    if(links.bindings.some(b=>b.material_id===e.material_id&&(e.target?b.target.id===e.target:b.target.candidate_sense_id===e.sense_id)))fail("Existing material target; avoid duplicate contribution "+e.material_id);
    links.bindings.push({id:"material-knowledge:"+String(++linkNumber).padStart(7,"0"),material_id:e.material_id,reviewed_material_revision:unit.revision,target,contribution_kind:"provides_method",covered_aspects:[requireText(e.aspect,"aspect")],context:e.scope,justification:e.aspect,state:e.target?"assistant_source_checked_proposed_link":"awaiting_target_reconciliation",does_not_establish:requireText(e.limitation,"limitation")});
    const mapping=e.target?index.by_concept:index.by_candidate_sense;
    (mapping[e.target||e.sense_id]??=[]).push(e.material_id)
  }
}
const coverage=index.coverage;
coverage.extracted_candidate_mentions+=mentions.length;
coverage.extracted_candidate_assertions+=assertions.length;
coverage.material_knowledge_bindings=links.bindings.length;
coverage.material_knowledge_bindings_proposed=links.bindings.filter(b=>b.state==="assistant_source_checked_proposed_link").length;
coverage.material_knowledge_bindings_unresolved=links.bindings.filter(b=>b.target.id===null).length;
coverage.candidate_senses_pending_reconciliation=senses.candidates.filter(s=>s.decision==="pending_reconciliation").length;
const batch={schema_version:1,extraction_contract:"passage_review_v2",input_commit:parent,edition:id,scope:requireText(batchSpec.scope,"batch scope"),material_registry_path:root+"materials/catalog.json",source_manifest_path:root+"source-manifest.json",concept_registry_path:root+"concepts.json",review_status:"assistant_source_checked_candidates_not_independently_validated",mentions,assertions,passage_reviews:reviews,coverage:{selected_material_units:reviews.length,mentions:mentions.length,candidate_assertions:assertions.length,assertions_human_reviewed:0},revision_contract:"Review and claims expire when material revision or source span changes."};
const changes=[[batchPath,batch],[root+"material-index.json",index],[root+"material-knowledge-maps/links.json",links],[root+"candidate-senses.json",senses]];
const tree=await tools.mcp__GitHub__create_tree({repository_full_name:repo,base_tree_sha:info.commit.commit.tree.sha,tree_elements:changes.map(([path,o])=>({path,type:"blob",mode:"100644",content:JSON.stringify(o,null,2)+"\n"}))});
const commit=await tools.mcp__GitHub__create_commit({repository_full_name:repo,tree_sha:tree.result.sha,parent_sha:parent,message:"Extraire "+assertions.length+" assertions candidates : "+id});
const moved=await tools.mcp__GitHub__update_ref({repository_full_name:repo,branch_name:branch,sha:commit.result.sha,expected_sha:parent});
if(!moved.result.success)fail("Branch moved; no publication");
text({commit:commit.result.sha,batch:id,reviewedPassages:reviews.length,newMentions:mentions.length,newAssertions:assertions.length,totalAssertions:coverage.extracted_candidate_assertions,totalLinks:coverage.material_knowledge_bindings});
