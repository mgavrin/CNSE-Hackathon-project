import bluetooth 
import socket

class EmgInterface():
	
	def __init__(self,deviceId,channels):
		self.deviceId = deviceId
		self.channels = channels
		self.zerocount = 0
		self.samplerate = 500 #sample rate in Hz
		self.timebase = 0.01 #10ms blocks
		self.bytestoread = int(channels * 2 * self.samplerate * self.timebase + 8)
		self.sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM)
         # self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.sock.connect((self.deviceId, channels))
		self.sock.send(chr(int(0x80 + ord('M'))))
		self.sock.send(chr(int(0x30)))
		self.sock.send(chr(int(0x80 + ord('M')+ 0x30)))
		self.sock.recv(1) #Recieve M character response
		self.currpack = [0 for x in xrange(self.channels)]
		self.chavg = [0 for x in xrange(self.channels)]
		self.state = [0,0,0,0,0,0,0,0]
		self.sprite = [[0 for x in xrange(5)] for x in xrange(3)]
		self.filtered = [0,0,0,0,0]
		self.threshed = [0,0,0,0,0]
		self.i = 0
		self.zeros = [0,0,0,0,0]
        
	def getState(self):
		self.sprite[self.i] = self.readPacket()
		
		#print self.sprite
		self.i +=1
		if (self.i >= 3): self.i = 0     	#sprite len
		for j in range (0,5):
			sum = 0
			for k in range(0,3):			#sprite len
				sum += self.sprite[k][j]
			self.filtered[j] = sum / 3		#sprite len
			
		#filtered mother fucker


		if (self.filtered[0] > 1200): 
			self.threshed[0] = 1
		else: 
			self.threshed[0] = 0
			
		if (self.filtered[1] > 1200): 
			self.threshed[1] = 1
		else: 
			self.threshed[1] = 0			
							
							
		if (self.filtered[2] > 1000): 
			self.threshed[2] = 1
		else: 
			self.threshed[2] = 0		
		
		if (self.filtered[3] > 1000): 
			self.threshed[3] = 1
		else: 
			self.threshed[3] = 0
			
			
		if (self.filtered[4] > 500): 
			self.threshed[4] = 1
		else: 
			self.threshed[4] = 0			


		#that shit just got thresh
		
		#ed
		
		#state 1 forward
		self.state[0] = self.threshed[4]
		
		#state 2 left
		self.state[1] = (self.threshed[3] and not self.threshed[2] and not self.state[0])
		
		#state 3 right
		self.state[2] = (self.threshed[2] and not self.threshed[3] and not self.state[0])
		
		#state 4 vacuum
		self.state[3] = (self.threshed[2] and self.threshed[3])
		
		#state 5 vac off
		self.state[4] = not self.state[3]
		
		#state 6 m up
		self.state[5] = (self.threshed[0] and not self.threshed[1])
		
		#state 7 m down
		self.state[6] = (self.threshed[1] and not self.threshed[0])
		
		#state 8 m fire
		self.state[7] = (self.threshed[0] and self.threshed[1])
		
		return self.state
		
	def start(self):
		self.sock.send(chr(int(0x80 + ord('B')))) # send start command

	def stop(self):
		state = 0
		self.sock.send(chr(int(0x80 + ord('E'))))

	def close(self):
		self.serial.close()

	def readPacket(self):
		packout = [[0]*self.channels]
		btr2 = self.channels * self.timebase * self.samplerate
		
		data = []
		
		#while len(data) < self.bytestoread:
		data.extend(self.sock.recv(self.bytestoread, socket.MSG_WAITALL)) 			
	
		if(True):  #packet[len(packet)-9] == chr(0) and packet[len(packet)-5]):
			index = 0
			self.currpack = [0,0,0,0,0]
			for i in range(0, 5): #int(self.timebase * self.samplerate-3)):
				for j in range(0,self.channels):
					chan = (0b11100000 & ord(data[index*2]) ) >> 5 # / 32  #Mask the channel number.
					ms = (0b11111 & ord(data[index*2]))
					ls = ord(data[index*2 + 1])
					raw = (ms << 8) + ls
					fin = abs(raw - 4096) - self.zeros[j]
					if (fin > self.currpack[j]):
						self.currpack[j]  = fin
					#self.currpack[j] += fin
					index += 1
					#print (i, j)
			#print len(self.currpack)
			#print len(self.chavg)	
			#for now we dont care about the rest of each packet...
			#for v in range(0,5):	
			#	self.chavg[v] =  (self.currpack[v]/5  - self.zeros[v]) # (int(self.samplerate * self.timebase))
			#print(self.chavg)
			#self.currpack = [0,0,0,0,0]
		
			
			print self.currpack
			return self.currpack
            
		else:
			#Well crap.. lets try this again...
			self.stop()
			self.start()
			return self.readPacket()
	