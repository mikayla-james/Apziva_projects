# Client Summary Report

## Project Objective
Goal: Predict how fit the candidate is based on their available information (variable fit).

## Background Information
The two most common approaches in AI for ranking a list of entries or documents in response to a query such as “Aspiring human resources” are **vector space models** and **learning-to-rank models**.

Vector space models convert text into sets of numbers based on patterns like parts of speech, synonyms, and the surrounding context of words—a process known as *embedding*. I am currently using these embeddings to calculate **cosine similarity**, which provides a straightforward way to rank how well each entry matches a given query.

In an ideal setup, the model’s ranking would be refined using feedback signals such as the number of times a candidate profile is clicked or “starred.” That feedback acts as real-world evidence of what users consider the best matches, allowing the model to improve over time. However, since I don’t yet know how your candidate lists and documents are being collected or reviewed, this behavioral layer isn’t included in the current version.

Learning-to-rank models build on embeddings by combining them with these kinds of feedback signals and other features to jointly rank multiple query–document sets. I’ve included a simple example of this in my notebook, and I recommend experimenting with several queries such as “full-stack software engineer,” “engineering manager,” and “aspiring human resources,” along with their corresponding candidate lists.

If you’d like help extending the ranking system to incorporate review feedback or candidate-selection behavior, feel free to contact me at **mlouisejames11@gmail.com**.

## Model Overview
This prototype uses three pre-trained sentence-embedding models to represent text numerically. Each model captures slightly different patterns in language, and their combined output provides a more balanced similarity score.

## Candidate Rankings
To calculate each entry’s **ranking score**, I used results from three vector space models (each model produces a cosine similarity score showing how closely an entry matches a query).

The steps are:

1. Take the **average cosine similarity** from the three models.
2. Multiply that by **0.8** (to give 80% weight to similarity).
3. Add the **connection score** multiplied by **0.2** (to give 20% weight to connection).
4. Repeat this for both queries — “Aspiring human resources” and “Seeking human resources.”
5. Average those two results to get the final ranking score.

| Rank | Job Title | Score |
|------|------------|-------|
| 1 | Seeking Human Resources Opportunities | 0.825267 |
| 2 | Human Resources, Staffing and Recruiting Professional | 0.809404 |
| 3 | Seeking Human Resources HRIS and Generalist Positions | 0.807303 |
| 4 | Aspiring Human Resources Management student seeking an internship | 0.757966 |
| 5 | Human Resources Generalist at Loparex | 0.714796 |
| 6 | Human Resources Generalist at Schwan's | 0.714026 |
| 7 | Human Resources Specialist at Luxottica | 0.707437 |
| 8 | Aspiring Human Resources Professional | 0.702619 |
| 9 | Aspiring Human Resources Professional | 0.691798 |
| 10 | Human Resources Generalist at ScottMadden, Inc. | 0.687342 |

## Interpretation Guide
Scores range from **0 to 1**. Higher scores mean stronger alignment between the candidate’s description and the query (“Aspiring human resources” or “Seeking human resources”). The ranking is relative within this dataset. The full table  can be founds as "ranked_candidates.csv".

## Next Steps and Recommendations
- Gather user feedback on which candidates were actually selected to refine the ranking model.
- Add more query phrases (e.g., “human resources coordinator,” “HR assistant”) to broaden coverage.
- Explore integrating behavioral feedback such as clicks or shortlists to enable a full learning-to-rank model.
