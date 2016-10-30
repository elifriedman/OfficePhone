
from watson_developer_cloud import AlchemyLanguageV1
import json

alchemy_language = AlchemyLanguageV1 (
    api_key="7f5df4ef1ed68a2f7749e238e4f38a5fba158922"
) 

s1 = "Hi, can I please schedule an appointment for next Thursday at 2:00?"
s2 = "Hi, can I please schedule an appointment for November 1st at 2:00?"

combined_operations = ['entity', 'keyword','concept', 'dates']
#print(json.dumps(alchemy_language.dates( html=s1, anchor_date='2016-10-30 00:00:00' ), indent=2))
#print(json.dumps(alchemy_language.dates( html=s2, anchor_date='2016-10-30 00:00:00' ), indent=2))
#print(json.dumps(alchemy_language.combined(text=s2, extract=combined_operations), indent=2))

response = alchemy_language.dates(
              text='Go there on October 3, 2015', show_source_text=True,
              anchor_date="2016-10-10 00:00:00"
           )
print(json.dumps(response, indent=2))

