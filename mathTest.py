import time
import random
import sys
    
DefaultNumberRange = 10
DefaultQuestionCount = 100
OutputFileName="mathTests.txt"
  
class MathOperator:
   def __init__(self):
      self.NotSet=0;
      self.Add=1;
      self.Sub=2;
      self.Multi=3;
      self.Div=4;
      
      self.NotSetStr="NotSet";
      self.AddStr="+";
      self.SubStr="-";
      self.MultiStr="X";
      self.DivStr="/";
      
      
   def getString(self, operator):
     
      if(operator==self.Add ):          
         return self.AddStr;
      elif operator==self.Sub :
         return self.SubStr;
      elif (operator==self.Multi):    
         return self.MultiStr;
      elif (operator==self.Div):    
         return self.DivStr;      
      else :
         return self.NotSetStr;

   
   
class OperatorOption:
   def __setOpOptions(self, add, sub, mul, div ):
      self.add=add
      self.sub=sub
      self.multi=mul
      self.div=div
       
      self.opList=[];
      
      if( self.add==True):
        self.opList.append(MathOperator().Add)
     
      if(self.sub==True):
        self.opList.append(MathOperator().Sub)
     
      if(self.multi==True):   
        self.opList.append(MathOperator().Multi)
     
      if(self.div==True):
        self.opList.append(MathOperator().Div)
     
      
   def __init__(self, add=True, sub=False, multi=False, div=False ):
      self.opList = list();
      
      self.__setOpOptions(add, sub, multi, div  )     
      
       
   def getRandomOperator(self):      
      return random.choice(self.opList)
  
   def getOptionString(self):
      opListStr=""
      for op in self.opList:
         opListStr = opListStr + " " + MathOperator().getString(op)
         
      return opListStr
 
   
 
class QuestionItem(object):
    
    __questionText="default question";
    __answerText="default answer";
    
    @property    
    def questionText(self):
       return self.__questionText

    @property    
    def answerText(self):
       return str(self.__answerText)
       
       
    def __updateQuestionText(self):
      self.__questionText= str(self.arg1)+" "+ MathOperator().getString(self.operator) + " "+str(self.arg2) + " =   ";
       
    def __updateAnswerText(self):
       
      if( self.operator== MathOperator().Add):
         self.__answerText = self.arg1 + self.arg2;
      elif(self.operator== MathOperator().Sub):
         self.__answerText = self.arg1 - self.arg2;
      elif(self.operator== MathOperator().Multi):
         self.__answerText = self.arg1 * self.arg2;
      elif(self.operator== MathOperator().Div):
         self.__answerText = self.arg1 / self.arg2;
       
    
    def __init__(self, arg1, arg2, op):
           
      self.arg1=arg1;
      self.arg2=arg2;
      self.operator = op;
      self.__updateQuestionText();
      # now question text is set and ready
      
      self.__updateAnswerText();
           
      
      
class QuestionGenerator:
   # eg. 0 --20 , +
   def __init__(self, argRangeLower, argRangeUpper, opOption, allowNegative=False):
      self.argRangeLower = argRangeLower;
      self.argRangeUpper = argRangeUpper;
      self.OpOption = opOption;
      self.allowNegative = allowNegative
  
   def __getRandomArg(self, avoidZero = False):
      
      if(avoidZero):
          while(True):
            randomArg = random.randint(self.argRangeLower, self.argRangeUpper)            
            if(not (randomArg==0)):
               break;
      else :
          randomArg = random.randint(self.argRangeLower, self.argRangeUpper)            
      return randomArg;
    
          
     
   def generateQuestion(self):
      
      op = self.OpOption.getRandomOperator()
      arg1 = self.__getRandomArg()
      
      if(op==MathOperator().Div):
         # if it's div, avoid use zero as arg2
         arg2 = self.__getRandomArg(True)
      else:
         arg2 = self.__getRandomArg()
      
      if(not self.allowNegative and op==MathOperator().Sub):
         # if negative is not allow, if it's - , then , bigger number should be arg1
          if(arg2>arg1):
              temp = arg1
              arg1=arg2
              arg2=temp
      
      quest = QuestionItem(arg1, arg2, op);

            
      return quest;
      
   # return a ques list
   def generateQuestionList(self, n=20):
   
      questionList = list();   
      for i in range(n):
        questionItem = self.generateQuestion();
        questionList.append(questionItem);

      return questionList      
      
        

   def printAllQuestions(self, fileObj, questlist):
   
      i=0
      for q in questlist :
         i=i+1
         indexStr = "(" + str(i)+")  "
         fileOutput(fileObj, indexStr + q.questionText+"\n");
    
   def printAllAnswers(self, fileObj, questlist):
     i=0
     for q in questlist :
        i=i+1
        indexStr = "(" + str(i)+") "
        fileOutput(fileObj, indexStr + q.answerText+"  ");
   
   def printOptions(self):
      print("")
      print("")
      print("Question generator Option: ")
      print("argument range " + str(self.argRangeLower) + " - " + str(self.argRangeUpper )) 
      print("Operator is " + self.OpOption.getOptionString())
      if( self.allowNegative ) :
         print("Negative number is allowed")
      else:    
         print("Negative number is NOT allowed")
      #self.OpOption = opOption;
      #self.allowNegative = allowNegative


# ask user questions and create generator object, return
def UI_getUserInput_Create_Generator():
   
   add = False
   sub = False
   mul = False
   div = False
   neg = False
   
   inpu = raw_input("do you want ADD ? (y/n) ,  [Enter] means y")
   if(inpu == "y" or inpu == "Y" or inpu ==""):
      add = True
   
   inpu = raw_input("do you want Subtraction ? (y/n), [Enter] means y")
   if(inpu == "y" or inpu == "Y" or inpu ==""):
      sub = True
   
   inpu = raw_input("do you want multiply ? (y/n), [Enter] means y")      
   if(inpu == "y" or inpu == "Y"  or inpu ==""):
      mul = True
      
   inpu = raw_input("do you want Divide ? (y/n), [Enter] means y")
   if(inpu == "y" or inpu == "Y"  or inpu ==""):
      div = True
      
   if(sub==True):
      inpu = raw_input("do you want negative numbers ? ")
      if(inpu == "y" or inpu == "Y" ):
         neg = True
      else :
         neg = False
         
   if(add==False and sub==False and mul==False and div==False):
      fileOutput("no operator is needed ??  enable Add")
      add=True
   
   opOption=OperatorOption(add, sub, mul, div);

   numRange = raw_input("number range max (integer), ie. 10: ")
   if(numRange==""):
      #default range value
      numRange = DefaultNumberRange
   else:
      numRange =int(numRange)
      
   return  QuestionGenerator(0, numRange, opOption, neg)   
   
 

def fileOutput(fileObj, text):
    #print(text)  output to screen
    
   fileObj.write(text)
    
   
def main():


   print("in main() ");
     
   generator = UI_getUserInput_Create_Generator();
   
   
   generator.printOptions()
      
   print("")
      
   inpu = raw_input("How many questions do you want ? ie. 50:  ")   
   
   if( inpu==""):
      inpu=DefaultQuestionCount
   
   qlist = generator.generateQuestionList(int(inpu));
   
   print("")
   print("")


   fileobj = open('mathTests.txt', 'w')
    
   generator.printAllQuestions(fileobj, qlist);
   
   print("")
   print("")
   print("")
   print("")
   
   fileOutput(fileobj, "\n\n")
   generator.printAllAnswers(fileobj, qlist);

   fileobj.close(); 

   print("Done, check "+ OutputFileName)
   
main()
   











