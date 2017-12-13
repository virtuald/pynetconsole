
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
    
    def __init__(self):
        
        self.frames = {
            11: self._onError,
            12: self._onInfo
        }
        
        self.cond = threading.Condition()
        self.sock = None
        self.sockaddr = None
        
    
    def start(self, address, port=1741):
        if self.running:
            raise ValueError("Cannot start without stopping first")
        
        with self.cond:
            self.sockaddr = (address, port)
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
    
    def _keepAliveReady(self):
        if not self.running:
            return -1
        
    
    def _keepAlive(self):
        self.reconnect()
        while self.running:
            time.sleep(2000)
            try:
                self.sockwfp.write(b'\x00\x00')
                self.sockwfp.flush()
            except IOError:
                self.reconnect()
    
    def _readThreadReady(self):
        if not self.running:
            return -1
        return self.sockrfp
    
    def _readThread(self):
        while True:
            with self.cond:
                sockrfp = self.cond.wait_for(self._readThreadReady)
                if sockrfp == -1:
                    return
                
                # readStruct
                sz = s.size
                data = self.sockrfp.read(sz)
                if len(data) != sz:
                    raise StreamEOF("connection dropped")
                return s.unpack(data)
            
                blen, tag = self._readStruct(self._header)
                blen -= 1
                
                buf = sockrfp.read(blen)
                if len(buf) != blen:
                    raise StreamEOF("connection dropped")
                
                # process the frame
                fn = self.frames.get(tag)
                if fn:
                    fn(buf)
                else:
                    print("ERROR: Unknown tag %s; Ignoring..." % tag)
                
    def _reconnect(self):
        # returns once the socket is connected
        
        self.connected = False
        if self.sock:
        
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
            # notifyAll()
            break
        
    _header = struct.Struct('>Hb')
    
    _errorFrame = struct.Struct('>dHH')
    _errorFrameSz = _errorFrame.size
    
    _infoFrame = struct.Struct('>dH')
    _infoFrameSz = _infoFrame.size
    
    _short = struct.Struct('>H')
    _shortSz = _short.size
    
    def _onError(self, b):
        ts, _seq, _numOcc, errorCode, flags = self._errorFrame.unpack(b[:self._errorFrameSz])
        details, nidx = self._getStr(b, self._errorFrameSz)
        location, nidx = self._getStr(b, nidx)
        callStack, _ = self._getStr(b, nidx)
        
        print('[%0.2f]' % ts, errorCode, details, location, callStack)
    
    def _getStr(self, b, idx):
        sidx = idx + self._shortSz
        blen = self._short.unpack(b[idx:sidx])
        nextidx = sidx + blen
        return b[sidx:nextidx].decode('utf-8', errors='replace'), nextidx
    
    def _onInfo(self, b):
        ts, _seq = self._infoFrame.unpack(b[:self._infoFrameSz])
        msg = b[self._infoFrameSz:].decode('utf-8', errors='replace')
        print('[%0.2f]' % ts, msg)


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

