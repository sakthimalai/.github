import plot
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict
import plot

def retrieve_data(input_date):
    cursor = None
    if len(input_date) == 4:  # If input is a year
        cursor =plot.collection.find({"date": {"$regex": f"^{input_date}-.{{3}}"}})
    elif len(input_date) == 7:  # If input is a year-month
        cursor = plot.collection.find({"date": {"$regex": f"^{input_date}-.*"}})
    elif len(input_date) == 10:  # If input is a full date
        cursor = plot.collection.find({"date": input_date})
    else:
        st.warning("Invalid input format. Please provide input in the format 'YYYY', 'YYYY-MM', or 'YYYY-MM-DD'")
        return None
    
    if cursor:
        yearly_counts = defaultdict(int)
        monthly_counts = defaultdict(int)
        for document in cursor:
            date = datetime.strptime(document['date'], "%Y-%m-%d")
            year = date.year
            month = date.month
            lumpy_skin_count = document['lumpy_skin_count']
            mouth_disease_count = document['mouth_disease_count']

            # Aggregate yearly counts
            yearly_counts[year] += lumpy_skin_count + mouth_disease_count

            # Aggregate monthly counts
            monthly_counts[(year, month)] += lumpy_skin_count + mouth_disease_count

        return yearly_counts, monthly_counts
    else:
        return None, None


def plot_yearly_counts(yearly_counts):
    if not yearly_counts:
        st.warning("No data found for the given input")
        return
    plt.figure(figsize=(10, 6))
    bars = plt.bar(yearly_counts.keys(), yearly_counts.values(), color='skyblue')
    plt.title('Total Disease Counts by Year')
    plt.xlabel('Year')
    plt.ylabel('Total Count')
    plt.xticks(list(yearly_counts.keys()))
    plt.grid(axis='y')
    
    # Add annotations to each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height}', ha='center', va='bottom')

    plt.tight_layout()
    st.pyplot()
    st.set_option('deprecation.showPyplotGlobalUse', False)


def plot_monthly_counts(monthly_counts):
    if not monthly_counts:
        st.warning("No data found for the given input")
        return
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    plt.figure(figsize=(10, 6))
    for year in sorted(set(year for year, month in monthly_counts.keys())):
        monthly_data = [monthly_counts[(year, month)] for month in range(1, 13)]
        plt.plot(months, monthly_data, label=year)
    plt.title('Total Disease Counts by Month')
    plt.xlabel('Month')
    plt.ylabel('Total Count')
    plt.legend(title='Year')
    plt.grid(True)
    plt.tight_layout()
    st.pyplot()
    st.set_option('deprecation.showPyplotGlobalUse', False)

    
def additional_section():
    st.markdown("<h1 style='text-align: left; color: #49f222; font-size: 46px; font-weight:600;'>Analyse By Time</h1>", unsafe_allow_html=True)
    # Sidebar
    input_date = st.text_input("Enter a year (YYYY), year-month (YYYY-MM), or full date (YYYY-MM-DD):")
    
    # Retrieve and plot data based on user input
    if st.button("Plot Yearly Counts"):
        yearly_counts, _ = retrieve_data(input_date)
        plot_yearly_counts(yearly_counts)
    
    if st.button("Plot Monthly Counts"):
        _,monthly_counts = retrieve_data(input_date)
        plot_monthly_counts(monthly_counts)
