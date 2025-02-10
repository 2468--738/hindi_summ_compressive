# Hindi Summarization Compressive

This project focuses on compressive summarization of Hindi text. The goal is to generate concise summaries of Hindi documents while retaining the most important information.

## Task

The main task of this project is to evaluate summaries by using compressive summarization on Hindi text. This involves:
- Preprocessing the Hindi text data
- Evaluating the performance of the summarization model using different approaches to compressive summarization
- Generating summaries for new Hindi text inputs

## Installation

To set up the project, follow these steps:

1. Clone the repository:
    ```
    git clone https://github.com/yourusername/hindi_summ_compressive.git
    cd hindi_summ_compressive
    ```

2. Create a virtual environment:
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required libraries:
    ```
    pip install -r requirements.txt
    ```

## Required Libraries

The following libraries are required to run the project:

- `pandas`
- `stanza`
- `tqdm`
- `transformers`

You can install these libraries using the following command:

pip install -r requirements.txt

## Running the Code

The main code for this project is in the `summ_pipeline.ipynb` notebook. To run the code, open the notebook and execute the cells in order.

Rudra sir, for the ritz pipeline, run the `summ_pipeline_rits.ipynb` notebook. There is also `summ_pipeline_code.py` which is not a notebook but a python file that you can run.

Do not forget to set the API_KEY and openai_api_base variables.