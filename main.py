import streamlit as st
import requests
import json
import pandas as pd

# Set up the title for the Streamlit app
st.title("Keyword Suggestor for Keyword Research")

# Text input for user to enter their keyword
keyword = st.text_input("Enter your keyword:")

# Function to make the initial API call and generate keyword suggestions
def api_call(keyword):
    keywords = [keyword]
    
    # Initial API call to get suggestions for the input keyword
    url = f"https://suggestqueries.google.com/complete/search?output=firefox&q={keyword}"
    response = requests.get(url, verify=False)
    
    try:
        suggestions = json.loads(response.text)
        for word in suggestions[1]:
            keywords.append(word)
    except Exception as e:
        st.error("Error fetching initial suggestions.")

    # Additional keywords from prefixes, suffixes, and numbers
    prefixes(keyword, keywords)
    suffixes(keyword, keywords)
    numbers(keyword, keywords)
    get_more(keyword, keywords)

    # Clean and display the keywords
    return clean_df(keywords, keyword)

# Function to add prefixes to the keyword
def prefixes(keyword, keywords):
    prefix_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'y', 'x', 'y', 'z', 'how', 'which', 'why', 'where', 'who', 'when', 'are', 'what']    
    for prefix in prefix_list:
        url = f"https://suggestqueries.google.com/complete/search?output=firefox&q={prefix} {keyword}"
        response = requests.get(url, verify=False)
        try:
            suggestions = json.loads(response.text)
            for suggestion in suggestions[1]:
                keywords.append(suggestion)
        except:
            continue

# Function to add suffixes to the keyword
def suffixes(keyword, keywords):
    suffix_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'y', 'x', 'y', 'z', 'like', 'for', 'without', 'with', 'versus', 'vs', 'to', 'near', 'except', 'has']
    for suffix in suffix_list:
        url = f"https://suggestqueries.google.com/complete/search?output=firefox&q={keyword} {suffix}"
        response = requests.get(url, verify=False)
        try:
            suggestions = json.loads(response.text)
            for suggestion in suggestions[1]:
                keywords.append(suggestion)
        except:
            continue

# Function to add numbers as suffixes to the keyword
def numbers(keyword, keywords):
    for num in range(10):
        url = f"https://suggestqueries.google.com/complete/search?output=firefox&q={keyword} {num}"
        response = requests.get(url, verify=False)
        try:
            suggestions = json.loads(response.text)
            for suggestion in suggestions[1]:
                keywords.append(suggestion)
        except:
            continue

# Function to get extended keywords
def get_more(keyword, keywords):
    for kw in keywords:
        url = f"https://suggestqueries.google.com/complete/search?output=firefox&q={kw}"
        response = requests.get(url, verify=False)
        try:
            suggestions = json.loads(response.text)
            for suggestion in suggestions[1]:
                keywords.append(suggestion)
            if len(keywords) >= 1000:
                break
        except:
            continue

# Function to clean the keywords and return as DataFrame
def clean_df(keywords, keyword):
    keywords = list(dict.fromkeys(keywords))
    filtered_keywords = [word for word in keywords if all(val in word for val in keyword.split())]
    df = pd.DataFrame(filtered_keywords, columns=['Keywords'])
    return df

# Button to trigger keyword suggestions
if st.button("Get Suggestions"):
    if keyword:
        suggestions_df = api_call(keyword)
        st.write("Suggested Keywords:")
        st.dataframe(suggestions_df)
        
        # Convert DataFrame to CSV and add download button
        csv = suggestions_df.to_csv(index=False)
        st.download_button("Download Keywords as CSV", data=csv, file_name=f"{keyword}-keywords.csv", mime="text/csv")
    else:
        st.warning("Please enter a keyword to get suggestions.")
