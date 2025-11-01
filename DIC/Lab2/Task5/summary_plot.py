import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True  
if __name__ == '__main__':
    df = pd.read_excel('summary.xlsx', index_col=0)
    plt.figure(figsize=(5,4))
    plt.plot(df.index, df['tp_total']*1e9, color='black')
    plt.scatter(df.index, df['tp_total']*1e9, color='black')
    plt.xlabel(r'N')
    plt.ylabel(r'$t_{p}/ns$', fontsize=14)
    plt.title('Propagation Delay vs Number of Inverters', fontsize=16)
    plt.grid(True)
    plt.xticks(df.index)
    plt.savefig('tp_N.png', dpi=300)
