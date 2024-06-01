# ScienceDeJargonizer

## About

We built a little system and wrote a short paper about it to submit to the Computation+Journalism Symposium 2024: **ScienceDeJargonizer** can simplify scientific jargon for journalists without scientific backgrounds, using Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG). This tool transforms complex terms into clear explanations, aiding accurate and accessible science reporting. It is a prototype, intended as a roof-of-concept to demonstrate the potential benefits and drawbacks of such an application. Here's our codebase for the study, with all our scrpaing code, data analysis, prompts, and datasets.

## Features

- **Jargon Identification**: Automatically identifies complex scientific terms within academic texts.
- **Personalization**: Identifies jargon terms based on the user’s expertise and background.
- **Clear Explanations**: Generates easy-to-understand definitions and explanations based on the context of a paper.

## How we built this

We ran a short pilot study to evaluate the potential of GPT-4 and RAG for identifying and defining jargon terms for the benefit of science reporters. We tested different prompts to (i) personalize jargon identification based on the reader's science expertise, and (ii) to generate accurate, high-quality definitions of jargon terms for easy reading.

We evaluated the identified jargon terms and definitions by comparing them to ground-truth annotations from two annotators with varying scientific expertise. This was a relatively small-scale study, we looked at jargon terms for arXiv CS abstracts (n=64), sampled from articles published in March 2024 and in the following primary categories: cs.AI, cs.HC, cs.CY. We aim to continue this work further, at scale, and with improved appraoches to prompting and UI design.

## Contact

- **Project Maintainers**: 
  - Sachita Nishal: nishal@u.northwestern.edu 
  - Eric Lee: ericlee2026@u.northwestern.edu

## Acknowledgements

- Thanks to the Computational Journalism Lab at Northwestern for their support.

---

Feel free to explore, use, and contribute to the ScienceDeJargonizer project. Together, we can make scientific knowledge more accessible to everyone!
