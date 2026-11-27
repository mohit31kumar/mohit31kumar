#!/usr/bin/env python3
"""Generate the static and animated assets used by the MOHIT.OS profile."""
import argparse, html, json, math, random, xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
COL={"bg":(11,11,18),"pink":(255,46,136),"lime":(182,255,0),"cyan":(0,229,255),"purple":(168,85,247),"white":(244,240,255),"muted":(145,145,166)}
def load(path,default):
 p=ROOT/path
 return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default
def font(size=12,bold=False):
 p="/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
 try:return ImageFont.truetype(p,size)
 except OSError:return ImageFont.load_default()
def t(x,y,value,size=13,color="#F4F0FF",bold=False):
 return f'<text x="{x}" y="{y}" fill="{color}" font-family="monospace" font-size="{size}" font-weight="{700 if bold else 400}">{html.escape(str(value))}</text>'
def svg(rel,w,h,body,label):
 p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(label)}"><defs><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#202233"/></pattern></defs><rect width="100%" height="100%" fill="#0B0B12"/><rect width="100%" height="100%" fill="url(#grid)"/><rect x="12" y="12" width="{w-24}" height="{h-24}" fill="none" stroke="#34364B"/>{body}</svg>',encoding="utf-8")
def render_boot():
 out=ROOT/"assets/boot";out.mkdir(parents=True,exist_ok=True)
 lines=["BIOS INITIALIZATION ................. OK","LOADING KERNEL MODULES .............. OK","DEVELOPER ENVIRONMENT ............... FOUND","OPERATOR: MOHIT KUMAR","MOHIT.OS // SYSTEM ONLINE"]
 frames=[]
 for f in range(12):
  im=Image.new("RGB",(700,190),COL["bg"]);d=ImageDraw.Draw(im)
  d.rectangle((8,8,692,182),outline=(64,66,90));d.rectangle((8,8,692,38),outline=COL["pink"])
  d.text((24,17),"MOHIT.OS / BOOTLOADER v1.0",font=font(9),fill=COL["pink"])
  for i,line in enumerate(lines[:min(5,f//2+1)]):d.text((24,54+i*22),"> "+line,font=font(10),fill=COL["lime"] if ("OK" in line or "FOUND" in line) else COL["cyan"])
  if f>=9:d.text((24,168),"SYSTEM READY // OPERATOR VERIFIED",font=font(9),fill=COL["lime"])
  frames.append(im)
 frames[-1].save(out/"boot-static.png",optimize=True)
 q=[im.quantize(colors=24,method=Image.Quantize.MEDIANCUT) for im in frames]
 q[0].save(out/"boot-sequence.gif",save_all=True,append_images=q[1:],duration=220,loop=0,optimize=True)
def render_neural():
 activity=load("assets/activity/contributions.json",{"weeks":[],"total_contributions":0})
 weeks=activity.get("weeks",[])
 levels=[max(0,min(4,int(v))) for week in weeks[-53:] for v in week[:7]]
 rng=random.Random(23);nodes=[]
 for i in range(90):
  a=i*2.399963;r=22+145*math.sqrt(i/90);level=levels[i%len(levels)] if levels else 0
  nodes.append((math.cos(a)*r,math.sin(a)*r*.58,rng.uniform(-28,28),level))
 frames=[]
 for f in range(12):
  im=Image.new("RGB",(600,250),COL["bg"]);d=ImageDraw.Draw(im)
  for x in range(20,600,30):d.line((x,62,x,235),fill=(19,21,33))
  for y in range(62,235,28):d.line((15,y,585,y),fill=(19,21,33))
  d.rectangle((10,10,590,240),outline=(58,60,82))
  d.text((22,20),"MOHIT.OS // THE LIVING MACHINE",font=font(13,True),fill=COL["white"])
  d.text((22,43),"NEURAL ACTIVITY FIELD / 365D CONTRIBUTION SIGNAL",font=font(8),fill=COL["cyan"])
  angle=f*math.tau/12;projected=[]
  for x,y,z,level in nodes:
   xr=x*math.cos(angle)-z*math.sin(angle);zr=x*math.sin(angle)+z*math.cos(angle);scale=1/(1+zr*.002)
   projected.append((300+xr*.72*scale,145+y*.68*scale,zr,level))
  for i,p in enumerate(projected):
   near=sorted(((p[0]-q[0])**2+(p[1]-q[1])**2,j) for j,q in enumerate(projected) if j>i)[:2]
   for _,j in near:
    q=projected[j]
    if p[3]+q[3]>0:d.line((p[0],p[1],q[0],q[1]),fill=(25,90,105),width=1)
  palette=[(55,60,83),COL["cyan"],COL["purple"],COL["pink"],COL["lime"]]
  for x,y,z,level in sorted(projected,key=lambda p:p[2]):
   r=1.4+level*.7;d.ellipse((x-r,y-r,x+r,y+r),fill=palette[max(0,min(4,level))])
  d.line((20,220,580,220),fill=(55,58,78))
  d.text((22,226),f"CONTRIBUTIONS / {activity.get('total_contributions',0):,} // ACTIVITY-DERIVED SIGNAL",font=font(7),fill=COL["cyan"])
  frames.append(im)
 out=ROOT/"assets/living-machine";out.mkdir(parents=True,exist_ok=True)
 frames[-1].save(out/"neural-network-static.png",optimize=True)
 q=[im.quantize(colors=32,method=Image.Quantize.MEDIANCUT) for im in frames]
 q[0].save(out/"neural-network.gif",save_all=True,append_images=q[1:],duration=160,loop=0,optimize=True)
 body='<text x="28" y="42" fill="#FF2E88" font-family="monospace" font-size="16">LIVING MACHINE / STATIC NEURAL MAP</text>'
 for i,(x,y,z,level) in enumerate(nodes):
  px=600+x*2.0; py=270+y*2.0
  for j,(xx,yy,zz,ll) in enumerate(nodes[i+1:i+4],i+1):
   qx=600+xx*2.0; qy=270+yy*2.0
   if level+ll>0: body+=f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{qx:.1f}" y2="{qy:.1f}" stroke="#00E5FF" opacity=".38"/>'
  color=["#373C53","#00E5FF","#A855F7","#FF2E88","#B6FF00"][level]
  body+=f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{2+level}" fill="{color}"/>'
 svg("assets/living-machine/neural-network-static.svg",1200,540,body,"Static contribution-driven neural network")
def render_svgs():
 projects=load("data/projects.json",{"projects":[]}).get("projects",[])
 cats=[("TOOLS / ENGINEERING","tools"),("APPLICATIONS","applications"),("SECURITY","security"),("ARCHIVE","archive")]
 body=t(35,45,"02 / PROJECT UNIVERSE",16,"#FF2E88",True)
 for i,(label,category) in enumerate(cats):
  x=35+i*300;body+=f'<rect x="{x}" y="75" width="270" height="300" fill="#10111B" stroke="#34364B"/>'+t(x+15,108,label,12,"#00E5FF",True)
  for j,p in enumerate([p for p in projects if p.get("category")==category][:5]):body+=t(x+17,155+j*42,"• "+p["name"],12)
 svg("assets/world/project-universe.svg",1240,410,body,"Categorized project universe")
 body=t(38,48,"01 / OPERATOR IDENTITY",16,"#FF2E88",True)+t(38,125,"MOHIT KUMAR",42,"#F4F0FF",True)+t(38,165,"SOFTWARE DEVELOPER / FULL-STACK APPLICATIONS",16,"#00E5FF")+t(38,210,"Building practical software systems across interfaces, APIs and data.",13,"#9291A6")
 body+='<g transform="translate(930 155)" fill="none" stroke="#00E5FF" stroke-width="2">'+''.join(f'<ellipse rx="{38+i*5}" ry="{52+i*4}" transform="rotate({i*11})" opacity="{.75-i*.045}"/>' for i in range(12))+'<circle r="7" fill="#B6FF00"/></g>'
 svg("assets/identity/biometric-scan.svg",1200,280,body,"Operator biometric identity scan")
 skills=load("data/skills.json",{"groups":[]}).get("groups",[])
 body=t(35,45,"03 / PLAYER PROFILE // TECHNOLOGY INVENTORY",16,"#FF2E88",True)
 for i,g in enumerate(skills[:4]):
  x=35+(i%2)*590;y=75+(i//2)*165
  body+=f'<rect x="{x}" y="{y}" width="550" height="135" fill="#10111B" stroke="#34364B"/>'+t(x+18,y+30,g["name"].upper(),14,"#00E5FF",True)
  for j,item in enumerate(g.get("items",[])):body+=t(x+18+(j%3)*175,y+68+(j//3)*30,item,12)
 svg("assets/profile/skill-matrix.svg",1240,430,body,"Developer technology inventory")
 profile=load("data/profile.json",{})
 metrics=[("CONTRIBUTIONS / 365D",profile.get("total_contributions","—")),("ACTIVE DAYS",profile.get("active_days","—")),("PUBLIC REPOSITORIES",profile.get("public_repositories","—")),("TOTAL STARS",profile.get("stars","—")),("TOTAL FORKS",profile.get("forks","—")),("LANGUAGES TRACKED",len(profile.get("top_languages",[])) or "—")]
 body=t(35,45,"05 / SYSTEM TELEMETRY",16,"#FF2E88",True)
 for i,(label,value) in enumerate(metrics):
  x=35+(i%3)*390;y=75+(i//3)*130
  shown=f"{value:,}" if isinstance(value,int) else value
  body+=f'<rect x="{x}" y="{y}" width="350" height="100" fill="#10111B" stroke="#34364B"/>'+t(x+16,y+30,label,11,"#9291A6")+t(x+16,y+72,shown,25,"#00E5FF",True)
 body+=t(35,335,"UPDATED / "+profile.get("updated_at","Awaiting first API sync"),10,"#9291A6")
 svg("assets/telemetry/dashboard.svg",1240,370,body,"GitHub telemetry dashboard")
 langs=profile.get("top_languages",[]);body=t(35,45,"LANGUAGE MATRIX / PUBLIC REPOSITORIES",16,"#FF2E88",True)
 if langs:
  for i,item in enumerate(langs[:6]):body+=t(35+(i%3)*390,95+(i//3)*55,f'{item["name"]} / {item["percent"]}%',13)
 else:body+=t(35,100,"Language distribution populates after the first API sync.",13)
 svg("assets/telemetry/languages.svg",1240,190,body,"Top programming languages")
 total=int(profile.get("total_contributions",0));earned=[n for n in (100,250,500,1000,2500,5000) if total>=n]
 body=t(35,45,"07 / VERIFIED MILESTONES",16,"#FF2E88",True)
 if earned:
  for i,n in enumerate(earned):
   x=35+(i%2)*590;y=75+(i//2)*65
   body+=f'<rect x="{x}" y="{y}" width="550" height="48" fill="#10111B" stroke="#B6FF00"/>'+t(x+18,y+30,f"{n:,} CONTRIBUTIONS",13,"#F4F0FF",True)
 else:body+=t(35,105,"Milestones populate after contribution data is collected.",13)
 svg("assets/achievements/achievement-board.svg",1240,300,body,"Verified contribution milestones")
 body=t(35,55,"08 / SYSTEM SHUTDOWN",16,"#FF2E88",True)+t(35,130,"END OF TRANSMISSION",38,"#F4F0FF",True)+t(35,175,"MOHIT.OS / OPERATOR SESSION CLOSED",14,"#00E5FF")
 svg("assets/shutdown/system-shutdown.svg",1200,250,body,"MOHIT.OS shutdown")
def validate():
 required=["assets/boot/boot-sequence.gif","assets/boot/boot-static.png","assets/identity/biometric-scan.svg","assets/world/project-universe.svg","assets/profile/skill-matrix.svg","assets/living-machine/neural-network.gif","assets/living-machine/neural-network-static.svg","assets/telemetry/dashboard.svg","assets/telemetry/languages.svg","assets/achievements/achievement-board.svg","assets/shutdown/system-shutdown.svg"]
 for rel in required:
  p=ROOT/rel
  if not p.exists() or not p.stat().st_size:raise SystemExit("Missing asset: "+rel)
  if rel.endswith(".svg"):ET.parse(p)
  elif rel.endswith(".gif"):
   im=Image.open(p)
   if im.n_frames<2:raise SystemExit("GIF must be animated: "+rel)
  else:Image.open(p).verify()
 readme=(ROOT/"README.md").read_text(encoding="utf-8")
 for rel in required:
  if rel != "assets/boot/boot-static.png" and rel not in readme:raise SystemExit("README does not reference "+rel)
 if (ROOT/"assets/living-machine/neural-network.gif").stat().st_size>2500000:raise SystemExit("Living Machine GIF exceeds 2.5 MB")
 print("MOHIT.OS validation passed.")
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--render",action="store_true");p.add_argument("--validate",action="store_true");a=p.parse_args()
 if a.render:render_boot();render_neural();render_svgs()
 if a.validate:validate()
