# LLM-NER Job App Parser

This is a project exploring the application of Named Entity Recognition through Large Language Models to assist with Job Application, by parsing and analyzing text on job application emails.  

## Description

The main model used in this project is Universal NER model, which is  based on ising lightweight models like LLama 7b with  chain-of-the-though distillation in order to create specialized repsonses. More information about the Universal NER model can be found [here.](https://ollama.com/zeffmuks/universal-ner)

Using virutal machines with GPUI acceleration and API is used to allow analyze email application to extract relevant job information for their job serach. 

## Getting Started

### Dependencies

* Python 3.10 >
* Ollama
* beautifulsoup4==4.11.1
* google_api_python_client==2.127.0
* google_auth_oauthlib==1.2.0
* jsonpath_ng==1.6.1
* ollama==0.1.9
* pandas==1.5.3
* protobuf==5.26.1
* spacy_llm==0.7.1
* tqdm==4.65.0


### Installing

### Executing program


## Acknowledgments
Zhou, W., Zhang, S., Gu, Y., Chen, M., & Poon, H. (2023). Universalner: Targeted distillation from large language models for open named entity recognition. arXiv preprint arXiv:2308.03279
https://arxiv.org/pdf/2308.03279
