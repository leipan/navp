. restore() and checkpoint() can produc an infinite loop, like shown
  in test_restore.py:

[leipan@3a0eb412eb5f python]$ dmtcp_launch python test_checkpoint.py 
before checkpoint() 1:  1
after checkpoint() 1:  1
before checkpoint() 2:  2
after checkpoint() 2:  2
before checkpoint() 3:  3
after checkpoint() 3:  3
[leipan@3a0eb412eb5f python]$ dmtcp_launch python test_restore.py
-------- 1 ----------
before checkpoint() 1:  1
after checkpoint() 1:  1
-------- 2 ----------
before restore() 2:  2
Restoring the latest session
session[1]:  /home/leipan/navp/python/dmtcp_restart_script_236164f94a82146c-40000-a22cdfe0890495.sh
[40000] NOTE at processinfo.cpp:419 in restoreHeap; REASON='Area between saved_break and curr_break not mapped, mapping it now'
     _savedBrk = 10264576
     curBrk = 23023616
after checkpoint() 1:  1
-------- 2 ----------
before restore() 2:  2
Restoring the latest session
session[1]:  /home/leipan/navp/python/dmtcp_restart_script_236164f94a82146c-40000-a22cdfe0890495.sh
[40000] NOTE at processinfo.cpp:419 in restoreHeap; REASON='Area between saved_break and curr_break not mapped, mapping it now'
     _savedBrk = 10264576
     curBrk = 27922432
after checkpoint() 1:  1
-------- 2 ----------
before restore() 2:  2
Restoring the latest session
session[1]:  /home/leipan/navp/python/dmtcp_restart_script_236164f94a82146c-40000-a22cdfe0890495.sh
[40000] NOTE at processinfo.cpp:419 in restoreHeap; REASON='Area between saved_break and curr_break not mapped, mapping it now'
     _savedBrk = 10264576
     curBrk = 13471744
after checkpoint() 1:  1
-------- 2 ----------
before restore() 2:  2
Restoring the latest session
session[1]:  /home/leipan/navp/python/dmtcp_restart_script_236164f94a82146c-40000-a22cdfe0890495.sh
after checkpoint() 1:  1
-------- 2 ----------
before restore() 2:  2
Restoring the latest session
session[1]:  /home/leipan/navp/python/dmtcp_restart_script_236164f94a82146c-40000-a22cdfe0890495.sh
[40000] NOTE at processinfo.cpp:419 in restoreHeap; REASON='Area between saved_break and curr_break not mapped, mapping it now'
     _savedBrk = 10264576
     curBrk = 18415616
after checkpoint() 1:  1
-------- 2 ----------
before restore() 2:  2
Restoring the latest session
session[1]:  /home/leipan/navp/python/dmtcp_restart_script_236164f94a82146c-40000-a22cdfe0890495.sh
[40000] NOTE at processinfo.cpp:419 in restoreHeap; REASON='Area between saved_break and curr_break not mapped, mapping it now'
     _savedBrk = 10264576
     curBrk = 25223168
after checkpoint() 1:  1
-------- 2 ----------
before restore() 2:  2
Restoring the latest session
session[1]:  /home/leipan/navp/python/dmtcp_restart_script_236164f94a82146c-40000-a22cdfe0890495.sh
[40000] NOTE at processinfo.cpp:419 in restoreHeap; REASON='Area between saved_break and curr_break not mapped, mapping it now'
     _savedBrk = 10264576
     curBrk = 25436160
after checkpoint() 1:  1
-------- 2 ----------
before restore() 2:  2
Restoring the latest session
session[1]:  /home/leipan/navp/python/dmtcp_restart_script_236164f94a82146c-40000-a22cdfe0890495.sh
[40000] NOTE at processinfo.cpp:419 in restoreHeap; REASON='Area between saved_break and curr_break not mapped, mapping it now'
     _savedBrk = 10264576
     curBrk = 13660160
after checkpoint() 1:  1
-------- 2 ----------
before restore() 2:  2
Restoring the latest session
session[1]:  /home/leipan/navp/python/dmtcp_restart_script_236164f94a82146c-40000-a22cdfe0890495.sh
[40000] NOTE at processinfo.cpp:419 in restoreHeap; REASON='Area between saved_break and curr_break not mapped, mapping it now'
     _savedBrk = 10264576
     curBrk = 11644928
after checkpoint() 1:  1
-------- 2 ----------
before restore() 2:  2
Restoring the latest session
session[1]:  /home/leipan/navp/python/dmtcp_restart_script_236164f94a82146c-40000-a22cdfe0890495.sh
^C
[leipan@3a0eb412eb5f python]$ 
