import salesforce_config as sfconf
from simple_salesforce import Salesforce
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Dashboard(object):

    def __init__(self, active_users, query_string):

        self.credentials = sfconf.credentials
        self.active_users = active_users
        self.query_string = query_string
        self.sf = Salesforce(username = self.credentials['username'], password = self.credentials['password'],\
                             security_token = self.credentials['security_token'])


    def get_salesforce_data(self):

        query_results = self.sf.query(self.query_string % self.active_users)
        query_results = query_results['records']
        result = {}
        users = self.sf.query('SELECT id, Name FROM User WHERE isActive = true')
        users = users['records']
        user_names = {}
        sales_names = []
        print query_results

        for user in users:
            user_names[user['Id']] =user['Name']

        for query_result in query_results:
            if user_names.has_key(query_result['OwnerId']):
                result[user_names[query_result['OwnerId']]] = query_result['expr0']
                sales_names.append(user_names[query_result['OwnerId']])

        return result, sales_names