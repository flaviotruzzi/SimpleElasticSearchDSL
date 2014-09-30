__author__ = 'ftruzzi'


class Query(object):

    def __init__(self):
        self.query_type = 'query'
        self.options = set()

    @staticmethod
    def __process_attribute__(attribute):
        if isinstance(attribute, Query):
            return attribute.generate()
        elif isinstance(attribute, list):
            return [Query.__process_attribute__(inner_attribute) for inner_attribute in attribute]
        else:
            return attribute

    def __setup__(self, slots=None):
        if slots:
            return {option: self.__process_attribute__(self.__getattribute__(option)) for option in slots if
                    self.__getattribute__(option)}
        else:
            return {option: self.__process_attribute__(self.__getattribute__(option)) for option in
                    self.__valid_keys__() if self.__getattribute__(option)}

    def __valid_keys__(self):
        for key in self.__dict__:
            if key in self.options:
                yield key

    def generate(self):
        query = {'query': {self.query_type: {}}}
        query['query'][self.query_type].update(self.__setup__())
        return query


class MatchQuery(Query):

    def __init__(self, field, query, operator=None, minimum_should_match=None, analyzer=None, fuzziness=None,
                 prefix_length=None, max_expansions=None, zero_terms_query=None, cutoff_frequency=None):
        super(MatchQuery, self).__init__()
        self.field = field
        self.query = query
        self.operator = operator
        self.minimum_should_match = minimum_should_match
        self.analyzer = analyzer
        self.fuzziness = fuzziness
        self.prefix_length = prefix_length
        self.max_expansions = max_expansions
        self.zero_terms_query = zero_terms_query
        self.cutoff_frequency = cutoff_frequency
        self.query_type = "match"
        self.options = {'query', 'operator', 'minimum_should_match', 'analyzer', 'fuzziness', 'prefix_length', 'max_expansions',
                        'zero_terms_query', 'cutoff_frequency'}

    def generate(self):
        query = {'query': {self.query_type: {self.field: {}}}}
        query['query'][self.query_type][self.field].update(self.__setup__())
        return query


class MatchAllQuery(MatchQuery):
    def __init__(self, field, **kwargs):
        super(MatchAllQuery, self).__init__(field, query="", **kwargs)
        self.zero_terms_query = 'all'

    def generate(self):
        query = super(MatchAllQuery, self).generate()
        query['query'][self.query_type][self.field]['query'] = ""
        return query


class MatchPhraseQuery(MatchQuery):

    def __init__(self, field, query, slop=None, **kwargs):
        super(MatchPhraseQuery, self).__init__(field, query, **kwargs)
        self.type = "phrase"
        self.slop = slop
        self.options.update({'slop', 'type'})


class MultiMatch(Query):
    __slots__ = ['fields', 'query', 'type', 'tie_breaker', 'analyzer',
                 'boost', 'operator', 'minimum_should_match', 'fuzziness',
                 'prefix_length', 'max_expansions', 'zero_terms_query',
                 'rewrite', 'cutoff_frequency']

    def __init__(self, fields, query, type=None, tie_breaker=None, minimum_should_match=None, cutoff_frequency=None,
                 zero_terms_query=None, max_expansions=None, prefix_length=None, fuzziness=None, analyzer=None,
                 boost=None, operator=None, rewrite=None):
        super(MultiMatch, self).__init__()
        self.fields = fields
        self.query = query
        self.type = type
        self.tie_breaker = tie_breaker
        self.minimum_should_match = minimum_should_match
        self.analyzer = analyzer
        self.fuzziness = fuzziness
        self.prefix_length = prefix_length
        self.max_expansions = max_expansions
        self.zero_terms_query = zero_terms_query
        self.cutoff_frequency = cutoff_frequency
        self.boost = boost
        self.operator = operator
        self.rewrite = rewrite


class BoolQuery(Query):
    __slots__ = ['must', 'must_not', 'should', 'minimum_should_match', 'disable_coord', 'boost']

    def __init__(self, must=None, must_not=None, should=None, minimum_should_match=None, disable_coord=None,
                 boost=None):
        super(BoolQuery, self).__init__()
        self.must = must
        self.must_not = must_not
        self.should = should
        self.minimum_should_match = minimum_should_match
        self.disable_coord = disable_coord
        self.boost = boost
        self.query_type = 'bool'


class BoostingQuery(Query):
    __slots__ = ['positive', 'negative', 'negative_boost']

    def __init__(self, positive=None, negative=None, negative_boost=None):
        super(BoostingQuery, self).__init__()
        self.positive = positive
        self.negative = negative
        self.negative_boost = negative_boost
        self.query_type = 'boosting'


class CommonTermsQuery(Query):
    __slots__ = ['query', 'field', 'low_freq_operator', 'boost', 'analyzer', 'disable_coord', 'minimum_should_match',
                 'cutoff_frequency']

    def __init__(self, query, field, low_freq_operator=None, boost=None, analyzer=None, disable_coord=None,
                 minimum_should_match=None, cutoff_frequency=None):
        super(CommonTermsQuery, self).__init__()
        self.query = query
        self.field = field
        self.low_freq_operator = low_freq_operator
        self.boost = boost
        self.analyzer = analyzer
        self.disable_coord = disable_coord
        self.minimum_should_match = minimum_should_match
        self.cutoff_frequency = cutoff_frequency
        self.query_type = 'common'


class ConstantScoreQuery(Query):
    __slots__ = ['filter', 'boost']

    def __init__(self, filter, boost=None):
        super(ConstantScoreQuery, self).__init__()
        self.filter = filter
        self.boost = boost
        self.query_type = 'constant_score'


class TermQuery(Query):
    __slots__ = ['field', 'query', 'boost']

    def __init__(self, field, query, boost=None):
        super(TermQuery, self).__init__()
        self.field = field
        self.query = query
        self.boost = boost
        self.query_type = 'term'

    def generate(self):
        query = {self.query_type: {self.field: {'value': self.query}}}
        if self.boost:
            query[self.query_type][self.field].update({'boost': self.boost})
        return query


class DisMaxQuery(Query):
    __slots__ = ['queries', 'boost', 'tie_breaker']

    def __init__(self, queries, boost=None, tie_breaker=None):
        super(DisMaxQuery, self).__init__()
        self.queries = queries
        self.boost = boost
        self.tie_breaker = tie_breaker
        self.query_type = 'dis_max'


class FilteredQuery(Query):
    __slots__ = ['query', 'filter', 'strategy']

    def __init__(self, query=None, filter=None, strategy=None):
        super(FilteredQuery, self).__init__()
        self.query = query
        self.filter = filter
        self.strategy = strategy
        self.query_type = 'filtered'


# FilteredQuery(query=MatchQuery("tweet", "full text search"),
# filter=BoolQuery(should=[TermQuery("featured", True),
#                                        TermQuery("starred", True)],
#                                must_not=TermQuery("deleted", False)))


class FuzzyLikeThis(Query):
    __slots__ = ['like_text', 'fields', 'max_query_terms', 'ignore_tf', 'max_query_terms', 'fuzziness', 'boost',
                 'analyzer', 'prefix_length']

    def __init__(self, like_text, fields=None, max_query_terms=None, ignore_tf=None, fuzziness=None, boost=None,
                 analyzer=None, prefix_length=None):
        super(FuzzyLikeThis, self).__init__()
        self.prefix_length = prefix_length
        self.max_query_terms = max_query_terms
        self.like_text = like_text
        self.fields = fields
        self.max_query_terms = max_query_terms
        self.ignore_tf = ignore_tf
        self.max_query_terms = max_query_terms
        self.fuzziness = fuzziness
        self.boost = boost
        self.analyzer = analyzer
        self.query_type = 'fuzzy_like_this'


class FuzzyLikeThisField(Query):
    __slots__ = ['like_text', 'field', 'max_query_terms', 'ignore_tf', 'fuzziness', 'boost', 'analyzer',
                 'prefix_length']

    def __init__(self, like_text, field, max_query_terms=None, ignore_tf=None, fuzziness=None, boost=None,
                 analyzer=None, prefix_length=None):
        super(FuzzyLikeThisField, self).__init__()
        self.query_type = 'fuzzy_like_this_field'
        self.like_text = like_text
        self.field = field
        self.ignore_tf = ignore_tf
        self.fuzziness = fuzziness
        self.boost = boost
        self.analyzer = analyzer
        self.prefix_length = prefix_length
        self.max_query_terms = max_query_terms


class ScriptScore(Query):
    __slots__ = ['script', 'lang', 'params']

    def __init__(self, script, lang=None, params=None):
        super(ScriptScore, self).__init__()
        self.params = params
        self.lang = lang
        self.script = script
        self.query_type = 'script_score'


class RandomScore(Query):
    __slots__ = ['seed']

    def __init__(self, seed):
        super(RandomScore, self).__init__()
        self.seed = seed
        self.query_type = 'random_score'


class FieldValueFactor(Query):
    __slots__ = ['field', 'factor', 'modifier']

    def __init__(self, field, factor, modifier=None):
        super(FieldValueFactor, self).__init__()
        self.query_type = 'field_value_factor'
        self.field = field
        self.factor = factor
        self.modifier = modifier


#TODO: implement decay function


class FunctionScoreQuery(Query):
    def __init__(self, query=None, filter=None, boost=None, functions=None, boost_mode=None, max_boost=None,
                 score_mode=None):
        super(FunctionScoreQuery, self).__init__()
        self.query = query
        self.boost = boost
        self.functions = functions
        self.boost_mode = boost_mode
        self.max_boost = max_boost
        self.score_mode = score_mode
        self.filter = filter
        self.query_type = 'function_score'


class FuzzyQuery(Query):
    __slots__ = ['field', 'value', 'boost', 'fuzziness', 'prefix_length', 'max_expansions']

    def __init__(self, field, value, boost=None, fuzziness=None, prefix_length=None, max_expansions=None):
        super(FuzzyQuery, self).__init__()
        self.query_type = 'fuzzy'
        self.field = field
        self.value = value
        self.boost = boost
        self.fuzziness = fuzziness
        self.prefix_length = prefix_length
        self.max_expansions = max_expansions

    def generate(self):
        query = {self.query_type: {self.field: {}}}
        query[self.query_type][self.field].update(self.__setup__(('boost', 'fuzziness', 'prefix_length',
                                                                  'max_expansions')))
        return query


FuzzyQuery("user", "ki", boost=1.0, fuzziness=2, prefix_length=0, max_expansions=100)


#TODO: Create GeoShapeQuery


class HasChild(Query):
    __slots__ = ['query', 'type', 'score_mode', 'min_children', 'max_children']

    def __init__(self, query, type, score_mode=None, min_children=None, max_children=None):
        super(HasChild, self).__init__()
        self.score_mode = score_mode
        self.min_children = min_children
        self.max_children = max_children
        self.query = query
        self.type = type


class HasParent(HasChild):
    def __init__(self, **kwargs):
        super(HasParent, self).__init__(**kwargs)
        self.query_type = 'has_parent'


class IdsQuery(Query):
    __slots__ = ['type', 'values']

    def __init__(self, values, type=None):
        super(IdsQuery, self).__init__()
        self.query_type = 'ids'
        self.type = type
        self.values = values


class IndicesQuery(Query):
    __slots__ = ['query', 'indices', 'index', 'no_match_query']

    def __init__(self, query, indices=None, index=None, no_match_query=None):
        super(IndicesQuery, self).__init__()
        self.query = query
        self.indices = indices
        self.index = index
        self.no_match_query = no_match_query
        self.query_type = 'indices'
        assert indices or index


class MoreLikeThisQuery(Query):
    __slots__ = ['like_text', 'fields', 'min_term_freq', 'max_query_terms', 'docs', 'ids', 'include',
                 'percent_terms_to_match', 'stop_words', 'min_doc_freq', 'max_doc_freq', 'min_word_length',
                 'max_word_length', 'boost', 'analyzer']

    def __init__(self, like_text, fields, min_term_freq=None, max_query_terms=None, docs=None, ids=None, include=None,
                 percent_terms_to_match=None, stop_words=None, min_doc_freq=None, max_doc_freq=None,
                 min_word_length=None, max_word_length=None, boost=None, analyzer=None):
        super(MoreLikeThisQuery, self).__init__()
        self.like_text = like_text
        self.fields = fields
        self.min_term_freq = min_term_freq
        self.max_query_terms = max_query_terms
        self.docs = docs
        self.ids = ids
        self.include = include
        self.percent_terms_to_match = percent_terms_to_match
        self.stop_words = stop_words
        self.min_doc_freq = min_doc_freq
        self.max_doc_freq = max_doc_freq
        self.min_word_length = min_word_length
        self.max_word_length = max_word_length
        self.boost = boost
        self.analyzer = analyzer
        self.query_type = 'more_like_this'


class MoreLikeThisFieldQuery(MoreLikeThisQuery):
    def __init__(self, like_text, field, **kwargs):
        super(MoreLikeThisFieldQuery, self).__init__(like_text, field, **kwargs)
        self.query_type = 'more_like_this_field'

    def generate(self):
        query = {self.query_type: {self.fields: {}}}
        query[self.query_type][self.fields].update(self.__setup__(self.__slots__[2:]))


class NestedQuery(Query):
    __slots__ = ['path', 'score_mode', 'query']

    def __init__(self, query, path, score_mode):
        super(NestedQuery, self).__init__()
        self.query = query
        self.path = path
        self.score_mode = score_mode
        self.query_type = 'nested'


#print(NestedQuery(BoolQuery(must=[MatchQuery("obj1.name", "blue")]), path="obj1", score_mode="avg").generate())


class PrefixQuery(Query):
    __slots__ = ['query', 'field', 'boost']

    def __init__(self, query, field, boost=None):
        super(PrefixQuery, self).__init__()
        self.query_type = 'prefix'
        self.query = query
        self.field = field
        self.boost = boost

    def generate(self):
        query = {self.query_type: {self.field: {'value': self.query, 'boost': self.boost}}}
        return query


class QueryStringQuery(Query):
    __slots__ = ['query', 'default_field', 'default_operator', 'tie_breaker', 'use_dis_max', 'fields', 'rewrite',
                 'locale', 'lenient', 'minimum_should_match', 'auto_generate_phrase_queries', 'analyze_wildcard',
                 'boost', 'phrase_slop', 'fuzzy_prefix_length', 'fuzziness', 'fuzzy_max_expansions',
                 'enable_position_increments', 'lowercase_expanded_terms', 'allow_leading_wildcard', 'analyzer']

    def __init__(self, query=None, default_field=None, default_operator=None, tie_breaker=None, use_dis_max=None,
                 fields=None, rewrite=None, locale=None, lenient=None, minimum_should_match=None,
                 auto_generate_phrase_queries=None, analyze_wildcard=None, boost=None, phrase_slop=None,
                 fuzzy_prefix_length=None, fuzziness=None, fuzzy_max_expansions=None, enable_position_increments=None,
                 lowercase_expanded_terms=None, allow_leading_wildcard=None, analyzer=None):
        super(QueryStringQuery, self).__init__()
        self.query_type = 'query_string'
        self.default_field = default_field
        self.default_operator = default_operator
        self.analyzer = analyzer
        self.allow_leading_wildcard = allow_leading_wildcard
        self.lowercase_expanded_terms = lowercase_expanded_terms
        self.enable_position_increments = enable_position_increments
        self.fuzzy_max_expansions = fuzzy_max_expansions
        self.fuzziness = fuzziness
        self.fuzzy_prefix_length = fuzzy_prefix_length
        self.phrase_slop = phrase_slop
        self.boost = boost
        self.analyze_wildcard = analyze_wildcard
        self.auto_generate_phrase_queries = auto_generate_phrase_queries
        self.minimum_should_match = minimum_should_match
        self.lenient = lenient
        self.locale = locale
        self.rewrite = rewrite
        self.fields = fields
        self.use_dis_max = use_dis_max
        self.tie_breaker = tie_breaker
        self.query = query


# stopped at http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/query-dsl-nested-query.html






























