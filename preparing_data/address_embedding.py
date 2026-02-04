import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


half_prepared_csv = pd.read_csv('csv_folder/half_prepared.csv', sep=';')


def make_embedding(df, col_name, emb_dim, prefix):
    """
    Creates a random embedding for a categorical column
    and adds it as new columns with names prefix_1 ... prefix_n
    """
    df[col_name] = df[col_name].fillna('missing')
    le = LabelEncoder()
    df[col_name] = le.fit_transform(df[col_name])
    
    num_classes = df[col_name].nunique()
    embedding_matrix = np.random.randn(num_classes, emb_dim)
    
    embedded_vectors = embedding_matrix[df[col_name]]
    
    # tworzymy kolumny w df
    for i in range(emb_dim):
        df[f"{prefix}_{i+1}"] = embedded_vectors[:, i]
    
    return df

# -----------------------
# Tworzymy embeddingi
half_prepared_csv = make_embedding(half_prepared_csv, 'city', 8, 'city')
half_prepared_csv = make_embedding(half_prepared_csv, 'locality', 10, 'locality')
half_prepared_csv = make_embedding(half_prepared_csv, 'street', 20, 'street')
half_prepared_csv.to_csv('csv_folder/embedded_data.csv',sep=';',index=False)

