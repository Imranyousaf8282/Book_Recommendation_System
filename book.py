import streamlit as st
import numpy as np
import pickle

def Books_Recommend_System(book_name):
    if book_name not in pt.index:
        st.error(f"Book '{book_name}' not found in the dataset.")
        return []

    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]
    
    data = []
    for i in similar_items:
        temp_df = books[books["Book-Title"] == pt.index[i[0]]]
        if temp_df.empty:
            continue
        item = []
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))
        data.append(item)
    
    return data

st.title("Book Recommender System")

try:
    books = pickle.load(open('book_l.pkl', 'rb'))
    pt = pickle.load(open('pt.pkl', 'rb'))
    similarity_score = pickle.load(open('similarity.pkl', 'rb'))
    popular = pickle.load(open('popular.pkl', 'rb'))
except FileNotFoundError as e:
    st.error(f"Error: {e}")
    st.stop()

book_list = pt.index.values
selected_books = st.selectbox("Select books", book_list)

if st.button("Recommend"):
    if selected_books:
        Recom_books = Books_Recommend_System(selected_books)
        if Recom_books:
            for book in Recom_books:
                st.write(f"**Title:** {book[0]}")
                st.write(f"**Author:** {book[1]}")
                st.image(book[2])
        else:
            st.write("No recommendations available.")
    else:
        st.error("Please select a book to get recommendations.")
