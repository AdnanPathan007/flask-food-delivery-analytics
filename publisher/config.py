import os

path = os.path.join(
    os.getcwd(),
    "jsonkey.json"
)
credentials_path = path
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

topic_path = "projects/project-65b029a2-02f6-40de-986/topics/food-delivery-app-topic"

