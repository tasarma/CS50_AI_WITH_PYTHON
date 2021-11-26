import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    #"""
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    #"""
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    linked_pages = list(corpus[page])
    probability = dict()
    
    probability[page] = 0

    # Choose a link at random linked to by `page`
    for i in linked_pages:
        probability[i] = damping_factor / len(linked_pages)
    
    # Choose a link at random chosen from all pages in the corpus.
    for i in probability.keys():
        probability[i] += (1 - damping_factor) / len(corpus.keys())

    return probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Choose a page at random
    sample = random.choice(list(corpus.keys()))

    data = {i: 0 for i in corpus.keys()}

    for i in range(n-1):
        next_sample = transition_model(corpus, sample, damping_factor)
        
        # Count each sample
        data[sample] += 1

        # Choose next sample using transition model
        sample = random.choices(list(next_sample.keys()), list(next_sample.values()), k=1)[0]

    data = {i: data[i]/n for i in data}
   
    return data


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # The total number of pages in the corpus
    N = len(corpus)

    # Assig each page a rank of 1 / N, where N is the total number of pages in the corpus
    current_rank_values = {i: 1/N for i in corpus.keys()}
    random_page = (1 - damping_factor) / N

    new_rank_values = {}

    # Repeatedly calculating new rank values basing on all of the current rank values
    while True:
        for page in corpus:
            sum_of_link_page = 0
            for linking_page in corpus:

                # Check if page links to our page
                if page in corpus[linking_page]:
                    sum_of_link_page +=  current_rank_values[linking_page] / len(corpus[linking_page])

                # If page has no links, interpret it as having one link for every other page
                if len(corpus[linking_page]) == 0:
                    sum_of_link_page += current_rank_values[linking_page] / N

            sum_of_link_page *= damping_factor
            sum_of_link_page += random_page

            new_rank_values[page] = sum_of_link_page

        diff = max([abs(new_rank_values[page] - current_rank_values[page]) for page in current_rank_values])
        if diff < 0.001:
            break
        current_rank_values = new_rank_values.copy()

    return current_rank_values

if __name__ == "__main__":
    main()
