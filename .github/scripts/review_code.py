import openai
import os
import requests

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PR_NUMBER = os.getenv("PR_NUMBER")
REPO = os.getenv("GITHUB_REPOSITORY")

# Read PR diff from file
with open("pr_diff.txt", "r") as file:
    pr_diff = file.read()

# Send PR diff to OpenAI for review
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an expert code reviewer. Provide a structured review of the following code changes."},
        {"role": "user", "content": f"Review this code:\n\n{pr_diff}"}
    ]
)

# Extract AI-generated feedback
feedback = response["choices"][0]["message"]["content"]

# Post feedback as a PR comment
comment_url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

payload = {"body": feedback}

requests.post(comment_url, json=payload, headers=headers)
