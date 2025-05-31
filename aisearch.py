import yagooglesearch
import llama
import re

def complete_search(query):
    queryrevised = llama.askLlama(
        "You are made to refine search queries",
        f"Find me the cheapest widely-known option for buying a product that is similar to this description: {query}"
    )
    client = yagooglesearch.SearchClient(
        queryrevised,
        tbs="li:1",
        max_search_result_urls_to_return=20,
        http_429_cool_off_time_in_minutes=45,
        http_429_cool_off_factor=1.5,
        verbosity=5,
        verbose_output=True,
    )
    client.assign_random_user_agent()
    urls = client.search()

    output = ""
    for url in urls:
        output += f'{url["rank"]} - {url["title"]}\n'
        output += f'{url["description"]}\n'
        output += f'{url["url"]}\n'
        output += "-" * 80 + "\n"

    matches = []
    while not matches:
        gptout = llama.askLlama(
            "You are an expert in web searching. You have information from 20 sites, and you should keep those together to find the product at hand for the cheapest from a well-known source. Once you have carefully considered all sources, display your final number in square brackets (e.g. [45]). Do NOT use any formatting in your answer. Your answer should just be an integer.",
            f"Product: {query} \nSearches:\n{output}"
        )
        print(gptout)
        matches = re.findall(r'\[\d+\]', gptout)

    return matches[0].replace("[","").replace("]", "")