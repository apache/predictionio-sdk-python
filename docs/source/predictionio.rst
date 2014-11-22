predictionio Package Documentation
====================================

.. automodule:: predictionio

The SDK comprises of two clients: 

1. EventClient, it is for importing data into the PredictionIO platform. 
2. EngineClient, it is for querying PredictionIO Engine Instance, submit query
   and extract prediction results.

Please read `PredictionIO Quick Start
<http://docs.prediction.io/0.8.2/recommendation/quickstart.html>`_ for
detailed explanation.

predictionio.EventClient Class
------------------------------

.. autoclass:: EventClient
  :members:

  .. note::

    The "threads" parameter specifies the number of connection threads to
    the PredictionIO server. Minimum is 1. The client object will spawn
    out the specified number of threads. Each of them will establish a
    connection with the PredictionIO server and handle requests
    concurrently.

  .. note::

    If you ONLY use `blocking request methods`,
    setting "threads" to 1 is enough (higher number will not improve
    anything since every request will be blocking). However, if you want
    to take full advantage of
    `asynchronous request methods`, you should
    specify a larger number for "threads" to increase the performance of
    handling concurrent requests (although setting "threads" to 1 will still
    work). The optimal setting depends on your system and application
    requirement.
   

predictionio.EngineClient Class
------------------------------

.. autoclass:: EngineClient
   :members:

predictionio.AsyncRequest Class
------------------------------

.. autoclass:: AsyncRequest
   :members:

predictionio SDK Usage Notes
-------------------------

Asynchronous Requests
^^^^^^^^^^^^^^^^^^^^^

In addition to normal `blocking (synchronous) request methods`,
this SDK also provides `non-blocking (asynchronous) request methods`.
All methods
prefixed with 'a' are asynchronous (eg, :meth:`~EventClient.aset_user`,
:meth:`~EventClient.aset_item`).  Asynchronous requests are handled by separate
threads in the background, so you can generate multiple requests at the same
time without waiting for any of them to finish.  These methods return
immediately without waiting for results, allowing your code to proceed to work
on something else.  The concept is to break a normal blocking request (such as
:meth:`~EventClient.set_user`) into two steps:

1. generate the request (e.g., calling :meth:`~EngineClient.asend_query`);
2. get the request's response by calling :meth:`~AsyncRequest.get_response`.

This allows you to do other work between these two steps.

.. note::
   In some cases you may not care whether the request is successful for performance or application-specific reasons, then you can simply skip step 2.

.. note::
   If you do care about the request status or need to get the return data, then at a later time you will need to call :meth:`~Client.aresp` with the AsyncRequest object returned in step 1.
   Please refer to the documentation of :ref:`asynchronous request methods <async-methods-label>` for more details.

For example, the following code first generates an asynchronous request to
retrieve recommendations, then get the result at later time::

    >>> # Generates asynchronous request and return an AsyncRequest object
    >>> engine_client = EngineClient()
    >>> request = engine_client.asend_query(data={"uid": "1", "n" : 3})
    >>> <...you can do other things here...>
    >>> try:
    >>>    result = request.get_response() # check the request status and get the return data.
    >>> except:
    >>>    <log the error>


Batch Import Data
^^^^^^^^^^^^^^^^^^^^^

When you import large amount of data at once, you may also use asynchronous
request methods to generate lots of requests in the beginning and then check the
status at a later time to minimize run time.

For example, to import 100000 of user records::

  >>> # generate 100000 asynchronous requests and store the AsyncRequest objects
  >>> event_client = EventClient(access_key=<YOUR_ACCESS_KEY>)
  >>> for i in range(100000):
  >>>   event_client.aset_user(user_record[i].uid)
  >>>
  >>> <...you can do other things here...>
  >>>
  >>> # calling close will block until all requests are processed
  >>> event_client.close()

Alternatively, you can use blocking requests to import large amount of data, but this has significantly lower performance::

  >>> for i in range(100000):
  >>>   try:
  >>>      client.set_user(user_record[i].uid)
  >>>   except:
  >>>      <log the error>


