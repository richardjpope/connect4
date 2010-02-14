import json
import urllib
import urllib2

class Connect4:

    # properties
    _terms = []
    _matrix = []

    # constructor
    def __init__(self, terms = [], search_type = 'google'):
        self._terms = terms
        self._build_matrix()
        self._populate_matrix()
        
        if search_type not in self.list_search_types():
            print "Unsupported seach type, see grid.list_search_types() for a list of available search types"
            raise Exception()
        elif search_type == 'google':
            self._set_from_google_search()
    
     #supported search types
    def list_search_types(self):
    
        return ['google',]

    # get column names
    def get_column_names(self):
        return self._terms

    # get row names
    def get_row_names(self):
        return self._terms        
    
    # get data
    def get_matrix(self):
        retun self._matrix
    
    # print the matrix as a grid
    def to_string(self):
        result = ''

        # work out the length of the longest title
        max_length = 0
        padding = 3
        for term in self._terms:
            if len(term) > max_length:
                max_length = len(term)

        # column titles
        result += ''.ljust(max_length + padding)
        for col in self._terms:
            result += col.ljust(max_length + padding)
        result += '\n'

        result += '-'.ljust(max_length + padding, '-')
        for col in self._terms:
            result += '-'.ljust(max_length + padding, '-')
        result += '\n'

        # row columns and data
        row_position = 0
        for row in self._terms:
            result += row.ljust(max_length) + '  | '
            for col_position in range(0, len(self._terms)):
                # if the col and rown not the same term, print it out, else just print a '-'
                value = '-'
                if row_position != col_position:
                    value = self._get_item(col_position, row_position)
                result += str(value).ljust(max_length) + '  | '
            result += '\n'

            row_position = row_position + 1

        return result
                    
    # generate the matrix
    def _build_matrix(self):
       for row in self._terms:
            ea_row = []
            for col in self._terms:
                ea_row.append(0)
            self._matrix.append(ea_row)

    def _populate_matrix(self):            
        for i in range(0, len(self._terms)):
            for ii in range(0, len(self._terms)):
                self._set_item(i, ii, None)

    def _set_item(self, col, row, v):
        self._matrix[col-1][row-1] = v

    def _get_item(self, col, row):
        return self._matrix[col-1][row-1]

    def _set_from_google_search(self):

        #keep track of position
        col_position = 0
        row_position = 0

        # loop through teh matrix
        for col in self._terms:
            for row in self._terms:
                
                #get the count for this position
                search_count = self._get_google_search_count([col, row])
                self._set_item(col_position, row_position, search_count)
                row_position = row_position + 1
            
            #reset row position and skip to next column
            row_position = 0
            col_position = col_position + 1
    

    # get a google search count for a list of terms, terms are combined for the search
    def _get_google_search_count(self, search_terms):
        result_count = 0
        
        encoded_terms = []
        for search_term in search_terms:
            encoded_terms.append('"' + urllib.quote(search_term) + '"')

        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s' % '%20'.join(encoded_terms)
        fin = urllib2.urlopen(url)
        text = unicode(fin.read(), errors="replace").encode("ascii", "ignore")
        fin.close()

        json_data = json.loads(text)
        response_status = json_data['responseStatus']
        if response_status == 200 and json_data.has_key('responseData'):           
                if json_data['responseData'].has_key('cursor'):
                    if json_data['responseData']['cursor'].has_key('estimatedResultCount'):
                        result_count = json_data['responseData']['cursor']['estimatedResultCount']


        return result_count    
