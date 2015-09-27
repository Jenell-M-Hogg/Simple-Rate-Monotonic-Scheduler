import pdb

class Task:
    def __init__(self, name, period, execution):
        self.name=name
        self.period=period
        self.execution=execution
        self.timeLeft=execution
        self.available=True

    def checkDeadline(self,t):
        #Checks to see if a task has missed its deadline at time t, returns true if it has, returns false otherwise
        if self.timeLeft!=0:
            x=lcm(t,self.period)
            tLessThanPeriod= t>=self.period and x % t ==0
            tMoreThanPeriod= t % x ==0 and t<=self.period

            if (tLessThanPeriod or tMoreThanPeriod):
                if self.available==True:
                    return True

        return False


    def checkRelease(self,t):
        #Checks to see if a task becomes available at time t, returns true if it does, returns false otherwise
        
        if t % self.period == 0:
            return True
        return False

    def reset(self):
        #Resets the state variables to default
        #Happens when the task is released
        self.timeLeft=self.execution
        self.available=True
        
    def run(self):
        #Given the current time t, run the task from t to t+1. If the task finishes executing, it becomes unavailable
        self.timeLeft=self.timeLeft-1
        if self.timeLeft==0:
            self.available=False
        


def rateMonotonic(tasks):
    tasks=prioritySort(tasks)
    scheduleLength=findScheduleLength(tasks)
    t=0
    schedule=[]

    while (t<scheduleLength):
        
        t,tasks, schedule, deadlineMissed =incrementTime(t,scheduleLength, tasks, schedule)
        
        if deadlineMissed is not "NONE":
            scheduleIsInfeasible(t,schedule, deadlineMissed)
            return "INFEASIBLE"

    printSchedule(schedule)


def prioritySort(tasks):
    #Given a list of tasks, returns a list of the tasks that are sorted by priority (Highest to lowest)
    #This sort is terribly inefficient but I couldn't be bothered. Lol
    sortedT=[tasks[0]]
    for i in range(1,len(tasks)):
        for m in range(len(sortedT)):
             if tasks[i].period<= sortedT[m].period:
                       sortedT.insert(m,tasks[i])
                       
                       break

        if (tasks[i] not in sortedT):
            sortedT.append(tasks[i])
                       
    return sortedT

def findScheduleLength(tasks):
    #Given a list of periodic tasks, find the cyclic schedule length
    length=tasks[0].period
                       
    for i in range(1,len(tasks)):
        length=lcm(length,tasks[i].period)
            
    return length


def incrementTime(t, scheduleLength, tasks, schedule):

    #Find the task with the highest priority that is available. If no tasks are available, be idle!

    for task in tasks:
        if task.available:
            task.run()
            schedule.append(task.name)
            #Don't keep looking after you've run the task
            break
     #After the task has been run, check to make sure no one has missed their deadline. Then update the state variable of a task with reset() if the task was released at t+1                   
    for task in tasks:
        if task.checkRelease(t+1):
            if task.checkDeadline(t+1):
                return t+1,tasks,schedule,task.name
            else:
                if(t+1 != scheduleLength):
                    task.reset()

    
    #If no task was executed (and therefore added to the schedule, be idle!)
    if len(schedule)==t:
        
        schedule.append("IDLE")

    return t+1,tasks,schedule,"NONE"
    
            
def scheduleIsInfeasible(t,schedule,deadlineMissed):


    printSchedule(schedule)

    print(str(deadlineMissed)+" missed its deadline at time " + str(t))
    print("RM does not produce a feasible schedule!")





def printSchedule(schedule):
    print(schedule)
    time=0
    while time<len(schedule):
        chain=0
        i=time
        while schedule[time]==schedule[i] :
            chain=chain+1
            i=i+1
            if i == len(schedule):
                break
        
            

        
        if schedule[time] is not "IDLE":              
            print(schedule[time]+ " executes from time   "+ str(time)+ " to time " +str(time+chain) + " for a total of " + str(chain) +" time units.")

        else:
            print("The system is idle from " + str(time) + " to time "+ str(time+chain)+ " for a total of "+ str(chain) + " time units")
        time=time+chain  
       
        
    

def lcm(x, y):
#This function returns the lowest common multiple of x and y
    lcm = (x*y)//gcd(x,y)
    return lcm

def gcd(x, y):
#   """This function implements the Euclidian algorithm
#   to find G.C.D. of two numbers"""
    while(y):
        x, y = y, x % y

    return x
           
        
def main():
  
    print("This program determines whether or not a schedule for a set of tasks is feasible with the Rate Monotonic Method. If a schedule is feasible with the RM method, it will print it out. If a schedule is not feasible, it print out the schedule up to the first missed deadline")    
    print("Please note the following assumptions:")
    print("(1) Pre-emption is allowed at no extra cost")
    print("(2) The period is the same as the deadline and the release time for all tasks.")
    print("(3) There are NO sporadic tasks")
    print("(4) The execution time and the period are positive integers greater than zero")
    print("")
    anotherGo=True
    while anotherGo:
        try:
            tasks=[]
            while True:
                while True:
                    numberT=raw_input("How many tasks are there to schedule? : ")
                    if type(numberT)==int:
                        print("why are you trying to break my code??")
                    else:
                        break


                for i in range(int(numberT)):
                    while True:
                        period=raw_input("Enter in the period for task T"+str(i+1)+": ")
                        if type(period)== int:
                            print("The period HAS to be an integer. Sorry man.")
                        else:
                            break
                    while True:
                        execution=raw_input("Enter in the execution time (how long it must run) for task "+ str(i)+": ")
                        if type(execution) == int:
                            print("The execution HAS to be an integer. Sorry man")
                        else:
                            break

                    x=Task("T"+str(i+1),int(period),int(execution))
                    tasks.append(x)
                break
            
           
            rateMonotonic(tasks)
            print("Let's schedule another set of tasks!")
            print("")
        
        except:
            print("")
            print("Something went wrong...")

              
def checkTasks(tasks):
    for task in tasks:
        print(task.name)
        print("Period: "+ str(task.period))
        print("Execution Time: " + str(task.timeLeft)+ "out of " +str(task.execution)+ "remaining")
        print("Is available? " + str(task.available))



def checkTest():
    x=Task("T1",2,1)
    x1=Task("T2",4,  2)
    rateMonotonic([x,x1])

main()
