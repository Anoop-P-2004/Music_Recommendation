from flask import Flask,request, render_template
import pickle

with open('df.pkl', 'rb') as file:
    df= pickle.load(file)
with open('similarity.pkl', 'rb') as file:
    similarity= pickle.load(file)

def recommendation(song_df):
    index = df[df['song'] == song_df].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
    songs = []
    for m_id in distances[1:6]:
        songs.append(df.iloc[m_id[0]].song)
    return songs

app=Flask(__name__)

@app.route('/')
def index():
    song_list=df["song"].sort_values().tolist()
    return render_template('index.html',songs=song_list)

@app.route('/prediction',methods=["POST"])
def prediction():
    str=request.form.get('songs')
    rec_songs=recommendation(str)
    song_list=df["song"].sort_values().tolist()
    return render_template('result.html',rec_songs=rec_songs,songs=song_list,selected_song=str)
if __name__ == '__main__':
    app.run(debug=True)
