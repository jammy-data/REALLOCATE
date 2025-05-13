# visualization_utils.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def create_barplot(data):
    """
    Creates a bar plot from a list of dictionaries with date and value using Matplotlib.
    
    Args:
    data (list): A list of dictionaries where keys are dates and values are integers.
                 Example: [{"2023-01-31": 52}, {"2023-04-30": 93}, ...]
    
    Returns:
    None: Displays the bar plot using Streamlit.
    """
    
    # Convert list of dictionaries to a DataFrame
    data_tuples = [(list(item.keys())[0], list(item.values())[0]) for item in data]
    df = pd.DataFrame(data_tuples, columns=['Date', 'Value'])
    
    # Convert 'Date' column to datetime for proper handling
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    
    # Set 'Date' as the index
    df.set_index('Date', inplace=True)

    # Create a bar plot
    plt.figure(figsize=(10, 6))
    plt.bar(df.index.strftime('%Y-%m-%d'), df['Value'], color='blue', width=0.1)
    plt.text(0, df['Value'][0]/(1.5), 'Before\nIntervention', ha='center', va='top', rotation=90, color="white", fontweight='bold')
    plt.text(1, df['Value'][1]/(1.5), 'After\nIntervention', ha='center', va='top', rotation=90, color="white", fontweight='bold')

    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Value')
    # plt.title('Bar Plot of Date vs. Value')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    # plt.legend()
    
    # Show the plot in the Streamlit app
    st.pyplot(plt)

    # # Optional: Display the DataFrame for reference
    # st.write("Bar Plot of Date vs. Value")
    # st.dataframe(df)


def create_linechart(data, highlight_start, highlight_end):
    # Convert the list of dictionaries to a DataFrame
    # dates = []
    # values = []
    
    # for entry in data:
    #     for date, value in entry.items():
    #         dates.append(date)
    #         values.append(value)

    # Convert list of dictionaries to a DataFrame
    data_tuples = [(list(item.keys())[0], list(item.values())[0]) for item in data]
    df = pd.DataFrame(data_tuples, columns=['Date', 'Value'])
    
    # Convert 'Date' column to datetime for proper handling
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

    df.set_index('Date', inplace=True)
    
    # Create the line chart
    plt.figure(figsize=(10, 5))
    plt.plot(df.index.strftime('%Y-%m-%d'), df['Value'], marker='o', color='b', linestyle='-')

    # Highlight the area between two dates
    plt.fill_between(df.index.strftime('%Y-%m-%d'), df['Value'], where=(df.index >= highlight_start) & (df.index <= highlight_end), 
                 color='orange', alpha=0.5, label='Intervention Period')
    
    
    # Formatting the plot
    # plt.title('Line Chart of Values Over Time')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.xticks(rotation=45)  # Rotate date labels for better readability
    # Add a custom legend entry for the highlighted area
    # plt.fill_between([], [], color='orange', alpha=0.5, label='Intervention Period')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    st.pyplot(plt)
