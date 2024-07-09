import os, sys
import uproot
import awkward as ak
import pandas as pd

files = [
    'photon_GJet_PT-10to40.root',
    'photon_QCD_PT-120to170.root',
    'photon_QCD_PT-300toInf.root',
    'photon_TauGun_E-100to3000.root',
    'photon_GJet_PT-40.root',
    'photon_QCD_PT-170to300.root',
    'photon_QCD_PT-80to120.root',
    'photon_TauGun_E-10to100.root'
]

tree   = 'Events'
indir  = 'InputRootFiles'
outdir = 'FlattenedCSVFiles'
os.makedirs(outdir, exist_ok=True)

def flatten_df(df):
    flattened_data = []
    for index, row in df.iterrows():
        n_pho = row['nPho']
        for i in range(n_pho):
            #In each event:
            photon_data = {}
            for col in df.columns:
                if col == 'nPho': continue
                if isinstance(row[col], list): photon_data[col] = row[col][i]
                else:                          photon_data[col] = row[col]

            flattened_data.append(photon_data)
            
    df_flattened = pd.DataFrame(flattened_data)
    return df_flattened

print('Hold on! This will take a while.')
for f in files:
    ifname = f.split('photon_')[1]
    ifname = ifname.split('.root')[0]
    ofname = 'df_'+ifname+'.csv'
    print('reading '+f+' ... ')

    with uproot.open(os.path.join(indir, f)) as infile:
        arrays = infile[tree].arrays()
        df = pd.DataFrame(ak.to_list(arrays))
        df = flatten_df(df)
        #print(df.head())
        print('Saving '+ofname+' ... ', end='')
        df.to_csv(outdir+'/'+ofname, index=False)
        print('done!')
    
    #break
print('\ncsv files ready!')

