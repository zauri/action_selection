from fastDamerauLevenshtein import damerauLevenshtein

print(damerauLevenshtein('abc', 'acb'))

print(damerauLevenshtein('abc', 'acb', similarity=False) / len('abc'))

print(1- damerauLevenshtein('abc', 'acb'))

print(damerauLevenshtein('abc','acb', similarity=False))