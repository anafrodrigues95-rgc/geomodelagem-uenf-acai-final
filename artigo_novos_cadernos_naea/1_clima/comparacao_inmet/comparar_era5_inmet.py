import pandas as pd, numpy as np, json
e=pd.read_csv('../resultados/climatologia_mensal.csv')
era={v:e[e['var']==v].sort_values('month').clim_mean.values for v in e['var'].unique()}
days=np.array([31,28.25,31,30,31,30,31,31,30,31,30,31])
era['prec_mm']=era['precip_mm_day']*days
st={'82263':'Cametá','82191':'Belém','82188':'Breves'}
pairs={'PREC':'prec_mm','TMEDSECA':'temp_C','TMAX':'temp_C_15h','UR':'rh_pct'}
rows=[];series={}
for f,v in pairs.items():
    d=pd.read_excel(f'inmet/{f}.xlsx',header=2); d=d.rename(columns={d.columns[0]:'Código'}); d['Código']=d['Código'].astype(str).str.strip()
    for c,n in st.items():
        r=d[d['Código']==c]
        if r.empty: continue
        obs=pd.to_numeric(r.iloc[0,3:15],errors='coerce').values.astype(float)
        m=~np.isnan(obs); x=era[v][m]; y=obs[m]
        b=np.mean(x-y); rmse=np.sqrt(np.mean((x-y)**2)); rr=np.corrcoef(x,y)[0,1]
        row=dict(var=f,station=n,code=c,n_months=int(m.sum()),bias=b,rmse=rmse,r=rr,era_mean=x.mean(),obs_mean=y.mean())
        if f=='PREC':
            row.update(era_annual=era[v].sum(),obs_annual=np.nansum(obs) if m.all() else np.nan,rel_bias_pct=100*(x.sum()-y.sum())/y.sum())
            wet=[0,1,2,3,4];dry=[7,8,9,10]
            row.update(rel_bias_wet=100*(era[v][wet].sum()-obs[wet].sum())/obs[wet].sum(),rel_bias_dry=100*(era[v][dry].sum()-obs[dry].sum())/obs[dry].sum())
        rows.append(row); series[(f,n)]=obs
out=pd.DataFrame(rows); pd.set_option('display.width',250)
print(out.round(2).to_string())
out.to_csv('comparacao_era5_inmet.csv',index=False)
pd.to_pickle((era,series),'series.pkl')
print('ERA prec monthly',era['prec_mm'].round(0)); print('ERA dry/wet months order check')
