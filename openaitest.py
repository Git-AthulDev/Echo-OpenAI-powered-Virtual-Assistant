import openai
from config import apikey

openai.api_key = apikey

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Write an email to my boss for resignation?",
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response)

'''
{
  "id": "cmpl-893gmc6UoCc9auVE8uTdr4wgCxgM7",
  "object": "text_completion",
  "created": 1697169824,
  "model": "text-davinci-003",
  "choices": [
    {
      "text": "\n\nSubject: Resignation\n\nDear [Name],\n\nI am writing to inform you of my resignation from my position as [Position] with [Company].\n\nMy last day of employment will be [Date].\n\nI appreciate the opportunities for growth and development that I have had while working here. I have enjoyed my time here and wish the company all the best in the future.\n\nPlease let me know if there is any additional information or paperwork I need to provide before my last day.\n\nSincerely,\n\n[Your Name]",
      "index": 0,
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 116,
    "total_tokens": 125
  }
}
'''