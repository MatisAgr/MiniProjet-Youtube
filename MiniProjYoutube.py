import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import json

files_and_countries = [
    ('dataset/FRvideos.csv', 'FR'),
    ('dataset/USvideos.csv', 'US'),
    ('dataset/CAvideos.csv', 'CA'),
    ('dataset/DEvideos.csv', 'DE'),
    ('dataset/GBvideos.csv', 'GB'),
    ('dataset/INvideos.csv', 'IN'),
    ('dataset/JPvideos.csv', 'JP'),
    ('dataset/KRvideos.csv', 'KR'),
    ('dataset/MXvideos.csv', 'MX'),
    ('dataset/RUvideos.csv', 'RU')
]

dataframes = []


# 1. En utilisant une boucle, chargez les 5 fichiers, 
# •	Ajoutez une nouvelle colonne “country” qui contient le code du pays : par exemple pour  France le code « FR »
# •	Indiquez la colonne “video_id” comme index
# A partir de cette question, vous travaillez sur le df concaténée
for file, country in files_and_countries:
    df = pd.read_csv(file, index_col='video_id', encoding='ISO-8859-1')
    df['country'] = country
    dataframes.append(df)

merged_df = pd.concat(dataframes)

# 2. Supprimez la colonne “thumbnail_link”, Reformatter la colonne “trending_date” (%y%d%m) et la colonne “publish_time” (%Y%m%d%T%M%S)
merged_df = merged_df.drop(columns=['thumbnail_link'])
merged_df['trending_date'] = pd.to_datetime(merged_df['trending_date'], format='%y.%d.%m', dayfirst=True)
merged_df['publish_time'] = pd.to_datetime(merged_df['publish_time'], format='%Y-%m-%dT%H:%M:%S.%fZ')

#3.	Supprimez les lignes en doublons et jugez de la pertinence de suppression des données manquantes et des valeurs aberrantes ; s’il y en a
merged_df = merged_df.drop_duplicates()

#4.	Calculez le nombre total des videos et le nombre de video unique
totalvideo = merged_df.shape[0]
totalview = merged_df['views'].sum()
uniquevideo = merged_df.index.nunique()

print ("total videos: ", totalvideo)
print ("total views: ", totalview)
print ("unique videos: ", uniquevideo)

# 5. Trouvez le top 5 des vidéos qui ont eu le plus de Views dans l’absolue, par pays et réaliser le graphe correspondant 
top5MostView = merged_df.groupby('country').apply(lambda x: x.nlargest(5, 'views'))
# print ("top 5 videos by views: ", top5MostView)
top5MostView = top5MostView.drop_duplicates()
sns.barplot(x='views', y='title', data=top5MostView, hue='country')
plt.show()

# 6.Trouvez le top 5 des vidéos qui ont eu le plus de Likes dans l’absolue, par pays et réaliser le graphe correspondant
top5MostLike = merged_df.groupby('country').apply(lambda x: x.nlargest(5, 'likes'))
# print ("top 5 videos by likes: ", top5MostLike)
top5MostLike = top5MostLike.drop_duplicates()
sns.barplot(x='likes', y='title', data=top5MostLike, hue='country')
plt.show()

#7.	Trouvez le top 5 des vidéos qui ont eu le plus de nb de comment dans l’absolue, par pays et réaliser le graphe correspondant
top5MostComment = merged_df.groupby('country').apply(lambda x: x.nlargest(5, 'comment_count'))
# print ("top 5 videos by comment count: ", top5MostComment)
top5MostComment = top5MostComment.drop_duplicates()
sns.barplot(x='comment_count', y='title', data=top5MostComment, hue='country')
plt.show()

#8.	Affichez avec un bar chart le top 10 channel en termes de période de trending (nom de channel  en axe des X, nombre de jour trending en Y)
top10Channel = merged_df.groupby('channel_title').apply(lambda x: x['trending_date'].nunique())
top10Channel = top10Channel.nlargest(10)
top10Channel.plot(kind='bar')
plt.show()

# 9. Ajouter une nouvelle colonne qui contiendra les noms de catégories en utilisant les json (“categories_map_CodePays”) fournie dans le dossier (avec les csv)
# {country code}_category_id.json

json_files = []
categories = []

for _, country in files_and_countries:
    json_files.append(f'dataset/{country}_category_id.json')
    
for file in json_files:
    with open(file, 'r') as f:
        data = json.load(f)
        categories.append(data)
    

