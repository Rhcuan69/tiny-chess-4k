import json,os,sys,urllib.request as q;U=os.environ.get("MAKEFUN_ENV_URL") or sys.exit("no env");V=[0,100,320,330,500,900,0];PAWN=[0,0,0,0,50,50,50,50,10,10,20,30,5,5,10,25,0,0,0,20,5,-5,-10,0,5,10,10,-20,0,0,0,0];KNIGHT=[-50,-40,-30,-30,-40,-20,0,0,-30,0,10,15,-30,5,15,20,-30,0,15,20,-30,5,10,15,-40,-20,0,5,-50,-40,-30,-30];BISHOP=[-20,-10,-10,-10,-10,0,0,0,-10,0,5,10,-10,5,5,10,-10,0,10,10,-10,10,10,10,-10,5,0,0,-20,-10,-10,-10];ROOK=[0,0,0,0,5,10,10,10,-5,0,0,0,-5,0,0,0,-5,0,0,0,-5,0,0,0,-5,0,0,0,0,0,0,5];QUEEN=[-20,-10,-10,-5,-10,0,0,0,-10,0,5,5,-5,0,5,5,0,0,5,5,-10,5,5,5,-10,0,5,0,-20,-10,-10,-5];KING=[-30,-40,-40,-50,-30,-40,-40,-50,-30,-40,-40,-50,-30,-40,-40,-50,-20,-30,-30,-40,-10,-20,-20,-20,20,20,0,0,20,30,10,0];PST=[0,PAWN,KNIGHT,BISHOP,ROOK,QUEEN,KING];IX=[(7-(q>>4))*4+min(q&7,7-(q&7)) for q in range(128)];PV=[[0]*32]+[[V[t]+PST[t][i] for i in range(32)] for t in range(1,7)];KN=[33,31,18,14,-14,-18,-31,-33];KI=[1,-1,16,-16,15,17,-15,-17];BI=[15,17,-15,-17];RO=[1,-1,16,-16];CR=[15]*128
for s,v in ((0,13),(7,14),(4,12),(112,7),(119,11),(116,3)): CR[s]=v
MATE=100000
NL=22000
N=NW=NB=0
TT={}
KIL={}
class AB(Exception): pass
def on(s): return 0<=s<128 and not s&0x88
def sq(s): return ord(s[0])-97|int(s[1])-1<<4
def us(m):
 f=m&127;t=m>>7&127;r=chr(97+(f&7))+str((f>>4)+1)+chr(97+(t&7))+str((t>>4)+1);return r if not m>>14 else r+"nbrq"[(m>>14)-2]
def parse(f):
 b=[0]*128;q=f.split();r=7;x=0
 for ch in q[0]:
  if ch=="/": r-=1;x=0
  elif ch.isdigit(): x+=int(ch)
  else:
   c="PNBRQK".find(ch.upper())+1;b[r*16+x]=c if ch.isupper() else c+6;x+=1
 w=1 if q[1]=="w" else -1;c=0
 if "K" in q[2]: c|=1
 if "Q" in q[2]: c|=2
 if "k" in q[2]: c|=4
 if "q" in q[2]: c|=8
 e=-1 if q[3]=="-" else sq(q[3])
 return b,[w,c,e,int(q[4]),b.index(6),b.index(12)]
def atk(b,s,w):
 pc=4-3*w
 for d in (15,17):
  t=s-w*d
  if on(t) and b[t]==pc: return 1
 nc=5-3*w
 for d in KN:
  t=s+d
  if on(t) and b[t]==nc: return 1
 kc=9-3*w
 for d in KI:
  t=s+d
  if on(t) and b[t]==kc: return 1
 for d in BI:
  t=s+d
  while on(t):
   p=b[t]
   if p:
    if p in (6-3*w,8-3*w): return 1
    break
   t+=d
 for d in RO:
  t=s+d
  while on(t):
   p=b[t]
   if p:
    if p in (7-3*w,8-3*w): return 1
    break
   t+=d
 return 0
def gen(b,st):
 w,c,e,h,kw,kb=st;ms=[]
 for s in range(128):
  if s&0x88: continue
  p=b[s]
  if not p or (p<=6)!=(w>0): continue
  t_=p if p<=6 else p-6
  if t_==1:
   d=16*w;t=s+d
   if on(t) and not b[t]:
    if (t>>4)==(7 if w>0 else 0):
     for q in (5,4,3,2): ms.append(s|t<<7|q<<14)
    else:
     ms.append(s|t<<7)
     if (s>>4)==(1 if w>0 else 6) and not b[s+2*d]: ms.append(s|(s+2*d)<<7)
   for dd in (d-1,d+1):
    t=s+dd
    if on(t):
     q=b[t]
     if q and (q<=6)!=(w>0):
      if (t>>4)==(7 if w>0 else 0):
       for pr in (5,4,3,2): ms.append(s|t<<7|pr<<14)
      else: ms.append(s|t<<7)
     elif t==e and e>=0: ms.append(s|t<<7)
  elif t_==2:
   for d in KN:
    t=s+d
    if on(t) and (not b[t] or (b[t]<=6)!=(w>0)): ms.append(s|t<<7)
  elif t_==6:
   for d in KI:
    t=s+d
    if on(t) and (not b[t] or (b[t]<=6)!=(w>0)): ms.append(s|t<<7)
   if s==(4 if w>0 else 116):
    if w>0:
     if c&1 and not b[5] and not b[6] and not atk(b,4,-1) and not atk(b,5,-1) and not atk(b,6,-1): ms.append(4|6<<7)
     if c&2 and not b[3] and not b[2] and not b[1] and not atk(b,4,-1) and not atk(b,3,-1) and not atk(b,2,-1): ms.append(4|2<<7)
    else:
     if c&4 and not b[117] and not b[118] and not atk(b,116,1) and not atk(b,117,1) and not atk(b,118,1): ms.append(116|118<<7)
     if c&8 and not b[115] and not b[114] and not b[113] and not atk(b,116,1) and not atk(b,115,1) and not atk(b,114,1): ms.append(116|114<<7)
  else:
   ds=BI if t_==3 else RO if t_==4 else BI+RO
   for d in ds:
    t=s+d
    while on(t):
     q=b[t]
     if not q: ms.append(s|t<<7)
     else:
      if (q<=6)!=(w>0): ms.append(s|t<<7)
      break
     t+=d
 return ms
def make(b,st,m):
 f=m&127;t=m>>7&127;pr=m>>14&7;w,c,e,h,kw,kb=st;p=b[f];cap=b[t];epc=-1;kw0=kw;kb0=kb
 if p in (1,7) and t==e and not cap:
  epc=t-16*w;cap=b[epc];b[epc]=0
 b[f]=0;b[t]=(pr if w>0 else pr+6) if pr else p
 if p in (6,12) and abs(t-f)==2:
  rf,rt=(f+3,f+1) if t>f else (f-4,f-1);b[rt]=b[rf];b[rf]=0
 nc=c&CR[f]&CR[t];ne=f+16*w if p in (1,7) and abs(t-f)==32 else -1;nh=0 if p in (1,7) or cap else h+1
 if p==6: kw=t
 if p==12: kb=t
 st[0]=-w;st[1]=nc;st[2]=ne;st[3]=nh;st[4]=kw;st[5]=kb
 return (m,cap,epc,e,c,h,kw0,kb0)
def unmake(b,st,u):
 m,cap,epc,e,c,h,kw,kb=u;f=m&127;t=m>>7&127;pr=m>>14&7;w=-st[0];p=b[t]
 if pr: p=1 if w>0 else 7
 b[f]=p;b[t]=cap if epc<0 else 0
 if epc>=0: b[epc]=cap
 if p in (6,12) and abs(t-f)==2:
  rf,rt=(f+3,f+1) if t>f else (f-4,f-1);b[rf]=b[rt];b[rt]=0
 st[0]=w;st[1]=c;st[2]=e;st[3]=h;st[4]=kw;st[5]=kb
def md(a,b):
 return (7-max(abs(a%8-b%8),abs(a//16-b//16)))*20+max(abs(b%8-3),abs(b//16-3))*10
def ev(b,st):
 global NW,NB
 s=pc=mn=wn=bn=0;wk,bk=st[4:6];NW=NB=0;wb=bb=0
 for q in range(128):
  if q&0x88: continue
  p=b[q]
  if p:
   t=p if p<=6 else p-6
   pc+=t in(1,4,5);mn+=t in(2,3)
   if t!=6: wn+=p<7;bn+=p>6
   if 1<t<6: NW+=p<7;NB+=p>6
   if t==3: wb+=p<7;bb+=p>6
   v=PV[t][IX[q] if p<=6 else IX[q^112]];s+=v if p<=6 else -v
 if pc<1 and mn<2: return None
 if wb==2: s+=30
 if bb==2: s-=30
 if bn==0 and wn: s+=md(wk,bk)
 elif wn==0 and bn: s-=md(bk,wk)
 return s
def key(b,st): return bytes(b)+bytes((st[0]+1,st[1],st[2]+1))
def order(b,st,ms,ttm,ply):
 def sc(m):
  f=m&127;t=m>>7&127;v=b[t];s=0
  if v: s=10000+V[v if v<=6 else v-6]*10-V[b[f] if b[f]<=6 else b[f]-6]
  if m==ttm: s+=1000000
  if m in KIL.get(ply,()): s+=9000
  return -s
 ms.sort(key=sc);return ms
def qs(b,st,a,be,ply,seen):
 global N;N+=1
 if N>NL: raise AB
 k=key(b,st)
 if st[3]>=100: return 0
 e=ev(b,st)
 if e is None: return 0
 if k in seen: return -30 if e*st[0]>0 else 30
 w=st[0];s=e*w
 if s>=be: return be
 if s>a: a=s
 ks=st[4] if w>0 else st[5];e2=st[2]
 if atk(b,ks,-w):
  ms=gen(b,st);ic=1
 else:
  ms=[m for m in gen(b,st) if b[m>>7&127] or m>>14 or (m>>7&127)==e2];ic=0
 order(b,st,ms,0,ply);nl=0
 for m in ms:
  u=make(b,st,m)
  if atk(b,st[4] if w>0 else st[5],-w):unmake(b,st,u);continue
  nl+=1;v=-qs(b,st,-be,-a,ply+1,seen);unmake(b,st,u)
  if v>=be: return be
  if v>a: a=v
 if ic and not nl: return -MATE+ply
 return a
def search(b,st,d,a,be,ply,seen):
 global N;N+=1
 if N>NL: raise AB
 k=key(b,st)
 if st[3]>=100: return 0
 e=ev(b,st)
 if e is None: return 0
 if k in seen: return 30 if e*st[0]<=0 else -30
 t=TT.get(k);ttm=0
 if t:
  _,v,fl,mv=t;ttm=mv
  if t[0]>=d:
   if fl==0: return v
   if fl==1 and v>a: a=v
   elif fl==2 and v<be: be=v
   if a>=be: return v
 w=st[0]
 if atk(b,st[4] if w>0 else st[5],-w): d+=1
 elif d>=3 and e*w>=be and (NW if w>0 else NB):
  s0,s2,s3=st[0],st[2],st[3];st[0]=-w;st[2]=-1;st[3]+=1
  v=-search(b,st,d-3,-be,-be+1,ply+1,seen)
  st[0],st[2],st[3]=s0,s2,s3
  if v>=be: return be
 if d<=0: return qs(b,st,a,be,ply,seen)
 ms=gen(b,st)
 order(b,st,ms,ttm,ply);seen.add(k);best=-MATE;bm=0;fl=2;ao=a;nl=0
 try:
  for m in ms:
   t2=m>>7&127;cap=b[t2] or m>>14 or t2==st[2]
   u=make(b,st,m)
   if atk(b,st[4] if w>0 else st[5],-w):unmake(b,st,u);continue
   nl+=1
   if nl>3 and d>=3 and not cap:
    v=-search(b,st,d-2,-be,-a,ply+1,seen)
    if v>a: v=-search(b,st,d-1,-be,-a,ply+1,seen)
   else:
    v=-search(b,st,d-1,-be,-a,ply+1,seen)
   unmake(b,st,u)
   if v>best: best=v;bm=m
   if v>a: a=v
   if a>=be:
    fl=1
    if not b[m>>7&127] and not m>>14:
     kl=KIL.setdefault(ply,[])
     if m not in kl:
      kl.append(m)
      if len(kl)>2: kl.pop(0)
    break
 finally:
  seen.discard(k)
 if not nl:
  ks=st[4] if w>0 else st[5]
  return -MATE+ply if atk(b,ks,-w) else 0
 if best<=ao: fl=2
 elif best>=be: fl=1
 else: fl=0
 TT[k]=(d,best,fl,bm)
 return best
def pmv(s,b,st):
 f=sq(s[:2]);t=sq(s[2:4]);pr=0
 if len(s)==5: pr="nbrq".find(s[4])+2
 return f|t<<7|pr<<14
def root(b,st,moves,rep,hist):
 global N;N=0;best=moves[0];rk=key(b,st);order(b,st,moves,0,0)
 try:
  for d in range(1,64):
   cur=[]
   for m in moves:
    u=make(b,st,m);v=-search(b,st,d-1,-MATE,MATE,1,rep|{rk});unmake(b,st,u);cur.append((v,m))
   cur.sort(key=lambda x:-x[0]);best=cur[0][1];moves=[m for _,m in cur]
   bv=cur[0][0]
   if bv>100:
    for v,m in cur:
     if v<bv-50: break
     u=make(b,st,m);k=key(b,st);unmake(b,st,u)
     if k not in hist: best=m;moves=[m]+[x for _,x in cur if x!=m];break
   if N>NL: break
 except AB:
  pass
 return best
def post(p,body):
 r=q.Request(U+p,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
 try:
  with q.urlopen(r) as x: return json.load(x)
 except Exception:
  sys.exit(p)
while True:
 g=post("/game",{})
 if g["status"]=="done": break
 while g["status"]=="your_move":
  b0,st0=parse("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
  hist={}
  for mv in g["moves"]:
   m=pmv(mv,b0,st0);make(b0,st0,m);kk=key(b0,st0);hist[kk]=hist.get(kk,0)+1
  rep={kk for kk,c in hist.items() if c>=2}
  b,st=parse(g["fen"]);moves=[pmv(mv,b,st) for mv in g["legal_moves"]];mv=root(b,st,moves,rep,hist);g=post("/move",{"game":g["game"],"move":us(mv)})
