#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Python client library for Sensei
"""


import urllib
import urllib2
import json
import sys
import logging
import datetime
from datetime import datetime
import time
import re


logger = logging.getLogger("sensei_client_lib")



#
# REST API parameter constants
#
PARAM_OFFSET = "start"
PARAM_COUNT = "rows"
PARAM_QUERY = "q"
PARAM_QUERY_PARAM = "qparam"
PARAM_SORT = "sort"
PARAM_SORT_ASC = "asc"
PARAM_SORT_DESC = "desc"
PARAM_SORT_SCORE = "relevance"
PARAM_SORT_SCORE_REVERSE = "relrev"
PARAM_SORT_DOC = "doc"
PARAM_SORT_DOC_REVERSE = "docrev"
PARAM_FETCH_STORED = "fetchstored"
PARAM_SHOW_EXPLAIN = "showexplain"
PARAM_ROUTE_PARAM = "routeparam"
PARAM_GROUP_BY = "groupby"
PARAM_MAX_PER_GROUP = "maxpergroup"
PARAM_SELECT = "select"
PARAM_SELECT_VAL = "val"
PARAM_SELECT_NOT = "not"
PARAM_SELECT_OP = "op"
PARAM_SELECT_OP_AND = "and"
PARAM_SELECT_OP_OR = "or"
PARAM_SELECT_PROP = "prop"
PARAM_FACET = "facet"
PARAM_DYNAMIC_INIT = "dyn"
PARAM_PARTITIONS = "partitions"

PARAM_FACET_EXPAND = "expand"
PARAM_FACET_MAX = "max"
PARAM_FACET_MINHIT = "minhit"
PARAM_FACET_ORDER = "order"
PARAM_FACET_ORDER_HITS = "hits"
PARAM_FACET_ORDER_VAL = "val"

PARAM_DYNAMIC_TYPE = "type"
PARAM_DYNAMIC_TYPE_STRING = "string"
PARAM_DYNAMIC_TYPE_BYTEARRAY = "bytearray"
PARAM_DYNAMIC_TYPE_BOOL = "boolean"
PARAM_DYNAMIC_TYPE_INT = "int"
PARAM_DYNAMIC_TYPE_LONG = "long"
PARAM_DYNAMIC_TYPE_DOUBLE = "double"
PARAM_DYNAMIC_VAL = "vals"

PARAM_RESULT_PARSEDQUERY = "parsedquery"
PARAM_RESULT_HIT_STORED_FIELDS = "stored"
PARAM_RESULT_HIT_STORED_FIELDS_NAME = "name"
PARAM_RESULT_HIT_STORED_FIELDS_VALUE = "val"
PARAM_RESULT_HIT_EXPLANATION = "explanation"
PARAM_RESULT_FACETS = "facets"

PARAM_RESULT_TID = "tid"
PARAM_RESULT_TOTALDOCS = "totaldocs"
PARAM_RESULT_NUMHITS = "numhits"
PARAM_RESULT_HITS = "hits"
PARAM_RESULT_HIT_UID = "uid"
PARAM_RESULT_HIT_DOCID = "docid"
PARAM_RESULT_HIT_SCORE = "score"
PARAM_RESULT_HIT_SRC_DATA = "srcdata"
PARAM_RESULT_TIME = "time"

PARAM_SYSINFO_NUMDOCS = "numdocs"
PARAM_SYSINFO_LASTMODIFIED = "lastmodified"
PARAM_SYSINFO_VERSION = "version"
PARAM_SYSINFO_FACETS = "facets"
PARAM_SYSINFO_FACETS_NAME = "name"
PARAM_SYSINFO_FACETS_RUNTIME = "runtime"
PARAM_SYSINFO_FACETS_PROPS = "props"
PARAM_SYSINFO_CLUSTERINFO = "clusterinfo"
PARAM_SYSINFO_CLUSTERINFO_ID = "id"
PARAM_SYSINFO_CLUSTERINFO_PARTITIONS = "partitions"
PARAM_SYSINFO_CLUSTERINFO_NODELINK = "nodelink"
PARAM_SYSINFO_CLUSTERINFO_ADMINLINK = "adminlink"

PARAM_RESULT_HITS_EXPL_VALUE = "value"
PARAM_RESULT_HITS_EXPL_DESC = "description"
PARAM_RESULT_HITS_EXPL_DETAILS = "details"

PARAM_RESULT_FACET_INFO_VALUE = "value"
PARAM_RESULT_FACET_INFO_COUNT = "count"
PARAM_RESULT_FACET_INFO_SELECTED = "selected"

#
# JSON API parameter constants
#

JSON_PARAM_COLUMNS = "columns"
JSON_PARAM_EXPLAIN = "explain"
JSON_PARAM_FACETS = "facets"
JSON_PARAM_FACET_INIT = "facetInit"
JSON_PARAM_FETCH_STORED = "fetchStored"
JSON_PARAM_FETCH_TERM_VECTORS = "fetchTermVectors"
JSON_PARAM_FILTER = "filter"
JSON_PARAM_FROM = "from"
JSON_PARAM_GROUPBY = "groupBy"
JSON_PARAM_PARTITIONS = "partitions"
JSON_PARAM_QUERY = "query"
JSON_PARAM_QUERY_STRING = "query_string"
JSON_PARAM_ROUTEPARAM = "routeParam"
JSON_PARAM_SELECTIONS = "selections"
JSON_PARAM_SIZE = "size"
JSON_PARAM_SORT = "sort"
JSON_PARAM_TOP = "top"
JSON_PARAM_VALUES = "values"
JSON_PARAM_EXCLUDES = "excludes"
JSON_PARAM_OPERATOR = "operator"
JSON_PARAM_NO_OPTIMIZE = "_noOptimize"

# Group by related column names
GROUP_VALUE = "groupvalue"
GROUP_HITS = "grouphits"

# Default constants
DEFAULT_REQUEST_OFFSET = 0
DEFAULT_REQUEST_COUNT = 10
DEFAULT_REQUEST_MAX_PER_GROUP = 10
DEFAULT_FACET_MINHIT = 1
DEFAULT_FACET_MAXHIT = 10
DEFAULT_FACET_ORDER = PARAM_FACET_ORDER_HITS

#
# Utilities for result display
#

def print_line(keys, max_lens, char='-', sep_char='+'):
  sys.stdout.write(sep_char)
  for key in keys:
    sys.stdout.write(char * (max_lens[key] + 2) + sep_char)
  sys.stdout.write('\n')

def print_header(keys, max_lens, char='-', sep_char='+'):
  print_line(keys, max_lens, char=char, sep_char=sep_char)
  sys.stdout.write('|')
  for key in keys:
    sys.stdout.write(' %s%s |' % (key, ' ' * (max_lens[key] - len(key))))
  sys.stdout.write('\n')
  print_line(keys, max_lens, char=char, sep_char=sep_char)

def print_footer(keys, max_lens, char='-', sep_char='+'):
  print_line(keys, max_lens, char=char, sep_char=sep_char)

def safe_str(obj):
  """Return the byte string representation of obj."""
  try:
    return str(obj)
  except UnicodeEncodeError:
    # obj is unicode
    return unicode(obj).encode("unicode_escape")


class SenseiClientError(Exception):
  """Exception raised for all errors related to Sensei client."""

  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)


class SenseiFacets:
  def __init__(self):
    self.facets={}

  def add_facet(self, facet_name, expand=False,minHits=1,maxCounts=10,orderBy=PARAM_FACET_ORDER_HITS):
    self.facets[facet_name]={"max":maxCounts, "minCount":minHits, "expand":expand, "order":orderBy }
    return self

  def get_facets(self):
    return self.facets
  
  
class SenseiSelection:
  def __init__(self, type):
    self.type = type;
    self.selection = {}
    
  def get_type(self):
    return self.type
  
  def get_selection(self):
    return self.selection

class SenseiSelectionTerm(SenseiSelection):
  def __init__(self, column, value):
    SenseiSelection.__init__(self, "term")
    self.selection = {"term": {column : {"value" : value}}}


class SenseiSelectionTerms(SenseiSelection):
  def __init__(self, column, values, excludes, operator):
    SenseiSelection.__init__(self, "terms")
    self.selection={"terms": {column : {"values" : values, "excludes":excludes, "operator":operator}}}
    

class SenseiSelectionRange(SenseiSelection):
  def __init__(self, column, from_str="*", to_str="*", include_lower=True, include_upper=True):
    SenseiSelection.__init__(self, "range")
    self.selection={"range":{column:{"to":to_str, "from":from_str, "include_lower":include_lower, "include_upper":include_upper}}}
    
class SenseiSelectionPath(SenseiSelection):
  def __init__(self, column, value, strict=False, depth=1):
    SenseiSelection.__init__(self, "path")
    self.selection={"path": {column : {"value":value, "strict":strict, "depth":depth}}}
    

class SenseiQuery:
  def __init__(self, type):
    self.type = type
    self.query = {}
    
  def get_type(self):
    return self.type
  
  def get_query(self):
    return self.query  

class SenseiQueryMatchAll(SenseiQuery):
  def __init__(self):
    SenseiQuery.__init__(self, "match_all")
    self.query={"match_all":{"boost":1.0}}
    
  def set_boost(self, boost):
    target = (self.query)["match_all"]
    target["boost"]=boost
    return self
      
class SenseiQueryIDs(SenseiQuery):
  def __init__(self, values, excludes):
    SenseiQuery.__init__(self, "ids")
    self.query={"ids" : {"values" : [], "excludes":[], "boost":1.0}}
    if isinstance(values, list) and isinstance(excludes, list):
      self.query = {"ids" : {"values" : values, "excludes":excludes, "boost":1.0}}

  def add_values(self, values):
    if self.query.has_key("ids"):
      values_excludes = self.query["ids"]
      if values_excludes.has_key("values"):
        orig_values =  values_excludes["values"]
        orig_set = set(orig_values)
        for new_value in values:
          if new_value not in orig_set:
            orig_values.append(new_value)
    return self

  def add_excludes(self, excludes):
    if self.query.has_key("ids"):
      values_excludes = self.query["ids"]
      if values_excludes.has_key("excludes"):
        orig_excludes = values_excludes["excludes"]
        orig_set = set(orig_excludes)
        for new_value in excludes:
          if new_value not in orig_set:
            orig_excludes.append(new_value)
    return self
            
  def set_boost(self, boost):
    target = (self.query)["ids"]
    target["boost"]=boost
    return self

class SenseiQueryString(SenseiQuery):
  def __init__(self, query):
    SenseiQuery.__init__(self, "query_string")
    self.query={"query_string":{"query":query, 
                                "default_field":"contents", 
                                "default_operator":"OR",
                                "allow_leading_wildcard":True,
                                "lowercase_expanded_terms":True,
                                "enable_position_increments":True,
                                "fuzzy_prefix_length":0,
                                "fuzzy_min_sim":0.5,
                                "phrase_slop":0,
                                "boost":1.0,
                                "auto_generate_phrase_queries":False,
                                "fields":[],
                                "use_dis_max":True,
                                "tie_breaker":0 
                                 }}
  
  def set_field(self, field):
    self.query["query_string"]["default_field"]=field
    return self
    
  def set_operator(self, operator):
    self.query["query_string"]["default_operator"]=operator
    return self

  def set_allow_leading_wildcard(self, allow_leading_wildcard):
    self.query["query_string"]["allow_leading_wildcard"]=allow_leading_wildcard
    return self
    
  def set_lowercase_expanded_terms(self, lowercase_expanded_terms):
    self.query["query_string"]["lowercase_expanded_terms"]=lowercase_expanded_terms
    return self
        
  def set_enable_position_increments(self, enable_position_increments):
    self.query["query_string"]["enable_position_increments"]=enable_position_increments
    return self
    
  def set_fuzzy_prefix_length(self, fuzzy_prefix_length):
    self.query["query_string"]["fuzzy_prefix_length"]=fuzzy_prefix_length
    return self
    
  def set_fuzzy_min_sim(self, fuzzy_min_sim):
    self.query["query_string"]["fuzzy_min_sim"]=fuzzy_min_sim
    return self
        
  def set_phrase_slop(self, phrase_slop):
    self.query["query_string"]["phrase_slop"]=phrase_slop
    return self
    
  def set_boost(self, boost):
    self.query["query_string"]["boost"]=boost
    return self
    
  def set_auto_generate_phrase_queries(self, auto_generate_phrase_queries):
    self.query["query_string"]["auto_generate_phrase_queries"]=auto_generate_phrase_queries
    return self
    
  def set_fields(self, fields):
    if isinstance(fields, list):
      self.query["query_string"]["fields"]=fields
      return self
    
  def set_use_dis_max(self, use_dis_max):
    self.query["query_string"]["use_dis_max"]=use_dis_max
    return self
        
  def set_tie_breaker(self, tie_breaker):
    self.query["query_string"]["tie_breaker"]=tie_breaker
    return self
                                
   
class SenseiQueryText(SenseiQuery):
  def __init__(self, message, operator, type):
    SenseiQuery.__init__(self, "text")
    self.query={"text":{"message":message, "operator":operator, "type":type}}   
    
class SenseiQueryTerm(SenseiQuery):
  def __init__(self, column, value):
    SenseiQuery.__init__(self, "term")
    self.query={"term":{column:{"value":value, "boost":1.0}}}
  
  def set_boost(self, boost):
    target = (self.query)["term"]
    for column, desc in target.iterms():
      desc["boost"]=boost
    return self  
        
                  
class SenseiFilter:
  def __init__(self, type):
    self.type = type
    self.filter = {}
    
  def get_type(self):
    return self.type
  
  def get_filter(self):
    return self.filter  
  
    
class SenseiFilterIDs(SenseiFilter):
  def __init__(self, values, excludes):
    SenseiFilter.__init__(self, "ids")
    self.filter={"ids" : {"values" : [], "excludes":[]}}
    if isinstance(values, list) and isinstance(excludes, list):
      self.filter = {"ids" : {"values" : values, "excludes":excludes}}

  def add_values(self, values):
    if self.filter.has_key("ids"):
      values_excludes = self.filter["ids"]
      if values_excludes.has_key("values"):
        orig_values =  values_excludes["values"]
        orig_set = set(orig_values)
        for new_value in values:
          if new_value not in orig_set:
            orig_values.append(new_value)
    return self

  def add_excludes(self, excludes):
    if self.filter.has_key("ids"):
      values_excludes = self.filter["ids"]
      if values_excludes.has_key("excludes"):
        orig_excludes =  values_excludes["excludes"]
        orig_set = set(orig_excludes)
        for new_value in excludes:
          if new_value not in orig_set:
            orig_excludes.append(new_value)
    return self
            
class SenseiFilterBool(SenseiFilter):
  def __init__(self, must_filter=None, must_not_filter=None, should_filter=None):            
    SenseiFilter.__init__(self, "bool");
    self.filter = {"bool":{"must":{}, "must_not":{}, "should":{}}}
    if must_filter is not None and isinstance(must_filter, SenseiFilter):
      target = (self.filter)["bool"]
      target["must"]=must_filter.get_filter()
    if must_not_filter is not None and isinstance(must_not_filter, SenseiFilter):
      target = (self.filter)["bool"]
      target["must_not"]=must_not_filter.get_filter()  
    if should_filter is not None and isinstance(should_filter, list):
      should_filters_json=[]
      for should_item in should_filter:
        should_filters_json.append(should_item.get_filter())
      target = (self.filter)["bool"]
      target["should"]=should_filters_json
      
class SenseiFilterAND(SenseiFilter):
  def __init__(self, filter_list):
    SenseiFilter.__init__(self, "and")
    self.filter={"and":[]}
    old_filter_list = (self.filter)["and"]
    if isinstance(filter_list, list):
      for new_filter in filter_list:
        if isinstance(new_filter, SenseiFilter):
          old_filter_list.append(new_filter.get_filter())  
          
class SenseiFilterOR(SenseiFilter):
  def __init__(self, filter_list):
    SenseiFilter.__init__(self, "or")
    self.filter={"or":[]}
    old_filter_list = (self.filter)["or"]
    if isinstance(filter_list, list):
      for new_filter in filter_list:
        if isinstance(new_filter, SenseiFilter):
          old_filter_list.append(new_filter.get_filter())              
    
class SenseiFilterTerm(SenseiFilter):
  def __init__(self, column, value, noOptimize=False):
    SenseiFilter.__init__(self, "term")
    self.filter={"term":{column:{"value": value, "_noOptimize":noOptimize}}} 
    

class SenseiFilterTerms(SenseiFilter):
  def __init__(self, column, values=None, excludes=None, operator="or", noOptimize=False):
    SenseiFilter.__init__(self, "terms")
    self.filter={"terms":{}}
    if values is not None and isinstance(values, list):
      if excludes is  not None and isinstance(excludes, list):
        # complicated mode
        self.filter={"terms":{column:{"values":values, "excludes":excludes, "operator":operator, "_noOptimize":noOptimize}}}
      else:
        self.filter={"terms":{column:values}}
        
class SenseiFilterRange(SenseiFilter):
  def __init__(self, column, from_val, to_val):
    SenseiFilter.__init__(self, "range")
    self.filter={"range":{column:{"from":from_val, "to":to_val, "_noOptimize":False}}}         

  def set_No_optimization(self, type, date_format=None):
    range = (self.filter)["range"]
    for key, value in range.items():
      if value is not None:
        value["_type"] = type
        value["_noOptimize"] = True
        if type == "date" and date_format is not None:
          value["_date_format"]=date_format
    return self
  
class SenseiFilterQuery(SenseiFilter):
  def __init__(self, query):
    SenseiFilter.__init__(self, "query")
    self.filter={"query":{}}
    if isinstance(query, SenseiQuery):
      self.filter={"query": query.get_query()}
      
class SenseiFilterSelection(SenseiFilter):
  def __init__(self, selection):
    SenseiFilter.__init__(self, "selection")
    self.filter = {"selection":{}}
    if isinstance(selection, SenseiSelection):
      self.filter={"selection":selection.get_selection()}        
    
    
class SenseiSort:
  def __init__(self, field, reverse=False):
    self.field = field
    self.dir = None
    if not (field == PARAM_SORT_SCORE or
            field == PARAM_SORT_SCORE_REVERSE or
            field == PARAM_SORT_DOC or
            field == PARAM_SORT_DOC_REVERSE):
      if reverse:
        self.dir = PARAM_SORT_DESC
      else:
        self.dir = PARAM_SORT_ASC

  def __str__(self):
    return self.build_sort_field()

  def build_sort_field(self):
    if self.dir:
      return self.field + ":" + self.dir
    else:
      return self.field

  def build_sort_spec(self):
    if self.dir:
      return {self.field: self.dir}
    elif self.field == PARAM_SORT_SCORE:
      return "_score"
    else:
      return self.field

class SenseiFacetInits:
  def __init__(self):
    self.facet_init={}
    
  def add_facet_init(self, facet_name, param_name, param_values, param_type="string"):
    if isinstance(param_values, list):
      #  parameter type, valid values are: "int","string","boolean","long","bytes","double", default: "string"
      if facet_name in self.facet_init:
        params = self.facet_init[facet_name]
        params[param_name]={"type":param_type, "values":param_values}
      else:
        (self.facet_init)[facet_name]={}
        params = self.facet_init[facet_name]
        params[param_name]={"type":param_type, "values":param_values} 
    return self
      
  def get_facet_inits(self):
    return self.facet_init
           

class SenseiFacetInfo:

  def __init__(self, name, runtime=False, props={}):
    self.name = name
    self.runtime = runtime
    self.props = props

  def get_name(self):
    return self.name

  def set_name(self, name):
    self.name = name

  def get_runtime(self):
    return self.runtime

  def set_runtime(self, runtime):
    self.runtime = runtime

  def get_props(self):
    return self.props

  def set_props(self, props):
    self.props = props


class SenseiNodeInfo:

  def __init__(self, id, partitions, node_link, admin_link):
    self.id = id
    self.partitions = partitions
    self.node_link = node_link
    self.admin_link = admin_link

  def get_id(self):
    return self.id

  def get_partitions(self):
    return self.partitions

  def get_node_link(self):
    return self.node_link

  def get_admin_link(self):
    return self.admin_link


class SenseiSystemInfo:

  def __init__(self, json_data):
    logger.debug("json_data = %s" % json_data)
    self.num_docs = int(json_data.get(PARAM_SYSINFO_NUMDOCS))
    self.last_modified = long(json_data.get(PARAM_SYSINFO_LASTMODIFIED))
    self.version = json_data.get(PARAM_SYSINFO_VERSION)
    self.facet_infos = []
    for facet in json_data.get(PARAM_SYSINFO_FACETS):
      facet_info = SenseiFacetInfo(facet.get(PARAM_SYSINFO_FACETS_NAME),
                                   facet.get(PARAM_SYSINFO_FACETS_RUNTIME),
                                   facet.get(PARAM_SYSINFO_FACETS_PROPS))
      self.facet_infos.append(facet_info)
    # TODO: get cluster_info
    self.cluster_info = None

  def display(self):
    """Display sysinfo."""

    keys = ["facet_name", "facet_type", "runtime", "column", "column_type", "depends"]
    max_lens = None
    # XXX add existing flags

    def get_max_lens(columns):
      max_lens = {}
      for column in columns:
        max_lens[column] = len(column)
      for facet_info in self.facet_infos:
        props = facet_info.get_props()

        tmp_len = len(facet_info.get_name())
        if tmp_len > max_lens["facet_name"]:
          max_lens["facet_name"] = tmp_len

        tmp_len = len(props.get("type"))
        if tmp_len > max_lens["facet_type"]:
          max_lens["facet_type"] = tmp_len

        # runtime can only contain "true" or "false", so len("runtime")
        # is big enough

        tmp_len = len(props.get("column"))
        if tmp_len > max_lens["column"]:
          max_lens["column"] = tmp_len

        tmp_len = len(props.get("column_type"))
        if tmp_len > max_lens["column_type"]:
          max_lens["column_type"] = tmp_len

        tmp_len = len(props.get("depends"))
        if tmp_len > max_lens["depends"]:
          max_lens["depends"] = tmp_len
      return max_lens

    max_lens = get_max_lens(keys)
    print_header(keys, max_lens)

    for facet_info in self.facet_infos:
      props = facet_info.get_props()
      sys.stdout.write('|')
      val = facet_info.get_name()
      sys.stdout.write(' %s%s |' % (val, ' ' * (max_lens["facet_name"] - len(val))))

      val = props.get("type")
      sys.stdout.write(' %s%s |' % (val, ' ' * (max_lens["facet_type"] - len(val))))

      val = facet_info.get_runtime() and "true" or "false"
      sys.stdout.write(' %s%s |' % (val, ' ' * (max_lens["runtime"] - len(val))))

      val = props.get("column")
      sys.stdout.write(' %s%s |' % (val, ' ' * (max_lens["column"] - len(val))))

      val = props.get("column_type")
      sys.stdout.write(' %s%s |' % (val, ' ' * (max_lens["column_type"] - len(val))))

      val = props.get("depends")
      sys.stdout.write(' %s%s |' % (val, ' ' * (max_lens["depends"] - len(val))))

      sys.stdout.write('\n')

    print_footer(keys, max_lens)

  def get_num_docs(self):
    return self.num_docs

  def set_num_docs(self, num_docs):
    self.num_docs = num_docs

  def get_last_modified(self):
    return self.last_modified

  def set_last_modified(self, last_modified):
    self.last_modified = last_modified

  def get_facet_infos(self):
    return self.facet_infos

  def set_facet_infos(self, facet_infos):
    self.facet_infos = facet_infos

  def get_version(self):
    return self.version

  def set_version(self, version):
    self.version = version

  def get_cluster_info(self):
    return self.cluster_info

  def set_cluster_info(self, cluster_info):
    self.cluster_info = cluster_info


class SenseiRequest:

  def __init__(self,
               bql_req=None,
               offset=DEFAULT_REQUEST_OFFSET,
               count=DEFAULT_REQUEST_COUNT,
               max_per_group=DEFAULT_REQUEST_MAX_PER_GROUP,
               facet_map=None):
    self.qParam = {}
    self.explain = False
    self.route_param = None
    self.query = None
    self.offset = offset
    self.count = count
    self.columns = []
    self.sorts = None
    self.selections = []
    self.filter = {}
    self.query_pred = {}
    self.facets = {}
    self.fetch_stored = False
    self.groupby = None
    self.max_per_group = max_per_group
    self.facet_init_param_map = {}

  def set_offset(self, offset):
    self.offset = offset
    return self
    
  def set_count(self, count):
    self.count = count
    return self
    
  def set_query(self, query):
    self.query = query.get_query()
    return self
    
  def set_explain(self, explain):
    self.explain = explain
    return self
  
  def set_fetch_stored(self, fetch_stored):
    self.fetch_stored = fetch_stored
    return self
    
  def set_route_param(self, route_param):
    self.route_param = route_param
    return self
    
  def set_sorts(self, sorts):    
    self.sorts = sorts
    return self
    
  def append_sort(self, sort):
    if isinstance(sort, SenseiSort):
      if self.sorts is None:
        self.sorts = []
        self.sorts.append(sort)
      else:  
        self.sorts.append(sort)
    return self
    
  def set_filter(self, filter):
    self.filter = filter.get_filter()
    return self
    
  def append_selection(self, selection):
    if self.selections is None:
      self.selections = []
    if isinstance(selection, SenseiSelection):
      self.selections.append(selection.get_selection())
    return self
  
        
  def set_facets(self, facets):
    self.facets = facets.get_facets()
    return self
    
  def set_groupby(self, groupby):
    self.groupby = groupby
    return self
    
  def set_max_per_group(self, max_per_group):
    self.max_per_group = max_per_group
    return self
      
  def set_facet_init_param_map(self, facet_init_param_map):
    self.facet_init_param_map = facet_init_param_map
    return self
    
  def get_columns(self):
    return self.columns

  
class SenseiHit:
  def __init__(self):
    self.docid = None
    self.uid = None
    self.srcData = {}
    self.score = None
    self.explanation = None
    self.stored = None
  
  def load(self, jsonHit):
    self.docid = jsonHit.get(PARAM_RESULT_HIT_DOCID)
    self.uid = jsonHit.get(PARAM_RESULT_HIT_UID)
    self.score = jsonHit.get(PARAM_RESULT_HIT_SCORE)
    srcStr = jsonHit.get(PARAM_RESULT_HIT_SRC_DATA)
    self.explanation = jsonHit.get(PARAM_RESULT_HIT_EXPLANATION)
    self.stored = jsonHit.get(PARAM_RESULT_HIT_STORED_FIELDS)
    if srcStr:
      self.srcData = json.loads(srcStr)
    else:
      self.srcData = None
  

class SenseiResultFacet:
  value = None
  count = None
  selected = None
  
  def load(self,json):
    self.value=json.get(PARAM_RESULT_FACET_INFO_VALUE)
    self.count=json.get(PARAM_RESULT_FACET_INFO_COUNT)
    self.selected=json.get(PARAM_RESULT_FACET_INFO_SELECTED,False)

  
class SenseiResult:
  """Sensei search results for a query."""

  def __init__(self, json_data):
    logger.debug("json_data = %s" % json_data)
    self.jsonMap = json_data
    self.parsedQuery = json_data.get(PARAM_RESULT_PARSEDQUERY)
    self.totalDocs = json_data.get(PARAM_RESULT_TOTALDOCS, 0)
    self.time = json_data.get(PARAM_RESULT_TIME, 0)
    self.total_time = 0
    self.numHits = json_data.get(PARAM_RESULT_NUMHITS, 0)
    self.hits = json_data.get(PARAM_RESULT_HITS)
    map = json_data.get(PARAM_RESULT_FACETS)
    self.facetMap = {}
    if map:
      for k, v in map.items():
        facetList = []
        for facet in v:
          facetObj = SenseiResultFacet()
          facetObj.load(facet)
          facetList.append(facetObj)
        self.facetMap[k]=facetList

  def display(self, columns=['*'], max_col_width=40):
    """Print the results in SQL SELECT result format."""

    keys = []
    max_lens = None
    has_group_hits = False

    def get_max_lens(columns):
      max_lens = {}
      has_group_hits = False
      for col in columns:
        max_lens[col] = len(col)
      for hit in self.hits:
        group_hits = [hit]
        if hit.has_key(GROUP_HITS):
          group_hits = hit.get(GROUP_HITS)
          has_group_hits = True
        for group_hit in group_hits:
          for col in columns:
            if group_hit.has_key(col):
              v = group_hit.get(col)
            else:
              v = '<Not Found>'
            if isinstance(v, list):
              v = ','.join([safe_str(item) for item in v])
            elif isinstance(v, (int, long, float)):
              v = str(v)
            value_len = len(v)
            if value_len > max_lens[col]:
              max_lens[col] = min(value_len, max_col_width)
      return max_lens, has_group_hits

    if not self.hits:
      print "No hit is found."
      return
    elif not columns:
      print "No column is selected."
      return

    if len(columns) == 1 and columns[0] == '*':
      keys = self.hits[0].keys()
      if GROUP_HITS in keys:
        keys.remove(GROUP_HITS)
      if GROUP_VALUE in keys:
        keys.remove(GROUP_VALUE)
      if PARAM_RESULT_HIT_SRC_DATA in keys:
        keys.remove(PARAM_RESULT_HIT_SRC_DATA)
    else:
      keys = columns

    max_lens, has_group_hits = get_max_lens(keys)

    print_header(keys, max_lens,
                 has_group_hits and '=' or '-',
                 has_group_hits and '=' or '+')

    # Print the results
    for hit in self.hits:
      group_hits = [hit]
      if hit.has_key(GROUP_HITS):
        group_hits = hit.get(GROUP_HITS)
      for group_hit in group_hits:
        sys.stdout.write('|')
        for key in keys:
          if group_hit.has_key(key):
            v = group_hit.get(key)
          else:
            v = '<Not Found>'
          if isinstance(v, list):
            v = ','.join([safe_str(item) for item in v])
          elif isinstance(v, (int, float, long)):
            v = str(v)
          else:
            # The value may contain unicode characters
            v = safe_str(v)
          if len(v) > max_col_width:
            v = v[:max_col_width]
          sys.stdout.write(' %s%s |' % (v, ' ' * (max_lens[key] - len(v))))
        sys.stdout.write('\n')
      if has_group_hits:
        print_line(keys, max_lens)

    print_footer(keys, max_lens,
                 has_group_hits and '=' or '-',
                 has_group_hits and '=' or '+')

    sys.stdout.write('%s %s%s in set, %s hit%s, %s total doc%s (server: %sms, total: %sms)\n' %
                     (len(self.hits),
                      has_group_hits and 'group' or 'row',
                      len(self.hits) > 1 and 's' or '',
                      self.numHits,
                      self.numHits > 1 and 's' or '',
                      self.totalDocs,
                      self.totalDocs > 1 and 's' or '',
                      self.time,
                      self.total_time
                      ))

    # Print facet information
    for facet, values in self.jsonMap.get(PARAM_RESULT_FACETS).iteritems():
      max_val_len = len(facet)
      max_count_len = 1
      for val in values:
        max_val_len = max(max_val_len, min(max_col_width, len(val.get('value'))))
        max_count_len = max(max_count_len, len(str(val.get('count'))))
      total_len = max_val_len + 2 + max_count_len + 3

      sys.stdout.write('+' + '-' * total_len + '+\n')
      sys.stdout.write('| ' + facet + ' ' * (total_len - len(facet) - 1) + '|\n')
      sys.stdout.write('+' + '-' * total_len + '+\n')

      for val in values:
        sys.stdout.write('| %s%s (%s)%s |\n' %
                         (val.get('value'),
                          ' ' * (max_val_len - len(val.get('value'))),
                          val.get('count'),
                          ' ' * (max_count_len - len(str(val.get('count'))))))
      sys.stdout.write('+' + '-' * total_len + '+\n')
  


class SenseiServiceProxy:
  """Sensei client class."""

  def __init__(self, host='localhost', port=8080, path='sensei', sysinfo=None):
    self.host = host
    self.port = port
    self.path = path
    self.url = 'http://%s:%d/%s' % (self.host, self.port, self.path)
    self.opener = urllib2.build_opener()
    self.opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.91 Safari/534.30')]

    if sysinfo:
      self.sysinfo = SenseiSystemInfo(sysinfo)
    else:
      urlReq = urllib2.Request(self.url + "/sysinfo")
      res = self.opener.open(urlReq)
      line = res.read()
      jsonObj = json.loads(line)
      # print json.dumps(jsonObj, indent=4)
      self.sysinfo = SenseiSystemInfo(jsonObj)
    self.facet_map = {}
    for facet_info in self.sysinfo.get_facet_infos():
      self.facet_map[facet_info.get_name()] = facet_info


  def buildJsonString(self, req, sort_keys=True, indent=None):
    """Build a Sensei request in JSON format.

    Once built, a Sensei request in JSON format can be sent to a Sensei
    broker using the following command:

    $ curl -XPOST http://localhost:8080/sensei -d '{
      "fetchStored": "true", 
      "from": 0, 
      "size": 10
    }'

    """

    output_json = {}

    output_json[JSON_PARAM_FROM] = req.offset
    output_json[JSON_PARAM_SIZE] = req.count

    if req.query:
      output_json[JSON_PARAM_QUERY] = req.query

    if req.explain:
      output_json[JSON_PARAM_QUERY] = req.explain
    if req.fetch_stored:
      output_json[JSON_PARAM_FETCH_STORED] = req.fetch_stored
    if req.route_param:
      output_json[JSON_PARAM_ROUTEPARAM] = req.route_param
    if req.sorts:
      output_json[JSON_PARAM_SORT] = [sort.build_sort_spec() for sort in req.sorts]

    if req.filter:
      output_json[JSON_PARAM_FILTER] = req.filter

    if req.query_pred:
      output_json[JSON_PARAM_QUERY] = req.query_pred[JSON_PARAM_QUERY]

    if req.selections:
      output_json[JSON_PARAM_SELECTIONS] = req.selections

    if req.facets:
      output_json[JSON_PARAM_FACETS]=req.facets
      
    facet_init_map = {}
    for facet_name, initParams in req.facet_init_param_map.iteritems():
      inner_map = {}
      for name, vals in initParams.bool_map.iteritems():
        inner_map[name] = {PARAM_DYNAMIC_TYPE : PARAM_DYNAMIC_TYPE_BOOL,
                           "values" : vals}
      for name, vals in initParams.int_map.iteritems():
        inner_map[name] = {PARAM_DYNAMIC_TYPE : PARAM_DYNAMIC_TYPE_INT,
                           "values" : [safe_str(val) for val in vals]}
      for name, vals in initParams.long_map.iteritems():
        inner_map[name] = {PARAM_DYNAMIC_TYPE : PARAM_DYNAMIC_TYPE_LONG,
                           "values" : [safe_str(val) for val in vals]}
      for name, vals in initParams.string_map.iteritems():
        inner_map[name] = {PARAM_DYNAMIC_TYPE : PARAM_DYNAMIC_TYPE_STRING,
                           "values" : vals}
      for name, vals in initParams.byte_map.iteritems():
        inner_map[name] = {PARAM_DYNAMIC_TYPE : PARAM_DYNAMIC_TYPE_BYTEARRAY,
                           "values" : [safe_str(val) for val in vals]}
      for name, vals in initParams.double_map.iteritems():
        inner_map[name] = {PARAM_DYNAMIC_TYPE : PARAM_DYNAMIC_TYPE_DOUBLE,
                           "values" : [safe_str(val) for val in vals]}
      facet_init_map[facet_name] = inner_map
    if facet_init_map:
      output_json[JSON_PARAM_FACET_INIT] = facet_init_map

    if req.groupby:
      # For now we only support group-by on single column
      output_json[JSON_PARAM_GROUPBY] = {
        JSON_PARAM_COLUMNS: [req.groupby],
        JSON_PARAM_TOP: req.max_per_group
        }

    # print ">>> output_json = ", output_json
    return json.dumps(output_json, sort_keys=sort_keys, indent=indent)

  @staticmethod
  def buildUrlString(req):
    paramMap = {}
    paramMap[PARAM_OFFSET] = req.offset
    paramMap[PARAM_COUNT] = req.count
    if req.query:
      paramMap[PARAM_QUERY]=req.query
    if req.explain:
      paramMap[PARAM_SHOW_EXPLAIN] = "true"
    if req.fetch_stored:
      paramMap[PARAM_FETCH_STORED] = "true"
    if req.route_param:
      paramMap[PARAM_ROUTE_PARAM] = req.route_param

    if req.sorts:
      paramMap[PARAM_SORT] = ",".join(sort.build_sort_field() for sort in req.sorts)

    if req.qParam.get("query"):
      paramMap[PARAM_QUERY] = req.qParam.get("query")
      del req.qParam["query"]
    if req.qParam:
      paramMap[PARAM_QUERY_PARAM] = ",".join(param + ":" + req.qParam.get(param)
                                             for param in req.qParam.keys() if param != "query")

    for selection in req.selections.values():
      paramMap[selection.getSelectNotParam()] = selection.getSelectNotParamValues()
      paramMap[selection.getSelectOpParam()] = selection.operation
      paramMap[selection.getSelectValParam()] = selection.getSelectValParamValues()
      if selection.properties:
        paramMap[selection.getSelectPropParam()] = selection.getSelectPropParamValues()
    
    
    for facet_name, facet_spec in req.facets.iteritems():
      paramMap["%s.%s.%s" % (PARAM_FACET, facet_name, PARAM_FACET_MAX)] = facet_spec.maxCounts
      paramMap["%s.%s.%s" % (PARAM_FACET, facet_name, PARAM_FACET_ORDER)] = facet_spec.orderBy
      paramMap["%s.%s.%s" % (PARAM_FACET, facet_name, PARAM_FACET_EXPAND)] = facet_spec.expand and "true" or "false"
      paramMap["%s.%s.%s" % (PARAM_FACET, facet_name, PARAM_FACET_MINHIT)] = facet_spec.minHits

    for facet_name, initParams in req.facet_init_param_map.iteritems():
      for name, vals in initParams.bool_map.iteritems():
        paramMap["%s.%s.%s.%s" %
                 (PARAM_DYNAMIC_INIT, facet_name, name, PARAM_DYNAMIC_TYPE)] = PARAM_DYNAMIC_TYPE_BOOL
        paramMap["%s.%s.%s.%s" %
                 (PARAM_DYNAMIC_INIT, facet_name, name,
                  PARAM_DYNAMIC_VAL)] = ','.join([val and "true" or "false" for val in vals])
      for name, vals in initParams.int_map.iteritems():
        paramMap["%s.%s.%s.%s" %
                 (PARAM_DYNAMIC_INIT, facet_name, name, PARAM_DYNAMIC_TYPE)] = PARAM_DYNAMIC_TYPE_INT
        paramMap["%s.%s.%s.%s" %
                 (PARAM_DYNAMIC_INIT, facet_name, name,
                  PARAM_DYNAMIC_VAL)] = ','.join([safe_str(val) for val in vals])
      for name, vals in initParams.long_map.iteritems():
        paramMap["%s.%s.%s.%s" %
                 (PARAM_DYNAMIC_INIT, facet_name, name, PARAM_DYNAMIC_TYPE)] = PARAM_DYNAMIC_TYPE_LONG
        paramMap["%s.%s.%s.%s" %
                 (PARAM_DYNAMIC_INIT, facet_name, name,
                  PARAM_DYNAMIC_VAL)] = ','.join([safe_str(val) for val in vals])
      for name, vals in initParams.string_map.iteritems():
        paramMap["%s.%s.%s.%s" %
                 (PARAM_DYNAMIC_INIT, facet_name, name, PARAM_DYNAMIC_TYPE)] = PARAM_DYNAMIC_TYPE_STRING
        paramMap["%s.%s.%s.%s" %
                 (PARAM_DYNAMIC_INIT, facet_name, name,
                  PARAM_DYNAMIC_VAL)] = ','.join(vals)
      for name, vals in initParams.byte_map.iteritems():
        paramMap["%s.%s.%s.%s" %
                 (PARAM_DYNAMIC_INIT, facet_name, name, PARAM_DYNAMIC_TYPE)] = PARAM_DYNAMIC_TYPE_BYTEARRAY
        paramMap["%s.%s.%s.%s" %
                 (PARAM_DYNAMIC_INIT, facet_name, name,
                  PARAM_DYNAMIC_VAL)] = ','.join([safe_str(val) for val in vals])
      for name, vals in initParams.double_map.iteritems():
        paramMap["%s.%s.%s.%s" %
                 (PARAM_DYNAMIC_INIT, facet_name, name, PARAM_DYNAMIC_TYPE)] = PARAM_DYNAMIC_TYPE_DOUBLE
        paramMap["%s.%s.%s.%s" %
                 (PARAM_DYNAMIC_INIT, facet_name, name,
                  PARAM_DYNAMIC_VAL)] = ','.join([safe_str(val) for val in vals])

    if req.groupby:
      paramMap[PARAM_GROUP_BY] = req.groupby
      if req.max_per_group > 0:
        paramMap[PARAM_MAX_PER_GROUP] = req.max_per_group

    return urllib.urlencode(paramMap)
    
  def doQuery(self, req, using_json=True):
    """Execute a search query."""

    time1 = datetime.now()
    query_string = None
    if using_json: # Use JSON format
      query_string = self.buildJsonString(req)
    else:
      query_string = SenseiClient.buildUrlString(req)
    logger.debug(query_string)
    urlReq = urllib2.Request(self.url, query_string)
    res = self.opener.open(urlReq)
    line = res.read()
    jsonObj = json.loads(line)
    res = SenseiResult(jsonObj)
    delta = datetime.now() - time1
    res.total_time = delta.seconds * 1000 + delta.microseconds / 1000
    return res

  def get(self, ids):
    """Get the source data through a list of document IDs.
       The input is either a list of ID numbers, or ID strings;
       The output is a jsonarray string;
    """
    ids_str = '['
    count = 0
    for id in ids:
      if count == 0 :
        ids_str = ids_str + str(id)
      else:
        ids_str = ids_str + ',' + str(id)
    ids_str = ids_str+ ']'
    ids = '[1,2]'
    urlReq = urllib2.Request(self.url + '/get', ids_str)
    res = self.opener.open(urlReq)
    #print res.read()
    return res.read()

  def get_sysinfo(self):
    return self.sysinfo

  def get_facet_map(self):
    return self.facet_map
  


def main(argv):

  # create a sample sensei request
    
  req = SenseiRequest()
    
  # add paging info;
  req.set_count(50)    \
  .set_offset(0)
    
  # add query info;
  req.set_query(SenseiQueryTerm("tags", "automatic"))
    
  # add selection info;
  range_selection = SenseiSelectionRange("year", "1995", "2000", True, False)  # [1995 TO 2000)
  req.append_selection(range_selection)
    
  # add filter info;
  req.set_filter(SenseiFilterRange("price", 7900, 11000))
    
  # add group by;
  req.set_groupby("category").set_max_per_group(4)
    
  # add sort;
  req.append_sort(SenseiSort("color", True))
    
  # add fetch_stored
  req.set_fetch_stored(False)
    
  # need explain or not
  req.set_explain(False)
    
  # add facets information
  facets = SenseiFacets().add_facet("color", False, 1, 10, "hits")  \
                         .add_facet("year")
  req.set_facets(facets)
    
  # execute and display results;
  proxy = SenseiServiceProxy()
  sensei_results = proxy.doQuery(req)
  sensei_results.display(["*"], max_col_width=40)
  
  print proxy.get([1,2])
  
  print proxy.get(['1','2'])

if __name__ == "__main__":
  main(sys.argv)
