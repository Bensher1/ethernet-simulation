# Ethernet Simulation

### Motivation
I did this project for my Computer Networks class. We studied different retransmission policies for packets when they collide on a broadband network. This program simulates the use of 4 different retransmission polices using simpy in Python. By simulating the different retransmission policies, I was able to see how each of the policies perform under different loads after long periods of time. 

### Different Policies
When more than one node is transmitting in a given slot, the data transmissions will collide with eachother and the data will be lost. The retransmission policies shedule when the node will retransmit it's data. 
#### p-persistent ALOHA:
When collision happens, the active nodes will retransmit in the very next slot with probability 1) p = 0.50 and 2) p = 1/N
#### Binary Exponential Backoff:
The number of slots to delay after the n<sup>th</sup> attempt at retransmission is chosen randomly in the range  0 ≤ r ≤ 2<sup>k</sup> where k = min(N, 10)
#### Linear Backoff
The number of slots to delay after the n<sup>th</sup> attempt at retransmission is chosen randomly in the range  0 ≤ r ≤ k where k = min(N, 1024)
##### See the Ethernet Simulation Report for the results
