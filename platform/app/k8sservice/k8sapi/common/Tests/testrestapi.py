#!/usr/bin/env python

import requests
from common import logging as log


#token = 'eyJ1aWQiOiAzLCAidXNlcl9vcmFnIjogImJveGxpbmtlciIsICJ0b2tlbmlkIjogIjg4NWZlZDcyZjUyYTkwNWRiOGM0NjY1ZSIsICJ1c2VyX25hbWUiOiAiYm94bGlua2VyIiwgImV4cGlyZXMiOiAxNDcyNjMzMDYzLjgwNjQzLCAidXNlcl9yb2xlIjogIjEiLCAidXNlcl9pcCI6ICIxMjcuMC4wLjEiLCAic2FsdCI6ICJlZjlmMDc4YzAxNTAwMDVkNjc5NGM1OTEiLCAiZW1haWwiOiAibGl2ZW5vd2h5QDEyNi5jb20ifbVUnbMQdSQGXCbw7MPb8H0='

#url = 'http://kibana.boxlinker.com/elasticsearch/_msearch'
url = 'http://kibana.boxlinker.com/elasticsearch/_msearch?timeout=0&ignore_unavailable=true&preference=1473311382257'

headers = {'kbn-version': '4.5.4'}
body = '{"index":["logstash-2016.09.08"],"ignore_unavailable":true} \n {"size":500,"sort":[{"@timestamp":{"order":"desc","unmapped_type":"boolean"}}],"highlight":{"pre_tags":["@kibana-highlighted-field@"],"post_tags":["@/kibana-highlighted-field@"],"fields":{"*":{}},"require_field_match":false,"fragment_size":2147483647},"query":{"filtered":{"query":{"query_string":{"query":"*","analyze_wildcard":true}},"filter":{"bool":{"must":[{"query":{"match":{"docker.container_id":{"query":"79340854e68e306c8d7910399e86b423326dbbf309a8871d8a5d9722e7bd4577","type":"phrase"}}}},{"range":{"@timestamp":{"gte":1473304819729,"lte":1473305719729,"format":"epoch_millis"}}}],"must_not":[]}}}},"aggs":{"2":{"date_histogram":{"field":"@timestamp","interval":"30s","time_zone":"Asia/Shanghai","min_doc_count":0,"extended_bounds":{"min":1473304819728,"max":1473305719728}}}},"fields":["*","_source"],"script_fields":{},"fielddata_fields":["@timestamp","time"]} \n'

try:
    r = requests.get(url, headers=headers, data=body)
except Exception, e:
    log.error('requests error, reason=%s' % (e))

print('r.url = %s' % (r.url))

print('r.text = %s' % (r.text))

print('r.json = %s' % (r.json()))

#print('ret = %d' % (r.json()['status']))
