#Idea: A goal tracker.
# Program asks for user to enter in a goal that they accomplished. 
# Asks user about goal difficulty (easy, medium, hard), 
# when it was completed (month with day and year),
# and to add a short reflection about the goal 
# Goal gets saved to a txt file and user is able to view a list of their completed goals 
#completed by difficulty and ascending date

from tkinter import *
from tkinter import messagebox
from datetime import datetime #need for validating the date

class GoalTrackerGUI:
    def __init__(self):
        self.main_window = Tk()
        self.main_window.title('Goal Tracker')
        self.view_goals() #calling function at beginning

        #establishing the frames
        self.top_frame = Frame()
        self.middle_difficulty_frame = Frame()
        self.middle_date_frame = Frame()
        self.middle_reflection_frame = Frame()
        self.middle_reflection_entry_frame = Frame()
        self.bottom_frame = Frame()

#TOP FRAME; no actual entries in this one
        self.goal_prompt_label = Label(self.top_frame,
                                      text = "Completed a new goal? Enter it below:")
        self.goal_prompt_label.pack(side='bottom')

#MIDDLE FRAMES #Asking for user input; difficulty, date, reflection
    #goal difficulty
        self.difficulty_label = Label(self.middle_difficulty_frame,
                                          text = "Enter difficulty (easy/medium/hard):")
        self.difficulty_entry = Entry(self.middle_difficulty_frame,
                                      width=8)
        #packing
        self.difficulty_label.pack(side='left')
        self.difficulty_entry.pack(side='left')
        
    #date
        self.date_label = Label(self.middle_date_frame,
                                text = "Enter date of completion (mm/dd/yyyy):")
        self.date_entry = Entry(self.middle_date_frame,
                                width=10)
        #packing
        self.date_label.pack(side='left')
        self.date_entry.pack(side='left')

    #the goal and reflection
        self.goal_reflection_label = Label(self.middle_reflection_frame,
                                      text="Enter in the goal with a short reflection:")
        self.goal_reflection_entry = Entry(self.middle_reflection_entry_frame,
                                       width=70)
        #packing
        self.goal_reflection_label.pack(side='left')
        self.goal_reflection_entry.pack(side='left')

        #label for viewing the goals
        self.sorted_goals_value = StringVar()
        self.sorted_goals_label = Label(self.bottom_frame,
                                        textvariable=self.sorted_goals_value)
        self.sorted_goals_label.pack(side='bottom')

#BOTTOM FRAME #buttons: view goals, save, save and quit, quit without saving
    #create buttons for bottom frame:
        #view goals buttons; need 2 now bc difficulty and date
        self.view_goal_difficulty = Button(self.bottom_frame,
                                           text = "View goals by difficulty",
                                           command=self.sort_goals_difficulty)
        self.view_goal_date = Button(self.bottom_frame,
                                           text = "View goals by ascending date",
                                           command=self.sort_goals_date)

        #save_goal button... messed up names but the save goal button adds the add goal. don't forget
        self.save_goal_button = Button(self.bottom_frame,
                                       text = "Save Goal",
                                       command=self.add_goal)

        #quit button
        self.quit_button = Button(self.bottom_frame,
                                      text = 'Quit',
                                      command=self.main_window.destroy)

        #pack the bottom frame buttons:
        self.view_goal_difficulty.pack(side='left',padx=10)
        self.view_goal_date.pack(side='left',padx=10)
        self.save_goal_button.pack(side='left',padx=10)
        self.quit_button.pack(side='left',padx=10)
        
#PACK THE FRAMES HERE:
        self.top_frame.pack()
        self.middle_difficulty_frame.pack()
        self.middle_date_frame.pack()
        self.middle_reflection_frame.pack()
        self.middle_reflection_entry_frame.pack()
        self.bottom_frame.pack()

        mainloop() #REMEMBER TO HAVE THIS. The GUI won't show up otherwise

    #adds goal
    def add_goal(self): #gets goal difficulty, completion date, and reflection (one function)
        #we have to get the entries for each of these 3 variables
        goalDifficulty = self.difficulty_entry.get().lower() #takes input and makes lowercase
        completionDate = self.date_entry.get()
        goalAndReflection = self.goal_reflection_entry.get()
        #validating difficulty
        if goalDifficulty not in ['easy','medium','hard']: 
            messagebox.showinfo('Error',\
                                'Please enter a valid difficulty')
            return #return prevents from clearing out entries
        #validating date
        try:
            datetime.strptime(completionDate,'%m/%d/%Y') #month/day/year format
        except ValueError:
            messagebox.showinfo('Error',\
                                'Please enter a valid date')
            return
        self.save_goal(goalDifficulty,completionDate,goalAndReflection)
        self.view_goals() #updates list with goal just added
        #clears entry fields
        self.difficulty_entry.delete(0, END)
        self.date_entry.delete(0,END)
        self.goal_reflection_entry.delete(0,END)

    #writes to file
    def save_goal(self, goalDifficulty, completionDate, goalAndReflection):
        #create dictionary
        goal = {
            'Difficulty': goalDifficulty,
            'Completion Date':completionDate,
            'Goal and Reflection':goalAndReflection
            }
        #save goal to the file goals.txt
        goalFile = open('goals.txt','a') #open file   #a appends, instead of just using w 
        goalFile.write(f"{goal['Difficulty']}:{goal['Completion Date']}:{goal['Goal and Reflection']}")  #write to file; convert goal dictionary to string so it can be written
        goalFile.write("\n") #create new line to separate goals whenever entry is made
        goalFile.close()  #close file              
        
    def view_goals(self): #views goals with option to sort by date, difficulty
        #create empty list, so we can view goals
        self.goals = []
        #checks to find goals.txt
        try:
            goalFile = open('goals.txt','r') #read goals, since different function, can I name variable same as save_goal?
        except FileNotFoundError: #if goals.txt isn't found then it creates it.
            goalFile = open('goals.txt','w') 
            goalFile.close()
            return
        for line in goalFile:
            goal_parse = line.strip().split(':') #colon is the delimiter
            parsed_goal = {
                'Difficulty': goal_parse[0], #takes the position of each file and parses accordingly
                'Completion Date':goal_parse[1],
                'Goal and Reflection':goal_parse[2],
            }
            self.goals.append(parsed_goal) #this takes goals, the empty list at the beginning and adds (appends) it to the parsed_goal dictionary we made
        goalFile.close()

    #lambda is needed to sort by each key, then x: x specifies the key

    #view by difficulty button goes to this; sort by difficulty
    def sort_goals_difficulty(self):
        self.goals = sorted(self.goals,key=lambda x: ('easy','medium','hard').index(x['Difficulty']))
        self.display_goals()

    #view by date button goes to this; sort by completion date
    def sort_goals_date(self):
        self.goals.sort(key=lambda x: datetime.strptime(x['Completion Date'], '%m/%d/%Y'))
        self.display_goals()

    def display_goals(self):
        sorted_goals = ""
        for goal in self.goals:
            sorted_goals += (f"Difficulty: {goal['Difficulty']}, Date: {goal['Completion Date']}, Goal and Reflection: {goal['Goal and Reflection']}\n")
        self.sorted_goals_value.set(sorted_goals)

if __name__ == '__main__':
    goal_tracker = GoalTrackerGUI()
