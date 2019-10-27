from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from rake_nltk import Rake

def google_nlp_sentiment(text):
    client = language.LanguageServiceClient()
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    
    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    return sentiment

def keypoint_extractor(text):
    from rake_nltk import Rake
    r = Rake()
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases()[:5]
    return keywords
