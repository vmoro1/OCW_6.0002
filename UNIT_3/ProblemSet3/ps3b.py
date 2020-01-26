import random
import pylab
#import ps3b_precompiled_37
#random.seed(0)


class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce.
    """


class SimpleVirus(object):
    """
    Representation of a simple virus(does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance.
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ 
        Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        return random.random() <= self.clearProb
    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        if random.random() <= self.maxBirthProb * (1 - popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException(Exception)



class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses

    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop

    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step by executing the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated.
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        tmp_viruses = self.viruses[:]
        for virus in tmp_viruses:   
            if virus.doesClear():
                self.viruses.remove(virus)
            else:
                popDensity = min(len(self.viruses) / self.maxPop, 1)
                try:
                    self.viruses.append(virus.reproduce(popDensity))
                except NoChildException:
                    continue                   
        return len(self.viruses)



def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    The simulation runs and plots the graph for a regular patient( no drugs are 
    used, viruses do not have any drug resistance).    
    For each of trials: instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    virus_population_sizes = 300 * [0]
    for trial in range(numTrials):
        viruses = []
        for virus in range(numViruses):
            viruses.append(SimpleVirus(maxBirthProb, clearProb))
        patient = Patient(viruses, maxPop)
        for timeStep in range(300):
            patient.update()
            virus_population_sizes[timeStep] += float(patient.getTotalPop())
    
    average_population = []
    for  population_size in virus_population_sizes:
        average_population.append(population_size / numTrials)
    pylab.figure()
    pylab.plot(average_population, label = 'SimpleVirus')
    pylab.title('SimpleVirus simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.legend(loc = 'best')
    pylab.show()    



class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb )
        self.resistances = resistances
        self.mutProb = mutProb

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances
        
    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb
    
    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug.

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug and False
        otherwise.
        """
        if drug in self.resistances:
            return self.resistances[drug]
        else:
            return False

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. A virus particle will only reproduce if it is resistant to
        all the drugs in the activeDrugs list. 
        For example, if there are 2 drugs in the activeDrugs list and the virus
        particle is resistant to 1 or no drugs, then it will not reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      
        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus. The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       
        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle.Raises a NoChildException if this 
        virus particle does not reproduce.
        """
        reproduce = True
        for drug in activeDrugs:
            if not self.resistances[drug]:
                reproduce = False
        if reproduce:
            if random.random() <= self.maxBirthProb * (1 - popDensity):
                copy_resistances = self.resistances.copy()
                for trait in copy_resistances:
                    if random.random() <= self.mutProb:
                        copy_resistances[trait] = not copy_resistances[trait]
                return ResistantVirus(self.maxBirthProb, self.clearProb, 
                                      copy_resistances, self.mutProb)
            else:
                raise NoChildException(Exception)
        else:
            raise NoChildException(Exception)
                


class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        initializes viruses, maxPop and the list of drugs being administered
        (initially includes no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)
        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses, maxPop)
        self.active_drugs = []


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).
        """
        if newDrug not in self.active_drugs:
            self.active_drugs.append(newDrug)                  

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.active_drugs


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        nonresistantPopulation = 0
        for virus in self.viruses:
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    nonresistantPopulation += 1
                    break
        resistantPopulation = self.getTotalPop() - nonresistantPopulation
        return resistantPopulation

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        tmp_viruses = self.viruses[:]
        for virus in tmp_viruses:   
            if virus.doesClear():
                self.viruses.remove(virus)
            else:
                popDensity = min(len(self.viruses) / self.maxPop, 1)
                try:
                    self.viruses.append(virus.reproduce(popDensity, self.active_drugs))
                except NoChildException:
                    continue                   
        return len(self.viruses)



def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    For each of the trials: instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    """
    virus_population = 300 * [0]
    resistant_population = 300 * [0]
    for trial in range(numTrials):
        viruses = []
        for virus in range(numViruses):
            viruses.append(ResistantVirus(maxBirthProb, clearProb,  resistances, mutProb))
        patient = TreatedPatient(viruses, maxPop)
        for timeStep in range(150):
            patient.update()
            virus_population[timeStep] += float(patient.getTotalPop())
            resistant_population[timeStep] += float(patient.getResistPop(['guttagonol']))
        patient.addPrescription('guttagonol')
        for timeStep in range(150, 300):
            patient.update()
            virus_population[timeStep] += float(patient.getTotalPop())
            resistant_population[timeStep] += float(patient.getResistPop(['guttagonol']))
        
    average_population = []
    average_resistant_population = []
    for total_population, total_resistant_population in zip(virus_population, resistant_population):
        average_population.append(total_population / numTrials)
        average_resistant_population.append(total_resistant_population / numTrials)
    pylab.figure()
    pylab.plot(average_population, label = 'Total population')
    pylab.plot(average_resistant_population, label = 'Resistant population' )
    pylab.title('ResistantVirus simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.legend(loc = 'best')    
    pylab.show()    