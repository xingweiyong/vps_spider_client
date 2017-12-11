#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# [SNIPPET_NAME: Threaded Server]
# [SNIPPET_CATEGORIES: Python Core, socket, threading]
# [SNIPPET_DESCRIPTION: Simple example of Python's socket and threading modules]
# [SNIPPET_DOCS: http://docs.python.org/library/socket.html, http://docs.python.org/library/threading.html]
# [SNIPPET_AUTHOR: Gonzalo  <gnunezr@gmail.com>]
# [SNIPPET_LICENSE: GPL]

# -*- coding: utf-8 -*-
import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import socket
import threading
import time
import codecs
import json
import re
#from DB.MySQLDB import MySql
import math
import settings

QUIT = False
files_dir =settings.files_dir

#
# task_pool
#
# from 数据库
#pre_url = 'https://web.immomo.com/live/%s'
#db = MySql('10.13.38.44',3307, 'crawler', 'crawlerQaz', 'chaser')
#urls = db.select('''
#        select DISTINCT momoid from momoid_list list''')
#task_list = [pre_url %str(x[0]) for x in urls]

# from 文件
files = os.listdir(files_dir)
task_list = []
for each_file in files:
    if 'shop_url.txt' in each_file:
        with open(os.path.join(files_dir,each_file),'r') as f:
            task_list = [x.split('\n')[0] for x in f]
    if 'shop_url_old.txt' in each_file:
        print 'shop_url_old exists...'
        with open(os.path.join(files_dir,each_file),'r') as f:
            task_list_old = [x.split('\n')[0] for x in f]
            task_list = list(set(task_list) ^ set(task_list_old))
flag_cursor = 0
flag_num = 5
flag = int(math.ceil(len(task_list)/float(flag_num)))


class ClientThread( threading.Thread ):
    ''' 
    Class that implements the client threads in this server
    '''
    def __init__( self, client_sock ):
        '''
        Initialize the object, save the socket that this thread will use.
        '''
        threading.Thread.__init__( self )
        self.client = client_sock

    def run( self ):
        ''' 
        Thread's main loop. Once this function returns, the thread is finished 
        and dies. 
        '''
        #
        # Need to declare QUIT as global, since the method can change it
        #
        global QUIT
        global flag_cursor
        done = False
        cmd = self.readline()
        #
        # Read data from the socket and process it
        #
        while not done:
            if cmd == 'quit':
                self.writeline( 'Ok, bye' )
                # QUIT 表示退出程序，done 表示连接的子线程结束
                QUIT = True
                done = True
            elif cmd == 'bye':
                self.writeline( 'Ok, bye' )
                done = True
            elif cmd == 'ready':
                # 操作全局队列，分发任务
                current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                if len(task_list)>0 and flag_cursor < flag:
                    task = {'func_name':'crawler_tmall','detail':task_list[flag_cursor*flag_num:(flag_cursor+1)*flag_num]}
                    flag_cursor += 1
                    print '[%s],%s / %s'%(current_time,flag_cursor,flag)
                    with open(os.path.join(files_dir, 'shop_url_old.txt'), 'a') as f:
                        for each_task in task['detail']:
                            f.write(each_task + '\n')
                else:
                    task = 'no more'
                task_item = {'time':current_time,'task':task}
                self.writeline( json.dumps(task_item) )
            else:
                try:
                    data = json.loads(cmd)
                    print type(data),data
                except Exception,e:
                    print 'get cmd error:',e

            cmd = self.readline()
        #
        # Make sure the socket is closed once we're done with it
        #
        self.client.close()
        return

    def readline( self ):
        ''' 
        Helper function, reads up to 1024 chars from the socket, and returns 
        them as a string, all letters in lowercase, and without any end of line 
        markers '''
        try:
            result = self.client.recv( 102400 )
            if( None != result ):
                result = result.strip().lower()
            return result
        except:
            return None

    def writeline( self, text ):
        ''' 
        Helper function, writes teh given string to the socket, with an end of 
        line marker appended at the end 
        '''
        # print text
        try:
            self.client.send( text.strip() + '\n' )
        except:
            pass

class Server:
    ''' 
    Server class. Opens up a socket and listens for incoming connections.
    Every time a new connection arrives, it creates a new ClientThread thread
    object and defers the processing of the connection to it. 
    '''
    def __init__( self ):
        self.sock = None
        self.thread_list = []

    def run( self ):
        '''
        Server main loop. 
        Creates the server (incoming) socket, and listens on it of incoming
        connections. Once an incomming connection is deteceted, creates a 
        ClientThread to handle it, and goes back to listening mode.
        '''
        all_good = False
        try_count = 0
        #
        # Attempt to open the socket
        #
        while not all_good:
            if 3 < try_count:
                #
                # Tried more than 3 times, without success... Maybe the port
                # is in use by another program
                #
                sys.exit( 1 )
            try:
                #
                # Create the socket
                #
                self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
                #
                # Bind it to the interface and port we want to listen on
                #
                self.sock.bind( ( '', 12345 ) )
                #
                # Listen for incoming connections. This server can handle up to
                # 5 simultaneous connections
                #
                self.sock.listen( 5 )
                all_good = True
                break
            except socket.error, err:
                #-
                # Could not bind on the interface and port, wait for 10 seconds
                #
                print 'Socket connection error... Waiting 10 seconds to retry.'
                del self.sock
                time.sleep( 10 )
                try_count += 1

        print "Server is listening for incoming connections."
        print "Try to connect through the command line, with:"
        print "telnet localhost 5050"
        print "and then type whatever you want."
        print
        print "typing 'bye' finishes the thread, but not the server ",
        print "(eg. you can quit telnet, run it again and get a different ",
        print "thread name"
        print "typing 'quit' finishes the server"

        try:
            #
            # NOTE - No need to declare QUIT as global, since the method never 
            #    changes its value
            #
            while not QUIT:
                try:
                    #
                    # Wait for half a second for incoming connections
                    #
                    self.sock.settimeout( 0.500 )
                    client = self.sock.accept()[0]
                    #
                    # Make it blocking.
                    #
                    client.setblocking(1)
                except socket.timeout:
                    #
                    # No connection detected, sleep for one second, then check
                    # if the global QUIT flag has been set
                    #
                    time.sleep( 1 )
                    if QUIT:
                        print "Received quit command. Shutting down..."
                        break
                    continue
                #
                # Create the ClientThread object and let it handle the incoming
                # connection
                #
                new_thread = ClientThread( client )
                print 'Incoming Connection. Started thread ',
                print new_thread.getName()
                self.thread_list.append( new_thread )
                new_thread.start()

                #
                # Go over the list of threads, remove those that have finished
                # (their run method has finished running) and wait for them 
                # to fully finish
                #
                for thread in self.thread_list:
                    if not thread.isAlive():
                        self.thread_list.remove( thread )
                        thread.join()

        except KeyboardInterrupt:
            print 'Ctrl+C pressed... Shutting Down'
        except Exception, err:
            print 'Exception caught: %s\nClosing...' % err

        #
        # Clear the list of threads, giving each thread 1 second to finish
        # NOTE: There is no guarantee that the thread has finished in the
        #    given time. You should always check if the thread isAlive() after
        #    calling join() with a timeout paramenter to detect if the thread
        #    did finish in the requested time
        #
        for thread in self.thread_list:
            thread.join( 1.0 )
        #
        # Close the socket once we're done with it
        #
        self.sock.close()

if "__main__" == __name__:
    
    server = Server()
    server.run()

    print "Terminated"
