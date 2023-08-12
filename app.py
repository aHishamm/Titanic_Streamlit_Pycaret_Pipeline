import pandas as pd 
import numpy as np 
from pycaret.classification import ClassificationExperiment
import streamlit as st
import preprocess as prp
#widescreen view in streamlit 
st.set_page_config(layout='wide') 
#reading the dataframes 
train_df = pd.read_csv('train.csv') 
test_df = pd.read_csv('test.csv') 
#viewing the train_df 
st.subheader("Original Dataframe")
st.dataframe(train_df) 
#preprocessing the train_df
of_title_list=['Mrs', 'Mr', 'Master', 'Miss', 'Major', 'Rev',
                    'Dr', 'Ms', 'Mlle','Col', 'Capt', 'Mme', 'Countess',
                    'Don', 'Jonkheer']         
names = list(train_df['Name'])
title_list = [] 
new_list = [] 
for i in names: 
    title_list.append(i.split()[1][:-1])
train_df['Name'] = title_list
train_df.rename(columns = {'Name':'Title'}, inplace = True,errors='ignore')
filtered_train_df = train_df[train_df['Title'].isin(of_title_list)]
#Applying the function to the dataframe 
filtered_train_df['Title'] = filtered_train_df.apply(prp.replace_titles,axis=1)
filtered_train_df['Cabin'] = filtered_train_df['Cabin'].fillna('U')
cabin_list = list(filtered_train_df['Cabin'])
for i in cabin_list: 
    new_list.append(list(i)[0])
filtered_train_df['Cabin'] = new_list
filtered_train_df['Family_Size']=filtered_train_df['SibSp']+filtered_train_df['Parch']
filtered_train_df['Age*Class']=filtered_train_df['Age']*filtered_train_df['Pclass']
filtered_train_df['Fare_Per_Person']=filtered_train_df['Fare']/(filtered_train_df['Family_Size']+1)
filtered_train_df.drop(columns=['PassengerId','Ticket'], inplace=True,errors='ignore')
#viewing the post processed dataframe 
st.subheader("Processed Dataframe")
st.dataframe(filtered_train_df)
s = ClassificationExperiment() 
s.setup(filtered_train_df,target='Survived',session_id=123)
best = s.compare_models()
results = s.pull() 
st.subheader('ML Results Table') 
st.dataframe(results)
s.plot_model(best, plot = 'auc',display_format='streamlit')
s.plot_model(best, plot = 'pr',display_format='streamlit')
s.plot_model(best, plot = 'confusion_matrix',display_format='streamlit')
s.plot_model(best, plot = 'class_report',display_format='streamlit')
