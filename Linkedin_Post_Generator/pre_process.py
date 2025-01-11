import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def process_text(raw_file_path, processed_file_path):
    posts_with_metadata = []

    with open(raw_file_path, encoding = "utf-8") as file:
        posts = json.load(file)
    for post in posts:
        metadata = extract_metadata(post)
        new_post = post | metadata
        posts_with_metadata.append(new_post)

    unified_tags = extract_unified_tags(posts_with_metadata)

    for post in posts_with_metadata:
        tags = list(post["tags"])
        new_tags = {unified_tags[tag] for tag in tags}
        post["tags"] = list(new_tags)

    with open(processed_file_path,encoding = 'utf-8',mode ="w") as outfile:
        json.dump(posts_with_metadata,outfile,indent=4)

def extract_unified_tags(posts):
    unique_tags = set()

    for post in posts:
        unique_tags.update(post["tags"])

    unique_tags_list = ",".join(unique_tags)

    template = """
        You are given a list of unique tags. Your goal is to unify the tags.
        Here are some examples of how to do it:
        1- Unify tags like "Motivation","Inspiration","Drive" into "Motivation"
        2 - Unify tags like"Job Seekers", "Job Hunting" into "Job Search"
        3 - Unify tags like "Personal Growth", "Personal Improvement","Self Improvement" into "Self Improvement"
        4 - "Scam Alert", "Job Scam" into "Scam"
        
        Here are some other instructions:
        1 - Output should be in a Json format with the following key value pairs : {{"Old Tag" : "Unified Tag"}}
        2 - Here "Old Tag" is tag which is to be unified and "Unified Tag" is the tag to which the "Old Tag" is mapped
        3 - "Unified Tag" should be in a titular case like "Motivation","Scam".
        4 - Return the output only in Jason format with no preamble
        
        Here is the list of Unique tags which is to be unified : {tags}
    """

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    res = chain.invoke(input = {"tags" : str(unique_tags_list)})
    json_parser = JsonOutputParser()
    res = json_parser.parse(res.content)
    return res


def extract_metadata(post):
    prompt_template = """
    You are given a linkedin post. Your job is to extract number of lines, language and tags of each post.
    Here are the things to remember:
    1 - Return only a JSON output with no preamble.
    2 - JSON output will have three keys : "count_of_lines","language","tags".
    3 - Tags should be a text array with a maximum of two strings.
    4 - Language should be english or hinglish (hinglish is hindi + english)
    5 - Don't consider names in post as means to predict the language key. Only consider non-name
        text for language prediction
    Here is the linkedin post to perform the above operations:
    {post}
            """

    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm
    res = chain.invoke(input = {"post" : post})
    json_output_parser = JsonOutputParser()
    res = json_output_parser.parse(res.content)
    return res




if __name__ == "__main__":
    process_text("data/raw_posts.json","data/processed_posts.json")
