import time
import logging
import json

from sdow.database import Database
from sdow.helpers import InvalidRequest, fetch_wikipedia_pages_info


database = Database(sdow_database='/home/cpp/jerryhuang/sdow/scripts/dump/sdow.sqlite', searches_database='./searches.sqlite')


if __name__ == '__main__':
  start_time = time.time()

  file_path = '/home/cpp/jerryhuang/search2024/ASQA_augmented.jsonl'
  data = []
    
  with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
      json_object = json.loads(line.strip())
      data.append(json_object)
      
      print(json_object['question'])
      
      start_page_id = json_object['start_page_id']

      for qa_pair in json_object.get('qa_pairs'):
        if qa_pair['wikipage']:
            target_page_id = qa_pair['page_id']
            
            paths = database.compute_shortest_paths(int(start_page_id), int(target_page_id))
            qa_pair['paths'] = paths
  
  output_fp = "/home/cpp/jerryhuang/search2024/ASQA_augmented.jsonl"
  with open(output_fp, "w") as f:
    for entry in data:
      f.write(json.dumps(entry) + "\n")


  # paths = database.compute_shortest_paths(source_page_id, target_page_id)

  # print(f'paths: {paths}')
  # response = {
  #     'sourcePageTitle': source_page_title,
  #     'targetPageTitle': target_page_title,
  #     'isSourceRedirected': is_source_redirected,
  #     'isTargetRedirected': is_target_redirected,
  # }

  # # No paths found.
  # if len(paths) == 0:
  #   logging.info('No paths found from {0} to {1}'.format(source_page_id, target_page_id))
  #   response['paths'] = []
  #   response['pages'] = []
  # # Paths found
  # else:
  #   # Get a list of all IDs.
  #   page_ids_set = set()
  #   for path in paths:
  #     for page_id in path:
  #       page_ids_set.add(str(page_id))

  #   response['paths'] = paths
  #   # response['pages'] = fetch_wikipedia_pages_info(list(page_ids_set), database)
  #   t = fetch_wikipedia_pages_info(list(page_ids_set), database)
  #   print(f'pages: {t}')


  # # try:
  # #   database.insert_result({
  # #     'source_id': source_page_id,
  # #     'target_id': target_page_id,
  # #     'duration': time.time() - start_time,
  # #     'paths': paths,
  # #   })
  # # except Exception as e:
  # #   # Log the error and continue.
  # #   logging.error('An unexpected error occurred while inserting result: {0}'.format(e))

  # # print(jsonify(response))