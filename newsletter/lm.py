from langchain.chat_models import ChatOpenAI
from openai.error import InvalidRequestError


def _call_llm(*args, model="gpt-3.5-turbo-16k", **kwargs):
    try:
        return ChatOpenAI(model=model, request_timeout=10).invoke(*args, **kwargs)
    except InvalidRequestError as err:
        if err.code == "context_length_exceeded" and "32k" not in model:
            return _call_llm(*args, model="gpt-4-32k", **kwargs)
        raise


def summarize_post(title, content):
    result = _call_llm(
        f"""{title}

{content}
---

Generate a bulleted list that summarizes the main points from the above article. Prioritize:
1. Reducing the mental burden of reading the summary.
2. Conciseness over grammatical correctness.
3. Ability for general audience to understand.
4. Write the summary as if a 5 year old was the reader.
Generate at most 3 bullet points.
Here is the bulleted list summary:
"""
    )
    return result.content


def summarize_abstract(title, content):
    result = _call_llm(
        f"""{title}

{content}
---

Generate a bulleted list that summarizes the above paper abstract.
There should be exactly 3 bullets describing:
1. The motivation & why its important
2. The method & how it works
3. The results & how well it works

The format of the summary must look like the following:
```
- *Motivation*: <description of motivation>
- *Method*: <description of method>
- *Results*: <description of results>
```

Here is the summary:
"""
    )
    return result.content


def summarize_comment(title, summary, comment):
    result = _call_llm(
        f"""**Title**: {title}

**Article Summary**:
{summary}

**Comment**:
{comment}

Write an extremely short (less than 5 words; no need for grammatically correct) info bite summarizing the comment:
"""
    )
    return result.content


def matches_filter(summary, filter):
    result = _call_llm(
        f"""**Article**: {summary}

We are looking for Articles that match the following **Filter**: {filter}

Does the above Article match the above Filter? The Answer should be Yes or No:
**Answer**:
"""
    )
    content = result.content.strip().lower()
    return content == "yes" or content not in ["yes", "no"]
