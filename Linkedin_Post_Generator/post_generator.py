from few_shot import FewShots
from few_shot import FewShots
from llm_helper import llm
from langchain.prompts import PromptTemplate

fs = FewShots("data/processed_posts.json")
def get_prompt(language,length,tag):
    posts = fs.required_df(language,length,tag)

    prompt = """
        You are given of 3 attributes of linkedin post. These attributes are namely language,length and
        tag of a post. Your goal is generate a post having these three attributes.
        Here are some instructions:
        1 - Length refers to the number of lines in a post
        2 - Length is small if number of lines in a post is in the range - (0-5) , medium if in a range -
        (5-10) and large if a range greater then 10
        3 - Language is the language of the post
        4 - Tag refers to the topic of the post
        5 - Output only the post you generated and nothing else
        6 - Hinglish is a mix of hindi and english but written in roman script
        Here are the attributes of a post : {language},{length},{tag}
        """

    if len(posts)>0:
        prompt+= "\nUse the writing style of below posts"
        for i,post in enumerate(posts):
            post_text = post["text"]
            prompt+=f"\n\nExample {i+1} : {post_text}"
    pt = PromptTemplate.from_template(prompt)
    return pt

def post_generator(language,length,tag):
    pt= get_prompt(language,length,tag)
    chain = pt | llm
    res = chain.invoke(input = {"language" : language,"length" : length, "tag" : tag})
    return res.content

