# py_word_suggest/Selector_redis.py 
class SelectorError(Exception): pass

class SelectorNoBaseKeyFoundError(SelectorError): pass

class SelectorNoSuggestWordFoundError(SelectorError): pass

class SelectorEmptyValue(SelectorError): pass
# Selector to retreive bigram from json or pickle
#from app.util.decorators import empty_arguments
from .decorators import empty_arguments

from . import export
# class SelectorError(Exception): pass

# class SelectorNoBaseKeyFoundError(SelectorError): pass

# class SelectorNoSuggestWordFoundError(SelectorError): pass

# class SelectorEmptyValue(SelectorError): pass

@export
class Selector(object):
    """ Selector_redis. Class to retreive bigram from json or pickle    
    :Datastructure:
            dictionary: key:value(listOflist, 'lang:<language>:gram:2:<word>':[[<word>,<freq score>]]
    """

    def __init__(self, bigrams):
        self.bigrams = bigrams
        self._suggestWords = None
        self._selectedBaseKey = None #Bigram (key) that user selected
        self._selectedBigram = None#Bigram (value) that user selected

    # @empty_arguments(SelectorEmptyValue)
    def get_suggestWord(self,key:str,sort=True):
        """get_suggestWord: Generate suggested word
        :key: string 'lang:{language}:gram:2:{word}'
        :return: generator
        """
        
        # Set _selectedBaseKey
        self.set_bigram(key,reverse=sort)
        for x in self._selectedBigram:
            yield x[0]
    
    def gen_suggestWord(self,key:str,sort=True):
        """gen_suggestWord: Generate suggested word, sorted by hightest frequency
        :key: string 'lang:{language}:gram:2:{word}'
        :return: generator
        """
        for x in sorted(self.bigrams[key],reverse=sort):
            yield x[0]
        return None

    @empty_arguments(SelectorEmptyValue)
    def set_suggestedWords(self, key:str,**kwargs):
        """set_suggestedWords: Set all suggested word of giving key 
            Sorted by hightest frequency 
        :key: string 'lang:{language}:gram:2:{word}'
        :Todo: Look at exception
        :return: void generator type 
        """
        if not self.existBaseKey(key):
            raise SelectorNoBaseKeyFoundError("Error: key, '{k}' does not exists.".format(k=key))
            
        self._suggestWords = self.gen_suggestWord(key, **kwargs)

    @empty_arguments(SelectorEmptyValue)
    def set_baseKey(self, baseKey:str):
        """set_bigram: Set baseKey (key) to object 
        :baseKey: string 'lang:{language}:gram:2:{word}'
        :Todo: Look at exception
        :return: void 
        """
        if not self.existBaseKey(baseKey):
            raise SelectorNoBaseKeyFoundError("Error: key, '{k}' does not exists.".format(k=baseKey))
            
        self._selectedBaseKey = baseKey
        

    @empty_arguments(SelectorEmptyValue)
    def set_bigram(self, baseKey:str):
        """set_bigram: Set bigram (values) of giving baseKey 
        :baseKey: string 'lang:{language}:gram:2:{word}'
        :Todo: Look at exception
        :return: void 
        """
        if not self.existBaseKey(baseKey):
            raise SelectorNoBaseKeyFoundError("Error: key, '{k}' does not exists.".format(k=baseKey))
            
        self._selectedBigram = self.bigrams.get(baseKey, None)
        

    def containing(self, collection, targetItem):
        """containing: Checks if a item is or is not in a collection of items
        :items: collection of items
        :targetItem: 
        :returns: bool
        """
        return targetItem in collection

    @empty_arguments(SelectorEmptyValue)
    def existBaseKey(self, key):
        """existBaseKey: Checks if baseKay exist in bigram collection
        :key: collection of items
        :returns: bool
        """
        return key in self.bigrams

    
    
#     @empty_arguments(SelectorEmptyValue)
#     def addNewSuggestWord(self, key, word, freq=1):
#         """addNewSuggestWord: Adding new suggested word to key
#         :key: string
#         :word: string
#         :freq: int, score 
#         :returns: void
#         :TODO: Validate  if word only contains Alpha str.isalpha()
#         """
#         self.r.zadd(key, word, freq)

#     @empty_arguments(SelectorEmptyValue)
#     def removeSuggestWord(self, key, word):
#         """removeSuggestWord: Remove suggested word from key
#         :key: string
#         :word: string 
#         :returns: void
#         :TODO: validation
#         """
#         self.r.zrem(key, word)

#     @empty_arguments(SelectorEmptyValue)
#     def existBaseKey(self, key):
#         """existBaseKey: Check if key exists
#         :key: string
#         :returns: bool

#         """
#         return key in self.bigrams

#     @empty_arguments(SelectorEmptyValue)
#     def increaseScoreSuggestedWord(self, key, suggestedWord, score=1):
#         """increaseScoreSuggestedWord: Increase score of suggested word of giving key
#         :key: String
#         :suggestedWord: String
#         :score: int
#         :returns: void

#         """
#         # Check if key or suggestedWord are empty
#         # Test key exists
#         if not self.r.exists(key):
#             raise SelectorNoBaseKeyFoundError( "Error: key '{x}' does not exists.".format(x=key))
#         # Test suggested word
#         fetch_collection = self.gen_fetchWords(key)
#         suggestedWords = set(self.gen_suggestWord(*fetch_collection))
#         if not self.containing(suggestedWords, suggestedWord):
#             raise SelectorNoSuggestWordFoundError("Error: suggested word: '{x}' does not exists with basekey '{y}'.".format(x=suggestedWord, y=key))
#         if type(score) != int:
#             raise TypeError("Error: Score '{x}' needs to be an int or a float.".format(x=score))
#         # Update
#         self.r.zincrby(key, suggestedWord, score)
