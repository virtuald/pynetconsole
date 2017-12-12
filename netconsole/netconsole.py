
import socket
import struct
import sys
import threading
import time

def _output_fn(s):
    sys.stdout.write(s.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))

class StreamEOF(IOError):
    pass

class Netconsole:
    '''
        Implements the 2018+ netconsole protocol
    '''
    
    def __init__(self, address):
        
        self.frames = {
            11: self._onError,
            12: self._onInfo
        }
        
        self.cond = threading.Condition()
        self.sock = None
        
    
    def start(self):
        with self.cond:
            self.running = True
            
            self._rt = threading.Thread(target=self._readThread,
                                        name='nc-read-thread',
                                        daemon=True)
            self._rt.start()
            
            self._kt = threading.Thread(target=self._keepAlive,
                                        name='nc-keepalive-thread',
                                        daemon=True)
            self._kt.start()
    
    def stop(self):
        with self.cond:
            self.running = False
            self.cond.notifyAll()
            self.sock.close()
    
    def _readStruct(self, s):
        sz = s.size
        data = self.sockrfp.read(sz)
        if len(data) != sz:
            raise StreamEOF("connection dropped")
        return s.unpack(data)
    
    def _keepAlive(self):
        self.reconnect()
        while self.running:
            time.sleep(2000)
            try:
                self.sockwfp.write(b'\x00\x00')
                self.sockwfp.flush()
            except IOError:
                self.reconnect()
    
    def _readThread(self):
        while self.running:
            if not self._keepAliveThread.isAlive():
                break
            if self.connected:
                blen, tag = self._readStruct(self._header)
                blen -= 1
                
                buf = self.sockrfp.read(blen)
                if len(buf) != blen:
                    raise StreamEOF("connection dropped")
                
                # process the frame
                fn = self.frames.get(tag)
                if fn:
                    fn(buf)
                else:
                    print("ERROR: Unknown tag %s; Ignoring..." % tag)
                
    def _reconnect(self):
        self.connected = False
        while self.running:
            # close the old socket
            
            
            self.sock = socket.socket()
            self.sock.connect()#target, 1741, 3 second timeout
            # set tcp no delay
            self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.sockrfp = self.sock.makefile('rb')
            self.sockwfp = self.sock.makefile('wb')
            
            print("connected")
            self.connected = True
            break
        
    _header = struct.Struct('>Hb')
    _errorFrame = struct.Struct('>dHH')
    _infoFrame = struct.Struct('>dH')
    
    _short = struct.Struct('>H')
    
    
    def _onError(self, b):
        ts, _seq, _numOcc, errCode, flags = self._errorFrame.unpack(b[:])
        # get float - timestamp
        # get short - seq
        # get short - numOcc
        # get int - errorCode
        # get byte - flags
        # get details (str)
        # get location (str)
        # get callStack (str)
        pass
    
        "[${timestamp.round(2)}] ${type(flags)} ${errorCode} ${details} ${location} ${callStack}"
    
    def getStr(self, b, idx):
        blen = 
        # get short (size)
        # decode buffer
        pass
    
        return s, blen
    
    def _onInfo(self, b):
        ts, _seq = self._infoFrame.unpack(b[:2])
        # get float -ts
        self._in
        # get short - seq
        # decode utf-8
        s = b[2:].decode('utf-8', errors='replace')
        
        print()
        
    

def run(address, init_event=None):
    '''
        Starts the netconsole loop
    
        :param address: Address of the netconsole server
        :param init_event: a threading.event object, upon which the 'set'
                           function will be called when the connection has
                           succeeded.
    '''
    
    # do something about fakeds here? maybe a boolean parameter


def main():
    bcast_address = None
    if len(sys.argv) > 1:
        bcast_address = sys.argv[1]
    
    

    run(bcast_address=bcast_address)

