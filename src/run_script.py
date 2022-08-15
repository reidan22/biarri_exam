from packages import *
from constants import *
from functions import *

try:
    file_choice = int(sys.argv[1])
except:
    file_choice = 1


df = pd.read_csv(CSV_FILES[file_choice - 1])


df["SMAL"] = df['Price'].rolling(window = SMA_LOW).mean()
df["SMAH"] = df['Price'].rolling(window = SMA_HIGH).mean()

df["Crossover"] = df.apply(checkCrossover, axis=1)
df["Change"] = ""
df["isBuy"] = ""
df["TimeLimit"] = 0
df["Action"] = "---"
df["CurrentPrice"] = "---"



print(f"Running " + CSV_FILES[file_choice - 1] + " ...")
for index, row in df.iterrows():
    if index == 0:
        df["Change"][index] = "N/A"
        df["isBuy"][index] = True
        df["TimeLimit"][index] = 0
        df["Action"][index] = "Buy!"
        df["CurrentPrice"][index] = float(df["Price"][index])
        __currentMode = "Buy!"
        __currentProfit = df["CurrentPrice"][index]
        report["buy"]["price"] = df["Price"][index]


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
                df["CurrentPrice"][index] = df["Price"][index]
                report["buy"]["time"] = df["Time"][index]
                report["buy"]["price"] = df["Price"][index]
                df["TimeLimit"][index] = 0 
                
            if  df["Price"][index] > report["buy"]["price"] and df["TimeLimit"][index] in range(30,59 + 1) and df["Change"][index] == "Crossed" and not df["isBuy"][index] and __currentMode != "Sell!":
                df["Action"][index] = "Sell!"
                __currentMode = "Sell!"                    
                df["CurrentPrice"][index] = df["Price"][index]
                report["sell"]["time"] = df["Time"][index]
                report["sell"]["price"] = df["Price"][index]
                report["profit"] +=  report["sell"]["price"] -  report["buy"]["price"]                    
                reportMessage(report, df["TimeLimit"][index])

            
            elif df["TimeLimit"][index] in range(ALLOWABLE_MARGIN,59) and df["Price"][index] > report["buy"]["price"] and __currentMode != "Sell!":
                df["Action"][index] = "Sell!"
                __currentMode = "Sell!"
                df["CurrentPrice"][index] = df["Price"][index]
                report["sell"]["time"] = df["Time"][index]
                report["sell"]["price"] = df["Price"][index]
                report["profit"] +=  report["sell"]["price"] -  report["buy"]["price"]
                reportMessage(report, df["TimeLimit"][index],"CLOSED")


            
            elif df["TimeLimit"][index] >= 59 and __currentMode == "Buy!":
                df["Action"][index] = "Sell!"
                __currentMode = "Sell!"
                df["CurrentPrice"][index] = df["Price"][index]
                report["sell"]["time"] = df["Time"][index]
                report["sell"]["price"] = df["Price"][index]
                report["profit"] +=  report["sell"]["price"] -  report["buy"]["price"]
                reportMessage(report, df["TimeLimit"][index],"FORCED")
                            
print(f'\nTotal profit: {round(report["profit"],4):.4f}')