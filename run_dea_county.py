import pandas as pd
import gurobipy as gp
import numpy as np
import time
from scipy.stats import pointbiserialr
import json

df = pd.read_csv('Downloads/csv.csv')
df = df[df['state_code'] == 'PA']

extracted_df = df[['lei', 'census_tract', 'county_code','action_taken', 'loan_amount', 'property_value', 'income', 'debt_to_income_ratio','loan_term', 'denial_reason-1', 'denial_reason-2', 'loan_purpose','applicant_race-1','applicant_sex']]
# extracted_df = df
extracted_df = extracted_df[extracted_df['action_taken'].isin([1,3])] 
extracted_df = extracted_df[extracted_df['loan_purpose'] == 1]
#clean property value column
extracted_df = extracted_df[extracted_df['property_value'].notna()]
extracted_df['property_value'] = np.where(extracted_df['property_value'] == 'Exempt',1111, extracted_df['property_value'])
extracted_df["property_value"] = pd.to_numeric(extracted_df["property_value"])
extracted_df["property_value"] = extracted_df["property_value"]/1000

extracted_df["loan_amount"] = extracted_df["loan_amount"]/1000


# clean loan terms column
extracted_df['loan_term'] = np.where(extracted_df['loan_term'] == 'Exempt',1111, extracted_df['loan_term'])
extracted_df['loan_term'] = pd.to_numeric(extracted_df['loan_term'])

#clean debt to income ratio column
extracted_df['debt_to_income_ratio'] = np.where(extracted_df['debt_to_income_ratio'] == '<20%',10, extracted_df['debt_to_income_ratio'])
extracted_df['debt_to_income_ratio'] = np.where(extracted_df['debt_to_income_ratio'] == '20%-<30%',25, extracted_df['debt_to_income_ratio'])
extracted_df['debt_to_income_ratio'] = np.where(extracted_df['debt_to_income_ratio'] == '30%-<36%',33, extracted_df['debt_to_income_ratio'])
extracted_df['debt_to_income_ratio'] = np.where(extracted_df['debt_to_income_ratio'] == '50%-60%',55, extracted_df['debt_to_income_ratio'])
extracted_df['debt_to_income_ratio'] = np.where(extracted_df['debt_to_income_ratio'] == '>60%',60, extracted_df['debt_to_income_ratio'])
extracted_df['debt_to_income_ratio'] = np.where(extracted_df['debt_to_income_ratio'] == 'Exempt',1111, extracted_df['debt_to_income_ratio'])
extracted_df["debt_to_income_ratio"] = pd.to_numeric(extracted_df["debt_to_income_ratio"])

extracted_df = extracted_df[extracted_df['property_value']!= 1111]
extracted_df = extracted_df[extracted_df['debt_to_income_ratio']!= 1111]
extracted_df = extracted_df[extracted_df['loan_term']!= 1111]

extracted_df.loc[extracted_df['action_taken'] == 1, 'outcome'] = 1
extracted_df.loc[extracted_df['action_taken'] == 3, 'outcome'] = 0

extracted_df = extracted_df[extracted_df['debt_to_income_ratio'].notna()]
extracted_df = extracted_df[extracted_df['loan_amount'].notna()]
extracted_df = extracted_df[extracted_df['income'].notna()]
extracted_df = extracted_df[extracted_df['property_value'].notna()]

extracted_df = extracted_df[extracted_df['county_code'].notna()]



def pbc_cal(dataframe, x, y):
#     get continuous & binary data
    x_array = dataframe[x] #binary
    y_array = dataframe[y]

    pbc = pointbiserialr(x_array,y_array)
    return pbc[0], pbc[1]





class DEA_Score:
    def __init__(self, df, number_applications, correlation):
        self.number_applications = number_applications
        self.df = df.head(self.number_applications)
        self.r_val = correlation



    def DEA(self, app_index):
        env = gp.Env(empty=True)
        env.setParam('OutputFlag',0)
        env.start()
        
        time_before = time.time()
        
        weights = []
        model = gp.Model()

        E = model.addVar(ub=1)
        w = model.addVars(self.number_applications)
        
        for variable in self.r_val:
            if matrix[variable] < 0: #if correlation coefficient of the variable is <0, the variable is input
                model.addConstr(gp.quicksum(self.df[variable][j]*w[j] for j in range(self.number_applications)) <= self.df[variable][app_index]*E )
            else:
                model.addConstr(gp.quicksum(self.df[variable][j]*w[j] for j in range(self.number_applications))  >= self.df[variable][app_index])

    
        #sum of weights equal 1
        model.addConstr(gp.quicksum(w[j] for j in range(self.number_applications))  == 1)

        model.setObjective(E)
        model.optimize()

        weights = [w[i].x for i in range(self.number_applications)]
        
        time_after = time.time()
        print("TIME RUN: " + str(time_after - time_before))

        return model.ObjVal,weights

    
    def new_data(self):
        weights = {}
        dea_list = []
         

        for i in range (self.number_applications): #number of applications
            dea, weight = self.DEA(i)
            dea_list.append(dea)
            print("Processing DMU %i, Efficiency score %.3f" % (i, dea))
            for j in range (self.number_applications):
                if 'weights' + str(j) not in weights:
                    weights['weights' + str(j)] = [weight[j]]
                else:
                    weights['weights' + str(j)].append(weight[j])  
                    
        return dea_list, weights
        
        
        
county_list = extracted_df['county_code'].unique().tolist()
#Get county data 
for county in county_list: 
    county_df = extracted_df[extracted_df['county_code'] == county]
    county_df.reset_index(inplace = True, drop = True)   
    
    #Calculate correlation coefficient based on census tract data
    from pandas.api.types import is_numeric_dtype

    matrix = {}
    for col in ['loan_amount', 'property_value', 'income', 'debt_to_income_ratio']:
        if (is_numeric_dtype(county_df[col]) == True):
            notna_df = county_df[county_df[col].notna()]
            pbc, pval = pbc_cal(notna_df, 'outcome', col)
            matrix[col] = pbc
        
        
    DEA1 = DEA_Score(county_df,county_df.shape[0], matrix)
    DEA_score = DEA1.new_data()[0]
    weights = DEA1.new_data()[1]
    
    weights_json = json.dumps(weights)
    dea_json = json.dumps(DEA_score)
    
    print("SAVE JSON FILE")
    with open(str(county)+'_weights.json','w') as fp:
        json.dump(weights_json, fp, indent = '4')
    with open(str(county)+'_dea.json','w') as fp:
        json.dump(dea_json, fp, indent = '4')
    
#     dea_county_df = county_df[['loan_amount', 'property_value', 'income','debt_to_income_ratio', 'outcome']].copy()
#     dea_county_df = pd.concat([dea_county_df, pd.DataFrame(DEA_score, columns = ['DEA'])],  
#                            axis = 1)
#     dea_county_df = pd.concat([dea_county_df, pd.DataFrame.from_dict(weights)],  
#                            axis = 1)
#     dea_county_df.to_csv(str(county) + '_county_weights_dea.csv')
    
    
#     result_dea_county_df = dea_county_df[['loan_amount', 'property_value', 'income','debt_to_income_ratio', 'outcome',"DEA"]].copy()

#     for col in ['loan_amount', 'property_value', 'income','debt_to_income_ratio']:
#         efficient = np.matmul(dea_county_df.iloc[:,6:len(dea_county_df.columns)], np.asarray(dea_county_df[col]))
#         result_dea_county_df['eff_'+ col] = np.round(efficient,decimals=1)
    
#     result_dea_county_df.to_csv(str(county) + '_county_dea.csv')