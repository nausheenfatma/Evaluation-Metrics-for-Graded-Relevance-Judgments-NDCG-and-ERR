# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 13:45:14 2016

@author: nausheenfatma
"""

import math
import glob


class Evaluation: #for graded evaluations
    
    def __init__(self):
        self.ranked_list=[]
        self.ideal_list=[]
        self.grade_list=[]
        self.rank_items={} #key=rank,value=count of items for the rank
        self.gmax=4 #grademax,where grade begins from 0 
        self.grade_satisfaction_probability={0:0,1:1/float(math.pow(2,self.gmax)),2:3/float(math.pow(2,self.gmax)),3:7/float(math.pow(2,self.gmax)),4:15/float(math.pow(2,self.gmax))}
        
    
    def NDCG(self,evaluated_list):
        actual_list=evaluated_list[:]
        evaluated_list.sort(reverse=True)
        ideal_list=evaluated_list
        print "evaluated_list",actual_list
        print "ideal_list",ideal_list
        evaluated_dCG=self.find_DCG(actual_list)
        for item in actual_list:
            try :
                self.rank_items[item]=self.rank_items[item]+1
            except :
                self.rank_items[item]=1
        print "evaluated_dCG",evaluated_dCG
        ideal_DCG=self.find_DCG(ideal_list)
        print "ideal_DCG",ideal_DCG
        NDCG=evaluated_dCG/float(ideal_DCG)
        print "NDCG :",NDCG
        return NDCG
        
        
    def find_DCG(self,rankedlist):
        rankedlist_len=len(rankedlist)
        DCG_value=rankedlist[0]
        for i in range(1,rankedlist_len):
            answer = (rankedlist[i]-1)/float(math.log10(i+1)/float(math.log10(2)))
            DCG_value=DCG_value+answer
        
        return DCG_value
    
    def find_average_NDCG(self,arrayoflists):
        total_no_of_lists=len(arrayoflists)
        sum_NDCG=0
        for item in arrayoflists:
            print "---------------------------------------------------------"
            NDCG_item=self.NDCG(item)
            sum_NDCG=sum_NDCG+NDCG_item
        averageNDCG=sum_NDCG/float(total_no_of_lists)
        return averageNDCG
        
        
    def find_average_ERR(self,arrayoflists):
        total_no_of_lists=len(arrayoflists)
        #print "total_no_of_lists",total_no_of_lists
        sum_ERR=0
        for item in arrayoflists:
            print "---------------------------------------------------------"
            ERR_item=self.findERR(item)
            

            sum_ERR=sum_ERR+ERR_item
        averageERR=sum_ERR/float(total_no_of_lists)  
        return averageERR  
        
    def findERR(self,ranklist):
        print "evaluated list",ranklist
        pos=0
        ERR=0
        prev=[] # for storing previous grade_satisfaction_probability uptil pos i
        
        for grade in ranklist:
            rank=pos+1 #rank is the position in array starting from 1
            pos=pos+1
            rank_inverse=1/float(rank)
            p=self.grade_satisfaction_probability[grade]
            mult_score=1
            for k in prev:
                mult_score=mult_score*(1-k)
            mult_score=mult_score*p
            ERR=ERR+rank_inverse*mult_score
            prev.append(self.grade_satisfaction_probability[grade])
        
        print "ERR : ",ERR
        return ERR          
            
        
if __name__=='__main__' :
    e=Evaluation()
    
    average_NDCG=e.find_average_NDCG([[2,3,1,4,1,2,2,3],[1,2,3,3,4,0,0]])
    average_ERR=e.find_average_ERR([[2,3,1,4,1,2,2,3],[1,2,3,3,4,0,0]])
    print "--------------------------------------------------------"
    print "average_NDCG : ",average_NDCG
    print "average_ERR : ",average_ERR
    print "--------------------------------------------------------"
    
        
        
    