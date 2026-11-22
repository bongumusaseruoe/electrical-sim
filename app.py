import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SimuRelay - Electrical Simulator", layout="wide")
st.markdown("<h2 style='text-align:center'>⚡ SimuRelay - Electrical Simulator PRO</h2>", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
body{font-family:Arial;margin:0;background:#1e1e1e;color:white}
#toolbar{background:#2d2d2d;padding:10px;display:flex;gap:8px;flex-wrap:wrap}
button{padding:8px 12px;border-radius:8px;border:none;cursor:pointer;font-weight:bold}
.comp-btn{background:#444;color:white}
#canvas{position:relative;width:100%;height:600px;background:#111;background-image:linear-gradient(#222 1px,transparent 1px),linear-gradient(90deg,#222 1px,transparent 1px);background-size:25px 25px;border:2px solid #555;overflow:hidden}
.comp{position:absolute;width:90px;height:70px;background:#f5f5f5;color:black;border:2px solid #333;border-radius:8px;text-align:center;padding:5px;cursor:move;font-size:11px;font-weight:bold;user-select:none}
.comp.on{border:3px solid #00ff00;box-shadow:0 0 15px #00ff00}
.comp.motor{border-radius:50%;background:#ffcc00}
.wire{position:absolute;height:3px;background:yellow;transform-origin:left center;z-index:1}
#status{padding:10px;background:#333}
.active{color:#00ff00}
</style>
</head>
<body>
<div id="toolbar">
<button class="comp-btn" onclick="addComp('🔌 L1 L2 L3 POWER')">+ Power</button>
<button class="comp-btn" onclick="addComp('MCB 3-Pole')">+ MCB</button>
<button class="comp-btn" onclick="addComp('Contactor K1')">+ Contactor</button>
<button class="comp-btn" onclick="addComp('Overload Relay')">+ Overload</button>
<button class="comp-btn" onclick="addComp('🟢 START')">+ Start Btn</button>
<button class="comp-btn" onclick="addComp('🔴 STOP')">+ Stop Btn</button>
<button class="comp-btn" onclick="addComp('⏱ TIMER')">+ Timer</button>
<button class="comp-btn" onclick="addComp('⚙️ 3-Phase Motor')">+ Motor</button>
<button class="comp-btn" onclick="addComp('💡 Lamp')">+ Lamp</button>
<button class="comp-btn" onclick="addComp('🔔 Buzzer')">+ Buzzer</button>
<button style="background:green;color:white" onclick="simulate()">▶ SIMULATE</button>
<button style="background:red;color:white" onclick="stopSim()">■ STOP</button>
<button style="background:orange" onclick="clearAll()">🗑 Clear</button>
<button style="background:blue;color:white" onclick="loadPreset('DOL')">DOL Preset</button>
<button style="background:blue;color:white" onclick="loadPreset('STAR')">Star-Delta Preset</button>
<button style="background:blue;color:white" onclick="loadPreset('FWD')">Fwd/Rev Preset</button>
</div>
<div id="status">Status: <span id="st">Stopped - Drag components, Double-click to connect wires, Press SIMULATE</span> | <b>How to use:</b> Add components -> Drag them -> Double-click 2 components to wire them -> Simulate</div>
<div id="canvas" onclick="canvasClick(event)"></div>
<script>
let count=0, selected=null, wires=[], running=false;
function addComp(name){
  let d=document.createElement('div'); d.className='comp'; if(name.includes('Motor')) d.className+=' motor';
  d.innerText=name; d.id='c'+(count++);
  d.style.left=(50+Math.random()*500)+'px'; d.style.top=(50+Math.random()*300)+'px';
  d.ondblclick=(e)=>{e.stopPropagation(); selectComp(d)};
  d.onclick=(e)=>{e.stopPropagation(); if(name.includes('START')) toggleStart(); if(name.includes('STOP')) stopSim();};
  makeDrag(d); document.getElementById('canvas').appendChild(d);
}
function makeDrag(el){
  let x=0,y=0;
  el.onmousedown=(e)=>{x=e.clientX-el.offsetLeft; y=e.clientY-el.offsetTop;
    document.onmousemove=(ev)=>{el.style.left=(ev.clientX-x)+'px'; el.style.top=(ev.clientY-y)+'px'; drawWires()};
    document.onmouseup=()=>{document.onmousemove=null; document.onmouseup=null};
  }
}
function selectComp(d){
  if(!selected){selected=d; d.style.border='3px solid red';}
  else{
    let w={a:selected,b:d}; wires.push(w); selected.style.border='2px solid #333'; selected=null; drawWires();
    document.getElementById('st').innerText='Wired: '+w.a.innerText+' -> '+w.b.innerText;
  }
}
function drawWires(){
  document.querySelectorAll('.wire').forEach(e=>e.remove());
  wires.forEach(w=>{
    let x1=w.a.offsetLeft+45, y1=w.a.offsetTop+35, x2=w.b.offsetLeft+45, y2=w.b.offsetTop+35;
    let len=Math.hypot(x2-x1,y2-y1), ang=Math.atan2(y2-y1,x2-x1)*180/Math.PI;
    let line=document.createElement('div'); line.className='wire'; line.style.left=x1+'px'; line.style.top=y1+'px'; line.style.width=len+'px'; line.style.transform='rotate('+ang+'deg)';
    if(running) line.style.background='#00ff00'; line.style.boxShadow='0 0 8px #00ff00';
    document.getElementById('canvas').appendChild(line);
  });
}
function simulate(){
  running=true;
  document.querySelectorAll('.comp').forEach(c=>{ if(c.innerText.includes('Motor')||c.innerText.includes('Lamp')||c.innerText.includes('Contactor')) c.classList.add('on'); });
  document.getElementById('st').innerHTML='<span class=active>● RUNNING - Current Flowing! Motor Spinning ⚙️🔄</span>';
  drawWires();
}
function stopSim(){ running=false; document.querySelectorAll('.comp').forEach(c=>c.classList.remove('on')); document.getElementById('st').innerText='Stopped'; drawWires(); }
function toggleStart(){ if(running) stopSim(); else simulate(); }
function clearAll(){ document.getElementById('canvas').innerHTML=''; wires=[]; running=false; document.getElementById('st').innerText='Cleared'; }
function loadPreset(type){
  clearAll();
  if(type=='DOL'){ addComp('🔌 L1 L2 L3 POWER'); addComp('MCB 3-Pole'); addComp('Contactor K1'); addComp('Overload Relay'); addComp('🟢 START'); addComp('🔴 STOP'); addComp('⚙️ 3-Phase Motor'); }
  if(type=='STAR'){ addComp('🔌 L1 L2 L3 POWER'); addComp('MCB 3-Pole'); addComp('Contactor K1'); addComp('Contactor K1'); addComp('Contactor K1'); addComp('⏱ TIMER'); addComp('⚙️ 3-Phase Motor'); }
  if(type=='FWD'){ addComp('🔌 L1 L2 L3 POWER'); addComp('Contactor K1'); addComp('Contactor K1'); addComp('🟢 START'); addComp('🔴 STOP'); addComp('⚙️ 3-Phase Motor'); }
  setTimeout(()=>{document.getElementById('st').innerText=type+' Preset Loaded - Drag to arrange, Double-click to wire, Press SIMULATE';},300);
}
loadPreset('DOL');
</script>
</body>
</html>
"""
components.html(html_code, height=750, scrolling=False)
st.info("👆 **How to use like SimuRelay:** 1) Press DOL / Star-Delta / Fwd/Rev Preset  2) Drag components around  3) Double-click 2 components to draw a wire between them  4) Press SIMULATE - Motor turns green + wires glow green = Power flowing!")
