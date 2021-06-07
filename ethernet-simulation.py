import simpy
import math
import numpy as np
import matplotlib.pyplot as plt
import random


# First  define some global variables. You should change values
class G:
    RANDOM_SEED = 33
    SIM_TIME = 100000   # This should be large
    SLOT_TIME = 1
    N = 30
    ARRIVAL_RATES = [0.001, 0.002, 0.003, 0.004, 0.006, 0.012, 0.024, 0.030]  # Check the submission guidelines
    # ARRIVAL_RATES = [0.04]
    # ARRIVAL_RATES = [0.04]
    # RETRANMISSION_POLICIES = ["pp", "op", "beb", "lb"]
    RETRANMISSION_POLICIES = ["pp", "op", "beb"]
    LONG_SLEEP_TIMER = 1000000000

        
class Server_Process(object):
    def __init__(self, env, dictionary_of_nodes, retran_policy, slot_stat):
        self.env = env
        self.dictionary_of_nodes = dictionary_of_nodes 
        self.retran_policy = retran_policy 
        self.slot_stat = slot_stat
        self.current_slot = 0
        self.action = env.process(self.run())

        self.collision = False
        self.nodes_transmitting = 0

        self.successful_Tx = 0
            
    def run(self):
        print("Server process started")
        
        while True: 
            # sleep for slot time
            yield self.env.timeout(G.SLOT_TIME)
            
            # Code to determine what happens to a slot and 
            # then update node variables accordingly based 
            # on the algorithm 
            # for node in self.dictionary_of_nodes:
            #     print(node)
            # print("starting slot")

            self.collision = False

            for i in list(range(1,G.N+1)):

                # print("node " + str(i) + " slot " +  ": " + str(self.dictionary_of_nodes[i].scheduled_slot))
                # print("current slot: " + str(self.current_slot))
                
                # print("node " + str(i) + " packets: " + str(self.dictionary_of_nodes[i].packets))
                # if (self.dictionary_of_nodes[i].packets > 0) and (self.dictionary_of_nodes[i].transmitting == True):
                #     self.nodes_transmitting += 1
                # print("attempts: " + str(self.dictionary_of_nodes[i].attempts))
                if (self.dictionary_of_nodes[i].packets > 0) and (self.dictionary_of_nodes[i].scheduled_slot == self.current_slot):
                    self.nodes_transmitting += 1

            if self.nodes_transmitting > 1:
                # print("nodes transmitting " + str(self.nodes_transmitting))
                self.collision = True

            # print(self.collision)

            if self.collision == True:
                if self.retran_policy == "pp":
                    random_list = [1,2]
                    distribution = [.5, .5]
                    for i in list(range(1,G.N+1)):
                        if (self.dictionary_of_nodes[i].packets > 0) and (self.dictionary_of_nodes[i].scheduled_slot == self.current_slot):
                            random_number = random.choices(random_list, distribution)
                            # print(random_number)
                            if random_number[0] == 1:
                                # print("pooooooop")
                                self.dictionary_of_nodes[i].scheduled_slot = self.current_slot + 1
                                self.dictionary_of_nodes[i].attempts += 1
                            if random_number[0] == 2:
                                # print("pooooooop")
                                # self.dictionary_of_nodes[i].scheduled_slot = self.current_slot + 2
                                self.dictionary_of_nodes[i].attempts += 1
                        # else:
                        #     self.dictionary_of_nodes[i].scheduled_slot = self.current_slot + 1
                        # If node has more than one attempt and needs to "roll" again
                        elif self.dictionary_of_nodes[i].attempts > 0:
                            random_number = random.choices(random_list, distribution)
                            # print(random_number)
                            if random_number[0] == 1:
                                # print("pooooooop2")
                                self.dictionary_of_nodes[i].scheduled_slot = self.current_slot + 1
                                self.dictionary_of_nodes[i].attempts += 1
                            if random_number[0] == 2:
                                # print("pooooooop2")
                                # self.dictionary_of_nodes[i].scheduled_slot = self.current_slot + 2
                                self.dictionary_of_nodes[i].attempts += 1

                elif self.retran_policy == "op":
                    random_list = [1,2]
                    distribution = [1/G.N, 1-(1/G.N)]
                    for i in list(range(1,G.N+1)):
                        if (self.dictionary_of_nodes[i].packets > 0) and (self.dictionary_of_nodes[i].scheduled_slot == self.current_slot):
                            random_number = random.choices(random_list, distribution)
                            # print(random_number)
                            if random_number[0] == 1:
                                # print("pooooooop")
                                self.dictionary_of_nodes[i].scheduled_slot = self.current_slot + 1
                                self.dictionary_of_nodes[i].attempts += 1
                            if random_number[0] == 2:
                                # print("pooooooop")
                                # self.dictionary_of_nodes[i].scheduled_slot = self.current_slot + 2
                                self.dictionary_of_nodes[i].attempts += 1
                        # else:
                        #     self.dictionary_of_nodes[i].scheduled_slot = self.current_slot + 1
                        # If node has more than one attempt and needs to "roll" again
                        elif self.dictionary_of_nodes[i].attempts > 0:
                            random_number = random.choices(random_list, distribution)
                            # print(random_number)
                            if random_number[0] == 1:
                                # print("pooooooop2")
                                self.dictionary_of_nodes[i].scheduled_slot = self.current_slot + 1
                                self.dictionary_of_nodes[i].attempts += 1
                            if random_number[0] == 2:
                                # print("pooooooop2")
                                # self.dictionary_of_nodes[i].scheduled_slot = self.current_slot + 2
                                self.dictionary_of_nodes[i].attempts += 1

                elif self.retran_policy == "beb":
                    for i in list(range(1,G.N+1)):
                        if (self.dictionary_of_nodes[i].scheduled_slot == self.current_slot):
                            if self.dictionary_of_nodes[i].attempts < 10 and self.dictionary_of_nodes[i].packets > 0:
                                random_K = random.randint(0, self.dictionary_of_nodes[i].attempts)
                                self.dictionary_of_nodes[i].scheduled_slot += 2**random_K
                                self.dictionary_of_nodes[i].attempts += 1
                            elif self.dictionary_of_nodes[i].attempts > 9:
                                random_K = random.randint(0, 10)
                                self.dictionary_of_nodes[i].scheduled_slot += 2**random_K
                                self.dictionary_of_nodes[i].attempts += 1
                            


            if self.collision == False:
                for i in list(range(1,G.N+1)):
                    if (self.dictionary_of_nodes[i].packets > 0) and (self.dictionary_of_nodes[i].scheduled_slot == self.current_slot):
                        # print("node " + str(i) + " Tx packet")
                        self.successful_Tx += 1
                        self.dictionary_of_nodes[i].packets -= 1
                        self.dictionary_of_nodes[i].attempts = 0
                        # If node Tx and there is more packets left it schedules next packet for next slot
                        if (self.dictionary_of_nodes[i].packets > 0):
                            self.dictionary_of_nodes[i].scheduled_slot = self.current_slot + 1
                    # self.dictionary_of_nodes[i].scheduled_slot = self.current_slot + 1

                    # if pp or op didn't Tx this slot and need to roll for next slot 
                    elif self.dictionary_of_nodes[i].attempts > 0 and ((self.retran_policy == "op") or (self.retran_policy == "pp")):
                            random_number = random.choices(random_list, distribution)
                            # print(random_number)
                            if random_number[0] == 1:
                                # print("pooooooop2")
                                self.dictionary_of_nodes[i].scheduled_slot = self.current_slot + 1
                                self.dictionary_of_nodes[i].attempts += 1
                            if random_number[0] == 2:
                                # print("pooooooop2")
                                # self.dictionary_of_nodes[i].scheduled_slot = self.current_slot + 2
                                self.dictionary_of_nodes[i].attempts += 1

            

            self.nodes_transmitting = 0
            # print("going to next slot")
            self.current_slot += 1

               
                
class Node_Process(object): 
    def __init__(self, env, id, arrival_rate):
        
        self.env = env
        self.id = id
        self.arrival_rate = arrival_rate
        
        # Other state variables
        # How many times first node has tried to Tx
        self.attempts = 0
        # Which slot it will try to Tx
        self.scheduled_slot = 0
        # Number of packets in the queue
        self.packets = 0
        self.transmitting = True
        
        
        
        self.action = env.process(self.run())
        

    def run(self):
        # packet arrivals 
        print("Arrival Process Started:", self.id)
        
        # Code to generate the next packet and deal with it
        while True:
             # Infinite loop for generating packets
            yield self.env.timeout(random.expovariate(self.arrival_rate))
            self.packets += 1
            if (self.attempts == 0) and (self.packets == 1):
                self.scheduled_slot = math.ceil(self.env.now)
                # print("env.now ceil: " + str(math.ceil(self.env.now)))


        
        
        

class Packet:
    def __init__(self, identifier, arrival_time):
        self.identifier = identifier
        self.arrival_time = arrival_time


class StatObject(object):    
    def __init__(self):
        self.dataset =[]

    def addNumber(self,x):
        self.dataset.append(x)




def main():
    print("Simiulation Analysis of Random Access Protocols")
    random.seed(G.RANDOM_SEED)

    for retran_policy in G.RETRANMISSION_POLICIES:
        load = np.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
        index = 0
        throughput_array = np.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
        for arrival_rate in G.ARRIVAL_RATES:
            env = simpy.Environment()
            slot_stat = StatObject()
            dictionary_of_nodes  = {} # I chose to pass the list of nodes as a 
                                      # dictionary since I really like python dictionaries :)
            
            for i in list(range(1,G.N+1)):
                node = Node_Process(env, i, arrival_rate)
                dictionary_of_nodes[i] = node
            server_process = Server_Process(env, dictionary_of_nodes,retran_policy,slot_stat)
            env.run(until=G.SIM_TIME)
            
            # code to determine throughput
            throughput = server_process.successful_Tx/G.SIM_TIME
            print("sim time was: " + str(G.SIM_TIME))
            print("server successful: " + str(server_process.successful_Tx))
            # throughput = server_process.successful_Tx
            print("throughput: " + str(throughput))
            load[index] = arrival_rate * G.N
            print("load: " + str(load))
            throughput_array[index] = throughput
            print("throughput: " + str(throughput_array))
            index += 1
        
        # code to plot 
        plt.plot(load, throughput_array)
    plt.show()
           
    
if __name__ == '__main__': main()
