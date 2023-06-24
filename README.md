# HDMA-Research

## A. Research Problem
In recent years, there have been many applications and implementations of machine learning techniques in the financial domain, especially in the loan application decision-making process [1]. Many banks have adapted Artificial Intelligence/Machine Learning (AI/ML) algorithms to automate the process of granting loans and the reasons for the loan acceptance are of interest to both the bank and the applicants. However, as most of these methods are regarded as black box models that lack transparency in their decision-making process, the adoption of machine learning algorithms in loan decision-making has led to concerns about transparency and interpretability. Interpretable machine learning, which aims to provide context for these decisions, has therefore become an important research issue [2]. This research project proposes the use of counterfactual-based explanations to account for the predictions of these algorithms and to suggest how much the applicant’s financial profile needs to change to yield a desirable loan decision outcome. Furthermore, this research will implement a well-studied analytical methodology, Data Envelopment Analysis (DEA), which has not been previously used in loan decision-making to have a better understanding of the outcomes in the decision-making process of loan application algorithms.

## B. Research Value
Most of the time, applicants are only provided with general information about why their applications are rejected such as insufficient income, high debt-to-income ratio, etc. These explanations fall short of addressing how each applicant’s financial profile can be changed to achieve the desired outcome. I believe this would provide meaningful advice for future loan applicants to increase the chance of successful application, and hence enhance the interpretability of these algorithms for a transparent and fair process for loan decision-making.

## C. Project Description
Background:
In interpretable machine learning, counterfactual analysis is used to explain the predictions made by so-called black box models for individual instances [3]. A Counterfactual can be defined as a nearby instance of an actual observation but with a different prediction result from the model [3]. It may help understand for example how to ﬂip the predicted class of a loan application from rejected (undesired) to accepted (desired). For example, when an applicant asks for a loan that is rejected, an example of the counterfactual is: “If the income would have been $1000 higher than the current one, and if the customer had fully paid current debts with other banks, then the loan would have been accepted” [5].

Data envelopment analysis (DEA) is a frontier analysis approach to efficiency measurement of entities such as banks, hospitals, loan applicants, etc., collectively called Decision-Making Units (DMUs) with multi-inputs and multi-outputs by using a linear programming methodology to evaluate their performance in converting input to outputs [6]. The purpose of the analysis is to identify the DMU that most effectively transforms its inputs into outputs. These efficient units define what is called the efficiency frontier. The remaining units, located below the frontier, are deemed ineffective. For example, consider a set of banks, where each bank is considered a DMU. Each bank has exactly 10 tellers (the only input), and we measure a bank based on two outputs: checks cashed and loans processed. From Figure 1, bank A is considered as efficient because there is no other combination of banks B and C that can produce more than at least as much output (1000 checks and 20 loans) with the same input (10 tellers). Similarly, bank C also lies on the efficiency frontier (AC). Since bank B lies below the efficiency frontier, it is inefficient and there is a virtual bank V which is a combination of banks A and C that produces the output that bank B would have to produce with the current input to be considered as efficient as banks A and C [7].

<img width="429" alt="Screen Shot 2023-06-24 at 13 17 31" src="https://github.com/lhn004/HDMA-Research/assets/112211984/2d97e160-3e61-454f-bd29-76c63d33fbe0">

Figure 1: Illustration of the efficiency frontier given a set of three banks [7]

The efficiency score of DEA is 1.0 for frontier points, which are regarded as the benchmark for others to follow while it is less than 1.0 for insufficient points located behind the frontier. In our case, DMUs are loan applications, the outcome is a binary variable (0 if the application is rejected and 1 if it is accepted), and the outputs and inputs will be determined by measuring the intensity of the association between the outcome variable and potential explanatory variables. For any variables that have a positive correlation, they will be used as outputs for the model; otherwise, they are inputs. For any inefficient DMUs, the DEA will also return the weights, which represent a combination of efficient DMUs that would produce the same output as the inefficient DMU for smaller input.

Methodology:
This research will use the Home Mortgage Disclosure Act (HMDA) dataset in 2021, which contains information about mortgage applications and loan originations that lenders are required to report under the requirements of the Act. The data includes relevant information on loan applications with 100 data fields and around 23,300,000 records across the whole country. One of the challenges of this research is to determine the proper application of the DEA in the loan decision-making process since the variables are not correlated with mortgage approvals in the same direction. For example, income is positively correlated to loan decision outcome while debt to income ratio is negatively correlated. Thus, in this research, I will focus on interpreting these results from the DEA optimization model for loan applications using four financial variables which can be justified: the loan amount requested, the income, the debt-to-income ratio, and the property value as inputs and outputs. To construct the DEA model, I will first find the correlation between the chosen variables to determine the inputs and outputs. Based on the model-generated weights and efficiency score, I will determine the recommended inputs for rejected applications to be able to have their loan accepted. Furthermore, as the analysis compares the relative efficiency of loan application units and other instances where they have similar application profiles, this can show unfairness in the decision-making process if an inconsistency is detected. An inconsistency is determined if a loan application is accepted while not having an efficiency score higher than the one that is rejected. In other words, this application has similar financial profiles to the others but one got accepted while the other did not. 

Anticipated Outcome: 
Through the research, we hope to build a model implementing DEA methodology and we will examine if the results from the model are suitable and can be used to identify the lack of fairness in this process and explain the decisions made by ML systems for mortgage applications.

## D. References

[1] Cho, S. H., & Shin, K. (2023). Feature-weighted counterfactual-based explanation for 
bankruptcy prediction. Expert Systems with Applications, 216, 119390. https://doi.org/10.1016/j.eswa.2022.119390

[2] Carvalho, D. V., Pereira, E. M., & Cardoso, J. S. (2019). Machine learning interpretability: A survey on methods and metrics. Electronics, 8(8), 832. https://doi.org/10.3390/electronics8080832

[3] Khoshnevisan, L., & Vaziri, M. (2021). Counterfactual analysis in benchmarking. Journal of Business Research, 130, 418-429. https://doi.org/10.1016/j.jbusres.2021.01.014

[4] Molnar, C. (2019). Interpretable machine learning: A guide for making black box models explainable. Retrieved from https://christophm.github.io/interpretable-ml-book/counterfactual.html

[5] Luo, X., Xu, L., & Zhang, Y. (2022). Ensemble clustering with local randomization. Data Mining and Knowledge Discovery. Advance online publication. https://doi.org/10.1007/s10618-022-00831-6

[6] Emrouznejad, A., & Yang, G. (2010). Data envelopment analysis: History, models, and interpretations. Communications in Information Science and Management, 8(1), 1-13. https://doi.org/10.12733/cism.v8i1.1

[7] ​​Banciu, M. (2008), "Data Envelopment Analysis (DEA)", unpublished class notes.


