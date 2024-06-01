# ScienceDeJargonizer

## About
**ScienceDeJargonizer** simplifies scientific jargon for journalists without scientific backgrounds, using Large Language Models (LLMs). This tool transforms complex terms into clear explanations, aiding accurate and accessible science reporting. This is a prototype concept to demonstrate the effectiveness of such an application.

## Features
- **Jargon Identification**: Automatically identifies complex scientific terms within academic texts.
- **Contextual Understanding**: Uses LLMs to understand the context of the jargon.
- **Clear Explanations**: Generates easy-to-understand definitions and explanations tailored for journalists.
- **Personalization**: Adapts explanations based on the user’s expertise and background.
- **Annotation Support**: Provides a system for annotating and evaluating the quality of generated definitions.

## Project Structure
The codebase is organized into files where some files are used to pull data from arXiv and other files are used to create the application. The file structure is as follows:
## Project Structure

```bash
.
├── .ipynb_checkpoints
├── data
│   ├── final
│   ├── processed
│   └── raw
├── docs
├── logs
├── models
├── my-app
├── notebooks
├── src
│   ├── __init__.py
│   ├── process.py
│   ├── train_model.py
│   └── utils.py
├── tests
│   ├── __init__.py
│   ├── test_process.py
│   └── test_train_model.py
├── .DS_Store
├── .gitignore
├── 240508_rag_experiment.ipynb
├── 240521_gpt_jargon_eval_setup.ipynb
├── Makefile
├── README.md
├── get_arxiv_metadata.py
├── get_arxiv_texts.py
├── pyproject.toml
├── requirements.txt
└── config
    ├── main.yaml
    ├── model
    │   ├── model1.yaml
    │   └── model2.yaml
    └── process
        ├── process1.yaml
        └── process2.yaml


## Contact

- **Project Maintainers**:
  - Eric Lee: ericlee2026@u.northwestern.edu
  - Sachita Nishal: sachita@example.com

## Acknowledgements

- Thanks to the Computational Journalism Lab at Northwestern for their support.
- Inspired by Novikova’s RankME paper for annotation criteria.

---

Feel free to explore, use, and contribute to the ScienceDeJargonizer project. Together, we can make scientific knowledge more accessible to everyone!
