# parser dedicated to online uses  

import pandas as pd
import argparse
import config as cfg
import os

parser = argparse.ArgumentParser()

parser.add_argument('--metadata')
parser.add_argument('--metadata_cluster')
parser.add_argument('--cutoff',default=5)

arg = parser.parse_args()

md = arg.metadata
mdc = arg.metadata_cluster
cutoff = arg.cutoff

# load columns names from config file
cells = cfg.metadata_columns
mindex = cfg.metadata_index_columns


csv = pd.read_csv(mdc,sep='\t')
test = pd.read_csv(md,sep='\t')

t = csv['cluster'].value_counts()
csv['cluster_size'] = csv['cluster'].map(lambda x:t[x])
csv2 = csv.drop_duplicates(subset=['cluster_size','cluster'])
csv3 = csv2.sort_values(by='cluster_size',ascending=False)
csv4 = csv3[csv3['cluster_size']>=5]


result = pd.merge(csv4,test)


# concat filename
destination_dir = os.path.dirname(md)
source_filename = os.path.splitext(md)[0].split(os.sep)[-1]
tsv_name = os.path.join(destination_dir, '{}_web.tsv'.format(source_filename))

result.to_csv(tsv_name,sep='\t')