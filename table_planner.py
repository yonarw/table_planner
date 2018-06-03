
import codecs
import pygraphviz as pgv
from random import randint,shuffle
import time

num_tables = 3
places_per_table = 5

def read_all(fname):
    f = codecs.open(fname, 'r', encoding='utf8')
    lines = f.readlines()
    res = []
    for l in lines:
        l = l.replace("\n","")
        x = l.split(",")
        cx = []
        if len(x) >= 2:
            try:
                x[1] = int(x[1])
            except:
                continue
        for c in x:
            if type(c) is str:
                c = c.replace(" ","")
                c = c.replace("&","+")
                if c != "":
                    cx.append(c)
            else:
                cx.append(c)
        res.append(cx)
    return res


def eval_table(T, grp, PG):
    '''
    :param T: table
    :param grp: group to add
    :param PG: person graph
    :return: score for table
    '''
    score = 0
    for p in T[1]:
        if p in PG[grp][1]:
            score += 1
        else:
            # score -= 1
            pass
    return score

def make_assigns(PG={}):
    tables = []
    #table is num persons, person list, score for table
    for x in range(0,num_tables):
        tables.append([0,[],0])
    q = list(PG.keys())
    shuffle(q)
    s = []  #zugewiesen
    curr = ""
    while len(q) > 0:
        if curr == "":
            curr = q.pop(0)
        if not curr in s:
            if curr in q:
                q.remove(curr)
            free_tables = []
            for t in tables:
                if t[0] + PG[curr][0] <= places_per_table:
                    sc = eval_table(t, curr, PG)
                    free_tables.append([sc,t])
            if len(free_tables) == 0:
                #print("no table found for", curr)
                return [[0,[],0]]
            fts = sorted(free_tables, key=lambda ft: ft[0],reverse=True)
            #print(curr,":")
            if fts[0][0] == 0:
                tbls = sorted(free_tables, key=lambda t:t[1][0]) #take table with most places free
                t = tbls[0][1]
            else:
                t = fts[0][1] #table with highest score
                t[2] += fts[0][0]
            t[1].append(curr)
            t[0] += PG[curr][0]
            s.append(curr)
            #set next group from preferenced
            numprefs = len(PG[curr][1])
            if numprefs > 0:
                curr = PG[curr][1][randint(0, numprefs-1)]
            else:
                curr = ""
        else:
            if curr in q:
                q.remove(curr)
            curr = ""

    return tables

if __name__ == "__main__":
    G = pgv.AGraph()

    ppl = read_all("party.csv")

    PG = {}

    for x in ppl:
        G.add_node(x[0])
        PG[x[0]] = [x[1],[]]

    num_edges = 0

    for x in ppl:
        #print(x[0],"(",x[1],")",":")
        refs = PG[x[0]][1]
        for pref in x[2:]:
            if pref != "":
                # print("    ",pref)
                G.add_edge(x[0],pref)
                if not pref in refs:
                    num_edges += 1
                    refs.append(pref)
                orefs = PG[pref][1]
                if not x[0] in orefs:
                    num_edges += 1
                    orefs.append(x[0])

    print("nodes = ",len(PG),"edges = ",num_edges)

    G.layout(prog="dot")
    G.draw("party_dependencies.png")

    #for x in PG:
    #    print(x,"(",PG[x][0],")","->",PG[x][1])

    T_best = None
    best_score = -10000
    gs = 0
    make_movie = False
    while T_best == None:
        for i in range(0,10000):
            T = make_assigns(PG)
            scoresum = 0
            for t in T:
                scoresum += t[2]
            if len(T) > 1 and make_movie:
                GT = pgv.AGraph()
                tb = 0
                for t in T:
                    for ppl in t[1]:
                        GT.add_edge("Tisch_" + str(tb), ppl)
                    tb += 1
                GT.layout("neato")
                GT.draw("tries/tables_"+str(gs)+".png")
                gs += 1
            if scoresum > best_score:
                T_best = T
                best_score = scoresum
                print("new best score=",best_score)

    GT = pgv.AGraph()
    tb = 0
    for t in T_best:
        for ppl in t[1]:
            GT.add_edge("table " + str(tb), ppl)
        tb += 1
    GT.layout("fdp")
    GT.draw("tables.png")




