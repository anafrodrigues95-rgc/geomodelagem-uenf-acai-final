import pandas as pd, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
era,series=pd.read_pickle('series.pkl')
plt.rcParams.update({'font.family':'serif','font.size':9})
pan=[('PREC','prec_mm','Precipitation (mm month$^{-1}$)','ERA5-Land'),('TMEDSECA','temp_C','Mean temperature (°C)','ERA5-Land'),
     ('TMAX','temp_C_15h','Max. temp. (station) vs 15:00 (ERA5-Land) (°C)','ERA5-Land 15:00'),('UR','rh_pct','Relative humidity (%)','ERA5-Land')]
m=np.arange(1,13); lab='JFMAMJJASOND'
fig,ax=plt.subplots(1,4,figsize=(12,3.1))
for a,(f,v,t,el) in zip(ax,pan):
    a.plot(m,era[v],'k-',lw=2,label=el)
    a.plot(m,series[(f,'Cametá')],'o--',color='#1b7837',ms=4,label='INMET Cametá')
    a.plot(m,series[(f,'Belém')],'s--',color='#762a83',ms=4,label='INMET Belém')
    a.set_title(t,fontsize=9); a.set_xticks(m); a.set_xticklabels(list(lab)); a.grid(alpha=.3)
ax[0].legend(fontsize=7,frameon=False)
fig.tight_layout(); fig.savefig('Figure_S1_ERA5_INMET.png',dpi=300)
