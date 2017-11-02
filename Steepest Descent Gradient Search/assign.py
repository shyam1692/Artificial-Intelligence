import sys
#cost_evaluate(teams[1])
def cost_evaluate(x):
    lenx=len(x)
    cost=0
    for member in x:
        if (lenx != individuals[member]['team_size_prefer']) and (individuals[member]['team_size_prefer'] !=0):
            cost=cost+1
        #Check if preferred teammate in list    
        for preferred_teammate in individuals[member]['preferred_list']:
            if preferred_teammate not in x:
                cost=cost+n
        #Check if averse person in list
        for averse_teammate in individuals[member]['non_preferred']:
            if averse_teammate in x:
                cost=cost+m
    return cost
                

#Add to team
def add_to_team(x):
    #global count_empty_spaces
    #global count_add
    global cost_change
    global index_from
    global index_to
    global member_to
    global member_from    
    global temp1_final
    global temp2_final
    if len(teams[x])==1:
        member=teams[x][0]
        for i in list(range(0,len(teams)-1)):
            if (len(teams[i]) in [0,3]) or i==x:
                continue
            temp1=list(teams[i])
            temp1.append(member)
            if cost_evaluate(temp1) - (cost_evaluate(teams[x]) + cost_evaluate(teams[i]))-k < cost_change :
                cost_change= cost_evaluate(temp1) - (cost_evaluate(teams[x]) + cost_evaluate(teams[i]))-k
                temp2_final=list(temp1)
                temp1_final=list([])
                index_from=x
                index_to=i
                member_from=member  #If length=1, only 1 member added
                #teams[i].append(teams[x].pop())
                #individuals[member]['team_index']=i
                #count_empty_spaces = count_empty_spaces+1
                #count_add=count_add+1
                #break
    if len(teams[x])==2:        
        for member in teams[x]:
            for teammate in individuals[member]['preferred_list']:
                if (individuals[teammate]['team_index'] != individuals[member]['team_index']) and len(teams[ individuals[teammate]['team_index'] ]) !=1:
                    temp1=list(teams[x] + [teammate])
                    temp2=list(teams[ individuals[teammate]['team_index'] ])
                    del(temp2[temp2.index(teammate)])
                    if (cost_evaluate(temp1) + cost_evaluate(temp2)) - (cost_evaluate(teams[x]) + cost_evaluate(teams[individuals[teammate]['team_index']])) < cost_change:
                        cost_change= (cost_evaluate(temp1) + cost_evaluate(temp2)) - (cost_evaluate(teams[x]) + cost_evaluate(teams[individuals[teammate]['team_index']]))
                        temp1_final=list(temp1)
                        temp2_final=list(temp2)
                        #index_from=i #Adding to x here
                        index_to=x
                        index_from=individuals[teammate]['team_index']
                        member_from=teammate                        
                        #teams[x]=list(temp1)
                        #teams[individuals[teammate]['team_index']] = list(temp2)
                        #individuals[teammate]['team_index']=individuals[member]['team_index']
                        #count_add=count_add+1
                        #break
                        

                
                
def member_exchange(x):
    global count
    global cost_exchange
    global temp1_final_exchange
    global temp2_final_exchange
    global from_team_exchange_index
    global to_team_exchange_index
    global other_member_exchange
    global other_member_teammate_exchange
    for member in teams[x]:
        for teammate in individuals[member]['preferred_list']:
            if individuals[teammate]['team_index'] != individuals[member]['team_index']:
                for other_member in teams[x]:                                            
                    for other_member_teammate in teams[individuals[teammate]['team_index']]:
                        temp1=list(teams[x])
                        temp2=list(teams[individuals[other_member_teammate]['team_index']])
                        (temp1[temp1.index(other_member)],temp2[temp2.index(other_member_teammate)])=(temp2[temp2.index(other_member_teammate)],temp1[temp1.index(other_member)])
                        #cost1=cost_evaluate(teams[x])
                        #cost2=cost_evaluate(teams[individuals[other_member_teammate]['team_index']])
                        if (cost_evaluate(temp1) + cost_evaluate(temp2))-(cost_evaluate(teams[x]) + cost_evaluate(teams[individuals[other_member_teammate]['team_index']])) < cost_exchange:
                            temp1_final_exchange=list(temp1)
                            temp2_final_exchange=list(temp2)
                            from_team_exchange_index=x
                            to_team_exchange_index=individuals[other_member_teammate]['team_index']
                            other_member_exchange=other_member
                            other_member_teammate_exchange=other_member_teammate
                                        
#Empty Spaces init
count_empty_spaces=0                            
filename=sys.argv[1]                        
#k per team
k=int(sys.argv[2])

#Not work with / averse cost
m=int(sys.argv[3])

#Work with but not get cost
n=int(sys.argv[4])
teams=[]
cost=[]
individuals={}
f=open(filename)
for line in f:
    individuals[(line.split()[0])]={}
    individuals[(line.split()[0])]['team_index']=-1
    #Adding preferred
    individuals[(line.split()[0])]['preferred_list']=line.split()[2].split(",")
    if individuals[(line.split()[0])]['preferred_list']==["_"]:
        individuals[(line.split()[0])]['preferred_list']=[]
    individuals[(line.split()[0])]['non_preferred']=line.split()[3].split(",")
    #Adding non preferred
    if individuals[(line.split()[0])]['non_preferred']==["_"]:
        individuals[(line.split()[0])]['non_preferred']=[]
    #Adding team_size_prefer
    individuals[(line.split()[0])]['team_size_prefer']=float(line.split()[1])
    
f.close()



#Forming of Teams and updating team_index
for person in individuals:
    if individuals[person]['team_index']==-1:
        teams.append([person])
        individuals[person]['team_index']=len(teams)-1
        individuals[person]['array_team_index']=0
        count=0
        while (len(teams[ individuals[person]['team_index'] ])< individuals[person]['team_size_prefer']) and count<len(individuals[person]['preferred_list']):
           for teammate in individuals[person]['preferred_list']:
             count=count+1  
             if individuals[teammate]['team_index']==-1:
                teams[ individuals[person]['team_index'] ].append(teammate)
                individuals[teammate]['team_index']=individuals[person]['team_index']
                individuals[teammate]['array_team_index']=len(teams[ individuals[person]['team_index'] ])-1
              
    else:
        continue
    
#Calculating cost of each team
for team in teams:
    cost.append(cost_evaluate(team))



#Emulating Do while in python - https://coderwall.com/p/q_rd1q/emulate-do-while-loop-in-python
while True:    
    #Adding Team    
    cost_change=0
    index_from=0
    index_to=0
    member_from=''
    member_to=''
    temp1_final=[]
    temp2_final=[]
    count_empty_spaces=0
    count_add=0
    for j in list(range(0,(len(teams)-0))):
        add_to_team(j)        
        
    if cost_change<0:
        if len(teams[index_from])==1:                        
            teams[index_to].append(teams[index_from].pop())
            individuals[member_from]['team_index']=index_to
            count_empty_spaces = count_empty_spaces+1
            count_add=count_add+1            
        else:
            teams[index_to]= list(temp1_final)
            teams[index_from]=list(temp2_final)
            individuals[member_from]['team_index']=index_to
            count_add=count_add+1                        

#Exchange function called 
    count=0
    cost_exchange=0
    temp1_final_exchange=[]
    temp2_final_exchange=[]
    other_member_exchange=''
    other_member_teammate_exchange=''
    from_team_exchange_index=0
    to_team_exchange_index=0
    for i in list(range(0,(len(teams)-0))):
        member_exchange(i)
        
    if cost_exchange<0:
        teams[from_team_exchange_index]=list(temp1_final_exchange)
        teams[individuals[other_member_teammate_exchange]['team_index']] = list(temp2_final_exchange)
        individuals[other_member_exchange]['team_index']=individuals[other_member_teammate_exchange]['team_index']
        individuals[other_member_teammate_exchange]['team_index']=from_team_exchange_index
        count=count+1
        
    if count  + count_add ==0:
        break
    
    
    
    
    
#Computing Final Cost
final_teams=[]
for team in teams:
    if team!=[]:
        final_teams.append(team)
        
cost=[]
#Calculating cost of each team
for team in final_teams:
    cost.append(cost_evaluate(team))
    
final_cost=sum(cost) + (len(final_teams))*k

for team in final_teams:
   print( " ".join([element for element in team]))
   
print(final_cost)