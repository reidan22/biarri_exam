# Loading up libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Loading up csv
df = pd.read_csv(r"./csv/data_3600.csv")
# df = pd.read_csv(r"./csv/data_all.csv")
# pd.set_option('display.max_rows', 500)

results = []

# for i in range(0,2 + 1):
#     for j in range(16, 18+1):
for i in range(0,15 + 1):
    for j in range(16, 30+1):
        SMAL = df['Price'].rolling(window = i).mean()
        SMAH = df['Price'].rolling(window = j).mean()
        df["SMAL"] = SMAL
        df["SMAH"] = SMAH

        def checkCrossover(row):
            if row["SMAL"] > row["SMAH"]:
                return "Higher"
            else:
                return "Lower"

        df["Crossover"] = df.apply(checkCrossover, axis=1)
        df["Change"] = ""
        df["isBuy"] = ""
        df["TimeLimit"] = 0
        # df["isAllowed"] = "---"
        df["Action"] = "---"

        for index, row in df.iterrows():
            if index == 0:
                df["Change"][index] = "N/A"
                df["isBuy"][index] = True
                df["TimeLimit"][index] = 0
                df["Action"][index] = "Buy!"
                __currentMode = "Buy!"
            else:
                    df["TimeLimit"][index] = df["TimeLimit"][index - 1] + 1
                
                    __crossOverPrev = df["Crossover"][index - 1]
                    __crossOverPres = df["Crossover"][index]
                    __timeLimit = df["TimeLimit"][index]

                    if __crossOverPrev != __crossOverPres:
                        df["Change"][index] = "Crossed"
                    else:
                        df["Change"][index] = "---"
                    
                    if df["Crossover"][index] == "Lower":
                        df["isBuy"][index] = True
                    else:
                        df["isBuy"][index] = False           
                    
                    
                    
                    df["TimeLimit"][index] = __timeLimit    
                            
                            
                    if df["Change"][index] == "Crossed" and df["isBuy"][index] and __currentMode != "Buy!":
                        df["Action"][index] = "Buy!"
                        __currentMode = "Buy!"
                        df["TimeLimit"][index] = 0 
                    if df["TimeLimit"][index] in range(30,60 + 1) and df["Change"][index] == "Crossed" and not df["isBuy"][index] and __currentMode != "Sell!":
                            df["Action"][index] = "Sell!"
                            __currentMode = "Sell!"
                
                    if df["TimeLimit"][index] >= 60 and __currentMode == "Buy!":
                        df["Action"][index] = "Sell!"
                        __currentMode = "Sell!"


        buy = df[df["Action"] == "Buy!"]["Price"].sum()
        cbuy = df[df["Action"] == "Buy!"]["Price"].count()
        sell = df[df["Action"] == "Sell!"]["Price"].sum()
        csell = df[df["Action"] == "Sell!"]["Price"].count()
        profit = sell-buy
        print(f"window<{i},{j}>")
        # if profit > 0.12:
        print(f"""Buy: {cbuy} | Sell: {csell} | Profit: {profit} --- window < {i},{j} >""")
        results.append([cbuy,csell,profit])


for res in results:
    print(res)