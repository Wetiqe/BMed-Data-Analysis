import pandas as pd
import sqlite3
import numpy as np

def pd_setup():
    pd.set_option('max_columns',1000)
    pd.set_option('max_row',300)
    pd.set_option('display.float_format', lambda x: '%.4f' % x) # set how many decimal places to keep
    pd.options.mode.chained_assignment = None  # default='warn'; disalarm ' SettingWithCopyWarning'

# connect to db
def db_conn(db_dir=""):
    if db_dir:
        try:
            db = sqlite3.connect(db_dir,timeout=30)
            dbcr = db.cursor()
        
            return db, dbcr
        except:
            print("this func is for sqlite3")
    else:
        print("plz enter a directory")
    
    

# get arrtributes of table
def get_columns(table_name, dbcr):
    dbcr.execute("SELECT * FROM {}".format(table_name))
    col_list = [tuple[0] for tuple in dbcr.description]
    return col_list


def fill_na_mean(df, rd=2):
    for col in list(df.columns[df.isnull().sum() > 0]):
        mean_val = df[col].mean()
        df[col].fillna(round(mean_val,rd),inplace=True)
        
# According to the index(subjects' ID) of df，get corresponding info we need
def get_patient_info(Pt_included,df, arrtribute):
    return Pt_included.loc[[i for i in df.index if i[0] == 'P'], arrtribute]

def get_control_info(Con, df, arrtribute):
    return Con.loc[[i for i in df.index if i[0] == 'C'], arrtribute]

def create_final_table(result_df, df1, df2, columns=['Group1', 'Group2'], aconva=True):
    columns.extend(['t value', 'p value'])
    if aconva:
        columns.append('ancova p value')
    df1_desc = df1.describe()
    df2_desc = df2.describe()
    rows = len(result_df.index)
    cols = len(columns)
    ft = pd.DataFrame(np.zeros(rows*cols).reshape(rows,cols), index = result_df.index, columns=columns)
    for i, item in enumerate(ft.index):
        ft.loc[item, columns[0]] = '{} ± {}'.format(round(df1_desc.loc['mean', item],2), round(df1_desc.loc['std', item],2))
        ft.loc[item, columns[1]] = '{} ± {}'.format(round(df2_desc.loc['mean', item],2), round(df2_desc.loc['std', item],2))
        ft.loc[item, columns[2]] = round(result_df.iloc[i, -4], 2)
        ft.loc[item, columns[3]] = result_df.iloc[i, -3]
        if result_df.iloc[i, 1] < 0.05 or result_df.iloc[i, 3] < 0.05:
            ft.loc[item, columns[3]] = result_df.iloc[i, -2]
        if aconva:
            ft.loc[item, columns[4]] = result_df.iloc[i, -1]
    
    return ft


def create_paired_table(result_df, df1, df2, columns=['Group1', 'Group2']):
    columns.extend(['t value', 'p value'])
    df1_desc = df1.describe()
    df2_desc = df2.describe()
    rows = len(result_df.index)
    cols = len(columns)
    ft = pd.DataFrame(np.zeros(rows*cols).reshape(rows,cols), index = result_df.index, columns=columns)
    for i, item in enumerate(ft.index):
        ft.loc[item, columns[0]] = '{} ± {}'.format(round(df1_desc.loc['mean', item],2), round(df1_desc.loc['std', item],2))
        ft.loc[item, columns[1]] = '{} ± {}'.format(round(df2_desc.loc['mean', item],2), round(df2_desc.loc['std', item],2))
        ft.loc[item, columns[2]] = round(result_df.iloc[i, -3], 2)
        ft.loc[item, columns[3]] = result_df.iloc[i, -2]
        if result_df.iloc[i, 1] < 0.05 or result_df.iloc[i, 3] < 0.05:
            ft.loc[item, columns[3]] = result_df.iloc[i, -1]

    return ft
