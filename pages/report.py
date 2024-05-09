import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
if "shared" not in st.session_state:
   st.session_state["shared"] = True

from pages.Utils.helper_code import load_data
data = load_data()  # data import: ✅
# 1. Customer Satisfaction Score (CSS)
customer_satisfaction_score = data['CustomerSatisfaction'].mean()

# 2. Renewal Rate
total_customers = len(data)
renewed_customers = data[data['RenewalStatus'] == 'Renewed']['RenewalStatus'].count()
renewal_rate = (renewed_customers / total_customers) * 100

# 3. Average Time to Resolution
average_time_to_resolution = data['TimeToResolutionDays'].mean()

# 4. Claims Ratio
total_claims_made = data['ClaimsMade'].sum()
total_premiums_collected = data['PremiumMonthly'].sum()
claims_ratio = total_claims_made / total_premiums_collected

# 5. Customer Churn Rate
churned_customers = total_customers - renewed_customers
customer_churn_rate = (churned_customers / total_customers) * 100


st.title("Improving Operational Efficiency")

col1, col2, col3, col4, col5= st.columns(5, gap='small')
with col1:
    st.info("Renewal Rate", icon="📌")
    st.metric(label="ratio", value=f"{renewal_rate:,.2f}")    
with col2:
    st.info("Claims Ratio", icon="📌")
    st.metric(label="ratio", value=f"{claims_ratio:,.2f}")    
with col3:
    st.info("Churn Rate", icon="📌")
    st.metric(label="ratio", value=f"{customer_churn_rate:,.2f}")
with col4:
    st.info("Resolution", icon="📌")
    st.metric(label="Avg. in days", value=f"{average_time_to_resolution:,.2f}")    
with col5:
    st.info("Satisfy Score", icon="📌")
    st.metric(label="mean", value=f"{customer_satisfaction_score:,.2f}")

          
st.markdown("""---""")
st.write("Improving operational efficiency can be achieved by identifying areas where processes can be streamlined, resources can be optimized, and decision-making can be made more data-driven. Let's ")

st.markdown("""---""")
tab1, tab2, tab3 = st.tabs(["Customer Interactions & Satisfaction", "Claims Processing & Risk Management ", "Financials & Services Optimization"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        communication_method_counts = data['CommunicationMeans'].value_counts()
        fig = px.pie(names=communication_method_counts.index, values=communication_method_counts.values, title="Proportion of Communication Method", hole=0.4)
        fig.update_layout(font_family="Century Gothic", title_font_family="Century Gothic", title={
                    'x':0.5,
                    'xanchor': 'center'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(data, x='PolicyType',y='CustomerID',title="Popularity of PolicyType", color='Gender')
        fig.update_layout(font_family="Century Gothic", title_font_family="Century Gothic",title={
            'x':0.5,
            'xanchor': 'center'},yaxis_title="Total Customers", xaxis_title="Month",barmode='group',xaxis = {"categoryorder":"total descending", 'type': 'category'})
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""---""")
    policy = st.selectbox("Select Policy Type:", data['PolicyType'].unique())
    policy_data = data[data.PolicyType==policy]
    st.markdown("""---""")
    col_i, col_j = st.columns(2)
    with col_i:
         communication_counts = policy_data['CommunicationMeans'].value_counts()
         fig = px.bar(communication_counts, x=communication_counts,
                    labels={'x': 'Communication Method', 'y': 'Number of Customers'},
                    title='Communication Method per PolicyType')
         
         st.plotly_chart(fig, use_container_width=True)
    
    with col_j:
        high_satisfaction_customers = policy_data[policy_data['CustomerSatisfaction'] >= 4]
        feedback_counts = high_satisfaction_customers['ServiceNature'].value_counts()
        fig = px.pie(names=feedback_counts.index, values=feedback_counts.values, title="Common Services with High Satisfaction Scores")
        fig.update_layout(font_family="Century Gothic", title_font_family="Century Gothic", title={
                        'x':0.5,
                        'xanchor': 'center'})
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("""---""")
    region_contact_frequency = policy_data.groupby('Region')['CustomerServiceFrequency'].mean().reset_index()

    fig = px.bar(region_contact_frequency, x='Region', y='CustomerServiceFrequency', 
            title='Frequency of Customer Service Contact by Region',
            labels={'CustomerServiceFrequency': 'Average Customer Service Frequency'})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""---""")
    st.subheader("Recommendation")
    st.write("""* Tailoring marketing and retention strategies based on regional premium variations.
* Optimizing communication channels based on the most common communication method used by customers.
* Allocating resources for customer support teams based on the frequency of customer service contact by region.""")
    
with tab2:
    claims_by_policy_type = data.groupby('PolicyType')['ClaimsMade'].sum().reset_index()
    max_claims_policy_type = claims_by_policy_type.loc[claims_by_policy_type['ClaimsMade'].idxmax()]

    fig = px.bar(claims_by_policy_type, x='PolicyType', y='ClaimsMade',
            title='Policy Type with the Highest Number of Claims Made',
            labels={'ClaimsMade': 'Number of Claims Made'})

    fig.add_annotation(x=max_claims_policy_type['PolicyType'], y=max_claims_policy_type['ClaimsMade'],
                text="Highest", showarrow=True, arrowhead=1)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""---""")
    policy = st.selectbox("Select Policy Type:", data['PolicyType'].unique(), key='mine3')
    policy_data = data[data.PolicyType==policy]
    col_i, col_j = st.columns(2)

    with col_j:
        claims_by_age_and_reason = policy_data.groupby(['AgeGroup', 'ClaimReasons']).size().reset_index(name='Count')
        pivot_table = claims_by_age_and_reason.pivot(index='AgeGroup', columns='ClaimReasons', values='Count').fillna(0)

        fig = px.bar(pivot_table, x=pivot_table.index, y=pivot_table.columns, 
             title='Reasons for Claims Among Different Age Groups',
             labels={'x': 'Age Group', 'y': 'Number of Claims', 'color': 'Claim Reason'},
             barmode='stack')
        st.plotly_chart(fig, use_container_width=True)

        avg_time_to_resolution = policy_data.groupby('Region')['TimeToResolutionDays'].mean().reset_index()
        
        st.markdown("""---""")
        
        fig = px.bar(avg_time_to_resolution, x='Region', y='TimeToResolutionDays',
                title='Average Time to Resolution for Claims per Region',
                labels={'Region': 'Region', 'TimeToResolutionDays': 'Average Time to Resolution (Days)'})

        st.plotly_chart(fig, use_container_width=True)
    
    with col_i:
        claim_rejected_counts = policy_data['ClaimsRejected'].value_counts().reset_index()
        claim_rejected_counts.columns = ['ClaimsRejected', 'Number of Customers']

        total_customers = claim_rejected_counts['Number of Customers'].sum()
        claim_rejected_counts['Percentage of Total'] = (claim_rejected_counts['Number of Customers'] / total_customers) * 100

        fig = px.bar(claim_rejected_counts, x='ClaimsRejected', y='Percentage of Total',
                    title='How Many Times can a Claim be Rejected?',
                    labels={'ClaimsRejected': 'Claims Reject', 'Percentage of Total': 'Percentage of Total Customers'},
                    hover_data={'Percentage of Total': ':.2f'})
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""---""")
        
        last_year_data = policy_data[policy_data['PolicyStartYear'] == policy_data['PolicyStartYear'].max()]

        fraudulent_claims_last_year = last_year_data['FraudulentClaims'].sum()

        fraudulent_claims_df = pd.DataFrame({'Category': ['Fraudulent Claims', 'Non-Fraudulent Claims'],
                                            'Count': [fraudulent_claims_last_year, len(last_year_data) - fraudulent_claims_last_year]})

        fig = px.pie(fraudulent_claims_df, values='Count', names='Category',
                    title='Fraudulent Claims Recorded Last Year',
                    labels={'Count': 'Count', 'Category': 'Category'},
                    hole=0.3)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""---""")
    
    st.subheader("Recommendation")
    st.write("""* Understanding the common reasons for claims among different age groups can help in tailoring insurance products and services to better meet the needs of specific demographics. For example, if a particular age group frequently claims for health-related issues, offering specialized health insurance plans or wellness 
             programs can improve customer satisfaction and loyalty.
* Ivestigating customers with a high number of rejected claims can uncover potential fraud or misinterpretation of policy terms. Implementing stricter underwriting criteria, enhancing fraud detection systems, or providing targeted education to 
             customers on policy coverage can reduce the incidence of rejected claims and minimize losses. 
* Identifying the number of fraudulent claims recorded last year can help in refining fraud detection algorithms and improving claims investigation processes. Investing in advanced analytics tools or collaborating with industry partners to share fraud 
             intelligence can strengthen fraud prevention measures and minimize financial losses.""")

with tab3:
    # Dropdown for policy type with default selection as "All"
    policy = st.selectbox("Select Policy Type:", data['PolicyType'].unique(), key='mine')
    policy_data = data[data.PolicyType==policy]

    # Calculate the average monthly premium for each region and cover details
    average_premium_by_region_cover = policy_data.groupby(['Region', 'CoverDetails'])['PremiumMonthly'].mean().reset_index()

    # Create a grouped bar chart to visualize the average monthly premium for each region and cover details
    fig = px.bar(average_premium_by_region_cover, x='Region', y='PremiumMonthly', color='CoverDetails',
                title='Avg. Monthly Premium  by CoverDetails',
                labels={'PremiumMonthly': 'Average Monthly Premium ($)', 'CoverDetails': 'Cover Details'})
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""---""")
    col_i, col_j = st.columns(2)
    with col_i:
         # Group data by premium payment frequency and calculate the total missed payments
        missed_payments_by_frequency = policy_data.groupby('PremiumPaymentFrequency')['MissedPayments'].sum()

        # Extract missed payments for customers paying premiums annually
        missed_payments_annually = missed_payments_by_frequency.get('Annually', 0)

        # Calculate missed payments for other premium payment frequencies
        missed_payments_other = missed_payments_by_frequency.drop('Annually')

        # Create a dataframe for visualization
        missed_payments_df = pd.DataFrame({'Frequency': missed_payments_other.index.tolist() + ['Annually'],
                                        'Missed Payments': missed_payments_other.tolist() + [missed_payments_annually]})

        # Create a donut chart to visualize the proportion of missed payments
        fig = px.pie(missed_payments_df, names='Frequency', values='Missed Payments',
                    title='Proportion of Missed Payments by Premium Payment Frequency',
                    hole=0.4,
                    color_discrete_sequence=px.colors.sequential.thermal)

# Show the plot
        st.plotly_chart(fig, use_container_width=True)
    
    with col_j:
        # Group data by policy type and calculate the average discount for customers with and without claims
        discounts_by_policy_type = policy_data.groupby(['PolicyType', 'ClaimsMade'])['PolicyDiscounts'].mean().reset_index()

        # Filter data for customers with no claims
        no_claims_data = discounts_by_policy_type[discounts_by_policy_type['ClaimsMade'] == 0]

        # Filter data for customers with claims
        claims_data = discounts_by_policy_type[discounts_by_policy_type['ClaimsMade'] > 0]

        # Merge the two datasets to ensure consistency in policy types
        merged_data = pd.merge(no_claims_data, claims_data, on='PolicyType', suffixes=('_no_claims', '_claims'))

        # Rename columns for clarity
        merged_data.rename(columns={'PolicyDiscounts_no_claims': 'No Claims', 'PolicyDiscounts_claims': 'With Claims'}, inplace=True)

        # Melt the dataframe to create a long-form dataframe for plotting
        melted_data = pd.melt(merged_data, id_vars='PolicyType', value_vars=['No Claims', 'With Claims'], var_name='Claims', value_name='Average Discount')

        # Create a grouped bar chart to visualize discounts offered to customers with and without claims
        fig = px.bar(melted_data, x='PolicyType', y='Average Discount', color='Claims', barmode='group',
                    title='Discounts Offered to Customers with and without Claims by Policy Type',
                    labels={'Average Discount': 'Average Discount (%)', 'Claims': 'Claims'})

        st.plotly_chart(fig, use_container_width=True)
    st.markdown("""---""")
    
    fig = px.scatter(data[data.PolicyType==policy],
                    x='PolicyDurationMonths',
                    y='PremiumPaid',
                    color='TimeToResolutionDays',
                    title="Premium against Policy Duration in Months",
                    color_continuous_scale="Plasma"
                            )
    fig.update_layout(font_family="Century Gothic"
      , title_font_family="Century Gothic",title={
               'x':0.5,
               'xanchor': 'center'})
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""---""")

    # Calculate the average premium payments for each vehicle type
    average_premium_by_vehicle_type = policy_data.groupby('VehicleType')['PremiumMonthly'].mean().reset_index()

    # Sort the data by average premium payments in descending order
    average_premium_by_vehicle_type = average_premium_by_vehicle_type.sort_values(by='PremiumMonthly', ascending=False)

    # Create a bar chart to visualize the average premium payments for each vehicle type
    fig = px.bar(average_premium_by_vehicle_type, x='VehicleType', y='PremiumMonthly',
                title='Average Premium Payments by Vehicle Type',
                labels={'PremiumMonthly': 'Average Premium Payments ($)', 'VehicleType': 'Vehicle Type'})

    st.plotly_chart(fig, use_container_width=True)

    
    st.subheader("Recommendation")
    st.write("""* the variation in premium amounts across different regions can help in targeted marketing and resource allocation strategies. For regions with higher average premiums, more resources can be 
             allocated for customer acquisition and retention..
* discounts offered to customers who have not made any claims can help in designing targeted retention strategies. Offering personalized discounts based on customer behavior can 
             improve customer satisfaction and retention rates.
* Understanding which vehicle types are associated with the highest premium payments can inform pricing strategies and risk assessment models. Adjusting premiums based on vehicle type characteristics, such as 
             safety ratings or theft rates, can ensure fair pricing and optimize profitability.""")

         
        