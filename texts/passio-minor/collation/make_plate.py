#!/usr/bin/env python3
"""make_plate.py — the figure that replaces the conceptual stemma of Figure 2."""
import json, itertools
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Liberation Serif","DejaVu Serif"],
    "axes.edgecolor": "#3a342c", "text.color": "#241f18",
    "axes.labelcolor": "#241f18", "xtick.color": "#241f18", "ytick.color": "#241f18",
})
CREAM="#F6F1E4"; INK="#241f18"; RULE="#b9ac90"; ACC="#7a1f1f"

sig  = json.load(open("data/stemma_signal.json"))
wits = json.load(open("data/witnesses.json"))
ORDER=["Sg","V","M1","M2","Ad","W","P"]
LAB  ={"Sg":"Sg","V":"V","M1":"M¹","M2":"M²","Ad":"Ad","W":"W","P":"P"}
cites=sig["citations"]; pairs={p["pair"]:p for p in sig["pairs"]}

A=np.full((7,7),np.nan)
for i,a in enumerate(ORDER):
    for j,b in enumerate(ORDER):
        if i==j: continue
        k=f"{a}-{b}" if f"{a}-{b}" in pairs else f"{b}-{a}"
        if k in pairs: A[i,j]=pairs[k]["affinity"]

fig=plt.figure(figsize=(12.6,14.4),dpi=170); fig.patch.set_facecolor(CREAM)
gs=fig.add_gridspec(3,2,height_ratios=[.92,1.5,.72],hspace=.36,wspace=.20,
                    left=.065,right=.955,top=.925,bottom=.055)

fig.text(.5,.968,"Passio minor Kiliani — Witness Collation",ha="center",
         fontsize=25,weight="bold",color=INK)
fig.text(.5,.945,"Emmerich, $Der$ $heilige$ $Kilian$ (Würzburg 1896), pp. 3–10  ·  "
                 "251 lemma entries · 361 readings · 7 witnesses",
         ha="center",fontsize=11.5,color="#5a5244",style="italic")
fig.add_artist(plt.Line2D([.065,.955],[.936,.936],color=RULE,lw=1.1))

# ---- A. witness table
ax=fig.add_subplot(gs[0,:]); ax.axis("off"); ax.set_facecolor(CREAM)
ax.text(0,1.02,"A.  Siglum table with foliation",transform=ax.transAxes,
        fontsize=13.5,weight="bold",color=INK)
cols=[0.0,0.052,0.28,0.44,0.555,0.70,0.845]
hdr=["Sig.","Shelfmark","Repository","Date","Locus","Extent","Cited"]
for x,h in zip(cols,hdr):
    ax.text(x,0.90,h.upper(),fontsize=8.6,weight="bold",color="#6b6152",
            transform=ax.transAxes)
ax.add_artist(plt.Line2D([0,0.96],[0.865,0.865],color=INK,lw=1.0,transform=ax.transAxes))
REPO={"Sg":"Stiftsbibl. St. Gallen","V":"ÖNB Wien","M1":"BSB München",
      "M2":"BSB München","Ad":"Stiftsbibl. Admont","W":"UB Würzburg","P":"Schönborn, Pommersfelden"}
for r,wid in enumerate(ORDER):
    w=[x for x in wits if x["id"]==wid][0]; y=0.80-r*0.112
    ax.text(cols[0],y,LAB[wid],fontsize=11.5,weight="bold",style="italic",
            color=ACC,transform=ax.transAxes)
    ax.text(cols[1],y,w["shelfmark"],fontsize=9.8,transform=ax.transAxes)
    ax.text(cols[2],y,REPO[wid],fontsize=9.8,transform=ax.transAxes)
    ax.text(cols[3],y,w["century"],fontsize=9.8,transform=ax.transAxes)
    ax.text(cols[4],y,w["locus"] or "—",fontsize=9.8,transform=ax.transAxes)
    ax.text(cols[5],y,(w["extent"] or "—"),fontsize=9.8,transform=ax.transAxes)
    n=cites.get(wid,0)
    ax.text(cols[6],y,str(n),fontsize=10.4,weight="bold",transform=ax.transAxes)
    ax.add_patch(Rectangle((cols[6]+0.035,y-0.004),0.115*n/max(cites.values()),0.030,
                 transform=ax.transAxes,color=ACC,alpha=.33,lw=0))
    ax.add_artist(plt.Line2D([0,0.96],[y-0.035,y-0.035],color=RULE,lw=.45,transform=ax.transAxes))

# ---- B. affinity matrix
ax=fig.add_subplot(gs[1,0]); ax.set_facecolor(CREAM)
im=ax.imshow(A,cmap="YlOrBr",vmin=0.30,vmax=0.78)
ax.set_xticks(range(7)); ax.set_yticks(range(7))
ax.set_xticklabels([LAB[o] for o in ORDER],fontsize=11.5,style="italic")
ax.set_yticklabels([LAB[o] for o in ORDER],fontsize=11.5,style="italic")
for i in range(7):
    for j in range(7):
        if i==j:
            ax.add_patch(Rectangle((j-.5,i-.5),1,1,color="#e3dbc6",lw=0))
        elif not np.isnan(A[i,j]):
            ax.text(j,i,f"{A[i,j]:.2f}",ha="center",va="center",fontsize=9.6,
                    color=INK if A[i,j]<.62 else "white",
                    weight="bold" if A[i,j]>=.60 else "normal")
ax.set_title("B.  Pairwise affinity",loc="left",fontsize=13.5,weight="bold",pad=10)
ax.text(0.0,-0.115,"shared readings ÷ (shared + opposed), chronological order",
        transform=ax.transAxes,fontsize=9,style="italic",color="#5a5244")
for s in ax.spines.values(): s.set_color(RULE)

# ---- C. ranked pairs
ax=fig.add_subplot(gs[1,1]); ax.set_facecolor(CREAM)
top=sig["pairs"][:9][::-1]
ys=np.arange(len(top))
ax.barh(ys,[p["affinity"] for p in top],color=ACC,alpha=.78,height=.62)
ax.set_yticks(ys); ax.set_yticklabels(
    [p["pair"].replace("M1","M¹").replace("M2","M²") for p in top],fontsize=10.5,style="italic")
ax.set_xlim(0,.80); ax.set_xlabel("affinity",fontsize=10)
for y,p in zip(ys,top):
    ax.text(p["affinity"]+.012,y,f'{p["affinity"]:.3f}   ({p["agreements"]}:{p["oppositions"]})',
            va="center",fontsize=9.2,color="#5a5244")
ax.set_title("C.  Ranked witness pairs",loc="left",fontsize=13.5,weight="bold",pad=10)
ax.grid(axis="x",color=RULE,lw=.4,alpha=.6); ax.set_axisbelow(True)
for s in ax.spines.values(): s.set_color(RULE)

# ---- D. the worked example
ax=fig.add_subplot(gs[2,:]); ax.axis("off"); ax.set_facecolor(CREAM)
ax.set_title("D.  One lemma, read across the witnesses — p. 4, lemma 8",
             loc="left",fontsize=13.5,weight="bold",pad=8)
ax.text(0,.79,"propria contempni patriamque et parentes … relinquere et nudos sequi Christum",
        fontsize=12.6,style="italic",transform=ax.transAxes)
rows=[("Sg","s. IX","propria contempni","passive infinitive — the adopted reading"),
      ("W","s. XI","propria contempnere","active"),
      ("M²","s. XII","propria contemnere","active, classical orthography"),
      ("P","s. XIII–XIV","propriam contempnere","accusative singular — the object changes"),
      ("Ad","s. XII","secundum evangelium domini nudosque Christum sequi","whole clause transposed")]
for r,(s,c,rd,note) in enumerate(rows):
    y=.60-r*.135
    ax.text(.012,y,s,fontsize=11,weight="bold",style="italic",color=ACC,transform=ax.transAxes)
    ax.text(.065,y,c,fontsize=9.6,color="#5a5244",transform=ax.transAxes)
    ax.text(.17,y,rd,fontsize=10.6,transform=ax.transAxes)
    ax.text(.60,y,note,fontsize=9.6,style="italic",color="#5a5244",transform=ax.transAxes)
ax.text(.012,-.10,"contemnere and sequi hold across every witness.  propria does not.",
        fontsize=11,weight="bold",transform=ax.transAxes)

fig.text(.065,.022,"Transcribed from the plates at 430 dpi, not from the OCR layer.  "
                   "Affinity is a signal from a mixed apparatus, not a stemma: "
                   "agreements with the base text go uncited, and Emmerich does not mark which readings are errors.",
         fontsize=8.2,color="#6b6152",style="italic")
fig.savefig("passio_minor_collation.png",facecolor=CREAM,bbox_inches="tight")
print("wrote passio_minor_collation.png")
