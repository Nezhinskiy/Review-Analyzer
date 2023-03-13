import csv
from os.path import splitext
from typing import List, OrderedDict

import openai
from dotenv import load_dotenv


def parse_data_table() -> List[OrderedDict]:
    """
    Parses the data from the input csv file and returns a list of OrderedDicts
    where each OrderedDict represents a row from the csv file.

    :return:
        List[OrderedDict]: A list of OrderedDicts where each OrderedDict
        represents a row from the input csv file.
    """
    input_file = DATA_FILE_NAME
    data = []
    with open(input_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def get_data_for_request(data: List[OrderedDict]) -> str:
    """
    Extracts the review text from each row in the input data and returns them
    as a single string separated by newlines.

    :param data: (List[OrderedDict]): The input data in the form of a list of
        OrderedDicts.
    :return: str: A string consisting of all the review texts separated by
        newlines.
    """
    return ''.join(f'{row['review text']}\n' for row in data)


def get_openai_answer(task: str, payload: str) -> str:
    """
    Uses OpenAI's API to get a response to the given task and payload.

    :param task: (str): The task to be performed by the OpenAI API.
    :param payload: (str): The input data to be used for the task.
    :return: str: The response obtained from the OpenAI API.
    """
    openai.api_key = API_KEY
    prompt = f'{task}: {payload}'
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()


def add_rate_to_data_table(data: List[OrderedDict], gpt_answer: str
                           ) -> List[OrderedDict]:
    """
    Adds a "rate" field to each row in the input data, based on the ratings
    obtained from the GPT model.

    :param data: (List[OrderedDict]): The input data in the form of a list of
        OrderedDicts.
    :param gpt_answer: (str): The response obtained from the GPT model.
    :return: List[OrderedDict]: A list of OrderedDicts where each OrderedDict
        represents a row from the input csv file, with a new "rate" field added
        based on the ratings obtained from the GPT model.
    """
    rates = list(map(int, gpt_answer.strip().split()))
    for row, rate in zip(data, rates):
        row['rate'] = rate
    return data


def sort_data_by_rate(evaluated_data: List[OrderedDict]) -> List[OrderedDict]:
    """
    Sorts the input data based on the "rate" field in each row, in descending
    order.

    :param evaluated_data: (List[OrderedDict]): The input data in the form of a
        list of OrderedDicts, with a "rate" field added to each row.
    :return: List[OrderedDict]: A sorted list of OrderedDicts where each
        OrderedDict represents a row from the input csv file, sorted in
        descending order of the "rate" field.
    """
    return sorted(evaluated_data, key=lambda x: x['rate'], reverse=True)


def write_sorted_data_to_datatable(sorted_data: List[OrderedDict]) -> None:
    """
    Write the given sorted data to a CSV file named `data_analyzed.csv`.

    :param sorted_data: (List[OrderedDict]): The list of ordered dictionaries
        containing the data to be written. Each dictionary in the list should
        represent a row in the CSV file.
    :return: None
    """
    filename = DATA_FILE_NAME
    base_filename, ext = splitext(filename)
    new_filename = f'{base_filename}_analyzed{ext}'
    with open(new_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['email', 'review text', 'date', 'rate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in sorted_data:
            writer.writerow(row)


if __name__ == '__main__':
    load_dotenv()
    API_KEY: str = os.getenv('OPENAI_API_KEY')
    DATA_FILE_NAME: str = 'data.csv'
    data = parse_data_table()
    payload = get_data_for_request(data)
    number_of_reviews = str(len(payload.strip().split('\n')))
    task = (
        f'Rate all {number_of_reviews} reviews from 1 to 10, where 1 is the '
        f'most negative and 10 is the most enthusiastic. Output the results'
        f' as a space-separated list of ratings in the same order'
    )
    gpt_answer = get_openai_answer(task, payload)
    print(gpt_answer)
    evaluated_data = add_rate_to_data_table(data, gpt_answer)
    sorted_data = sort_data_by_rate(evaluated_data)
    write_sorted_data_to_datatable(sorted_data)
    
