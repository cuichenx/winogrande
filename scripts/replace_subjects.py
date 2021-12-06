import json
import pdb
import random
# some code is from this post: https://stackoverflow.com/questions/50475635/loading-jsonl-file-as-json-objects
# as well as here: https://galea.medium.com/how-to-love-jsonl-using-json-line-format-in-your-workflow-b6884f65175b

def dump_jsonl(data, output_path, append=False, to_csv=False):
    """
    Write list of objects to a JSON lines file.
    """
    mode = 'a+' if append else 'w'
    with open(output_path, mode, encoding='utf-8') as f:
        for line in data:
            if to_csv:
            else:
                json_record = json.dumps(line, ensure_ascii=False)
                f.write(json_record + '\n')
    print('Wrote {} records to {}'.format(len(data), output_path))

if __name__ == "__main__":
    with open('./dev.jsonl', 'r') as json_file:
        json_list = list(json_file)

    data = []
    for json_str in json_list:
        result = json.loads(json_str)
        result["sentence"] = result["sentence"].replace(result["option1"], "X").replace(result["option2"], "Y")
        result["option1"] = "X"
        result["option2"] = "Y"
        data.append(result)
        print(f"result: {result}")

    selected_data = random.choices(data, k=50)
    dump_jsonl(data, "dev_replaced.jsonl")
    dump_jsonl(selected_data, "")