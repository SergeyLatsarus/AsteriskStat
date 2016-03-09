# -*- coding: utf-8 -*-
from dashboard import Dashboard
import salesforce_config as sfconf
from simple_salesforce import Salesforce
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def main():

    credentials = sfconf.credentials
    sf = Salesforce(username = credentials['username'], password = credentials['password'],\
                                 security_token = credentials['security_token'])


    sales_managers_profile_id = '00eb0000000YXJL'
    users = sf.query('SELECT Id, Name FROM User WHERE profileid = \'%s\' AND isActive = true ' % sales_managers_profile_id)

    active_users = []
    users = users['records']

    for user in users:
        active_users.append(str(user['Id']))

    active_users = str(active_users).replace('[','(').replace(']',')')

    funding_by_users_query = "SELECT AccountId__r.ownerid, sum(amount__c) FROM AForexEvent__c WHERE EventType__c = 'funding' \
                              AND DateTimeOfEvent__c = THIS_MONTH AND AccountId__r.ownerid in %s GROUP BY ROLLUP(AccountId__r.ownerid)"

    withdrawal_by_users_query = "SELECT AccountId__r.ownerid, sum(amount__c) FROM AForexEvent__c WHERE EventType__c = 'Withdrawal' \
                                 AND DateTimeOfEvent__c = THIS_MONTH AND AccountId__r.ownerid in %s GROUP BY ROLLUP(AccountId__r.ownerid)"

    converted_leads_by_users_query = "SELECT Account__r.ownerid, count(Incentive_Deposit_Amount__c) FROM  Wallet__c WHERE First_Funding_Date__c = THIS_MONTH \
                                      AND Incentive_Deposit_Amount__c > 95 AND Account__r.ownerid in %s GROUP BY ROLLUP(Account__r.ownerid)"

    sum_of_incentive_deposites_by_users_query = "SELECT Account__r.ownerid, sum(Incentive_Deposit_Amount__c) FROM  Wallet__c \
                                                 WHERE First_Funding_Date__c = THIS_MONTH AND Account__r.ownerid in %s GROUP BY ROLLUP(Account__r.ownerid)"


    funding_by_users, funding_user_names = Dashboard(active_users, funding_by_users_query).get_salesforce_data()
    withdrawal_by_users, withdrawal_user_names = Dashboard(active_users, withdrawal_by_users_query).get_salesforce_data()
    converted_leads_by_users, converted_leads_user_names = Dashboard(active_users, converted_leads_by_users_query).get_salesforce_data()
    sum_of_incentive_deposites_by_users,  sum_of_incentive_user_names = Dashboard(active_users, sum_of_incentive_deposites_by_users_query).get_salesforce_data()

    return funding_by_users, funding_user_names, withdrawal_by_users, withdrawal_user_names, \
           converted_leads_by_users, converted_leads_user_names, sum_of_incentive_deposites_by_users,  sum_of_incentive_user_names