from allennlp.predictors.predictor import Predictor

predictor= Predictor.from_path('https://storage.googleapis.com/allennlp-public-models/bidaf-elmo-model-2020.03.19.tar.gz')



# passage_1='There were 12 men who where on the first jury'
#
# result_1 = predictor.predict(passage=passage_1,question='How many men were on the first jury ?')
# print(result_1['best_span_str'])

passage_2 = '''Elon Reeve Musk ( born June 28, 1971) is a business magnate, industrial designer, and engineer.[3] He is the founder, CEO, CTO, and chief designer of SpaceX; early investor,[b] CEO, and product architect of Tesla, Inc.; founder of The Boring Company; co-founder of Neuralink; and co-founder and initial co-chairman of OpenAI. A centibillionaire, Musk is one of the richest people in the world.[c]

Musk was born to a Canadian mother and South African father and raised in Pretoria, South Africa. He briefly attended the University of Pretoria before moving to Canada aged 17 to attend Queen's University. He transferred to the University of Pennsylvania two years later, where he received dual bachelor's degrees in economics and physics. He moved to California in 1995 to attend Stanford University but decided instead to pursue a business career, co-founding web software company Zip2 with his brother Kimbal. The startup was acquired by Compaq for $307 million in 1999. Musk co-founded online bank X.com that same year, which merged with Confinity in 2000 to form the company PayPal and was subsequently bought by eBay in 2002 for $1.5 billion.

In 2002, Musk founded SpaceX, an aerospace manufacturer and space transport services company, of which he is CEO, CTO, and lead designer. In 2004, he joined electric vehicle manufacturer Tesla Motors, Inc. (now Tesla, Inc.) as chairman and product architect, becoming its CEO in 2008. In 2006, he helped create SolarCity, a solar energy services company and current Tesla subsidiary. In 2015, he co-founded OpenAI, a nonprofit research company that promotes friendly artificial intelligence. In 2016, he co-founded Neuralink, a neurotechnology company focused on developing brain–computer interfaces, and founded The Boring Company, a tunnel construction company. Musk has also proposed the Hyperloop, a high-speed vactrain transportation system.

Musk has been the subject of criticism due to unorthodox or unscientific stances and highly publicized controversies. In 2018, he was sued for defamation by a diver who advised in the Tham Luang cave rescue; a California jury ruled in favor of Musk. Also in 2018, the US Securities and Exchange Commission (SEC) sued him for falsely tweeting that he had secured funding for a private takeover of Tesla. He settled with the SEC, temporarily stepping down from his chairmanship and accepting limitations on his Twitter usage. Musk has received criticism for his views on such matters as artificial intelligence and the COVID-19 pandemic.'''

result_2 = predictor.predict(passage=passage_2,question='Where was born Elon Musk ?')
print(result_2['best_span_str'])
