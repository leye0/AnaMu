/* AnaMu connector-only Markdown ingestion bridge.
 * NOT a node/CLI module; executed by the connected GitHub orchestration host.
 * Do not treat generated descriptions as musical interpretation.
 * Required injected variables: tools, text, batchLimit, ingestionMode.
 */
const repo="leye0/AnaMu";
const branch="analysis/material-registry-maintainable";
const metadataPaths=[
  "analysis/knowledge/source-manifest.json",
  "analysis/knowledge/materials/catalog.json",
  "analysis/knowledge/material-index.json",
  "analysis/knowledge/course-material-maps/links.json"
];
const files=await Promise.all(metadataPaths.map(path=>
  tools.mcp__GitHub__fetch_file({repository_full_name:repo,path,ref:branch})));
const parsed=await Promise.all(files.map(async r=>{
  let content=r.result.content;
  if(!content){
    content=(await tools.mcp__GitHub__fetch_blob({
      repository_full_name:repo,blob_sha:r.result.sha})).result.content
  }
  if(!content)throw Error("Cannot read metadata blob "+r.result.sha);
  return JSON.parse(content)
}));
const [sources,catalog,index,courseMap]=parsed;
const sourceByPath=new Map(sources.sources.map(r=>[r.path,r]));
if(catalog.material_units<457||catalog.chunks.length<36)throw Error("Unexpected catalogue version");
const nums=courseMap.bindings.map(r=>Number(r.id.split(":").at(-1)));
let nextMaterial=Math.max(catalog.material_units,...Object.values(index.by_document)
  .flat().map(id=>Number(id.split(":").at(-1))));
let nextBinding=Math.max(0,...nums);
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
function pythonRepr(s){
  let quote=s.includes("'")&&!s.includes('"')?'"':"'";
  return quote+s.replaceAll("\\","\\\\").replaceAll(quote,"\\"+quote)
    .replaceAll("\n","\\n").replaceAll("\r","\\r").replaceAll("\t","\\t")+quote
}
function sections(path,text){
  const lines=text.match(/[^\n]*\n|[^\n]+$/g)||[];
  const starts=[];
  let fence=null;
  for(let i=0;i<lines.length;i++){
    const line=lines[i],marker=line.match(/^\s{0,3}(`{3,}|~{3,})/);
    if(marker){
      const c=marker[1][0],n=marker[1].length;
      if(!fence)fence=[c,n];else if(c===fence[0]&&n>=fence[1])fence=null;
      continue
    }
    if(fence)continue;
    const m=line.replace(/\r?\n$/,"").match(/^(#{1,6})\s+(.+?)\s*#*\s*$/);
    if(m)starts.push([i,m[1].length,m[2]])
  }
  if(!starts.length||starts[0][0]>0)starts.unshift([0,0,"Preamble"]);
  const stack=[],out=[],occur=new Map();
  for(let i=0;i<starts.length;i++){
    const [start,level,heading]=starts[i];
    while(stack.length&&stack.at(-1)[0]>=level)stack.pop();
    const headingPath=stack.map(x=>x[1]).concat(heading);
    const key=JSON.stringify(headingPath),count=occur.get(key)||0;
    occur.set(key,count+1);
    const stop=i+1<starts.length?starts[i+1][0]:lines.length;
    let subtree=lines.length;
    for(let j=i+1;j<starts.length;j++)if(starts[j][1]<=level){subtree=starts[j][0];break}
    const content=lines.slice(start,stop).join("");
    const tuple="("+headingPath.map(pythonRepr).join(", ")+(headingPath.length===1?",":"")+")";
    out.push({heading,heading_path:headingPath,id:"fragment:"+
      sha256(path+"\n"+tuple+"\n"+count).slice(0,24),start_line:start+1,
      end_line:stop,subtree_end_line:subtree,content_sha256:sha256(content),text:content});
    stack.push([level,heading])
  }
  if(out.map(x=>x.text).join("")!==text)throw Error("Lossy partition: "+path);
  return out
}
function courseIdentity(path){
  const row=sourceByPath.get(path);
  if(row?.course_id)return row.course_id;
  const parts=path.split("/");
  return parts[2]+":"+parts.at(-1).replace(/\.md$/,"")
}
function createUnit(path,wholeSha,fragment,title){
  const body=(fragment.heading==="Preamble"?fragment.text:
    fragment.text.split(/\r?\n/).slice(1).join("\n")).trim();
  const paragraph=body.split(/\r?\n/).map(x=>x.trim())
    .find(x=>x&&!x.startsWith("#")&&!x.startsWith("|")&&!x.startsWith("---"))||"";
  const trimmed=paragraph.replace(/\s+/g," ").slice(0,240).trim();
  const id="material:"+String(++nextMaterial).padStart(7,"0");
  return {id,revision:1,kind:"markdown_section",title,
    title_origin:"source_heading_or_key",
    description:trimmed?"Extrait documentaire à qualifier : "+trimmed:
      "Titre ou passage sans description éditoriale vérifiée.",
    description_origin:"source_proposal_unreviewed",editorial_review:"unreviewed",
    review_required:true,covers:[],does_not_cover:[],notes:[],
    source_bindings:[{document_path:path,document_sha256:wholeSha,
      locator:{kind:"markdown_fragment",anchor:fragment.id,
        heading_path:fragment.heading_path,start_line:fragment.start_line,
        end_line:fragment.end_line,subtree_end_line:fragment.subtree_end_line},
      content_sha256:fragment.content_sha256,
      body_sha256:body?sha256(body):null,role:"primary"}],
    lifecycle:"active",locator_review:"unreviewed"}
}
const expectedChunks=new Set(catalog.chunks);
let docs=sources.sources.filter(x=>x.kind==="course_markdown"&&
  (!index.by_document[x.path]||ingestionMode==="partial"&&
    ["docs/courses/mcgill/MUTH-202.md",
     "docs/courses/berklee-online/OCOMP-491.md",
     "docs/courses/udem/MTE-3300.md",
     "docs/courses/mcgill/MUTH-528.md",
     "docs/courses/udem/MUL-3314.md",
     "docs/courses/berklee/CM-343.md",
     "docs/courses/udem/MUS-2327.md",
     "docs/courses/udem-supplementary/MUL-6262-H27.md"].includes(x.path)));
if(ingestionMode!=="partial")docs=docs.filter(x=>!index.by_document[x.path]);
else docs=docs.filter(x=>Boolean(index.by_document[x.path]));
docs.sort((a,b)=>a.path.localeCompare(b.path,"en"));
const offset=ingestionMode==="partial"?partialOffset:0;
docs=docs.slice(offset,offset+batchLimit);
if(!docs.length){text("No remaining course documents for "+ingestionMode);return;}
const downloaded=[];
for(let offset=0;offset<docs.length;offset+=12){
  const rows=await Promise.allSettled(docs.slice(offset,offset+12).map(async doc=>({
    doc,file:(await tools.mcp__GitHub__fetch_file({
      repository_full_name:repo,path:doc.path,ref:"main"})).result
  })));
  for(const row of rows){
    if(row.status!=="fulfilled")throw Error("Source fetch failed: "+String(row.reason));
    downloaded.push(row.value)
  }
}
const changes=[];
let newUnits=0,newDocs=0,reused=0;
for(const {doc,file} of downloaded){
  if(file.sha!==doc.git_blob_sha1)throw Error("Snapshot mismatch "+doc.path);
  const path=doc.path,fragmentList=sections(path,file.content),
    sourceSha=sha256(file.content),title=fragmentList.find(x=>x.heading!=="Preamble")?.heading||path;
  const rel="sources/"+sha256(path).slice(0,20)+".json";
  let units=[],newSource=!index.by_document[path];
  if(!newSource){
    if(!expectedChunks.has(rel))throw Error("No existing partial chunk "+path);
    const old=JSON.parse((await tools.mcp__GitHub__fetch_file({
      repository_full_name:repo,path:"analysis/knowledge/materials/"+rel,ref:branch})).result.content);
    if(old.source_document!==path)throw Error("Partial chunk source mismatch "+path);
    units=old.units;
    const freshAnchors=new Map(fragmentList.map(f=>[f.id,f]));
    for(const unit of units){
      const previous=unit.source_bindings.find(binding=>binding.role==="primary");
      const current=freshAnchors.get(previous.locator.anchor);
      if(!current||current.content_sha256!==previous.content_sha256)
        throw Error("Pre-existing reviewed fragment cannot be matched: "+unit.id);
    }
  }
  const anchors=new Set(units.map(x=>x.source_bindings.find(b=>b.role==="primary").locator.anchor));
  const knownIds=new Set(units.map(x=>x.id));
  if(knownIds.size!==units.length)throw Error("Duplicate existing unit "+path);
  let count=0;
  for(const fragment of fragmentList){
    if(anchors.has(fragment.id)){reused++;continue;}
    const unit=createUnit(path,sourceSha,fragment,
      fragment.heading==="Preamble"?"Préambule — "+title:fragment.heading);
    units.push(unit);newUnits++;count++;
    const course=courseIdentity(path);
    const bindingID="course-material:"+String(++nextBinding).padStart(7,"0");
    courseMap.bindings.push({id:bindingID,course_id:course,
      material_id:unit.id,source_path:path,attribution:"not_yet_reviewed",
      presentation_order:null,pedagogical_group:null,editorial_review:"unreviewed",
      lifecycle:"active"});
    (index.by_document[path]??=[]).push(unit.id);
    (index.by_course[course]??=[]).push(unit.id)
  }
  if(count===0)continue;
  if(newSource){catalog.chunks.push(rel);newDocs++;}
  units.sort((a,b)=>Number(a.id.split(":").at(-1))-Number(b.id.split(":").at(-1)));
  changes.push({path:"analysis/knowledge/materials/"+rel,mode:"100644",type:"blob",
    content:JSON.stringify({source_document:path,units},null,2)+"\n"})
}
if(!changes.length){text("No additional units in selected documents");return;}
catalog.chunks.sort();
catalog.material_units=nextMaterial;
index.coverage.material_units_active=nextMaterial;
index.coverage.material_units_requiring_review=nextMaterial;
index.coverage.course_material_bindings_active=courseMap.bindings.length;
index.coverage.source_course_documents_indexed=Object.keys(index.by_document)
  .filter(path=>path.startsWith("docs/courses/")).length;
index.coverage.course_documents_with_active_units=index.coverage.source_course_documents_indexed;
index.coverage.source_documents_with_active_units=Object.keys(index.by_document).length;
for(const [path,value] of [
  ["analysis/knowledge/materials/catalog.json",catalog],
  ["analysis/knowledge/material-index.json",index],
  ["analysis/knowledge/course-material-maps/links.json",courseMap]
]){
  changes.push({path,mode:"100644",type:"blob",
    content:JSON.stringify(value,null,2)+"\n"})
}
const currentBranch=JSON.parse((await tools.mcp__GitHub__fetch({
  url:"https://api.github.com/repos/leye0/AnaMu/branches/"+branch})).result.content);
const parent=currentBranch.commit.sha;
const tree=await tools.mcp__GitHub__create_tree({repository_full_name:repo,
  base_tree_sha:currentBranch.commit.commit.tree.sha,tree_elements:changes});
const commit=await tools.mcp__GitHub__create_commit({repository_full_name:repo,
  tree_sha:tree.result.sha,parent_sha:parent,message:
    "Indexer "+newUnits+" fragments de "+downloaded.length+
    " fiches sans promouvoir les descriptions automatiques"});
const update=await tools.mcp__GitHub__update_ref({repository_full_name:repo,
  branch_name:branch,sha:commit.result.sha,expected_sha:parent});
text(JSON.stringify({mode:ingestionMode,commit:commit.result.sha,
  moved:update.result.success,selected:downloaded.length,newDocs,newUnits,
  retainedUnits:reused,totalDocs:index.coverage.source_course_documents_indexed,
  totalUnits:catalog.material_units}));
