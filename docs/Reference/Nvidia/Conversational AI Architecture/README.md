Conversational AI Architectures Powered by Nvidia: Tools Guide
10 mins read
Author Aymane Hachcham
March 1st, 2021
With the latest improvements in deep learning fields such as natural speech synthesis and speech recognition, AI and deep learning models are increasingly entering our daily lives. Matter of fact, numerous harmless applications, seamlessly integrated with our everyday routine, are slowly becoming indispensable. 

Large, data-driven service companies rely heavily on complex network architectures, with pipelines that use conversational deep learning models, and comply with a wide variety of speech tasks to serve customers in the best way possible. 

More broadly, the term “conversational AI” means all intelligent systems capable of naturally mimicking human voice, understanding conversations, developing a personal spoken intent recognition profile (like Alexa or Google Assistant). In short, conversational AI is for human-like conversations. 

Deep learning played a huge role in improving existing speech synthesis approaches, by replacing the entire pipeline process with neural networks trained on pure data. Following that perspective, I’d like to explore two novel models that are well renowned in their field: 

Tacotron 2 for text-to-speech, 
Quartznet for automatic-speech recognition. 
The model versions we’ll cover are based on the Neural Modules NeMo technology recently introduced by Nvidia. 

We’ll explore their architectures, and dig into some Pytorch available on Github. Also, we’ll implement a Django REST API to serve the models through public endpoints, and to wrap up, we’ll create a small IOS application to consume the backend through HTTP requests at client-side. 
