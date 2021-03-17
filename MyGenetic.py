import random

class Chromosome:
    def __init__(self, genes, fitness):
        self.Genes = genes
        self.Fitness = fitness

def createPop(popSize, min, max):
    D = len(min)
    pop = []
    for i in range(0, popSize):
        chrom = []
        for j in range(0, D):
            chrom.append(random.uniform(min[j],max[j]))
        fitness = None
        pop.append(Chromosome(chrom, fitness))
    return pop

def mutate(chrom, min, max):
    index = random.randrange(0, len(min))
    newGene = random.uniform(min[index], max[index])
    Genes = chrom.Genes[:]
    Genes[index] = newGene
    return Chromosome(Genes, None)

def crossover(chrom1, chrom2):
    index = random.randrange(0, len(chrom1.Genes))
    newChrom1 = Chromosome(chrom1.Genes[:index]+chrom2.Genes[index:], None)
    newChrom2 = Chromosome(chrom2.Genes[:index]+chrom1.Genes[index:], None)
    return (newChrom1, newChrom2)

def minFit(pop):
    N = len(pop)
    idx = 0
    val = pop[0].Fitness
    for i in range(1, N):
        if pop[i].Fitness<val:
            val = pop[i].Fitness
            idx = i
    return (val, idx)
