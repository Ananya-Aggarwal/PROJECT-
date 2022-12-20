import sys
import mysql.connector
import random
mydb=mysql.connector.connect(host="localhost" ,user="root",passwd="Aggarwal@123",database="quiz")
mycursor=mydb.cursor()
def display_hangman(tries):
    stages = [ """
        --------
        |  |
        |  O
        | \|/
        |  |
        | / \

        """,
        """
        --------
        |  |
        |  O
        | \|/
        |  |
        |

        """,
        """
        --------
        |  |
        |  O
        |  |
        |  |
        | / \

        """,
        """
        --------
        |  |
        |
        |
        |
        |
        """
               ]
    return stages[tries]

#CODE TO ENTER MORE QUESTION:-
def Question():
    question="Yes"
    while question=="Yes" or question=="yes":
        print("Welcome to Question Portal")
        print("__________________________________\n")
        q=input("Enter the question :")
        op_1=input("Enter the option 1: ")
        op_2=input("Enter the option 2: ")
        op_3=input("Enter the option 3: ")
        op_4=input("Enter the option 4: ")
        answer=0
        while answer==0:
            option=int(input("Which option is correct answer (1,2,3,4): "))
            if option==1:
                answer=op_1
            elif option==2:
                answer=op_2
            elif option==3:
                answer=op_3
            elif option==4:
                answer=op_4
            else:
                print("Please choose the correct option as answer.")
        mycursor.execute("Select * from questions")
        data=mycursor.fetchall()
        qid=(mycursor.rowcount)+1
        mycursor.execute("Insert into questions values (%s,%s,%s,%s,%s,%s,%s)",(qid,q,op_1,op_2,op_3,op_4,answer))
        mydb.commit()
        print("Question Added.")
        question=input("Do you want to add more question: ")
    Home()

#CODE TO START THE QUIZ
def Quiz():
    print("Welcome to Quiz portal")
    print("_______________________________________\n")
    mycursor.execute("Select * from questions")
    data=mycursor.fetchall()
    name=input("Enter your name: ")
    rc=mycursor.rowcount
    noq=int(input("Enter the number of questions to attempt (max %s):" %rc))
    if noq<3:
        print("Minimum number of question is 3.")
        noq=int(input("Enter the number of questions to attempt (max %s):" %rc))
    l=[]
    while len(l)!=noq:
        x=random.randint(1,rc)
        if l.count(x)>0:
            l.remove(x)
        else:
            l.append(x)
    print("Quiz has started")
    count=1
    score=0
    for i in range(0,len(l)):
        mycursor.execute("Select * from questions where qid=%s",(l[i],))
        ques=mycursor.fetchone()
        print("--------------------------------------------------------------------------------------------")
        print("Q.",count,":",ques[1])
        print("A.",ques[2],"\t\tB.",ques[3])
        print("C.",ques[4],"\t\tD.",ques[5])
        print("--------------------------------------------------------------------------------------------\n")
        count+=1
        tries=0
        ans=None
        while ans==None:
            choice=input("Enter your answer (A,B,C,D): ")
            if choice=="A" or choice=="a":
                ans=ques[2]
            elif choice=="B" or choice=="b":
                ans=ques[3]
            elif choice=="C" or choice=="c":
                ans=ques[4]
            elif choice=="D" or choice=="d":
                ans=ques[5]
            else:
                print("Kindly select A,B,C,D as option only")
        if ans==ques[6]:
            print("Correct")
            score+=1
            print("Your Current Score is:",score)
            tries+=1
        else:
            print("Incorrect.")
            print("Correct answer is:",ques[6])
            print(display_hangman(count-score-2))
            print("Your Current Score is:",score)
            if count-score-2==2:
                print("Sorry, try again.")
                print("_____________________________________________")
                Home()
                break
    print("Quiz has ended!")
    print(name.upper()+"'s","FINAL SCORE IS:",score)
    input("Press any key to continue: ")
    Home()

def Home():
    f=1
    while f!=3:
        print("Welcome to Quiz")
        print("********************")
        print("1. Enter Questions")
        print("2. Take Quiz")
        print("3. Exit")
        f=int(input("Enter your choice: "))
        if f==1:
            Question()
        elif f==2:
            Quiz()
        elif f==3:
            print("Exiting the Quiz.")
            print("Thank You for Playing!")
            mycursor.close()
            mydb.close()
            sys.exit()
        else:
            print("Kindly select 1,2,3,4 as option only")
            Home()
Home()
