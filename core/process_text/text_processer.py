from nltk.corpus import stopwords
import re
import spacy
import unicodedata
import nltk

class Preprocesser:

    my_stopwords = [
        'prefeito',
        'prefeitura',
        'subprefeitura',
        'bruno covas',
        'programa de metas',
        'iniciativa',
        'meta',
        'bom dia',
        'boa tarde',
        'boa noite',
        'olá',
        'oi',
        'revisar',
        'ampliar'
    ]

    def __init__(self):

        #downloading data
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('stopwords')

        # Carregar modelo do spaCy para português
        self.spacy_nlp = spacy.load("pt_core_news_lg")

        self.custom_stopwords: set[str] = self.create_custom_stopwords(self.my_stopwords) 
        
        

       

    def create_custom_stopwords(self, new_stopwords:list[str])->set[str]:

        pt_stopwords: set[str] = set(stopwords.words('portuguese'))
        
        my_stopwords: set[str] = pt_stopwords.union(new_stopwords)

        return my_stopwords
    
    def remove_accents(self, text: str) -> str:
        return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))
    
    def preprocess_characters(self, text:str)->str:

        text = text.lower()  # Converter para minúsculas
        text = re.sub(r'\d+', '', text)  # Remover números
        text = re.sub(r'\W+', ' ', text)  # Remover caracteres especiais
        text = self.remove_accents(text) #remove acentos

        return text
    
    def remove_stopwords(self, text:str):
        
        doc = self.spacy_nlp(text)  # Processar texto com spaCy
        tokens = [token.lemma_ for token in doc 
                  if token.text #note que usa token.text, ou seja, o texto original
                  not in self.custom_stopwords and 
                  not token.is_punct]
        
        return ' '.join(tokens)
    
    def pipeline(self, text:str)->str:

        text = self.preprocess_characters(text)
        text = self.remove_stopwords(text)

        return text
    
    def __call__(self, text:str)->str:

        return self.pipeline(text)