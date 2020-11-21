# Here we will see about MultiProcessing package in Python.
# 1.Introduction:
""" Multiprocessing package supports spawning processes using API similar to threading module.
Multiprocessing offers local and remote concurrency(runs on unix and windows) using subprocesses instead of threads
Multiprocessing introduces API's which do not have analogs in threading module - pool object is example """
'''
# Pool object offers paralleling executing function across multiple i/p values,distributing i/p data across processes
# Here we defined function with n argument and to return n*2 values,used map() to wrap map() in a list[1, 4, 9] call
# Here list[1, 4, 9] refers to multiple i/p values passed to function fn using map, o/p 1*2, 4*2, 9*2 i.e [2, 8, 18]
from multiprocessing import Pool
def fn(n):
    return n*2

if __name__ == '__main__':
    with Pool(4) as p:
        print(p.map(fn, [1, 4, 9]))
'''

# (i).Process Class:
""" In Multiprocessing, processes are spawned by creating Process object and then call start() method
Process follows API of threading.Thread """
'''
# Here we created fun. f with name argument and print the name, under main assigned object for process p using Process
# Process has target details i.e fun. f, arguments of func. i.e name as arun, then process object is started and joined.
from multiprocessing import Process
def f(name):
    print('hello', name)  # o/p hello arun

if __name__ == '__main__':
    p = Process(target=f, args =('arun',))
    p.start()
    p.join()

# (ii).To get individual process ID''s involved,
# Here we can see infor() func is executed twice - 1st for main and then for f1 function.
from multiprocessing import Process
import os
def infor(title):
    print(title)  # o/p main line i.e main is executed 1st so get infor('main line') here
    print('module name:', __name__)  # o/p module name: __main__ i.e as main module is executed
    print('parent process:', os.getppid())  # o/p parent process: 22256
    print('process ID:', os.getpid())  # o/p process ID: 21844

def f1(name):
    infor('function f1')  # o/p function f1 i.e after main f1 func. is executed, after this get called to infor fn.
# so o/p is module name: __mp_main__, parent process: 21844, process ID: 17468. Here parent process is from previous run
    print('hello', name)  # o/p hello arun

if __name__ == '__main__':
    infor('main line')
    p1 = Process(target=f1, args=('arun',))
    p1.start()
    p1.join()
'''

# (iii).Contexts and start methods:
""" Based on platform, multiprocessing supports 3 ways to start a process - spawn, fork, forkserver 
1.spawn - parent process starts a fresh python interpreter process,child process inherit resources to run process objects
run() method, starting process is slow and available on unix and windows.
2.fork - Parent process uses os.fork() to fork Python interpreter.child process when begins is identical to parent process
all resources of parent are inherited by child process,safely forking multithreaded process is problematic.unix only
3.forkserver - when program starts and selects forkserver start method,server process is started.
whenever new process is needed,parent process connects to server and requests that it fork a new process.
fork server process is single threaded so safe to use os.fork(), unix available and support unix pipes."""
# To select start method,use set_start_method() in if __name__ == '__main__' clause of main module
# Here we have fun. with q arg and value 'Hi' is put in q, later in main module used start method as spawn and made queue
# used object p for process with target and args details, start an stop object.get q value and print.
# Note: set_start_method() should not be used more than once in program.
'''
import multiprocessing as mp

def fun(q):
    q.put('Hi')

if __name__ == '__main__':
    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=fun, args=(q,))
    p.start()
    print(q.get())  # o/p Hi
    p.join()

# use get_context() to obtain context object.Context objects have same API as multiprocessing module,
# get_context() allows one to use multiple start methods in same program.
if __name__ == '__main__':
    ctx = mp.get_context('spawn')
    q = ctx.Queue()
    p1 = ctx.Process(target=fun, args=(q,))
    p1.start()
    print(q.get())  # o/p Hi
    p1.join()
'''

# (iv).Exchanging objects between Processes:
""" Multiprocessing supports 2 types of communication channel b/w processes - Queues, Pipes """
# 1.Queues - Queue class is near clone of queue.Queue. Queues are thread and process safe.
# Here
from multiprocessing import Process, Queue
def f(n):
    n.put([64, 4.0, "Hello", 6+5j])

if __name__ == '__main__':
    n = Queue()
    p = Process(target=f, args=(n,))
    p.start()
    print(n.get())  # o/p [64, 4.0, 'Hello', (6+5j)] i.e list of all values put in n argument inside fun. f definition
    p.join()

# 2.Pipes - pipe() fun. returns pair of connection objects connected by pipe which by default is duplex(two-way).
# Here 2 connection objects parent_conn & child_conn returned by Pipe() represents 2 ends of pipe & has send(),recv() methods
# data in pipe may become corrupted if 2 processes try to read from/write to same end of pipe at same time.
# Note:No risk of corruption from processes using different ends of pipe at same time.
from multiprocessing import Process, Pipe
def f(conn):
    conn.send([64, 4.0, "Hello", 6+5j])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())
    p.join()

