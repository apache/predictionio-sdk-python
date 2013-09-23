predictionio Package Documentation
====================================

.. automodule:: predictionio

predictionio.Client Usage Overview
--------------------------------------

Before making any request through the PredictionIO API, you need to create a client object for your App.

    >>> client = predictionio.Client(<your App Key>)

.. note:: The App Key can be found in the PredictionIO Admin Server web control panel.

Afterwards, you can import data or retrieve recommendations for your App by calling methods of this object. For example,

**User**

  To import a user record from you App with user id = "u100":

    >>> client.create_user("u100")

  To import a user record with the optional predefined location attribute "pio_latlng":

    >>> client.create_user("u100", { "pio_latlng" : [1.23, 4.56] })

  You may also define your own custom attribute "custom" = "value":

    >>> client.create_user("u100", { "pio_latlng" : [1.23, 4.56], "custom": "value" })

  .. note:: custom attributes and values could be any string but all attribute names with prefix ``'pio_'`` are reserved. You should not use the prefix ``'pio_'`` when define your custom attributes to avoid conflicts.

**Item**

  To import an item record from your App with item id = "i200" and item type = "type3":

    >>> client.create_item("i200", ("type3",))

  To import an item record with the predefined optional attribute "pio_latlng":

    >>> client.create_item("i200", ("type3",), { "pio_latlng" : [1.23, 4.56] })

  You may also define your own custom attribute "custom" = "value":

    >>> client.create_item("i200", ("type3",), { "pio_latlng" : [1.23, 4.56], "custom": "value" })

  .. note:: custom attributes and values could be any string but all attribute names with prefix ``'pio_'`` are reserved. You should not use the prefix ``'pio_'`` when define your custom attributes to avoid conflicts.

**User Action on Item**

  To import a user "rate" action record from your App with user id = "u100", item id = "i200" and rating = 2:

    >>> client.identify("u100")
    >>> client.record_action_on_item("rate", "i200", { "pio_rate": 2 })

  .. note:: the "pio_rate" attribute is required for "rate" action.

  To import a "view" action record from your App for the same user and item:

    >>> client.record_action_on_item("view", "i200" )

  To import a "like" record with predefined optional timestamp attribute "pio_t":

    >>> client.record_action_on_item("like", "i200", { "pio_t": 12345678 })

  .. note:: predefined actions: "like", "dislike", "rate", "view", "conversion"

**Item Recommendation Engine**

  When there is enough data imported from your App and the prediction results are ready, you can get recommendations for a user.

  To get top 5 item recommendation for the same user id from the item recommendation engine "engine-1"

    >>> result = client.get_itemrec_topn("engine-1", 5)

**Item Similarity Engine**

  To get top 5 similar items of the item i200 from the item similarity engine "engine-2"

    >>> result = client.get_itemsim_topn("engine-2", "i200", 5)

Please refer to the documentation of the :class:`predictionio.Client` class for more details of all available methods.


Error Handling
--------------

An exception will be raised when an error occur during the request. Please refer to the documentation of the :class:`predictionio.Client` class for details.
In general, you may want to catch the exception and decide what to do with the error (such as logging it).

For example, the method :meth:`~Client.record_action_on_item` may raise ``U2IActionNotCreatedError``.

   >>> try:
   >>>   client.record_action_on_item("view", "i200")
   >>> except:
   >>>   <log the error>


Asynchronous Requests
---------------------

In addition to normal :ref:`blocking (synchronous) request methods <sync-methods-label>`, this SDK also provides :ref:`methods which can generate asynchronous requests <async-methods-label>`.
All methods prefixed with 'a' are asynchronous (eg, :meth:`~Client.acreate_user`, :meth:`~Client.acreate_item`).
Asynchronous requests are handled by separate threads in the background, so you can generate multiple requests at the same time without waiting for any of them to finish.
These methods return immediately without waiting for results, allowing your code to proceed to work on something else.
The concept is to break a normal blocking request (such as :meth:`~Client.create_user`) into two steps:

1. generate the request (e.g., calling :meth:`~Client.acreate_user`);
2. get the request status and return data (calling :meth:`~Client.aresp`);

This allows you to do other work between these two steps.

.. note::
   In some cases you may not care whether the request is successful for performance or application-specific reasons, then you can simply skip step 2.

.. note::
   If you do care about the request status or need to get the return data, then at a later time you will need to call :meth:`~Client.aresp` with the AsyncRequest object returned in step 1.
   Please refer to the documentation of :ref:`asynchronous request methods <async-methods-label>` for more details.

For example, the following code first generates an asynchronous request to retrieve recommendations, then get the result at later time::

    >>> # Generates asynchronous request and return an AsyncRequest object
    >>> request = client.aget_itemrec_topn("engine-1", 5)
    >>> <...you can do other things here...>
    >>> try:
    >>>    result = client.aresp(request) # check the request status and get the return data.
    >>> except:
    >>>    <log the error>


Batch Import Data
-----------------

When you import large amount of data at once, you may also use asynchronous request methods to generate lots of requests in the beginning and then check the status at a later time to minimize run time.

For example, to import 100000 of user records::

  >>> # generate 100000 asynchronous requests and store the AsyncRequest objects
  >>> req = {}
  >>> for i in range(100000):
  >>>    req[i] = client.acreate_user(user_record[i].uid)
  >>>
  >>> <...you can do other things here...>
  >>>
  >>> # now check the status of the previous asynchronous requests
  >>> for i in range(100000):
  >>>   try:
  >>>     result = client.aresp(req[i])
  >>>   except:
  >>>     <log the error>

Alternatively, you can use blocking requests to import large amount of data, but this has significantly lower performance::

  >>> for i in range(100000):
  >>>   try:
  >>>      client.create_user(user_record[i].uid)
  >>>   except:
  >>>      <log the error>


|

predictionio.Client Class
---------------------------------

.. Autoclass:: Client

  .. note::

    The "threads" parameter specifies the number of connection threads to
    the PredictionIO API server. Minimum is 1. The client object will spawn
    out the specified number of threads. Each of them will establish a
    connection with the PredictionIO API server and handle requests
    concurrently.

  .. note::

    If you ONLY use :ref:`blocking request methods <sync-methods-label>`,
    setting "threads" to 1 is enough (higher number will not improve
    anything since every request will be blocking). However, if you want
    to take full advantage of
    :ref:`asynchronous request methods <async-methods-label>`, you should
    specify a larger number for "threads" to increase the performance of
    handling concurrent requests (although setting "threads" to 1 will still
    work). The optimal setting depends on your system and application
    requirement.

  .. automethod:: close
  .. automethod:: identify

    .. versionadded:: 0.5.0

  .. automethod:: pending_requests

    .. versionadded:: 0.6.1
    
  |

  .. _sync-methods-label:

  .. note:: The following is blocking (synchronous) request methods

  .. automethod:: get_status
  .. automethod:: create_user
  .. automethod:: get_user
  .. automethod:: delete_user

  .. automethod:: create_item
  .. automethod:: get_item
  .. automethod:: delete_item

  .. automethod:: record_action_on_item

    .. versionadded:: 0.5.0

  .. automethod:: get_itemrec_topn

    .. versionadded:: 0.5.0

    .. versionchanged:: 0.6.0
      Change the order of parameters.

  .. automethod:: get_itemsim_topn

    .. versionadded:: 0.6.0

  .. automethod:: get_itemrec
  
    .. deprecated:: 0.5.0
      Use :func:`get_itemrec_topn` instead.

  .. automethod:: user_conversion_item
      
    .. deprecated:: 0.5.0
      Use :func:`record_action_on_item` instead.

  .. automethod:: user_dislike_item

    .. deprecated:: 0.5.0
      Use :func:`record_action_on_item` instead.

  .. automethod:: user_like_item

    .. deprecated:: 0.5.0
      Use :func:`record_action_on_item` instead.

  .. automethod:: user_rate_item

    .. deprecated:: 0.5.0
      Use :func:`record_action_on_item` instead.

  .. automethod:: user_view_item

    .. deprecated:: 0.5.0
      Use :func:`record_action_on_item` instead.

  |

  .. _async-methods-label:

  .. note:: The following is non-blocking (asynchronous) request methods

  .. automethod:: acreate_user
  .. automethod:: aget_user
  .. automethod:: adelete_user

  .. automethod:: acreate_item
  .. automethod:: aget_item
  .. automethod:: adelete_item

  .. automethod:: arecord_action_on_item

    .. versionadded:: 0.5.0

  .. automethod:: aget_itemrec_topn

    .. versionadded:: 0.5.0

    .. versionchanged:: 0.6.0
      Change the order of parameters.

  .. automethod:: aget_itemsim_topn

    .. versionadded:: 0.6.0

  .. automethod:: aget_itemrec

    .. deprecated:: 0.5.0
      Use :func:`aget_itemrec_topn` instead.

  .. automethod:: auser_conversion_item

    .. deprecated:: 0.5.0
      Use :func:`arecord_action_on_item` instead.

  .. automethod:: auser_dislike_item

    .. deprecated:: 0.5.0
      Use :func:`arecord_action_on_item` instead.

  .. automethod:: auser_like_item

    .. deprecated:: 0.5.0
      Use :func:`arecord_action_on_item` instead.

  .. automethod:: auser_rate_item

    .. deprecated:: 0.5.0
      Use :func:`arecord_action_on_item` instead.

  .. automethod:: auser_view_item

    .. deprecated:: 0.5.0
      Use :func:`arecord_action_on_item` instead.

  .. automethod:: aresp


