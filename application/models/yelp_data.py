from application import mongodb, app
from yelpapi import YelpAPI
import datetime


class YelpData(object):
    """
    This class will complete handle the calls for Yelp Data
    Business API - business_query()
    Business Match API - business_match_query()
    Reviews API - reviews_query()
    """
    def __init__(self):
        self.business_match = mongodb.db.business_match
        self.business_details = mongodb.db.business_details
        self.business_reviews = mongodb.db.business_reviews
        self.yelp_req = mongodb.db.yelp_request
        self.yelp_api = YelpAPI(app.config['YELP_API_KEY'])
        self.response = None

    @staticmethod
    def _remove_keys(json_data):
        del json_data['user_id']
        del json_data['_id']
        return json_data

    def get_business_match_data(self, user_id=None, name=None, address1='', address2=None, address3=None, city=None, state=None,
                                country=None, latitude=None, longitude=None, phone=None, zip_code=None,
                                yelp_business_id=None, limit=1, match_threshold='default'):
        """
                    Link: https://www.yelp.com/developers/documentation/v3/business_match
                    required parameters:
                        * name - business name
                        * city
                        * state
                        * country
        """
        self.response = self.yelp_api.business_match_query(name=name, address1=address1, address2=address2,
                                                           address3=address3, city=city, state=state, country=country,
                                                           latitude=latitude, longitude=longitude, phone=phone,
                                                           zip_code=zip_code, yelp_business_id=yelp_business_id,
                                                           limit=limit, match_threshold=match_threshold)
        self.response['user_id'] = user_id
        self.business_match.insert_one(self.response)
        self.response = self._remove_keys(self.response)
        return self.response

    def get_business_details(self, business_id, user_id):
        self.response = self.yelp_api.business_query(id=business_id)
        self.response['user_id'] = user_id
        self.business_details.insert_one(self.response)
        self.response = self._remove_keys(self.response)
        return self.response

    def get_business_reviews(self, business_id, user_id):
        self.response = self.yelp_api.reviews_query(id=self.business_id)
        self.response['user_id'] = user_id
        self.business_reviews.insert_one(self.response)
        self.response = self._remove_keys(self.response)
        return self.response

    def yelp_request(self, yelp_request, user_id):
        yelp_request['req_datetime'] = datetime.datetime.now()
        yelp_request['user_id'] = user_id
        return self.yelp_req.insert_one(yelp_request).acknowledged
