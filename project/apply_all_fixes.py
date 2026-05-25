import sys, re

print("=== Phase A: Restore previous changes ===")
with open('app/templates/kruskal_learning.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Track changes
changes = 0

# A1: 3-tab switching
old = "document.querySelectorAll('.module-pane').forEach(p => p.style.display = 'none');\n  document.getElementById(btn.dataset.module).style.display = 'block';"
new = "document.getElementById('m-learn').style.display = btn.dataset.module === 'm-learn' ? 'block' : 'none';\n  document.getElementById('m-quiz').style.display = btn.dataset.module === 'm-quiz' ? 'block' : 'none';\n  document.getElementById('m-report').style.display = btn.dataset.module === 'm-report' ? 'block' : 'none';"
if old in html: html = html.replace(old, new); changes += 1

# A2: profileState tracking
old = "let profileState = { total_steps_viewed:0, marked_lines:[], completed_runs:0 };"
new = "let profileState = { total_steps_viewed:0, marked_lines:[], completed_runs:0, question_concepts:[], wrong_concepts:[] };"
if old in html: html = html.replace(old, new); changes += 1

# A3: Quiz completion handling
old = "function renderQuiz(){\n  const q=quizQuestions[quizIdx], qDiv=el('quiz-question'), box=el('quiz-options');\n  box.innerHTML=''; el('quiz-feedback').textContent='';\n  if(!q){ qDiv.textContent='暂无题目'; return; }"
new = "function renderQuiz(){\n  const q=quizQuestions[quizIdx], qDiv=el('quiz-question'), box=el('quiz-options');\n  box.innerHTML=''; el('quiz-feedback').textContent='';\n  if(quizIdx >= quizQuestions.length){\n    qDiv.innerHTML=`<b style=\"color:#16a34a\">测验完成！</b> 共 ${quizTotal} 题，正确 <b>${quizCorrect}</b> 题（${quizTotal>0?Math.round(quizCorrect/quizTotal*100):0}%）`;\n    el('next-quiz-btn').textContent='重新开始'; return;\n  }\n  el('next-quiz-btn').textContent='下一题';\n  if(!q){ qDiv.textContent='暂无题目'; return; }"
if old in html: html = html.replace(old, new); changes += 1

# A4: Quiz answer tracking (correct/wrong)
old = "btn.onclick=()=>{ quizTotal++; const ok=idx===q.correctIndex; if(ok) quizCorrect++;"
new = "btn.onclick=()=>{ quizTotal++; const ok=idx===q.correctIndex; if(ok){ quizCorrect++; if(q.concept) profileState.question_concepts.push(q.concept); }else{ if(q.concept) profileState.wrong_concepts.push(q.concept); }"
if old in html: html = html.replace(old, new); changes += 1

# A5: Next-quiz-btn fix
old = "el('next-quiz-btn').onclick=()=>{if(quizQuestions.length===0)loadQuiz();else{quizIdx=(quizIdx+1)%quizQuestions.length;renderQuiz();}};"
new = "el('next-quiz-btn').onclick=()=>{if(quizQuestions.length===0){loadQuiz();return;}if(quizIdx>=quizQuestions.length){quizIdx=0;quizCorrect=0;quizTotal=0;renderQuiz();return;}quizIdx++;renderQuiz();};"
if old in html: html = html.replace(old, new); changes += 1

# A6: Report HTML
old = '<div id="m-report" class="card" style="display:none">\n  <h3 class="section-title">学习报告</h3>\n  <div class="viz-row">\n    <button class="btn" id="analyze-btn">生成报告</button>\n    <button class="btn secondary" id="save-profile-btn">保存进度</button>\n  </div>\n  <div id="skill-box" class="card" style="margin-bottom:8px">尚未生成掌握度。</div>\n  <div id="rec-box" class="card">尚未生成推荐。</div>\n</div>'
new = '<div id="m-report" class="card" style="display:none">\n  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:16px">\n    <h3 class="section-title" style="margin:0;border:none;padding:0">学习报告</h3>\n    <div style="display:flex;gap:6px"><button class="btn" id="analyze-btn">生成报告</button><button class="btn secondary" id="reanalyze-btn">重新生成</button><button class="btn secondary" id="save-profile-btn">保存进度</button></div>\n  </div>\n  <div id="report-content"><div style="text-align:center;padding:40px 20px;color:#94a3b8"><div style="font-size:40px;margin-bottom:12px">报告</div><p style="margin:0">点击生成报告基于你的学习行为分析掌握度</p></div></div>\n</div>'
if old in html: html = html.replace(old, new); changes += 1

# A7: GenerateReport rewrite
old_gr = """async function generateReport(){
  await syncProfile();
  const res=await fetch('/api/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({total_animation_steps:Math.max(animSteps.length,1)})});
  const data=await res.json();

  const skillBox = document.getElementById('skill-box');
  if(data.success){
    const items = Object.entries(data.skill_scores || {});
    skillBox.innerHTML = `<h4>掌握度</h4>${items.map(([k,v]) => `${k}: <b>${v}%</b>`).join('<br/>')}<br/><br/>测验正确数：<b>${quizCorrect}</b>`;
  } else {
    skillBox.textContent = data.error || '分析失败';
  }

  const recBox = document.getElementById('rec-box');
  const recs = (data.recommendations || []).map(r => `<li>${r.knowledge}（${r.score}%）- ${r.advice || ''} ${r.next_topic ? `→ 下一步：${r.next_topic}` : ''}</li>`);
  recBox.innerHTML = `<h4>推荐建议</h4><ul>${recs.join('') || '<li>暂无</li>'}</ul>`;
}"""

new_gr = """async function generateReport(){
  await syncProfile();
  const res=await fetch('/api/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({total_animation_steps:Math.max(animSteps.length,1),wrong_concepts:profileState.wrong_concepts||[]})});
  const data=await res.json();
  const box=document.getElementById('report-content');
  if(!data.success){ box.innerHTML='<div style=\"text-align:center;color:#dc2626;padding:20px\">分析失败</div>'; return; }
  const allScores=data.skill_scores||{}; const allRecs=data.recommendations||[];
  const scores=allScores; const recs=allRecs;
  const entries=Object.entries(scores).sort((a,b)=>a[1]-b[1]);
  if(!entries.length){ box.innerHTML='<div style=\"text-align:center;color:#94a3b8;padding:20px\">暂无掌握度数据。请先完成学习活动后再生成报告。</div>'; return; }
  const totalQ=quizTotal||0, correctQ=quizCorrect||0;
  const avgScore=Math.round(entries.reduce((s,e)=>s+e[1],0)/entries.length);
  box.innerHTML='<div style=\"display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin-bottom:16px\"><div class=\"stat-mini\"><div class=\"stat-big\">'+avgScore+'%</div><div class=\"stat-desc\">综合掌握度</div></div><div class=\"stat-mini\"><div class=\"stat-big\">'+correctQ+'/'+totalQ+'</div><div class=\"stat-desc\">测验正确率</div></div><div class=\"stat-mini\"><div class=\"stat-big\">'+recs.filter(function(r){return r.score<40;}).length+'</div><div class=\"stat-desc\">需重点学习</div></div><div class=\"stat-mini\"><div class=\"stat-big\">'+recs.filter(function(r){return r.score>=70;}).length+'</div><div class=\"stat-desc\">已良好掌握</div></div></div><h4 style=\"margin:0 0 10px;font-size:14px;color:#334155\">各项掌握度</h4><div style=\"display:flex;flex-direction:column;gap:6px;margin-bottom:16px\">'+entries.map(function(e){var name=e[0],score=e[1];var c=score>=70?'#16a34a':score>=40?'#ca8a04':'#dc2626';var bg=score>=70?'#dcfce7':score>=40?'#fef3c7':'#fee2e2';return'<div style=\"display:flex;align-items:center;gap:10px;padding:8px 12px;background:#fff;border:1px solid #e5e7eb;border-radius:10px\"><span>'+name+'</span><div style=\"width:120px;height:8px;background:#e5e7eb;border-radius:4px;overflow:hidden\"><div style=\"height:100%;width:'+score+'%;background:'+c+';border-radius:4px\"></div></div><span style=\"width:36px;text-align:right;font-size:12px;font-weight:700;color:'+c+'\">'+score+'%</span></div>';}).join('')+'</div><h4 style=\"margin:0 0 10px;font-size:14px;color:#334155\">学习建议</h4><div style=\"display:flex;flex-direction:column;gap:8px\">'+recs.map(function(r){var a=r.score>=70?'#16a34a':r.score>=40?'#ca8a04':'#dc2626';var bg=r.score>=70?'#f0fdf4':r.score>=40?'#fffbeb':'#fef2f2';return'<div style=\"background:'+bg+';border-left:3px solid '+a+';border-radius:0 8px 8px 0;padding:10px 14px\"><b>'+r.knowledge+'</b> <span>'+r.score+'%</span><div>'+ (r.advice||'') +'</div></div>';}).join('')+'</div>';
}"""
if old_gr in html: html = html.replace(old_gr, new_gr); changes += 1
else: print('WARN: old generateReport not found')

# A8: analyze/reanalyze/save buttons
old = "el('analyze-btn').onclick=generateReport;"
new = "el('analyze-btn').onclick=generateReport;\n  el('reanalyze-btn').onclick=()=>{el('report-content').innerHTML='<div style=\"text-align:center;color:#94a3b8;padding:20px\">正在重新分析...</div>';generateReport();};\n  el('save-profile-btn').onclick=async()=>{await syncProfile();el('report-content').innerHTML='<div style=\"text-align:center;color:#16a34a;padding:20px;font-weight:600\">已保存。点击生成报告更新分析。</div>';};"
if old in html: html = html.replace(old, new); changes += 1
html = html.replace("el('save-profile-btn').onclick=async()=>{await syncProfile();alert('已保存');};", "")

# A9: CSS additions
html = html.replace('</style>\n{% endblock %}', """
  .knowledge-panel{background:#f0f4ff;border:1px solid #bfdbfe;border-radius:8px;padding:12px}
  .stat-mini{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:14px;text-align:center}
  .stat-big{font-size:24px;font-weight:700;color:#0f172a}
  .stat-desc{font-size:11px;color:#64748b;margin-top:2px}
  .thinking-dots .dot1{animation:dotPulse 1.5s infinite}
  .thinking-dots .dot2{animation:dotPulse 1.5s infinite .3s}
  .thinking-dots .dot3{animation:dotPulse 1.5s infinite .6s}
  @keyframes dotPulse{0%,80%,100%{opacity:0}40%{opacity:1}}
  .viz-status-done{color:#16a34a;font-weight:700;animation:statusPulse .6s ease-in-out 3}
  @keyframes statusPulse{0%,100%{opacity:1}50%{opacity:.4}}
</style>
{% endblock %}""")
changes += 1

# A10: Chat formatMarkdown + thinking indicator
old_sc = """async function sendChat(prefill){
  const input=el('chat-input'); const q=(prefill||input.value||'').trim(); if(!q) return;
  const box=el('chat-messages'); const qd=document.createElement('div');
  qd.style.cssText='margin:6px 0;text-align:right'; qd.innerHTML=`<span style="background:#2563eb;color:#fff;border-radius:8px;padding:6px 10px;display:inline-block">${q}</span>`;
  box.appendChild(qd); input.value='';
  const res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q+'（当前学习：'+NODE.name+'）'})});
  const data=await res.json(); const a=document.createElement('div');
  a.style.cssText='margin:6px 0'; a.innerHTML=`<span style="background:#e2e8f0;color:#111827;border-radius:8px;padding:6px 10px;display:inline-block">${data.answer||'无响应'} <span class="muted">(${data.provider||'?'})</span></span>`;
  box.appendChild(a); box.scrollTop=box.scrollHeight;
}"""

new_sc = """function formatMarkdown(text){
  if(!text)return'';var h=text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  h=h.replace(/\\*\\*(.+?)\\*\\*/g,'<b>$1</b>');h=h.replace(/`([^`]+)`/g,'<code>$1</code>');
  h=h.replace(/\\n\\n/g,'</p><p>');h=h.replace(/\\n/g,'<br/>');return'<p>'+h+'</p>';
}
async function sendChat(prefill){
  const input=el('chat-input'); const q=(prefill||input.value||'').trim(); if(!q) return;
  const box=el('chat-messages'); const qd=document.createElement('div');
  qd.style.cssText='margin:6px 0;text-align:right'; qd.innerHTML=`<span style="background:#2563eb;color:#fff;border-radius:8px;padding:6px 10px;display:inline-block;max-width:85%">${q}</span>`;
  box.appendChild(qd); input.value='';
  const thinkDiv=document.createElement('div');thinkDiv.style.cssText='margin:6px 0';
  thinkDiv.innerHTML=`<span class="thinking-dots" style="background:#e2e8f0;color:#475569;border-radius:8px;padding:6px 12px;display:inline-block;font-size:13px">思考中<span class="dot1">.</span><span class="dot2">.</span><span class="dot3">.</span></span>`;
  box.appendChild(thinkDiv);box.scrollTop=box.scrollHeight;
  const res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q+'（当前学习：'+NODE.name+'）'})});
  const data=await res.json();
  thinkDiv.innerHTML=`<div style="background:#e2e8f0;color:#111827;border-radius:8px;padding:10px 14px;display:inline-block;max-width:90%;line-height:1.7;font-size:13px">${formatMarkdown(data.answer||'无响应')}<div style="margin-top:4px"><span class="muted" style="font-size:10px">(${data.provider||'?'})</span></div></div>`;
  box.scrollTop=box.scrollHeight;
}"""
if old_sc in html: html = html.replace(old_sc, new_sc); changes += 1
else: print('WARN: old sendChat not found')

print(f"Phase A complete: {changes} changes applied")

# ===== PHASE B: Fix issues from 待修改.txt =====
print("\n=== Phase B: Fix viz issues ===")

# B1: Code syntax highlighting
old = """function renderCodeBox(){
  const box=el('code-box'); if(!box) return; box.innerHTML='';
  CODE_LINES.forEach((text,idx)=>{
    const line=idx+1; let lc='';
    for(const [t,ls] of Object.entries(CODE_KM)){ if(ls.includes(line)){ lc=t; break; } }
    const row=document.createElement('div'); row.className='line';
    row.innerHTML=`<span class="line-num">${line}</span>${text||'&nbsp;'}<button data-line="${line}" class="mark-btn">?</button>`;"""
new = """function highlightCode(text){
  var t=(text||'&nbsp;');
  t=t.replace(/(\\/\\/.*)/g,'<span style="color:#6b7280">$1</span>');
  t=t.replace(/(\".*?\")/g,'<span style="color:#f59e0b">$1</span>');
  t=t.replace(/\\b(struct|class|void|int|bool|char|float|double|long|auto|const|static|return|if|else|for|while|do|switch|case|break|continue|new|delete|typedef|using|namespace|public|private|protected|template|typename|include|define)\\b/g,'<span style="color:#c084fc">$1</span>');
  t=t.replace(/\\b(vector|string|map|set|queue|stack|priority_queue|pair|sort|swap|min|max|push_back|empty|size|begin|end|front|back|top|push|pop|find|insert|erase|INT_MAX|MAXN)\\b/g,'<span style="color:#60a5fa">$1</span>');
  t=t.replace(/\\b(true|false|nullptr|NULL)\\b/g,'<span style="color:#f97316">$1</span>');
  t=t.replace(/\\b(\\d+)\\b/g,'<span style="color:#34d399">$1</span>');
  return t;
}
function renderCodeBox(){
  const box=el('code-box'); if(!box) return; box.innerHTML='';
  CODE_LINES.forEach((text,idx)=>{
    const line=idx+1; let lc='';
    for(const [t,ls] of Object.entries(CODE_KM)){ if(ls.includes(line)){ lc=t; break; } }
    const hl=highlightCode(text||'&nbsp;');
    const row=document.createElement('div'); row.className='line';
    row.innerHTML=`<span class="line-num">${line}</span>${hl}<button data-line="${line}" class="mark-btn">?</button>`;"""
if old in html: html = html.replace(old, new); changes += 1
else: print('WARN: old renderCodeBox not found')

# B2: Demo complete notification
old = "el('v-status').textContent=s.op;\n  el('v-accepted').textContent"
if old in html:
    html = html.replace(old, "el('v-status').textContent=s.op;if(s.type==='done'){el('v-status').className='viz-status-done';el('v-status').textContent='演示完成';}\n  el('v-accepted').textContent")
    changes += 1

# B3: Sorting random data
old = "const PRESETS={random8:[42,17,63,8,55,31,74,26],random12:[38,15,72,6,51,29,83,11,67,44,92,3],nearly:[3,8,11,15,22,29,31,38,44,51,55,63],reversed:[63,55,51,44,38,31,29,22,15,11,8,3]};"
new = "function genRand(n){var a=[];for(var i=0;i<n;i++)a.push(Math.floor(Math.random()*90)+5);return a;}\nvar PRESETS={get random8(){return genRand(8);},get random12(){return genRand(12);},nearly:[3,8,11,15,22,29,31,38,44,51,55,63],reversed:[63,55,51,44,38,31,29,22,15,11,8,3]};"
if old in html: html = html.replace(old, new); changes += 1

# B4: DFS backtracking
old = "function dfs(u){ visited[u]=true; order.push(u); animSteps.push({type:'visit',op:`"
new = "function dfs(u,parent){ visited[u]=true; order.push(u); animSteps.push({type:'visit',op:`"
if old in html: html = html.replace(old, new); changes += 1

old = "dfs(start);"
new = "dfs(start,-1);"
if old in html: html = html.replace(old, new); changes += 1

old = "adj[u].forEach(v=>{ if(!visited[v]){ dfs(v); } });"
new = "var hasChild=false;adj[u].forEach(v=>{if(!visited[v]){hasChild=true;dfs(v,u);}});if(!hasChild||adj[u].every(function(v){return visited[v];})){animSteps.push({type:'backtrack',op:'回溯到 '+vizData.nodes[parent>=0?parent:u],visited:clone(visited),order:clone(order),current:parent>=0?parent:u,queue:[]});}"
if old in html: html = html.replace(old, new); changes += 1

# B5: KMP match output
old = "if(text[i]===pat[j]){i++;j++;if(j===m){animSteps.push({type:'match',op:'匹配! 位置='+(i-m),i,j,next});j=next[j-1]||0;}}"
new = "if(text[i]===pat[j]){i++;j++;if(j===m){animSteps.push({type:'match',op:'匹配成功! index='+(i-m)+'到'+(i-1),i,j,next,matchPos:i-m});j=next[j-1]||0;}}"
if old in html: html = html.replace(old, new); changes += 1

# B6: KMP pattern position
old = "for(let k=0;k<pat.length;k++){const x=startX+(s.j>=0?s.j:0)*(cw+gap)+k*(cw+gap);"
new = "for(let k=0;k<pat.length;k++){const x=startX+(s.i>=0?Math.max(0,s.i-(s.j>=0?s.j:0)):0)*(cw+gap)+k*(cw+gap);"
if old in html: html = html.replace(old, new); changes += 1

# B7: Convex hull
old = "while(hull.length>sz&&cross(hull[hull.length-2],hull[hull.length-1],p)<=0){hull.pop();"
new = "while(hull.length>sz&&cross(hull[hull.length-2],hull[hull.length-1],p)<0){hull.pop();"
if old in html: html = html.replace(old, new); changes += 1

# B8: Knapsack value
old = "el('v-dpinfo').innerHTML=`<b>物品:</b> ${vizData.wt.map((w,i)=>`物品${i+1}:wt=${w},val=${vizData.val[i]}`).join(' | ')}`;"
new = "el('v-dpinfo').innerHTML=`<b>物品信息:</b><br/>${vizData.wt.map((w,i)=>`物品${i+1}:重量=${w},价值=<b style=\"color:#dc2626\">${vizData.val[i]}</b>`).join(' | ')}<br/><span class=\"muted\">dp[i][w]=max(不选dp[i-1][w],选dp[i-1][w-wt]+val)</span>`;"
if old in html: html = html.replace(old, new); changes += 1

# B9: Bellman-Ford highlight
old = "dt.textContent=s.dist[i]===Infinity?'inf':s.dist[i];svg.appendChild(dt);});"
new = "dt.setAttribute('font-weight','bold');dt.textContent=s.dist[i]===Infinity?'inf':s.dist[i];svg.appendChild(dt);if(s.edgeIdx>=0){var edge=vizData.edges[s.edgeIdx];if(edge&&(edge[0]===i||edge[1]===i)){c.setAttribute('stroke','#dc2626');c.setAttribute('stroke-width','3');}}});"
if old in html: html = html.replace(old, new); changes += 1

# B10: Code context for chat ask
old = "if(el('knowledge-ask-btn')) el('knowledge-ask-btn').onclick=()=>sendChat(el('knowledge-topic').textContent);"
new = "if(el('knowledge-ask-btn')) el('knowledge-ask-btn').onclick=()=>{var t=el('knowledge-topic').textContent;if(t==='点击代码行查看'||!t){var fb=el('knowledge-feedback');fb.innerHTML='<span style=\"color:#ca8a04\">请先点击左侧代码行选择知识点。</span>';setTimeout(function(){fb.innerHTML='';},2500);return;}sendChat('关于代码中的「'+t+'」部分，请解释这个概念。');};"
if old in html: html = html.replace(old, new); changes += 1

print(f"Phase B complete: {changes} total changes")

with open('app/templates/kruskal_learning.html', 'w', encoding='utf-8') as f:
    f.write(html)

# ===== B11: Graph homepage locate center =====
with open('app/templates/graph_home.html', 'r', encoding='utf-8') as f:
    gh = f.read()
gh = gh.replace(
    "highlightedCode = item.code; renderGraph();",
    "highlightedCode = item.code; var nm = window._lastNodeMap; if(nm && nm[item.code]){ viewX = Math.max(0, nm[item.code].x - 350); viewY = Math.max(0, nm[item.code].y - 200); } renderGraph();"
)
gh = gh.replace(
    "return {map, activeCols};",
    "window._lastNodeMap = map; return {map, activeCols};"
)
with open('app/templates/graph_home.html', 'w', encoding='utf-8') as f:
    f.write(gh)
print('Graph homepage: locate center + node map saved')

# ===== VERIFY =====
print('\n=== Verification ===')
from app import create_app
app = create_app('development')
with app.test_client() as c:
    r = c.get('/learn/kruskal-core')
    h = r.data.decode('utf-8')
    s1 = h.rfind('<script>'); s2 = h.rfind('</script>')
    js = h[s1+8:s2]
    diff = js.count('{') - js.count('}')
    print(f'kruskal-core brace: {"OK" if diff==0 else "BUG diff="+str(diff)}')
    for f in ['formatMarkdown', 'highlightCode', 'wrong_concepts', 'viz-status-done', 'genRand', 'reanalyze-btn', 'question_concepts']:
        print(f'  {f}: {"OK" if f in h else "MISSING"}')
    print(f'  HTML size: {len(h)} chars')
PYEOF