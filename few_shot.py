import json
import pandas as pd



class FewShots:
    def __init__(self,processed_file_path):
        self.df = None
        self.unique_tags = None
        self.load_df(processed_file_path)

    def load_df(self,processed_file_path):
        with open(processed_file_path,encoding = "utf-8") as file:
            posts = json.load(file)
        self.df = pd.DataFrame(posts)
        self.df["length"] = self.df["count_of_lines"].apply(self.categorize_length)
        self.unique_tags = list(set(self.df["tags"].sum()))


    def categorize_length(self,length):
        if 0<length<=5:
            return "small"

        if 5<length<=10:
            return "medium"

        if length>10:
            return "long"

    def required_df(self,language,length,tag):
        df_filtered = self.df[(self.df["tags"].apply(lambda tags : tag in tags)) &
                              (self.df["language"] == language) &
                              (self.df["length"] == length)]
        return df_filtered.to_dict(orient = "records")

    def get_unique_tags(self):
        return self.unique_tags

if __name__ == "__main__":
    fs = FewShots("data/processed_posts.json")
    print(fs.get_unique_tags())