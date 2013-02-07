""" PredictoinIO Python-SDK Package

This PredictoinIO Python-SDK package provides easy-to-use functions for integrating 
Python applications with PredictionIO REST API services.

"""

__author__ = "TappingStone"
__email__ = "help@tappingstone.com"
__copyright__ = "Copyright 2012, TappingStone"
__license__ = "Apache License, Version 2.0"

__version__ = "0.1"


# import packages
import re
import httplib
import json
import urllib

from predictionio.connection import Connection
from predictionio.connection import AsyncRequest
from predictionio.connection import AsyncResponse
from predictionio.connection import PredictionIOAPIError

"""Error exception defined for this API

Should be handled by the user
"""
class UserNotCreatedError(PredictionIOAPIError):
    "Error happened when tried to create user"
    pass

class UserNotFoundError(PredictionIOAPIError):
    "Error happened when tried to get user"
    pass

class UserNotDeletedError(PredictionIOAPIError):
    "Error happened when tried to delete user"
    pass

class ItemNotCreatedError(PredictionIOAPIError):
    "Error happened when tried to create item"
    pass

class ItemNotFoundError(PredictionIOAPIError):
    "Error happened when tried to get item"
    pass

class ItemNotDeletedError(PredictionIOAPIError):
    "Error happened when tried to delete item"
    pass

class U2IActionNotCreatedError(PredictionIOAPIError):
    "Error happened when tried to create user-to-item action"
    pass

class ItemRecNotFoundError(PredictionIOAPIError):
    "Error happened when tried to get item recommendation"
    pass

class InvalidArgumentError(PredictionIOAPIError):
    "Arguments are not valid"
    pass


# map to API
LIKE_API = "like"
DISLIKE_API = "dislike"
VIEW_API = "view"
CONVERSION_API = "conversion"
RATE_API = "rate"

class Client:
    """PredictionIO client object.
    
    This is an object representing a PredictionIO's client. This object provides methods for making PredictionIO API requests.
    
    :param appkey: the App Key provided by PredictionIO.
    :param threads: number of threads to handle PredictionIO API requests. Must be >= 1.
    :param apiurl: the PredictionIO API URL path.
    :param apiversion: the PredictionIO API version. (optional) (eg. "", or "/v1")
    
    
    """
    def __init__(self, appkey, threads=1, apiurl="http://localhost:8000", apiversion = ""):
        """Constructor of Client object.
        
        :param appkey: the appkey
        :param threads: number of threads for handling requests
        :param apiurl: the PredictionIO API URL path.
        :param apiversion: the PredictionIO API version. (optional) (eg. "", or "/v1")
        
        """
        self.appkey = appkey
        self.threads = threads
        self.apiurl = apiurl
        self.apiversion = apiversion
        
        # check connection type
        https_pattern = r'^https://(.*)'
        http_pattern = r'^http://(.*)'
        m = re.match(https_pattern, apiurl)
        self.https = True
        if m is None: # not matching https
            m = re.match(http_pattern, apiurl)
            self.https = False
            if m is None: # not matching http either
                raise InvalidArgumentError("apiurl is not valid: %s" % apiurl)
        self.host = m.group(1)
        
        self._connection = Connection(host=self.host, threads=self.threads, https=self.https)
        
    def close(self):
        """Close this client and the connection.
        
        Call this method when you want to completely terminate the connection with PredictionIO.
        It will wait for all pending requests to finish.
        """
        self._connection.close()
               
    def acreate_user(self, uid, **params):
        """Asynchronously create a user.
        
        :param uid: user id. type str or int.
        :param params: keyword arguments for optional attributes.
                For example, bday="1985-01-23", inactive="true".
        
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
            
        """
        path = "%s/users.json" % self.apiversion
        request = AsyncRequest("POST", path, appkey=self.appkey, uid=uid, **params)
        request.set_rfunc(self._acreate_user_resp)
        self._connection.make_request(request)
        
        return request

    def _acreate_user_resp(self, response):
        """Private function to handle the AsyncResponse of the acreate_user request.
        
        :param response: AsyncResponse object.
        
        :returns: 
            None.
        
        :raises: 
            UserNotCreatedError.
        
        """
        if response.error is not None:
            raise UserNotCreatedError("Exception happened: %s for request %s" % \
                                      (response.error, response.request))
        elif response.status != httplib.CREATED:
            raise UserNotCreatedError("request: %s status: %s body: %s" % \
                                      (response.request, response.status, response.body))
        
        return None

    def aget_user(self, uid):
        """Asynchronously get user.
        
        :param uid: user id. type str or int.
            
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        if type(uid) is int:
            enc_uid = uid
        else:
            enc_uid = urllib.quote(uid,"") # replace special char with %xx
        path = "%s/users/%s.json" % (self.apiversion, enc_uid)
        request = AsyncRequest("GET", path, appkey=self.appkey)
        request.set_rfunc(self._aget_user_resp)
        self._connection.make_request(request)
        
        return request
    
    def _aget_user_resp(self, response):
        """Private function to handle the AsyncResponse of the aget_user request .
        
        :param response: AsyncResponse object.
        
        :returns: 
            User data in Dictionary format.
        
        :rasies: 
            UserNotFoundError.
        
        """
        if response.error is not None:
            raise UserNotFoundError("Exception happened: %s for request %s" % \
                                    (response.error, response.request))
        elif response.status != httplib.OK:
            raise UserNotFoundError("request: %s status: %s body: %s" % \
                                    (response.request, response.status, response.body))
        
        data = json.loads(response.body) # convert json string to dict
        return data
 
    def adelete_user(self, uid):
        """Asynchronously delete user.
        
        :param uid: user id. type str or int.
            
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        if type(uid) is int:
            enc_uid = uid
        else:
            enc_uid = urllib.quote(uid,"") # replace special char with %xx
        path = "%s/users/%s.json" % (self.apiversion, enc_uid)
        request = AsyncRequest("DELETE", path, appkey=self.appkey)
        request.set_rfunc(self._adelete_user_resp)
        self._connection.make_request(request)
        
        return request 
    
    def _adelete_user_resp(self, response):
        """Private function to handle the AsyncResponse of the adelete_user request.
        
        :param response: AsyncResponse object.
        
        :returns: 
            None.
            
        :raises: 
            UserNotDeletedError.
        
        """
        if response.error is not None:
            raise UserNotDeletedError("Exception happened: %s for request %s" % \
                                      (response.error, response.request))
        elif response.status != httplib.OK:
            raise UserNotDeletedError("request: %s status: %s body: %s" % \
                                      (response.request, response.status, response.body))
        return None
  
    def acreate_item(self, iid, itypes, **params):
        """Asynchronously create item.
        
        :param iid: item id. type str or int.
        :param itypes: item types. Tuple of Str.
                For example, if this item belongs to item types "t1", "t2", "t3", "t4",
                then itypes=("t1", "t2", "t3", "t4").
                NOTE: if this item belongs to only one itype, use tuple of one element, eg. itypes=("t1",)
        :param params: keyword arguments for optional attributes.
                For example, latlng="123.4, 56.7". 
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        itypes_str = ",".join(map(str, itypes)) # convert to string and join items with ","
        path = "%s/items.json" % self.apiversion
        request = AsyncRequest("POST", path, appkey=self.appkey, iid=iid, itypes=itypes_str, **params)
        request.set_rfunc(self._acreate_item_resp)
        self._connection.make_request(request)
        return request

    def _acreate_item_resp(self, response):
        """Private function to handle the AsyncResponse of the acreate_item request 
        
        :param response: AsyncResponse object.
        
        :returns: 
            None
        :raises: 
            ItemNotCreatedError
        
        """
        if response.error is not None:
            raise ItemNotCreatedError("Exception happened: %s for request %s" % \
                                      (response.error, response.request))
        elif response.status != httplib.CREATED:
            raise ItemNotCreatedError("request: %s status: %s body: %s" % \
                                      (response.request, response.status, response.body))
        return None
    
    def aget_item(self, iid):
        """Asynchronously get item
        
        :param iid: item id. type str or int.
            
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        if type(iid) is int:
            enc_iid = iid
        else:
            enc_iid = urllib.quote(iid, "")
        path = "%s/items/%s.json" % (self.apiversion, enc_iid)
        request = AsyncRequest("GET", path, appkey=self.appkey)
        request.set_rfunc(self._aget_item_resp)
        self._connection.make_request(request)
        return request
    
    def _aget_item_resp(self, response):
        """Private function to handle the AsyncResponse of the aget_item request 
        
        :param response: AsyncResponse object.
        
        :returns: 
            item data in dictionary format.
        
        :raises: 
            ItemNotFoundError.
        
        """
        if response.error is not None:
            raise ItemNotFoundError("Exception happened: %s for request %s" % \
                                    (response.error, response.request))
        elif response.status != httplib.OK:
            raise ItemNotFoundError("request: %s status: %s body: %s" % \
                                    (response.request, response.status, response.body))
        
        data = json.loads(response.body) # convert json string to dict
        return data
    
    def adelete_item(self, iid):
        """Asynchronously delete item
        
        :param iid: item id. type str or int.
            
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        if type(iid) is int:
            enc_iid = iid
        else:
            enc_iid = urllib.quote(iid, "")
        path = "%s/items/%s.json" % (self.apiversion, enc_iid)
        request = AsyncRequest("DELETE", path, appkey=self.appkey)
        request.set_rfunc(self._adelete_item_resp)
        self._connection.make_request(request)
        return request 
    
    def _adelete_item_resp(self, response):
        """Private function to handle the AsyncResponse of the adelete_item request 
        
        :param response: AsyncResponse object
        
        :returns:
            None
            
        :raises:
            ItemNotDeletedError
        """
        if response.error is not None:
            raise ItemNotDeletedError("Exception happened: %s for request %s" % \
                                      (response.error, response.request))
        elif response.status != httplib.OK:
            raise ItemNotDeletedError("request: %s status: %s body: %s" % \
                                      (response.request, response.status, response.body))
        return None
    
    def aget_itemrec(self, uid, n, engine, **params):
        """Asynchronously get recommendations
        
        :param uid: user id. type str or int.
        :param n: number of recommendation. type int.
        :param engine: name of the prediction engine. type str.
        :param params: keyword arguments for optional attributes.
                For example, latlng="123.4, 56.7" 
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """        
        if type(uid) is int:
            enc_uid = uid
        else:
            enc_uid = urllib.quote(uid,"") # replace special char with %xx
        path = "%s/engines/itemrec/%s/topn.json" % (self.apiversion, engine)
        request = AsyncRequest("GET", path, appkey=self.appkey, uid=enc_uid, n=n, **params)
        request.set_rfunc(self._aget_itemrec_resp)
        self._connection.make_request(request)
        return request

    def _aget_itemrec_resp(self, response):
        """Private function to handle the AsyncResponse of the aget_itemrec request 
        
        :param response: AsyncResponse object
        
        :returns:
            data in dictionary format.
            
        :raises:
            ItemRecNotFoundError.
        """
        if response.error is not None:
            raise ItemRecNotFoundError("Exception happened: %s for request %s" % \
                                               (response.error, response.request))
        elif response.status != httplib.OK:
            raise ItemRecNotFoundError("request: %s status: %s body: %s" % \
                                               (response.request, response.status, response.body))
        
        data = json.loads(response.body) # convert json string to dict
        return data

    def _auser_action_item(self, action, uid, iid, **params):
        """Asynchronously create an user action on an item
        
        :param action: action type. type str. ("like", "dislike", "conversion", "rate", "view")
        :param uid: user id. type str or int.
        :param iid: item id. type str or int.
        :param params: keyword arguments for optional attributes.
                For example, latlng="123.4, 56.7" 
                For "rate" action, rate param is required. integer value of 1-5 (1 is least preferred and 5 is most preferred) (eg. rate=4)
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        path = "%s/actions/u2i/%s.json" % (self.apiversion, action)
        request = AsyncRequest("POST", path, appkey=self.appkey, uid=uid, iid=iid, **params)
        request.set_rfunc(self._au2i_action_resp)
        self._connection.make_request(request)
        return request
    
    def _au2i_action_resp(self, response):
        """Private function to handle the AsyncResponse of the auser_ACTION_item request 
        
        :param response: AsyncResponse object
        
        :returns:
            None
            
        :raises:
            U2IActionNotCreatedError
        """
        if response.error is not None:
            raise U2IActionNotCreatedError("Exception happened: %s for request %s" % \
                                           (response.error, response.request))
        elif response.status != httplib.CREATED:
            raise U2IActionNotCreatedError("request: %s status: %s body: %s" % \
                                           (response.request, response.status, response.body))
        return None
    
    def auser_conversion_item(self, uid, iid, **params):
        """Asynchronously create an user conversion action on an item
        
        :param uid: user id. type str or int.
        :param iid: item id. type str or int.
        :param params: keyword arguments for optional attributes.
                For example, latlng="123.4, 56.7" 
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        request = self._auser_action_item(action=CONVERSION_API, uid=uid, iid=iid, **params)
        return request
    
    def auser_dislike_item(self, uid, iid, **params):
        """Asynchronously create an user dislike action on an item
        
        :param uid: user id. type str or int.
        :param iid: item id. type str or int.
        :param params: keyword arguments for optional attributes.
                For example, latlng="123.4, 56.7" 
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        request = self._auser_action_item(action=DISLIKE_API, uid=uid, iid=iid, **params)
        return request

    def auser_like_item(self, uid, iid, **params):
        """Asynchronously create an user like action on an item
        
        :param uid: user id. type str or int.
        :param iid: item id. type str or int.
        :param params: keyword arguments for optional attributes.
                For example, latlng="123.4, 56.7" 
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        request = self._auser_action_item(action=LIKE_API, uid=uid, iid=iid, **params)
        return request
    
    def auser_rate_item(self, uid, iid, rate, **params):
        """Asynchronously create an user rate action on an item
        
        :param uid: user id. type str or int.
        :param iid: item id. type str or int.
        :param rate: rating. integer value of 1-5 (1 is least preferred and 5 is most preferred)
        :param params: keyword arguments for optional attributes.
                For example, latlng="123.4, 56.7" 
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        request = self._auser_action_item(action=LIKE_API, uid=uid, iid=iid, rate=rate, **params)
        return request
    
    def auser_view_item(self, uid, iid, **params):
        """Asynchronously create an user view action on an item
        
        :param uid: user id. type str or int.
        :param iid: item id. type str or int.
        :param params: keyword arguments for optional attributes.
                For example, latlng="123.4, 56.7" 
        :returns:
            AsyncRequest object. You should call the aresp() method using this AsyncRequest
            object as argument to get the final result or status of this asynchronous request.
        """
        request = self._auser_action_item(action=VIEW_API, uid=uid, iid=iid, **params)
        return request
    
    def aresp(self, request):
        """Get the result of the asynchronous request
        
        :param request: AsyncRequest object. This object must be returned by the asynchronous request function
                For example, to get the result of a aget_user() request, call this aresp() with the argument of 
                AsyncRequest object returned by aget_user().
        
        :returns:
            The result of this AsyncRequest. The return type is the same as the return type of corresponding blocking request.
            
            For example, 
            
            Calling aresp() with acreate_user() AsyncRequest returns the same type as create_user(), which is None.
            
            Calling aresp() with aget_user() AsyncRequest returns the same type as get_user(), which is dictionary data.
        
        :raises:
            Exception may be raised if there is error happened. The type of exception is the same as exception type 
            of the correspdoning blocking request.
            
            For example,
            
            Calling aresp() with acreate_user() AsyncRequest may raise UserNotCreatedError exception.
            
            Calling aresp() with aget_user() AsyncRequest may raise UserNotFoundError exception.

        """
        response = request.get_response()        
        result = request.rfunc(response)
        return result


    def create_user(self, uid, **params):
        """Blocking request to create user
        
        :param uid: user id. type str or int.
        :param params: keyword arguments for optional attributes.
                For example, bday="1985-01-23", inactive="true".
                
        :returns: 
            None.
        
        :raises: 
            UserNotCreatedError.
        
        """   
        request = self.acreate_user(uid, **params)
        result = self.aresp(request)
        return result
    
    def get_user(self, uid):
        """Blocking request to get user
        
        :param uid: user id. type str or int.
        
        :returns: 
            User data in Dictionary format.
        
        :rasies: 
            UserNotFoundError.
        
        """
        request = self.aget_user(uid)
        result = self.aresp(request)
        return result
    
    def delete_user(self, uid):
        """Blocking request to delete the user
        
        :param uid: user id. type str or int.
        
        :returns: 
            None.
            
        :raises: 
            UserNotDeletedError.
        
        """
        request = self.adelete_user(uid)
        result = self.aresp(request)
        return result
        
    def create_item(self, iid, itypes, **params):
        """Blocking request to create item
        
        :param iid: item id. type str or int.
        :param itypes: item types. Tuple of Str.
                For example, if this item belongs to item types "t1", "t2", "t3", "t4",
                then itypes=("t1", "t2", "t3", "t4").
                NOTE: if this item belongs to only one itype, use tuple of one element, eg. itypes=("t1",)
        :param params: keyword arguments for optional attributes.
                For example, latlng="123.4, 56.7". 
           
        :returns: 
            None
            
        :raises: 
            ItemNotCreatedError
             
        """
        request = self.acreate_item(iid, itypes, **params)
        result = self.aresp(request)
        return result
    
    def get_item(self, iid):
        """Blocking request to get item
        
        :param iid: item id. type str or int.
        
        :returns: 
            item data in dictionary format.
        
        :raises: 
            ItemNotFoundError.
        
        """
        request = self.aget_item(iid)
        result = self.aresp(request)
        return result
    
    def delete_item(self, iid):
        """Blocking request to delete item
        
        :param iid: item id. type str or int.
        
        :returns:
            None
            
        :raises:
            ItemNotDeletedError
            
        """
        request = self.adelete_item(iid)
        result = self.aresp(request)
        return result
    
    def get_itemrec(self, uid, n, engine, **params):
        """Blocking request to get recommendations
        
        :param uid: user id. type str or int.
        :param n: number of recommendation. type int.
        :param engine: name of the prediction engine. type str.
        :param params: keyword arguments for optional attributes.
                For example, latlng="123.4, 56.7" 
                
        :returns:
            data in dictionary format.
            
        :raises:
            ItemRecNotFoundError.
            
        """
        request = self.aget_itemrec(uid, n, engine=engine, **params)
        result = self.aresp(request)
        return result
        
    def _user_action_item(self, action, uid, iid, **params):
        """Blocking request to create user action on an item
        
        :param action: action type. type str. ("like", "dislike", "conversion", "rate", "view")
        :param uid: user id. type str or int.
        :param iid: item id. type str or int.
        :param params: keyword arguments for optional attributes.
                For example, latlng="123.4, 56.7" 
                For "rate" action, rate param is required. integer value of 1-5 (1 is least preferred and 5 is most preferred) (eg. rate=4)
        :returns:
            None
            
        :raises:
            U2IActionNotCreatedError
        """
        request = self._auser_action_item(action, uid, iid, **params)
        result = self.aresp(request)
        return result
    
    def user_conversion_item(self, uid, iid, **params):
        """Blocking request to create user conversion action on an item
        
        :param uid: user id. type str or int.
        :param iid: item id. type str or int.
        :param params: keyword arguments for optional attributes.
                For example, latlng="123.4, 56.7" 
                
        :returns:
            None
            
        :raises:
            U2IActionNotCreatedError
        """
        result = self._user_action_item(action=CONVERSION_API, uid=uid, iid=iid, **params)
        return result
    
    def user_dislike_item(self, uid, iid, **params):
        """Blocking request to create user dislike action on an item
        
        :param uid: user id. type str or int.
        :param iid: item id. type str or int.
        :param params: keyword arguments for optional attributes.
                For example, latlng="123.4, 56.7" 
        
        :returns:
            None
            
        :raises:
            U2IActionNotCreatedError
        """
        result = self._user_action_item(action=DISLIKE_API, uid=uid, iid=iid, **params)
        return result
    
    def user_like_item(self, uid, iid, **params):
        """Blocking request to create user like action on an item
        
        :param uid: user id. type str or int.
        :param iid: item id. type str or int.
        :param params: keyword arguments for optional attributes.
                For example, latlng="123.4, 56.7" 
                
        :returns:
            None
            
        :raises:
            U2IActionNotCreatedError
        """
        result = self._user_action_item(action=LIKE_API, uid=uid, iid=iid, **params)
        return result
    
    def user_rate_item(self, uid, iid, rate, **params):
        """Blocking request to create user rate action on an item
        
        :param uid: user id. type str or int.
        :param iid: item id. type str or int.
        :param rate: rating. integer value of 1-5 (1 is least preferred and 5 is most preferred)
        :param params: keyword arguments for optional attributes.
                For example, latlng="123.4, 56.7" 
        
        :returns:
            None
            
        :raises:
            U2IActionNotCreatedError
        """
        result = self._user_action_item(action=RATE_API, uid=uid, iid=iid, rate=rate, **params)
        return result
    
    def user_view_item(self, uid, iid, **params):
        """Blocking request to create user view action on an item
        
        :param uid: user id. type str or int.
        :param iid: item id. type str or int.
        :param params: keyword arguments for optional attributes.
                For example, latlng="123.4, 56.7" 
        
        :returns:
            None
            
        :raises:
            U2IActionNotCreatedError
        """
        result = self._user_action_item(action=VIEW_API, uid=uid, iid=iid, **params)
        return result
    