from cup_detector import *
from stepper_motor import *
from relay_control import relay_control
import time
import RPi.GPIO as gpio

class MachineController:

    def __init__(self):
        gpio.setwarnings(False)
        gpio.cleanup()
        
        self.t_out = 180.
        
        self.relay_pin_small = 27 
        self.relay_pin_big = 22 

        self.cup_size_pin = None
        self.collar = False
        self.type = "tradicional" #for compatibility only
        self.size = "small"
        self.small_time = 3. #need to be tested
        self.big_time = 5. # need to be tested
        self.collar_time =.5 # needs to tested
        self.working_path = "/home/pi/autochopp-machine/embedded_electronics/tmp/"
        self.human_time = 1.        
        #volumes TODO
        self.volume_big = 300
        self.volume_small = 200
        self.volume = 0 
        
        #cleaning 
        led_path = self.working_path + "leds.status"
        f = open(led_path, "w")
        f.write("")
        f.close()
      

    def power_on_nobreak(self):
        nobk_pin = 23
        gpio.setmode(gpio.BCM)
        gpio.setup(nobk_pin, gpio.IN, gpio.PUD_UP)
        print "$$$$$$$$$$$$$$$$$$$$$$$ nobreak $$$$$$$$$$$$$$$$$$$$$$$"
        if (not gpio.input(nobk_pin)):
            gpio.cleanup()
            return True
        else:
            gpio.cleanup()
            return False
    #receives and sets the settings
    def set_chopp(self, chopp):
        if chopp==0:
            self.cup_size_pin = self.relay_pin_small 
            self.collar = False
            self.type = "tradicional"
            self.size = "small"
            self.volume = self.volume_small
        
        elif chopp==1:
            self.cup_size_pin = self.relay_pin_small 
            self.collar = True
            self.type = "tradicional"
            self.size = "small"
            self.volume = self.volume_small
        elif chopp==2:
            self.cup_size_pin = self.relay_pin_big
            self.collar = False
            self.type = "tradicional"
            self.size = "big"
            self.volume = self.volume_big
        elif chopp==3:
            self.self.cup_size_pin = self.relay_pin_big
            self.collar = True
            self.type = "tradicional"
            self.size = "big"
            self.volume = self.volume_big

        print "########################### %s %%%%%%%%%%%%%%"%chopp
    #returns true when the cup drawer is open
    def is_drawer_open(self):
        #changes the state of the leds
        led_path = self.working_path + "leds.status"
        f = open(led_path, "w")
        f.write("taking_cup")
        f.close()


        relay_control(self.cup_size_pin, True)
        time.sleep(0.16)
        relay_control(self.cup_size_pin, False)
        
        time.sleep(self.human_time) #human delay

        return True # it stays open till the next step closes it
    
    #returns true if the cup is placed and in the right position to get beer
    def cup_activate(self):
        #detect cup in place
        if cup_in_place(self.t_out):
            return True
        else:
            return False 

    # returns true when the beer was already taken
    def already_got_beer(self):
        #pins to set
          
                
        #changes the state of the leds
        led_path = self.working_path + "leds.status"
        f = open(led_path, "w")
        f.write("pouring_chopp")
        f.close()

        time.sleep(self.human_time) #another human delay

        #check if it generates foam TODO
        #valve_control(True)
        #time.sleep(1) #to get some foam 
        #valve_control(False)
        
        if self.size=="small":
            t = self.small_time
        elif self.size=="big":
            t = self.big_time
        
        #set cup to position
        cup_to_position(True)
        
        #start time
        t1 = time.time()
        t2 = time.time()
        sensor = False
        #pouring chopp out
        

        valve_control(True)

        time.sleep(self.human_time) 
        
        print"total", t
        
        while( not sensor): #stops by time or beer level
            t2 = time.time()
            time.sleep(1)
            if (t2-t1)>= t:
                break
            else:
                print "time", t2-t1
            sensor = edge_detector()
            print"value sensor",  sensor
        #stops pouring

        time.sleep(self.human_time) 
        
        valve_control(False)
          
        time.sleep(self.human_time) 

        cup_to_position(False) 
        #making collar and closing chopp
        """
        if self.collar:
            foam(True)
            time.sleep(self.collar_time)
            foam(False)
        """
        #update volume on file 
        volume_path = self.working_path + "volume.vol"
        while(True):
            try:
                f = open(volume_path, "r")
                previous_volume = int(f.read())
                f.close()
                f = open(volume_path, "w")
                f.write("%s"%(previous_volume - self.volume ))
                f.close()
                break
            except:
                print "####### error updating volume" 
        
        #changes the state of the leds
        led_path = self.working_path + "leds.status"
        f = open(led_path, "w")
        f.write("")
        f.close()
       
        gpio.cleanup()
        return True


##################### TEST ########################
if __name__=="__main__":
    #while(True):
    #try:
    machine = MachineController()
    print"chopp test"
    print "Tirando chopp pequeno e pouco colarinho, status:", machine.set_chopp(1)
    print "Abrindo gaveta, status: ",  machine.is_drawer_open()
    print "Posicione o copo na base"
    print "Copo na base:", machine.cup_activate()
    print "Tirar chopp"
    print "chopp, status:", machine.already_got_beer()

       
    #print "Tirando chopp pequeno e pouco colarinho, status:", machine.set_chopp(1)
    #machine.already_got_beer()
    # print "power on nobreak: ", machine.power_on_nobreak()
    #except KeyboardInterrupt:
    #    break 
    #    gpio.cleanup()
    
