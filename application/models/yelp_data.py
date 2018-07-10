from application import mongodb, app
from yelpapi import YelpAPI

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
        self.yelp_api = YelpAPI(app.config['YELP_API_KEY'])
        self.business_id = None
        self.response = None

    def get_business_match_data(self, name=None, address1='', address2=None, address3=None, city=None, state=None,
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
        # self.business_match.insert(self.response)
        print(self.response)
        # self.business_id = dict(self.response)['id']
        return self.response

    def get_business_details(self):
        self.response = self.yelp_api.business_query(id=self.business_id)
        self.business_details.insert(self.response)
        return self.response

    def get_business_reviews(self):
        self.response = self.yelp_api.reviews_query(id=self.business_id)
        self.business_reviews.insert(self.response)
        return self.response
