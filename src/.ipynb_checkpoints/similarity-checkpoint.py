# File with functions to compute similarity of two terms
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

def process_jargon(jargon):


def ngrams(term, n):

    '''
    Get n-grams of a term.
    '''

    return [term[i:i+n] for i in range(len(term)-n+1)]

def jaccard_similarity(term1, term2, n=3):

    '''
    Compute Jaccard similarity of two terms, based on their n-grams.
    n=3 by default.
    '''

    ngrams1 = set(ngrams(term1, n))
    ngrams2 = set(ngrams(term2, n))
    intersection = ngrams1.intersection(ngrams2)
    union = ngrams1.union(ngrams2)
    return len(intersection) / len(union) if union else 0

def evaluate_jaccard(predicted_terms, ground_truth_terms, threshold=0.3, n=3):

    '''
    Evaluate the Jaccard similarity of predicted terms against ground truth terms.
    threshold=0.3 by default.
    n=3 by default.
    '''

    # Initialize counters -- FTP: Fuzzy True Positive, FFP: Fuzzy False Positive, FFN: Fuzzy False Negative
    FTP = 0
    FFP = 0
    FFN = 0

    for pred in predicted_terms:
        if any(jaccard_similarity(pred, gt, n) >= threshold for gt in ground_truth_terms):
            FTP += 1
        else:
            FFP += 1

    for gt in ground_truth_terms:
        if not any(jaccard_similarity(pred, gt, n) >= threshold for pred in predicted_terms):
            FFN += 1

    precision = FTP / len(predicted_terms) if predicted_terms else 0
    recall = FTP / len(ground_truth_terms) if ground_truth_terms else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0

    return precision, recall, f1_score
