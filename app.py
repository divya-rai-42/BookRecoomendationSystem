from flask import Flask, render_template, request
import pickle
import numpy as np

# reading all the pickle files
top_books = pickle.load(open('top_books.pkl','rb'))
pivot_t = pickle.load(open('pivot_t.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_value = pickle.load(open('similarity_value.pkl','rb'))

app = Flask(__name__)

# returning values to the index.html page for showing top 50 books. Popularity based recommendation technique has been used for recommending top 50 books
@app.route('/')
def index():
    return render_template('index.html',
                          book_name = list(top_books['Book-Title'].values),
                          author_name = list(top_books['Book-Author'].values),
                          book_image = list(top_books['Image-URL-M'].values),
                          rate_count = list(top_books['rating_count'].values),
                          rating = list(top_books['avg_rating'].values)
                          )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['post'])
#function to recommend a book using collaborative filtering technique
def recommend():
    user_input = request.form.get('user_input')  
    data_list = [] # list to store the recommendations with the required deatils like book-title, book-author, etc
    #fetching the index where book_name exist in pivot tabe
    arr = np.where(pivot_t.index==user_input) 
  
    if len(arr[0])>0: #checking whether given book is present or not
        index = arr[0][0] # index of the book fetched
        #extracting similarity values of the given book with the rest of the books and sorting it in descending order
        similar_items = sorted(list(enumerate(similarity_value[index])),key=lambda x:x[1],reverse=True)[1:6] 
        #Note that only indice 1 to 6 have been chose and not 0 because the 0th index will contain the given book itself
        
        # adding recommendations in data_list
        for i in similar_items:
            item = [] #this list will contain all details of a single recommended book
            temp_df = books[books['Book-Title'] == pivot_t.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)) #adding book title to item
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)) #adding book-author to item
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values)) #adding image url to item
            data_list.append(item) #appending item to the data_list
    
    print(data_list)
    return render_template('recommend.html',data=data_list)

if __name__ == '__main__':
    app.run(debug=True)